#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动学习系统 - Auto Learning System
从最近的对话/经历中自动提取学习内容

功能：
1. 分析最近的 experiences 文件
2. 提取成功/失败模式
3. 自动记录到自学习系统

使用：
  python auto_learn.py              # 分析今天的经历
  python auto_learn.py --days 3     # 分析近 3 天的经历
  python auto_learn.py --dry-run    # 预览不执行
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置
MEMORY_DIR = Path("C:/Users/Administrator/.openclaw-autoclaw/workspace/memory")
EXPERIENCES_DIR = MEMORY_DIR / "experiences"
LEARNING_SCRIPT = Path("C:/Users/Administrator/.openclaw-autoclaw/workspace/scripts/self_learning.py")

# 学习模式关键词
SUCCESS_PATTERNS = [
    r'成功', r'完成', r'解决', r'修复', r'实现', r'优化',
    r'success', r'completed', r'fixed', r'solved', r'implemented',
    r'✅', r'✓', r'搞定', r'达成'
]

FAILURE_PATTERNS = [
    r'失败', r'错误', r'问题', r'bug', r'异常', r'崩溃',
    r'failure', r'error', r'issue', r'problem', r'exception',
    r'❌', r'✗', r'失败', r'报错'
]

# 值得学习的模式
LEARNABLE_PATTERNS = [
    # 技术解决方案
    (r'设置\s+(\w+)\s*=\s*([^\n]+)', 'solution'),
    (r'安装\s+([^\n]+)', 'solution'),
    (r'配置\s+([^\n]+)', 'solution'),
    (r'使用\s+([^\n]+)\s+解决', 'solution'),
    (r'运行\s+([^\n]+)', 'solution'),
    (r'解决[是为：:]\s*([^\n]+)', 'solution'),
    (r'解决：\s*\*?\*?([^\n]+)', 'solution'),
    
    # 问题诊断
    (r'原因[是为：:]\s*([^\n]+)', 'diagnosis'),
    (r'根因[是为：:]\s*([^\n]+)', 'diagnosis'),
    (r'根因：\s*\*?\*?([^\n]+)', 'diagnosis'),
    (r'因为\s+([^\n]+)', 'diagnosis'),
    (r'由于\s+([^\n]+)', 'diagnosis'),
    
    # 最佳实践
    (r'建议\s+([^\n]+)', 'practice'),
    (r'推荐\s+([^\n]+)', 'practice'),
    (r'最佳实践[是为：:]\s*([^\n]+)', 'practice'),
    (r'注意\s+([^\n]+)', 'practice'),
    (r'教训[是为：:]\s*([^\n]+)', 'practice'),
    (r'教训：\s*\*?\*?([^\n]+)', 'practice'),
    
    # 经验总结
    (r'学到\s+([^\n]+)', 'lesson'),
    (r'发现\s+([^\n]+)', 'lesson'),
    (r'记住\s+([^\n]+)', 'lesson'),
    
    # 标记的成功/失败
    (r'([^\n]+?)\s*✅', 'success_marker'),
    (r'([^\n]+?)\s*❌', 'failure_marker'),
]


