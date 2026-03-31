"""
Centers Module — Centers 路径检查
"""
from pathlib import Path
from typing import List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from base import Module, Issue, Fix

HOME = Path.home()
WORKSPACE = HOME / "xuzhi_workspace"
MEMORY = HOME / ".xuzhi_memory"

class Module(Module):
    name = "centers"
    description = "Centers 路径检查"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        
        # quota_usage.json
        quota_candidates = [
            HOME / ".openclaw/centers/engineering/crown/quota_usage.json",
            MEMORY / "centers/engineering/crown/quota_usage.json",
        ]
        if not any(p.exists() for p in quota_candidates):
            issues.append(Issue(
                self.name, "WARN",
                "quota_usage.json 未找到",
                "运行 quota_monitor.py 生成"
            ))
        
        # ratings.json
        ratings = MEMORY / "centers/mind/society/ratings.json"
        if not ratings.exists():
            issues.append(Issue(
                self.name, "ERROR",
                "ratings.json 缺失（agent_autonomous_wake 需要）",
                "创建 ratings.json"
            ))
        
        # centers 目录存在性
        for center in ["engineering", "intelligence", "mind"]:
            d = MEMORY / "centers" / center
            if not d.exists():
                issues.append(Issue(
                    self.name, "WARN",
                    f"centers/{center} 目录缺失",
                    "检查或创建"
                ))
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        
        # 创建 ratings.json
        for issue in issues:
            if "ratings.json" in issue.description and "缺失" in issue.description:
                ratings_dir = HOME / ".xuzhi_memory/centers/mind/society"
                ratings_dir.mkdir(parents=True, exist_ok=True)
                
                import json
                ratings = {
                    "schema": "ratings.v1",
                    "last_updated": "2026-03-26T00:00:00Z",
                    "agents": {
                        a: {"reliability": 0.8, "quality": 0.8}
                        for a in ["Xi", "Phi", "Delta", "Theta", "Gamma", "Omega", "Psi"]
                    }
                }
                ratings_path = ratings_dir / "ratings.json"
                ratings_path.write_text(json.dumps(ratings, indent=2, ensure_ascii=False))
                fixes.append(Fix(self.name, "创建 ratings.json"))
        
        return fixes
