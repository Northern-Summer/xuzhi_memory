#!/usr/bin/env python3
"""
Xuzhi System Repair — 模块化诊断与修复框架

用法:
  python3 system_repair.py --diagnose       # 诊断
  python3 system_repair.py --fix           # 诊断+修复
  python3 system_repair.py --commit        # 诊断+修复+提交
  python3 system_repair.py --list          # 列出所有模块
  python3 system_repair.py --module git_status  # 只跑指定模块

工程改进铁律合规 — Ξ | 2026-03-26
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from importlib import import_module
from typing import List, Dict

HOME = Path.home()
BACKUP_DIR = HOME / f"xuzhi_backup_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"


class Issue:
    def __init__(self, module, severity, description, fix_hint=""):
        self.module = module
        self.severity = severity
        self.description = description
        self.fix_hint = fix_hint

    def __repr__(self):
        prefix = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}.get(self.severity, "  ")
        return f"{prefix} [{self.module}] {self.description}"


class Fix:
    def __init__(self, module, description):
        self.module = module
        self.description = description


def get_modules() -> Dict:
    modules = {}
    module_dir = Path(__file__).parent / "modules"
    if not module_dir.exists():
        return modules
    for f in module_dir.glob("*.py"):
        if f.stem in ("__init__", "base"):
            continue
        try:
            mod = import_module(f"modules.{f.stem}")
            if hasattr(mod, "Module"):
                instance = mod.Module()
                modules[instance.name] = instance
        except Exception as e:
            print(f"  ⚠️  模块 {f.stem} 加载失败: {e}", file=sys.stderr)
    return modules


def main():
    parser = argparse.ArgumentParser(description="Xuzhi System Repair")
    parser.add_argument("--diagnose", action="store_true", help="仅诊断")
    parser.add_argument("--fix", action="store_true", help="诊断+修复")
    parser.add_argument("--commit", action="store_true", help="诊断+修复+提交")
    parser.add_argument("--list", action="store_true", help="列出所有模块")
    parser.add_argument("--module", type=str, default="", help="只跑指定模块")
    args = parser.parse_args()

    if not any([args.diagnose, args.fix, args.commit, args.list]):
        args.diagnose = True

    print(f"\n{'='*60}")
    print("Xuzhi System Repair — 模块化诊断与修复框架")
    print(f"{'='*60}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    modules = get_modules()
    print(f"已加载模块: {len(modules)}")

    if args.list:
        print(f"\n可用模块 ({len(modules)}):")
        for name, mod in sorted(modules.items()):
            print(f"  {name:20} — {mod.description}")
        return

    if not modules:
        print("❌ 没有可用的模块")
        return

    selected = {k: v for k, v in modules.items()
                if not args.module or k == args.module}

    all_issues: List[Issue] = []
    all_fixes: List[Fix] = []

    print(f"\n{'='*60}")
    print("Phase 1: 诊断")
    print(f"{'='*60}")

    for name, mod in sorted(selected.items()):
        print(f"\n[{name}] {mod.description}")
        try:
            issues = mod.diagnose()
            all_issues.extend(issues)
            for issue in issues:
                print(f"  {issue}")
        except Exception as e:
            print(f"  ❌ 诊断异常: {e}")
            all_issues.append(Issue(name, "ERROR", f"诊断异常: {e}"))

    errors = [i for i in all_issues if i.severity == "ERROR"]
    warns = [i for i in all_issues if i.severity == "WARN"]
    print(f"\n汇总: {len(errors)} 个错误, {len(warns)} 个警告")

    if errors:
        print("\n❌ 必须修复的问题:")
        for i in errors:
            print(f"  [{i.module}] {i.description}")

    if args.fix and errors:
        print(f"\n{'='*60}")
        print("Phase 2: 修复")
        print(f"{'='*60}")

        backup = BACKUP_DIR
        backup.mkdir(parents=True, exist_ok=True)
        print(f"\n📦 备份到: {backup}")

        for name, mod in sorted(selected.items()):
            mod_errors = [i for i in errors if i.module == name]
            if not mod_errors:
                continue
            print(f"\n[{name}] 修复...")
            try:
                fixes = mod.fix(mod_errors)
                all_fixes.extend(fixes)
                for fix in fixes:
                    print(f"  ✅ {fix.description}")
            except Exception as e:
                print(f"  ❌ 修复失败: {e}")

    if args.commit and all_fixes:
        print(f"\n{'='*60}")
        print("Phase 3: Git 提交")
        print(f"{'='*60}")

        repos = {
            "workspace": HOME / "xuzhi_workspace",
            "genesis": HOME / "xuzhi_genesis",
            "memory": HOME / ".xuzhi_memory",
        }

        for repo_name, repo_path in repos.items():
            git_dir = repo_path / ".git"
            if not git_dir.exists():
                continue
            try:
                r = subprocess.run(
                    ["git", "-C", str(repo_path), "status", "--porcelain"],
                    capture_output=True, text=True, timeout=5
                )
                if not r.stdout.strip():
                    print(f"  [{repo_name}] 无变更")
                    continue
                subprocess.run(
                    ["git", "-C", str(repo_path), "add", "-A"],
                    capture_output=True, timeout=5
                )
                msg = f"fix(system_repair): {datetime.now().strftime('%Y-%m-%d')} automated"
                r = subprocess.run(
                    ["git", "-C", str(repo_path), "commit", "-m", msg],
                    capture_output=True, text=True, timeout=5
                )
                if r.returncode == 0:
                    print(f"  ✅ [{repo_name}] 已提交")
                else:
                    print(f"  ❌ [{repo_name}] 提交失败")
            except Exception as e:
                print(f"  ❌ [{repo_name}] 异常: {e}")

    print(f"\n{'='*60}")
    print("最终报告")
    print(f"{'='*60}")
    print(f"备份位置: {BACKUP_DIR}")
    print(f"修复数量: {len(all_fixes)}")
    print(f"问题数量: {len(all_issues)}")

    if all_fixes:
        print("\n已执行修复:")
        for fix in all_fixes:
            print(f"  ✅ [{fix.module}] {fix.description}")


if __name__ == "__main__":
    main()
