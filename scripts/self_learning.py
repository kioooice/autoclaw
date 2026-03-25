#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自学习系统 - OpenClaw Self-Learning System
基于 SONA + EWC++ 的自动学习与防遗忘

功能：
1. 自动从对话中学习模式
2. EWC++ 防止灾难性遗忘
3. 重要性评分和权重保护

使用：
  python self_learning.py learn <content> <success|failure>
  python self_learning.py patterns
  python self_learning.py stats
  python self_learning.py protect <pattern_id>
"""

import os
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import math

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置
MEMORY_DIR = Path("C:/Users/Administrator/.openclaw-autoclaw/workspace/memory")
LEARNING_DB_PATH = MEMORY_DIR / ".vectors" / "learning.db"
PATTERNS_FILE = MEMORY_DIR / "insights" / "patterns.json"

# EWC++ 参数
EWC_LAMBDA = 0.1  # 防遗忘强度
EWC_GAMMA = 0.95  # 衰减因子
MIN_IMPORTANCE = 0.1
MAX_IMPORTANCE = 1.0
IMPORTANCE_BOOST = 0.05
IMPORTANCE_DECAY = 0.01


class SelfLearning:
    """自学习系统"""
    
    def __init__(self):
        self.db_conn = None
        self._ensure_dirs()
        self._init_db()
        
    def _ensure_dirs(self):
        """确保目录存在"""
        (MEMORY_DIR / ".vectors").mkdir(parents=True, exist_ok=True)
        (MEMORY_DIR / "insights").mkdir(parents=True, exist_ok=True)
        
    def _init_db(self):
        """初始化学习数据库"""
        self.db_conn = sqlite3.connect(str(LEARNING_DB_PATH))
        self.db_conn.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                content_hash TEXT UNIQUE NOT NULL,
                category TEXT DEFAULT 'general',
                importance REAL DEFAULT 0.5,
                ewc_weight REAL DEFAULT 1.0,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                protected INTEGER DEFAULT 0
            )
        """)
        self.db_conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id INTEGER,
                event_type TEXT NOT NULL,
                context TEXT,
                reward REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pattern_id) REFERENCES patterns(id)
            )
        """)
        self.db_conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_content_hash ON patterns(content_hash)
        """)
        self.db_conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON patterns(category)
        """)
        self.db_conn.commit()
    
    def _compute_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def learn(self, content: str, outcome: str, context: str = "") -> Dict:
        """
        学习一个模式
        
        Args:
            content: 学习内容
            outcome: 结果 ("success" 或 "failure")
            context: 上下文信息
        
        Returns:
            学习结果
        """
        content_hash = self._compute_hash(content)
        reward = 1.0 if outcome == "success" else -0.5
        
        # 检查是否已存在
        cursor = self.db_conn.execute(
            "SELECT id, importance, ewc_weight, success_count, failure_count, protected FROM patterns WHERE content_hash = ?",
            (content_hash,)
        )
        row = cursor.fetchone()
        
        if row:
            # 更新现有模式
            pattern_id, importance, ewc_weight, success_count, failure_count, protected = row
            
            # 更新统计
            if outcome == "success":
                success_count += 1
            else:
                failure_count += 1
            
            # 计算新的重要性（EWC++ 加权更新）
            if protected:
                # 受保护模式：衰减更慢
                new_importance = min(MAX_IMPORTANCE, importance + IMPORTANCE_BOOST * ewc_weight * 0.5)
            else:
                # 普通模式：正常更新
                new_importance = importance + reward * IMPORTANCE_BOOST
                new_importance = max(MIN_IMPORTANCE, min(MAX_IMPORTANCE, new_importance))
            
            # EWC 权重更新（成功时增强保护）
            if outcome == "success":
                new_ewc_weight = min(2.0, ewc_weight + 0.1)
            else:
                new_ewc_weight = max(0.5, ewc_weight - 0.05)
            
            self.db_conn.execute("""
                UPDATE patterns 
                SET importance = ?, ewc_weight = ?, success_count = ?, failure_count = ?, last_accessed = ?
                WHERE id = ?
            """, (new_importance, new_ewc_weight, success_count, failure_count, datetime.now(), pattern_id))
            
            # 记录学习事件
            self.db_conn.execute("""
                INSERT INTO learning_events (pattern_id, event_type, context, reward)
                VALUES (?, ?, ?, ?)
            """, (pattern_id, outcome, context, reward))
            
            self.db_conn.commit()
            
            return {
                'status': 'updated',
                'pattern_id': pattern_id,
                'importance': new_importance,
                'ewc_weight': new_ewc_weight,
                'success_rate': success_count / (success_count + failure_count) if (success_count + failure_count) > 0 else 0
            }
        
        else:
            # 创建新模式
            cursor = self.db_conn.execute("""
                INSERT INTO patterns (content, content_hash, importance, success_count, failure_count, last_accessed)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (content, content_hash, 0.5, 1 if outcome == "success" else 0, 0 if outcome == "success" else 1, datetime.now()))
            
            pattern_id = cursor.lastrowid
            
            # 记录学习事件
            self.db_conn.execute("""
                INSERT INTO learning_events (pattern_id, event_type, context, reward)
                VALUES (?, ?, ?, ?)
            """, (pattern_id, outcome, context, reward))
            
            self.db_conn.commit()
            
            return {
                'status': 'created',
                'pattern_id': pattern_id,
                'importance': 0.5,
                'ewc_weight': 1.0
            }
    
    def protect_pattern(self, pattern_id: int) -> bool:
        """保护一个模式（防止遗忘）"""
        try:
            self.db_conn.execute(
                "UPDATE patterns SET protected = 1, ewc_weight = 2.0 WHERE id = ?",
                (pattern_id,)
            )
            self.db_conn.commit()
            return True
        except:
            return False
    
    def unprotect_pattern(self, pattern_id: int) -> bool:
        """取消保护"""
        try:
            self.db_conn.execute(
                "UPDATE patterns SET protected = 0 WHERE id = ?",
                (pattern_id,)
            )
            self.db_conn.commit()
            return True
        except:
            return False
    
    def get_patterns(self, category: str = None, min_importance: float = 0.3) -> List[Dict]:
        """获取模式列表"""
        if category:
            cursor = self.db_conn.execute("""
                SELECT id, content, category, importance, ewc_weight, success_count, failure_count, protected, last_accessed
                FROM patterns 
                WHERE category = ? AND importance >= ?
                ORDER BY importance DESC
            """, (category, min_importance))
        else:
            cursor = self.db_conn.execute("""
                SELECT id, content, category, importance, ewc_weight, success_count, failure_count, protected, last_accessed
                FROM patterns 
                WHERE importance >= ?
                ORDER BY importance DESC
            """, (min_importance,))
        
        patterns = []
        for row in cursor.fetchall():
            id, content, cat, importance, ewc_weight, success_count, failure_count, protected, last_accessed = row
            total = success_count + failure_count
            patterns.append({
                'id': id,
                'content': content[:200] + "..." if len(content) > 200 else content,
                'category': cat,
                'importance': importance,
                'ewc_weight': ewc_weight,
                'success_rate': success_count / total if total > 0 else 0,
                'total_uses': total,
                'protected': bool(protected),
                'last_accessed': last_accessed
            })
        
        return patterns
    
    def decay_unused(self, days: int = 7) -> int:
        """衰减长时间未使用的模式"""
        cutoff = datetime.now().replace(day=datetime.now().day - days)
        
        cursor = self.db_conn.execute("""
            UPDATE patterns 
            SET importance = MAX(?, importance - ?),
                ewc_weight = MAX(0.5, ewc_weight - 0.05)
            WHERE protected = 0 
            AND last_accessed < ?
            AND importance > ?
        """, (MIN_IMPORTANCE, IMPORTANCE_DECAY, cutoff, MIN_IMPORTANCE))
        
        affected = cursor.rowcount
        self.db_conn.commit()
        return affected
    
    def consolidate(self) -> Dict:
        """
        整合学习成果
        - 合并相似模式
        - 清理低重要性模式
        - 更新 EWC 权重
        """
        # 清理过低重要性的模式
        cursor = self.db_conn.execute("DELETE FROM patterns WHERE importance < ? AND protected = 0", (MIN_IMPORTANCE,))
        deleted = cursor.rowcount
        
        # 衰减未使用的模式
        decayed = self.decay_unused()
        
        # 统计
        cursor = self.db_conn.execute("SELECT COUNT(*), AVG(importance), AVG(ewc_weight) FROM patterns")
        total, avg_importance, avg_ewc = cursor.fetchone()
        
        cursor = self.db_conn.execute("SELECT COUNT(*) FROM patterns WHERE protected = 1")
        protected_count = cursor.fetchone()[0]
        
        self.db_conn.commit()
        
        return {
            'deleted_patterns': deleted,
            'decayed_patterns': decayed,
            'total_patterns': total or 0,
            'avg_importance': avg_importance or 0,
            'avg_ewc_weight': avg_ewc or 0,
            'protected_patterns': protected_count
        }
    
    def stats(self) -> Dict:
        """获取学习统计"""
        cursor = self.db_conn.execute("SELECT COUNT(*) FROM patterns")
        total_patterns = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("SELECT COUNT(*) FROM learning_events")
        total_events = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("SELECT COUNT(*) FROM patterns WHERE protected = 1")
        protected_count = cursor.fetchone()[0]
        
        cursor = self.db_conn.execute("""
            SELECT category, COUNT(*) as cnt, AVG(importance) as avg_imp
            FROM patterns 
            GROUP BY category 
            ORDER BY cnt DESC
        """)
        categories = cursor.fetchall()
        
        cursor = self.db_conn.execute("""
            SELECT content, importance, success_count, failure_count
            FROM patterns 
            ORDER BY importance DESC 
            LIMIT 5
        """)
        top_patterns = cursor.fetchall()
        
        cursor = self.db_conn.execute("""
            SELECT SUM(CASE WHEN event_type = 'success' THEN 1 ELSE 0 END) as success,
                   SUM(CASE WHEN event_type = 'failure' THEN 1 ELSE 0 END) as failure
            FROM learning_events
        """)
        row = cursor.fetchone()
        success = row[0] or 0
        failure = row[1] or 0
        
        return {
            'total_patterns': total_patterns,
            'total_events': total_events,
            'protected_patterns': protected_count,
            'success_rate': success / (success + failure) if (success + failure) > 0 else 0,
            'categories': [{'name': c[0], 'count': c[1], 'avg_importance': c[2]} for c in categories],
            'top_patterns': [{'content': p[0][:100], 'importance': p[1], 'success': p[2], 'failure': p[3]} for p in top_patterns]
        }
    
    def export_patterns(self) -> List[Dict]:
        """导出模式到 insights/patterns.json"""
        patterns = self.get_patterns(min_importance=0.2)
        
        with open(PATTERNS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'version': '1.0',
                'updated_at': datetime.now().isoformat(),
                'patterns': patterns
            }, f, ensure_ascii=False, indent=2)
        
        return patterns


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    sl = SelfLearning()
    
    if command == 'learn':
        if len(sys.argv) < 4:
            print("用法: python self_learning.py learn <content> <success|failure>")
            return
        content = sys.argv[2]
        outcome = sys.argv[3]
        context = sys.argv[4] if len(sys.argv) > 4 else ""
        
        result = sl.learn(content, outcome, context)
        print(f"✅ 学习完成:")
        print(f"   状态: {result['status']}")
        print(f"   重要性: {result['importance']:.2f}")
        print(f"   EWC 权重: {result['ewc_weight']:.2f}")
        if 'success_rate' in result:
            print(f"   成功率: {result['success_rate']:.1%}")
    
    elif command == 'patterns':
        patterns = sl.get_patterns()
        if not patterns:
            print("❌ 没有模式")
            return
        
        print(f"📊 已学习 {len(patterns)} 个模式\n")
        for p in patterns[:10]:
            protect_mark = "🔒" if p['protected'] else ""
            print(f"**{p['id']}.** {protect_mark} {p['content'][:50]}...")
            print(f"   重要性: {p['importance']:.2f} | 成功率: {p['success_rate']:.1%} | 使用: {p['total_uses']} 次")
    
    elif command == 'protect':
        if len(sys.argv) < 3:
            print("用法: python self_learning.py protect <pattern_id>")
            return
        pattern_id = int(sys.argv[2])
        if sl.protect_pattern(pattern_id):
            print(f"✅ 已保护模式 {pattern_id}")
        else:
            print(f"❌ 保护失败")
    
    elif command == 'consolidate':
        result = sl.consolidate()
        print("🔄 整合完成:")
        print(f"   删除: {result['deleted_patterns']} 条")
        print(f"   衰减: {result['decayed_patterns']} 条")
        print(f"   剩余: {result['total_patterns']} 条")
        print(f"   平均重要性: {result['avg_importance']:.2f}")
        print(f"   受保护: {result['protected_patterns']} 条")
    
    elif command == 'stats':
        stats = sl.stats()
        print("📊 自学习系统统计")
        print("=" * 40)
        print(f"总模式数: {stats['total_patterns']}")
        print(f"学习事件: {stats['total_events']}")
        print(f"受保护: {stats['protected_patterns']}")
        print(f"成功率: {stats['success_rate']:.1%}")
        print("\n分类统计:")
        for cat in stats['categories'][:5]:
            print(f"  {cat['name']}: {cat['count']} 条 (平均重要性: {cat['avg_importance']:.2f})")
        print("\nTop 模式:")
        for p in stats['top_patterns']:
            print(f"  {p['content'][:50]}... (重要性: {p['importance']:.2f})")
    
    elif command == 'export':
        patterns = sl.export_patterns()
        print(f"✅ 导出 {len(patterns)} 个模式到 {PATTERNS_FILE}")
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()