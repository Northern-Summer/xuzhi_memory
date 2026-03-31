import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
"""
Memory System Module — 记忆系统检查
"""
from pathlib import Path
from datetime import datetime
from typing import List
from base import Module, Issue, Fix

HOME = Path.home()
MEMORY = HOME / ".xuzhi_memory"
GENESIS = HOME / "xuzhi_genesis"

class Module(Module):
    name = "memory_system"
    description = "记忆系统检查"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        # L1 检查
        l1_dir = MEMORY / "memory"
        if not l1_dir.exists():
            issues.append(Issue(
                self.name, "ERROR",
                "L1 目录缺失: memory/",
                "mkdir -p memory/"
            ))
        else:
            # 今日日志
            today_file = l1_dir / f"{today}.md"
            if not today_file.exists():
                issues.append(Issue(
                    self.name, "WARN",
                    f"今日日志缺失: {today}.md",
                    "创建今日日志"
                ))
            
            # 最小文件数
            files = list(l1_dir.glob("*.md"))
            if len(files) < 2:
                issues.append(Issue(
                    self.name, "ERROR",
                    f"L1 日志文件过少: {len(files)} 个",
                    "检查记忆系统"
                ))
        
        # L2 检查
        l2_dir = MEMORY / "manifests"
        if not l2_dir.exists():
            issues.append(Issue(
                self.name, "WARN",
                "L2 目录缺失: manifests/",
                "mkdir -p manifests/"
            ))
        
        # L3 检查
        l3_dir = GENESIS / ".memory_backup"
        if not l3_dir.exists():
            issues.append(Issue(
                self.name, "WARN",
                "L3 备份目录缺失: .memory_backup/",
                "mkdir -p .memory_backup/"
            ))
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        
        for issue in issues:
            if issue.module != self.name:
                continue
            
            # 创建今日日志
            if "今日日志缺失" in issue.description:
                today = datetime.now().strftime("%Y-%m-%d")
                today_file = MEMORY / "memory" / f"{today}.md"
                if not today_file.exists():
                    today_file.parent.mkdir(parents=True, exist_ok=True)
                    today_file.write_text(f"# {today} 日志\n\n")
                    fixes.append(Fix(self.name, f"创建 {today}.md"))
            
            # 创建必要目录
            for dir_name in ["L1", "L2", "L3"]:
                if f"{dir_name} 目录缺失" in issue.description:
                    dir_path = {
                        "L1": MEMORY / "memory",
                        "L2": MEMORY / "manifests",
                        "L3": GENESIS / ".memory_backup",
                    }.get(dir_name)
                    if dir_path:
                        dir_path.mkdir(parents=True, exist_ok=True)
                        fixes.append(Fix(self.name, f"创建 {dir_name} 目录"))
        
        return fixes
