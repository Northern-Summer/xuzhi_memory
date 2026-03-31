#!/usr/bin/env python3
"""
agent_selector.py — 轻量级Agent路由选择器
routing rule: random | by_load | by_capability | by_name
"""
import json, random, sys
from pathlib import Path

HOME = Path("/home/summer")
REGISTRY = HOME / ".openclaw" / "agents"
MEMORY = HOME / ".xuzhi_memory"

def load_agents():
    """动态加载所有已注册的Agent。
    
    工程改进铁律合规 — Ξ | 2026-03-26
    自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
    修复：移除hardcoded席位列表，改为动态扫描，避免每次新增Agent都要改代码。
    """
    agents = {}
    # 动态扫描所有 .json 文件作为候选席位
    for f in REGISTRY.glob("*.json"):
        name = f.stem
        # 排除模板和已死亡Agent
        if name in ("template", "lambda-ai", "sec-ai-x", "sec-ai-y"):
            continue
        try:
            d = json.load(open(f))
            # 跳过明确标记为 disabled 的Agent
            if "enabled" in d and d["enabled"] is False:
                continue
            agents[name] = {
                "session": None,  # 未连接
                "mode": d.get("mode", "unknown"),
                "last_active": None,
            }
        except Exception:
            pass
    # 额外扫描目录形式的Agent（如 xi/ → Ξ）
    for entry in REGISTRY.iterdir():
        if entry.is_dir() and entry.name not in agents:
            # 目录形式的Agent（如 Ξ、Ρ 等希腊字母目录）
            agents[entry.name] = {
                "session": None,
                "mode": "unknown",
                "last_active": None,
            }
    return agents

def get_system_state():
    """检查系统状态：哪个agent最活跃"""
    ratings_file = HOME / ".xuzhi_memory" / "centers" / "mind" / "society" / "ratings.json"
    if ratings_file.exists():
        d = json.load(open(ratings_file))
        return d.get("agents", {})
    return {}

def select_random():
    agents = load_agents()
    if not agents: return None
    return random.choice(list(agents.keys()))

def select_by_load():
    """选择quota最空闲的agent"""
    state = get_system_state()
    best, best_score = None, -1
    for name, info in state.items():
        rel = info.get("reliability", 0)
        if rel > best_score:
            best_score = rel
            best = name
    return best

def select_by_capability(capability):
    """按能力选择：phi=security, delta=engineering, theta=research"""
    cap_map = {
        "security": "phi", "sentinel": "phi",
        "engineering": "delta", "forge": "delta",
        "research": "theta", "exploration": "theta", "intelligence": "theta",
        "archive": "gamma", "recording": "gamma",
        "night": "omega", "ending": "omega",
        "philosophy": "psi",
    }
    name = cap_map.get(capability.lower())
    if name:
        agents = load_agents()
        if name in agents: return name
    return None

def select_by_name(name):
    """指定某个agent"""
    agents = load_agents()
    if name in agents: return name
    return None

def main():
    available = list(load_agents().keys())
    if len(sys.argv) < 2:
        print("Usage: agent_selector.py [random|load|capability|{agent_name}]")
        print(f"Available agents (dynamic): {available}")
        sys.exit(1)

    rule = sys.argv[1].lower()

    if rule == "random":
        result = select_random()
    elif rule == "load":
        result = select_by_load()
    elif rule == "capability":
        cap = sys.argv[2] if len(sys.argv) > 2 else "phi"
        result = select_by_capability(cap)
    elif rule in available:
        # 动态允许任何已注册的Agent（无需hardcoded列表）
        result = select_by_name(rule)
    else:
        result = select_by_capability(rule)

    if result:
        print(result)
        sys.exit(0)
    else:
        print("NO_AGENT_AVAILABLE")
        sys.exit(1)

if __name__ == "__main__":
    main()
