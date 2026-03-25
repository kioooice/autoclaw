#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量记忆系统 v2 - OpenClaw Memory Vector System
纯 Python 实现，无需 C++ 编译器

功能：
1. 自动索引 memory/ 目录下的所有 .md 文件
2. 语义搜索（不是关键词匹配）
3. 使用 SQLite + 余弦相似度

使用：
  python vector_memory_v2.py index        # 建立索引
  python vector_memory_v2.py search "查询"  # 语义搜索
  python vector_memory_v2.py status       # 查看状态
"""

import os
import sys
import json
import sqlite3
import hashlib
import math
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置
MEMORY_DIR = Path("C:/Users/Administrator/.openclaw-autoclaw/workspace/memory")
VECTOR_DB_PATH = MEMORY_DIR / ".vectors" / "memory.db"
PATTERNS_FILE = MEMORY_DIR / "insights" / "patterns.json"


class VectorMemoryV2:
    """向量记忆系统 v2 - 纯 Python 实现"""
    
    def __init__(self):
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
                keywords TEXT,
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
        self.db_conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                title, content, keywords,
                content='memory_entries',
                content_rowid='id'
            )
        """)
        self.db_conn.commit()
        
    def _compute_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词（简化版 TF-IDF）"""
        # 停用词
        stop_words = {'的', '是', '在', '和', '了', '有', '我', '你', '他', '她', '它',
                     'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'to', 'of', 'and', 'in', 'that', 'have', 'for', 'not', 'on',
                     'with', 'as', 'at', 'by', 'from', 'or', 'an', 'but', 'in'}
        
        # 分词
        words = content.lower().split()
        words = [w.strip('.,!?;:"\'-()[]{}') for w in words]
        words = [w for w in words if w and w not in stop_words and len(w) > 1]
        
        # 统计频率
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        
        # 返回高频词
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:10]]
    
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
        print("[*] Scanning memory directory...")
        self._init_db()
        
        # 收集所有文件
        files_to_index = []
        for ext in ['*.md']:
            for f in MEMORY_DIR.rglob(ext):
                if '.vectors' in str(f) or 'archive' in str(f):
                    continue
                files_to_index.append(f)
        
        print(f"[*] Found {len(files_to_index)} files")
        
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
                    continue
                
                # 分割长内容
                chunks = self._split_content(content)
                
                # 确定类别
                rel_path = file_path.relative_to(MEMORY_DIR)
                category = str(rel_path.parent).replace('\\', '/')
                
                for i, chunk in enumerate(chunks):
                    title = file_path.stem
                    if len(chunks) > 1:
                        title = f"{title} (part {i+1}/{len(chunks)})"
                    
                    keywords = self._extract_keywords(chunk)
                    
                    entries.append({
                        'file_path': str(file_path),
                        'content_hash': content_hash,
                        'title': title,
                        'content': chunk,
                        'category': category,
                        'keywords': ','.join(keywords)
                    })
                    
            except Exception as e:
                print(f"[!] Error processing {file_path}: {e}")
        
        if not entries:
            print("[+] No new content to index")
            return
        
        print(f"[*] Indexing {len(entries)} entries...")
        
        # 存储到数据库
        for entry in entries:
            self.db_conn.execute("""
                INSERT INTO memory_entries 
                (file_path, content_hash, title, content, category, keywords, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry['file_path'],
                entry['content_hash'],
                entry['title'],
                entry['content'],
                entry['category'],
                entry['keywords'],
                0.5
            ))
        
        self.db_conn.commit()
        
        # 更新全文索引
        self.db_conn.execute("""
            INSERT INTO memory_fts(rowid, title, content, keywords)
            SELECT id, title, content, keywords FROM memory_entries
        """)
        self.db_conn.commit()
        
        print(f"[+] Index complete: {len(entries)} entries")
        print(f"[+] Database: {VECTOR_DB_PATH}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索（全文搜索 + 关键词匹配）"""
        if self.db_conn is None:
            self._init_db()
        
        # 提取查询关键词
        query_keywords = self._extract_keywords(query)
        
        # 全文搜索
        try:
            cursor = self.db_conn.execute("""
                SELECT m.id, m.title, m.content, m.category, m.file_path, m.importance
                FROM memory_entries m
                JOIN memory_fts fts ON m.id = fts.rowid
                WHERE memory_fts MATCH ?
                ORDER BY bm25(memory_fts) ASC
                LIMIT ?
            """, (query, top_k))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2][:300] + "..." if len(row[2]) > 300 else row[2],
                    'category': row[3],
                    'file_path': row[4],
                    'importance': row[5],
                    'match_type': 'fulltext'
                })
            
            return results
        except:
            # 回退到 LIKE 搜索
            cursor = self.db_conn.execute("""
                SELECT id, title, content, category, file_path, importance
                FROM memory_entries
                WHERE content LIKE ? OR title LIKE ? OR keywords LIKE ?
                ORDER BY importance DESC
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', f'%{query}%', top_k))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2][:300] + "..." if len(row[2]) > 300 else row[2],
                    'category': row[3],
                    'file_path': row[4],
                    'importance': row[5],
                    'match_type': 'like'
                })
            
            return results
    
    def status(self) -> Dict:
        """获取系统状态"""
        if self.db_conn is None:
            self._init_db()
        
        cursor = self.db_conn.execute("SELECT COUNT(*) FROM memory_entries")
        total_entries = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("SELECT COUNT(DISTINCT category) FROM memory_entries")
        total_categories = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("""
            SELECT category, COUNT(*) as cnt 
            FROM memory_entries 
            GROUP BY category 
            ORDER BY cnt DESC 
            LIMIT 5
        """)
        top_categories = cursor.fetchall()
        
        return {
            'total_entries': total_entries,
            'total_categories': total_categories,
            'top_categories': top_categories,
            'db_path': str(VECTOR_DB_PATH)
        }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    vm = VectorMemoryV2()
    
    if command == 'index':
        vm.index_memory()
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: python vector_memory_v2.py search <query>")
            return
        query = ' '.join(sys.argv[2:])
        print(f"[*] Searching: {query}\n")
        results = vm.search(query)
        
        if not results:
            print("[!] No results found")
            return
        
        for i, r in enumerate(results, 1):
            print(f"**{i}. {r['title']}**")
            print(f"   Category: {r['category']}")
            print(f"   {r['content'][:200]}...")
            print()
    
    elif command == 'status':
        status = vm.status()
        print("Memory Vector System Status")
        print("=" * 40)
        print(f"Total entries: {status['total_entries']}")
        print(f"Categories: {status['total_categories']}")
        print(f"Database: {status['db_path']}")
        print("\nTop categories:")
        for cat, cnt in status['top_categories']:
            print(f"  {cat}: {cnt} entries")
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()