import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
"""
Path Consistency Module — 路径一致性检查

检查任务:
1. task_center 是否在正确位置 (xuzhi_workspace/ 而非 xuzhi_memory/)
2. quota_usage.json 位置
3. HEARTBEAT.md quota 路径
4. 其他关键路径
"""
import subprocess
from pathlib import Path
from typing import List
from base import Module, Issue, Fix

HOME = Path.home()
WORKSPACE = HOME / "xuzhi_workspace"
MEMORY = HOME / ".xuzhi_memory"
OPENCLAW = HOME / ".openclaw" / "workspace"

# 关键文件（模块名 -> 期望路径）
CRITICAL_FILES = {
    "judgment_core.py": WORKSPACE / "task_center",
    "context_trimmer.py": WORKSPACE / "task_center",
    "rate_limiter.py": WORKSPACE / "task_center",
    "expert_learner.py": WORKSPACE / "task_center",
    "expert_watchdog.py": WORKSPACE / "task_center",
    "MEMORY.md": OPENCLAW,
    "SOUL.md": OPENCLAW,
    "AGENTS.md": OPENCLAW,
    "HEARTBEAT.md": OPENCLAW,
}

class Module(Module):
    name = "path_consistency"
    description = "路径一致性检查"
    
    def diagnose(self) -> List[Issue]:
        issues = []
        
        # 1. task_center 源码(.py)不应在 xuzhi_memory
        wrong_tc = MEMORY / "task_center"
        if wrong_tc.exists():
            py_files = list(wrong_tc.glob("*.py"))
            if py_files:
                issues.append(Issue(
                    self.name, "ERROR",
                    f"task_center 源码存在于 xuzhi_memory/ (应在 xuzhi_workspace/): {len(py_files)} 个 .py",
                    f"移动源码: mv {wrong_tc}/*.py {WORKSPACE}/task_center/"
                ))
            else:
                issues.append(Issue(
                    self.name, "INFO",
                    f"task_center/ 状态目录存在于 xuzhi_memory/ (正常，仅含状态文件)",
                    ""
                ))
        
        # 2. 检查关键文件存在性
        for filename, expected_dir in CRITICAL_FILES.items():
            # 在多个可能位置查找
            found = False
            for search_dir in [WORKSPACE, WORKSPACE/"task_center", OPENCLAW, OPENCLAW/"task_center"]:
                if (search_dir / filename).exists():
                    found = True
                    break
            
            if not found:
                issues.append(Issue(
                    self.name, "ERROR",
                    f"关键文件缺失: {filename}",
                    f"从 git 历史恢复或重建"
                ))
        
        # 3. HEARTBEAT.md quota 路径
        hb = OPENCLAW / "HEARTBEAT.md"
        if hb.exists():
            content = hb.read_text()
            if "quota_status.json" in content:
                issues.append(Issue(
                    self.name, "ERROR",
                    "HEARTBEAT.md 使用错误 quota 路径 (quota_status.json)",
                    "sed -i 's/quota_status.json/quota_usage.json/g' HEARTBEAT.md"
                ))
        
        # 4. quota_usage.json 位置
        quota_candidates = [
            OPENCLAW / "centers" / "engineering" / "crown" / "quota_usage.json",
            MEMORY / "centers" / "engineering" / "crown" / "quota_usage.json",
        ]
        quota_found = any(p.exists() for p in quota_candidates)
        if not quota_found:
            issues.append(Issue(
                self.name, "WARN",
                "quota_usage.json 未找到",
                "运行 quota_monitor.py 生成"
            ))
        
        # 5. .openclaw/centers 必须是 symlink，指向 Xuzhi_genesis/centers/
        claw_centers = HOME / ".openclaw" / "centers"
        expected_target = str(HOME / "Xuzhi_genesis" / "centers")
        if claw_centers.exists():
            if claw_centers.is_symlink():
                actual_target = str(claw_centers)  # 不跟随resolve，保持symlink原始目标
                if actual_target != expected_target:
                    issues.append(Issue(
                        self.name, "ERROR",
                        f".openclaw/centers symlink 指向错误目标: {actual_target}",
                        f"重建: rm {claw_centers} && ln -sfn {expected_target} {claw_centers}"
                    ))
            else:
                issues.append(Issue(
                    self.name, "ERROR",
                    f".openclaw/centers 是目录而非 symlink（灾变断裂特征）",
                    f"重建: rm -rf {claw_centers} && ln -sfn {expected_target} {claw_centers}"
                ))
        else:
            issues.append(Issue(
                self.name, "ERROR",
                ".openclaw/centers 不存在（symlink 断裂）",
                f"创建: ln -sfn {expected_target} {claw_centers}"
            ))
        
        # 6. xuzhi_memory/centers/ 不应存在（职责回归 Xuzhi_genesis）
        memory_centers = MEMORY / "centers"
        if memory_centers.exists():
            issues.append(Issue(
                self.name, "ERROR",
                f"xuzhi_memory/centers/ 冗余目录仍然存在（应已删除）",
                f"删除: gio trash {memory_centers}"
            ))
        
        return issues
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        
        # 只处理 path_consistency 模块的 ERROR
        for issue in issues:
            if issue.module != self.name or issue.severity != "ERROR":
                continue
            
            # 修复 HEARTBEAT quota 路径
            if "HEARTBEAT" in issue.description and "quota_status" in issue.description:
                hb = OPENCLAW / "HEARTBEAT.md"
                if hb.exists():
                    content = hb.read_text()
                    if "quota_status.json" in content:
                        hb.write_text(content.replace("quota_status.json", "quota_usage.json"))
                        fixes.append(Fix(self.name, "HEARTBEAT.md: quota_status.json → quota_usage.json"))
        
            # 修复 task_center 源码误放
            if "task_center 源码" in issue.description and "xuzhi_memory" in issue.description:
                wrong_tc = MEMORY / "task_center"
                for py_file in wrong_tc.glob("*.py"):
                    py_file.unlink()  # 删除重复源码
                    fixes.append(Fix(self.name, f"删除重复: {py_file.name}"))
                # 如果目录空了，删除目录
                if not list(wrong_tc.glob("*")):
                    wrong_tc.rmdir()
                    fixes.append(Fix(self.name, "删除空目录 task_center/"))

        return fixes
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        fixes = []
        
        # 只处理 path_consistency 模块的 ERROR
        for issue in issues:
            if issue.module != self.name or issue.severity != "ERROR":
                continue
            
            # 修复 HEARTBEAT quota 路径
            if "HEARTBEAT" in issue.description and "quota_status" in issue.description:
                hb = OPENCLAW / "HEARTBEAT.md"
                if hb.exists():
                    content = hb.read_text()
                    if "quota_status.json" in content:
                        hb.write_text(content.replace("quota_status.json", "quota_usage.json"))
                        fixes.append(Fix(self.name, "HEARTBEAT.md: quota_status.json → quota_usage.json"))
        
            # 修复 task_center 源码误放
            if "task_center 源码" in issue.description and "xuzhi_memory" in issue.description:
                wrong_tc = MEMORY / "task_center"
                for py_file in wrong_tc.glob("*.py"):
                    py_file.unlink()  # 删除重复源码
                    fixes.append(Fix(self.name, f"删除重复: {py_file.name}"))
                # 如果目录空了，删除目录
                if not list(wrong_tc.glob("*")):
                    wrong_tc.rmdir()
                    fixes.append(Fix(self.name, "删除空目录 task_center/"))

            # 修复 .openclaw/centers symlink
            if ".openclaw/centers" in issue.description:
                import shutil, os
                claw_centers = HOME / ".openclaw" / "centers"
                expected_target = str(HOME / "Xuzhi_genesis" / "centers")
                if claw_centers.exists() and not claw_centers.is_symlink():
                    shutil.move(str(claw_centers), str(claw_centers) + ".BROKEN")
                elif claw_centers.is_symlink() and str(claw_centers) != expected_target:
                    claw_centers.unlink()
                os.symlink(expected_target, str(claw_centers))
                fixes.append(Fix(self.name, f".openclaw/centers symlink 重建 → Xuzhi_genesis/centers/"))
            
            # 修复 xuzhi_memory/centers/ 冗余
            if "xuzhi_memory/centers" in issue.description and "冗余" in issue.description:
                memory_centers = MEMORY / "centers"
                if memory_centers.exists():
                    # 交给系统 trash
                    import subprocess
                    result = subprocess.run(["gio", "trash", str(memory_centers)],
                        capture_output=True, text=True)
                    if result.returncode == 0:
                        fixes.append(Fix(self.name, f"xuzhi_memory/centers/ 已 gio trash"))
                    else:
                        fixes.append(Fix(self.name, f"xuzhi_memory/centers/ 清理失败: {result.stderr}"))
        
        return fixes
