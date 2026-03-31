"""
Module Base — 模块基类
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Issue:
    module: str
    severity: str  # ERROR, WARN, INFO
    description: str
    fix_hint: str = ""

@dataclass
class Fix:
    module: str
    description: str
    backed_up: bool = False

class Module(ABC):
    name: str = ""
    description: str = ""
    
    def diagnose(self) -> List[Issue]:
        return []
    
    def fix(self, issues: List[Issue]) -> List[Fix]:
        return []
    
    def backup(self) -> bool:
        return True
