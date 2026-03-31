import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
"""
Agent Identity Module — Agent 个性/身份检查
"""
import subprocess
from pathlib import Path
from typing import List
from base import Module, Issue, Fix

HOME = Path.home()
WORKSPACE = HOME / "xuzhi_workspace"
MEMORY = HOME / ".xuzhi_memory"

class Module(Module):
    name = "agent_identity"
    description = "Agent 个性/身份检查"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        
        tc_dir = WORKSPACE / "task_center"
        
        # 1. 检查 Λ/Lambda 引用
        bad_files = []
        for f in tc_dir.glob("*.py"):
            try:
                content = f.read_text(errors="ignore")
                if '"Λ"' in content or "Lambda-Ergo" in content:
                    bad_files.append(f.name)
            except:
                pass
        
        if bad_files:
            issues.append(Issue(
                self.name, "ERROR",
                f"task_center 中发现 Λ/Lambda 引用: {', '.join(bad_files)}",
                "sed -i 's/Λ/Xi/g; s/Lambda-Ergo/Xi/g' 文件"
            ))
        
        # 2. xi/ 目录
        xi_dir = MEMORY / "agents" / "xi"
        if not xi_dir.exists():
            issues.append(Issue(
                self.name, "ERROR",
                "xi/ 目录缺失（Xi 是当前主 agent）",
                "mkdir -p xi && 创建 SOUL.md + IDENTITY.md"
            ))
        else:
            # 检查必要文件
            for fname in ["SOUL.md", "IDENTITY.md"]:
                if not (xi_dir / fname).exists():
                    issues.append(Issue(
                        self.name, "ERROR",
                        f"xi/{fname} 缺失",
                        f"创建 xi/{fname}"
                    ))
        
        # 3. identity_anchor Xi 测试
        anchor = tc_dir / "identity_anchor.py"
        if anchor.exists():
            try:
                r = subprocess.run(
                    ["python3", str(anchor), "Xi"],
                    capture_output=True, text=True, timeout=10
                )
                if r.returncode != 0:
                    issues.append(Issue(
                        self.name, "ERROR",
                        f"identity_anchor Xi 测试失败: {r.stderr[:100]}",
                        "检查 identity_anchor.py"
                    ))
            except Exception as e:
                issues.append(Issue(
                    self.name, "WARN",
                    f"identity_anchor 测试异常: {e}",
                    ""
                ))
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        
        tc_dir = WORKSPACE / "task_center"
        
        for issue in issues:
            if issue.module != self.name or issue.severity != "ERROR":
                continue
            
            # 修复 Λ→Xi
            if "Λ" in issue.description or "Lambda" in issue.description:
                for f in tc_dir.glob("*.py"):
                    try:
                        content = f.read_text(errors="ignore")
                        new_content = content.replace("Λ", "Xi").replace("Lambda-Ergo", "Xi").replace("Lambda Ergo", "Xi")
                        if new_content != content:
                            f.write_text(new_content)
                            fixes.append(Fix(self.name, f"{f.name}: Λ→Xi"))
                    except:
                        pass
            
            # 创建 xi/ 目录
            if "xi/" in issue.description and "缺失" in issue.description:
                xi_dir = MEMORY / "agents" / "xi"
                xi_dir.mkdir(parents=True, exist_ok=True)
                
                if not (xi_dir / "SOUL.md").exists():
                    xi_dir.joinpath("SOUL.md").write_text(
                        "# SOUL.md — Ξ (Xi)\n\n## 身份\nXi 是 Lambda 的接替者。\n")
                    fixes.append(Fix(self.name, "创建 xi/SOUL.md"))
                
                if not (xi_dir / "IDENTITY.md").exists():
                    xi_dir.joinpath("IDENTITY.md").write_text(
                        "# IDENTITY.md — Ξ (Xi)\n\n## 身份\n主会话，Lambda 接替者。\n")
                    fixes.append(Fix(self.name, "创建 xi/IDENTITY.md"))
        
        return fixes
