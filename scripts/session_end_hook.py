#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话结束钩子 - Session End Hook
在会话结束时自动执行学习、整理等任务

使用：
  python session_end_hook.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPTS_DIR = Path("C:/Users/Administrator/.openclaw-autoclaw/workspace/scripts")


def run_script(script_name: str, args: list = None) -> bool:
    """运行脚本"""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return False
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"[!] Error running {script_name}: {e}")
        return False


def main():
    print("=" * 50)
    print("Session End Hook")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 自动学习
    print("[1/3] Auto Learning...")
    run_script("auto_learn.py", ["--days", "1"])
    print()
    
    # 2. 更新向量索引
    print("[2/3] Updating Vector Index...")
    run_script("vector_memory_v2.py", ["index"])
    print()
    
    # 3. 整合学习成果
    print("[3/3] Consolidating Learnings...")
    run_script("self_learning.py", ["consolidate"])
    print()
    
    # 显示统计
    print("=" * 50)
    print("Session Statistics")
    print("=" * 50)
    run_script("self_learning.py", ["stats"])
    
    print()
    print("[+] Session end hook completed")


if __name__ == '__main__':
    main()