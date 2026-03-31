"""
Xuzhi System Repair — 模块注册表
"""
from pathlib import Path

# 动态加载所有模块
__all__ = []

for f in Path(__file__).parent.glob("*.py"):
    if f.stem not in ("__init__", "base"):
        __all__.append(f.stem)
