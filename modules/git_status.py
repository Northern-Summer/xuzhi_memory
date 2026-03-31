import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
"""
Git Status Module — Git 仓库状态检查
"""
import subprocess
from pathlib import Path
from typing import List
from base import Module, Issue, Fix

HOME = Path.home()
REPOS = {
    "workspace": HOME / "xuzhi_workspace",
    "genesis": HOME / "xuzhi_genesis",
    "memory": HOME / ".xuzhi_memory",
}

class Module(Module):
    name = "git_status"
    description = "Git 仓库状态"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        
        for name, path in REPOS.items():
            git_dir = path / ".git"
            
            if not git_dir.exists():
                issues.append(Issue(
                    self.name, "ERROR",
                    f"{name}: 不是 git 仓库（.git 缺失）",
                    f"cd {path} && git init"
                ))
                continue
            
            # 检查状态
            r = subprocess.run(
                ["git", "-C", str(path), "status", "--porcelain"],
                capture_output=True, text=True, timeout=5
            )
            status_clean = not r.stdout.strip()
            
            r2 = subprocess.run(
                ["git", "-C", str(path), "log", "--oneline", "origin/master..HEAD"],
                capture_output=True, text=True, timeout=5
            )
            ahead = len(r2.stdout.strip().splitlines())
            
            if not status_clean:
                issues.append(Issue(
                    self.name, "WARN",
                    f"{name}: 有未提交变更",
                    "git add && git commit"
                ))
            
            if ahead > 0:
                issues.append(Issue(
                    self.name, "WARN", 
                    f"{name}: {ahead} commits 待 push",
                    "git push"
                ))
            
            if status_clean and ahead == 0:
                pass  # 正常，无 issue
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        return []  # Git 状态由框架通过 --commit 处理
