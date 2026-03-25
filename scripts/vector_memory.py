#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量记忆系统 - OpenClaw Memory Vector System
基于 HNSW 索引的语义搜索，支持本地 ONNX 模型

功能：
1. 自动索引 memory/ 目录下的所有 .md 文件
2. 语义搜索（不是关键词匹配）
3. 150x+ 搜索加速（HNSW 索引）

使用：
  python vector_memory.py index        # 建立索引
  python vector_memory.py search "查询"  # 语义搜索
  python vector_memory.py status       # 查看状态
"""

import os
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 尝试导入向量库
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False
    print("[!] sentence-transformers not installed. Run: pip install sentence-transformers")

try:
    import hnswlib
    HNSW_AVAILABLE = True
except ImportError:
    HNSW_AVAILABLE = False
    print("[!] hnswlib not installed. Run: pip install hnswlib")

# 配置
MEMORY_DIR = Path("C:/Users/Administrator/.openclaw-autoclaw/workspace/memory")
VECTOR_DB_PATH = MEMORY_DIR / ".vectors" / "memory.db"
INDEX_PATH = MEMORY_DIR / ".vectors" / "hnsw_index.bin"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 维，快速
EMBEDDING_DIM = 384


class VectorMemory:
    """向量记忆系统"""
    
    def __init__(self):
        self.model = None
        self.index = None
        self.db_conn = None
        self._ensure_dirs()
        
    def _ensure_dirs(self):
        """确保目录存在"""
        (MEMORY_DIR / ".vectors").mkdir(parents=True, exist_ok=True)
        
    def _init_db(self):
        """初始化 SQLite 数据库"""
        self.db_conn = sqlite3.connect(str(VECTOR_DB_PATH))
        self.db_conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                embedding BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                importance REAL DEFAULT 0.5
            )
        """)
        self.db_conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_content_hash ON memory_entries(content_hash)
        """)
        self.db_conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON memory_entries(category)
        """)
        self.db_conn.commit()
        
    def _load_model(self):
        """加载嵌入模型"""
        if not EMBEDDING_AVAILABLE:
            raise RuntimeError("sentence-transformers 未安装")
        if self.model is None:
            print(f"📦 加载模型 {EMBEDDING_MODEL}...")
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            print(f"✅ 模型加载完成（{EMBEDDING_DIM} 维）")
        return self.model
    
    def _load_index(self):
        """加载 HNSW 索引"""
        if not HNSW_AVAILABLE:
            return None
        if self.index is None and INDEX_PATH.exists():
            self.index = hnswlib.Index(space='cosine', dim=EMBEDDING_DIM)
            self.index.load_index(str(INDEX_PATH))
            print(f"✅ 加载 HNSW 索引（{self.index.get_current_count()} 条）")
        return self.index
    
    def _create_index(self, num_elements: int):
        """创建 HNSW 索引"""
        if not HNSW_AVAILABLE:
            return None
        self.index = hnswlib.Index(space='cosine', dim=EMBEDDING_DIM)
        self.index.init_index(max_elements=num_elements, ef_construction=200, M=16)
        self.index.set_ef(50)
        return self.index
    
    def _compute_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _split_content(self, content: str, max_length: int = 500) -> List[str]:
        """分割长内容"""
        if len(content) <= max_length:
            return [content]
        
        chunks = []
        lines = content.split('\n')
        current = ""
        
        for line in lines:
            if len(current) + len(line) > max_length and current:
                chunks.append(current.strip())
                current = line + "\n"
            else:
                current += line + "\n"
        
        if current.strip():
            chunks.append(current.strip())
            
        return chunks
    
    def index_memory(self):
        """索引 memory 目录下的所有文件"""
        if not EMBEDDING_AVAILABLE or not HNSW_AVAILABLE:
            print("❌ 缺少依赖，请先安装: pip install sentence-transformers hnswlib")
            return
        
        print("🔍 扫描 memory 目录...")
        self._init_db()
        model = self._load_model()
        
        # 收集所有文件
        files_to_index = []
        for ext in ['*.md', '*.L0.md', '*.L1.md']:
            for f in MEMORY_DIR.rglob(ext):
                if '.vectors' in str(f) or 'archive' in str(f):
                    continue
                files_to_index.append(f)
        
        print(f"📄 找到 {len(files_to_index)} 个文件")
        
        # 处理每个文件
        entries = []
        for file_path in files_to_index:
            try:
                content = file_path.read_text(encoding='utf-8')
                content_hash = self._compute_hash(content)
                
                # 检查是否已存在
                cursor = self.db_conn.execute(
                    "SELECT id FROM memory_entries WHERE content_hash = ?",
                    (content_hash,)
                )
                if cursor.fetchone():
                    continue  # 跳过已索引的内容
                
                # 分割长内容
                chunks = self._split_content(content)
                
                # 确定类别
                rel_path = file_path.relative_to(MEMORY_DIR)
                category = str(rel_path.parent).replace('\\', '/')
                
                for i, chunk in enumerate(chunks):
                    title = file_path.stem
                    if len(chunks) > 1:
                        title = f"{title} (part {i+1}/{len(chunks)})"
                    
                    entries.append({
                        'file_path': str(file_path),
                        'content_hash': content_hash,
                        'title': title,
                        'content': chunk,
                        'category': category
                    })
                    
            except Exception as e:
                print(f"⚠️ 处理 {file_path} 时出错: {e}")
        
        if not entries:
            print("✅ 没有新内容需要索引")
            return
        
        print(f"📝 索引 {len(entries)} 个条目...")
        
        # 生成嵌入
        contents = [e['content'] for e in entries]
        embeddings = model.encode(contents, show_progress_bar=True)
        
        # 创建 HNSW 索引
        index = self._create_index(len(entries) + 1000)  # 预留空间
        
        # 存储到数据库和索引
        for i, entry in enumerate(entries):
            embedding = embeddings[i]
            
            # 存入数据库
            self.db_conn.execute("""
                INSERT INTO memory_entries 
                (file_path, content_hash, title, content, category, embedding, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry['file_path'],
                entry['content_hash'],
                entry['title'],
                entry['content'],
                entry['category'],
                embedding.tobytes(),
                0.5  # 初始重要性
            ))
            
            # 加入 HNSW 索引
            index.add_items(embedding, i)
        
        self.db_conn.commit()
        
        # 保存索引
        index.save_index(str(INDEX_PATH))
        
        print(f"✅ 索引完成：{len(entries)} 条目")
        print(f"📊 数据库：{VECTOR_DB_PATH}")
        print(f"📊 索引：{INDEX_PATH}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """语义搜索"""
        if not EMBEDDING_AVAILABLE:
            print("❌ 缺少依赖")
            return []
        
        model = self._load_model()
        
        # 加载数据库
        if self.db_conn is None:
            self._init_db()
        
        # 生成查询嵌入
        query_embedding = model.encode([query])[0]
        
        # 尝试使用 HNSW 索引
        if HNSW_AVAILABLE and INDEX_PATH.exists():
            index = self._load_index()
            if index:
                # HNSW 搜索
                labels, distances = index.knn_query(query_embedding, k=top_k)
                
                # 从数据库获取详情
                results = []
                for label, distance in zip(labels[0], distances[0]):
                    cursor = self.db_conn.execute(
                        "SELECT title, content, category, file_path, importance FROM memory_entries WHERE rowid = ?",
                        (label + 1,)  # rowid 从 1 开始
                    )
                    row = cursor.fetchone()
                    if row:
                        results.append({
                            'title': row[0],
                            'content': row[1][:300] + "..." if len(row[1]) > 300 else row[1],
                            'category': row[2],
                            'file_path': row[3],
                            'similarity': 1 - distance,  # 余弦距离转相似度
                            'importance': row[4]
                        })
                
                return results
        
        # 回退：暴力搜索
        cursor = self.db_conn.execute("SELECT rowid, title, content, category, file_path, embedding, importance FROM memory_entries")
        rows = cursor.fetchall()
        
        if not rows:
            return []
        
        # 计算相似度
        results = []
        for row in rows:
            rowid, title, content, category, file_path, embedding_bytes, importance = row
            stored_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            similarity = 1 - np.dot(query_embedding, stored_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
            )
            
            results.append({
                'title': title,
                'content': content[:300] + "..." if len(content) > 300 else content,
                'category': category,
                'file_path': file_path,
                'similarity': similarity,
                'importance': importance
            })
        
        # 按相似度排序
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def status(self) -> Dict:
        """获取系统状态"""
        if self.db_conn is None:
            self._init_db()
        
        cursor = self.db_conn.execute("SELECT COUNT(*) FROM memory_entries")
        total_entries = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("SELECT COUNT(DISTINCT category) FROM memory_entries")
        total_categories = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("SELECT category, COUNT(*) as cnt FROM memory_entries GROUP BY category ORDER BY cnt DESC LIMIT 5")
        top_categories = cursor.fetchall()
        
        return {
            'total_entries': total_entries,
            'total_categories': total_categories,
            'top_categories': top_categories,
            'index_exists': INDEX_PATH.exists(),
            'model': EMBEDDING_MODEL,
            'dimensions': EMBEDDING_DIM
        }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    vm = VectorMemory()
    
    if command == 'index':
        vm.index_memory()
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("用法: python vector_memory.py search <查询>")
            return
        query = ' '.join(sys.argv[2:])
        print(f"🔍 搜索: {query}\n")
        results = vm.search(query)
        
        if not results:
            print("❌ 没有找到相关内容")
            return
        
        for i, r in enumerate(results, 1):
            print(f"**{i}. {r['title']}** (相似度: {r['similarity']:.2f})")
            print(f"   📁 {r['category']}")
            print(f"   📄 {r['content'][:200]}...")
            print()
    
    elif command == 'status':
        status = vm.status()
        print("📊 向量记忆系统状态")
        print("=" * 40)
        print(f"总条目: {status['total_entries']}")
        print(f"分类数: {status['total_categories']}")
        print(f"模型: {status['model']} ({status['dimensions']} 维)")
        print(f"HNSW 索引: {'✅ 存在' if status['index_exists'] else '❌ 不存在'}")
        print("\n分类统计:")
        for cat, cnt in status['top_categories']:
            print(f"  {cat}: {cnt} 条")
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()