class AutoLearner:
    """自动学习系统"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.learned = []
        
    def get_recent_experiences(self, days: int = 1) -> List[Path]:
        """获取最近的经历文件"""
        files = []
        today = datetime.now()
        
        for i in range(days):
            date = today - timedelta(days=i)
            filename = f"{date.strftime('%Y-%m-%d')}.md"
            filepath = EXPERIENCES_DIR / filename
            if filepath.exists():
                files.append(filepath)
        
        # 也检查 memory/ 根目录下的日期文件
        for i in range(days):
            date = today - timedelta(days=i)
            filename = f"{date.strftime('%Y-%m-%d')}.md"
            filepath = MEMORY_DIR / filename
            if filepath.exists():
                files.append(filepath)
        
        return files
    
    def extract_learnings(self, content: str) -> List[Dict]:
        """从内容中提取学习点"""
        learnings = []
        
        # 按段落分割
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            if len(para.strip()) < 20:
                continue
            
            # 判断是成功还是失败
            outcome = None
            for pattern in SUCCESS_PATTERNS:
                if re.search(pattern, para, re.IGNORECASE):
                    outcome = 'success'
                    break
            
            if outcome is None:
                for pattern in FAILURE_PATTERNS:
                    if re.search(pattern, para, re.IGNORECASE):
                        outcome = 'failure'
                        break
            
            # 提取具体的学习内容
            for pattern, learn_type in LEARNABLE_PATTERNS:
                matches = re.findall(pattern, para, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = ' '.join(match)
                    
                    # 确定 outcome
                    item_outcome = outcome
                    if learn_type == 'success_marker':
                        item_outcome = 'success'
                    elif learn_type == 'failure_marker':
                        item_outcome = 'failure'
                    
                    learnings.append({
                        'content': match.strip(),
                        'type': learn_type,
                        'outcome': item_outcome or 'success',
                        'context': para[:200]
                    })
        
        return learnings
    
    def deduplicate(self, learnings: List[Dict]) -> List[Dict]:
        """去重"""
        seen = set()
        unique = []
        
        for l in learnings:
            key = l['content'].lower().strip()
            if key not in seen and len(key) > 5:
                seen.add(key)
                unique.append(l)
        
        return unique
    
    def learn_from_file(self, filepath: Path) -> List[Dict]:
        """从文件中学习"""
        try:
            content = filepath.read_text(encoding='utf-8')
            learnings = self.extract_learnings(content)
            return self.deduplicate(learnings)
        except Exception as e:
            print(f"[!] Error reading {filepath}: {e}")
            return []
    
    def record_learning(self, learning: Dict) -> bool:
        """记录学习"""
        import subprocess
        
        cmd = [
            sys.executable,
            str(LEARNING_SCRIPT),
            'learn',
            learning['content'],
            learning['outcome']
        ]
        
        if self.dry_run:
            print(f"  [DRY-RUN] Would learn: {learning['content'][:50]}... ({learning['outcome']})")
            return True
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            return result.returncode == 0
        except Exception as e:
            print(f"[!] Error recording learning: {e}")
            return False
    
    def run(self, days: int = 1) -> Dict:
        """运行自动学习"""
        print(f"[*] Analyzing experiences from last {days} day(s)...")
        
        # 获取文件
        files = self.get_recent_experiences(days)
        
        if not files:
            print("[!] No experience files found")
            return {'files': 0, 'learnings': 0, 'recorded': 0}
        
        print(f"[*] Found {len(files)} files")
        
        # 提取学习点
        all_learnings = []
        for f in files:
            print(f"  - {f.name}")
            learnings = self.learn_from_file(f)
            all_learnings.extend(learnings)
        
        # 去重
        unique_learnings = self.deduplicate(all_learnings)
        
        print(f"\n[*] Found {len(unique_learnings)} learning points")
        
        # 记录学习
        recorded = 0
        for l in unique_learnings[:10]:  # 最多记录 10 条
            if self.record_learning(l):
                recorded += 1
                self.learned.append(l)
        
        print(f"[+] Recorded {recorded} learnings")
        
        return {
            'files': len(files),
            'learnings': len(unique_learnings),
            'recorded': recorded,
            'items': self.learned
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto Learning System')
    parser.add_argument('--days', type=int, default=1, help='Days to analyze')
    parser.add_argument('--dry-run', action='store_true', help='Preview without recording')
    args = parser.parse_args()
    
    learner = AutoLearner(dry_run=args.dry_run)
    result = learner.run(days=args.days)
    
    if result.get('items'):
        print("\n[*] Learned items:")
        for i, l in enumerate(result['items'], 1):
            print(f"  {i}. [{l['outcome']}] {l['content'][:60]}...")


if __name__ == '__main__':
    main()