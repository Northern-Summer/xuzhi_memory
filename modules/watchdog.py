import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
"""
Watchdog Module — 守护进程检查
"""
import subprocess
from pathlib import Path
from typing import List
from base import Module, Issue, Fix

HOME = Path.home()
MEMORY = HOME / ".xuzhi_memory"

class Module(Module):
    name = "watchdog"
    description = "守护进程检查"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        
        # watchdog_supervisor
        r = subprocess.run(["pgrep", "-f", "watchdog_supervisor"], capture_output=True)
        if r.returncode != 0:
            issues.append(Issue(
                self.name, "WARN",
                "watchdog_supervisor 未运行",
                "启动: bash ~/watchdog_supervisor.sh &"
            ))
        
        # expert-watchdog cron
        r = subprocess.run(["openclaw", "cron", "list"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and "expert-watchdog" in r.stdout:
            import re
            match = re.search(r"expert-watchdog.*?([a-f0-9-]{36})", r.stdout)
            if match:
                cron_id = match.group(1)
                issues.append(Issue(
                    self.name, "INFO",
                    f"expert-watchdog cron 已注册 (ID: {cron_id[:8]}...)",
                    ""
                ))
        else:
            issues.append(Issue(
                self.name, "WARN",
                "expert-watchdog cron 未注册",
                "openclaw cron add --name expert-watchdog ..."
            ))
        
        # expert_watchdog stall_count
        state_file = MEMORY / "task_center/expert_watchdog_state.json"
        if state_file.exists():
            try:
                import json
                d = json.loads(state_file.read_text())
                count = d.get("stall_count", 0)
                if count > 0:
                    issues.append(Issue(
                        self.name, "ERROR",
                        f"expert_watchdog stall_count={count}（需重置）",
                        "重置: stall_count=0"
                    ))
            except:
                pass
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        
        for issue in issues:
            if issue.module != self.name or issue.severity != "ERROR":
                continue
            
            if "stall_count" in issue.description:
                state_file = MEMORY / "task_center/expert_watchdog_state.json"
                if state_file.exists():
                    try:
                        import json
                        d = json.loads(state_file.read_text())
                        d["stall_count"] = 0
                        state_file.write_text(json.dumps(d, indent=2))
                        fixes.append(Fix(self.name, "expert_watchdog stall_count 重置为 0"))
                    except Exception as e:
                        fixes.append(Fix(self.name, f"重置失败: {e}"))
        
        return fixes
