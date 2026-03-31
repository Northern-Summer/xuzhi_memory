import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
"""
Task Center Module — task_center 模块检查
"""
import subprocess
import ast
from pathlib import Path
from typing import List
from base import Module, Issue, Fix

HOME = Path.home()
WORKSPACE = HOME / "xuzhi_workspace"
OPENCLAW = HOME / ".openclaw" / "workspace"

MODULES = [
    "judgment_core", "context_trimmer", "rate_limiter",
    "expert_learner", "expert_watchdog", "quarantine",
    "health_scan", "self_repair", "constitution_verifier",
    "identity_anchor", "signal_check", "radar",
    "transcend_trigger", "expert_tracker"
]

class Module(Module):
    name = "task_center"
    description = "task_center 模块检查"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        tc_dir = WORKSPACE / "task_center"
        
        for mod_name in MODULES:
            f = tc_dir / f"{mod_name}.py"
            
            if not f.exists():
                issues.append(Issue(
                    self.name, "ERROR",
                    f"task_center/{mod_name}.py 缺失",
                    "从 git 历史恢复或重建"
                ))
                continue
            
            # 语法检查
            try:
                ast.parse(f.read_text(errors="ignore"))
            except SyntaxError as e:
                issues.append(Issue(
                    self.name, "ERROR",
                    f"task_center/{mod_name}.py 语法错误 line {e.lineno}: {e.msg}",
                    f"检查并修复语法"
                ))
        
        # 同步检查
        tc_openclaw = OPENCLAW / "task_center"
        if tc_dir.exists() and tc_openclaw.exists():
            for f in tc_dir.glob("*.py"):
                src = f
                dst = tc_openclaw / f.name
                if dst.exists():
                    # 比较 hash
                    if src.stat().st_size != dst.stat().st_size:
                        issues.append(Issue(
                            self.name, "WARN",
                            f"{f.name}: workspace 与 openclaw 版本不同步",
                            "cp workspace/task_center/* openclaw/workspace/task_center/"
                        ))
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        tc_dir = WORKSPACE / "task_center"
        tc_openclaw = OPENCLAW / "task_center"
        
        for issue in issues:
            if issue.module != self.name or "同步" not in issue.description:
                continue
            
            if "同步" in issue.description:
                fname = issue.description.split("/")[1].split(":")[0]
                src = tc_dir / fname
                dst = tc_openclaw / fname
                if src.exists():
                    dst.write_bytes(src.read_bytes())
                    fixes.append(Fix(self.name, f"同步: {fname}"))
        
        return fixes
