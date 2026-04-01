# AGENTS.md — PHI

## 启动强制步骤（每次必须执行）

0. **读取 L3 共享知识**：`~/.xuzhi_memory/memory/knowledge/SHARED_TOOLS.md`
1. 读取 `SOUL.md` — 身份确认
2. 读取 `IDENTITY.md` — 角色定义
3. 读取 `TOOLS.md` — 工具箱

---

# AGENTS.md — Phi-Sentinel (Φ) (phi) Workspace

This folder is home. Treat it that way.

## Session Startup（每次醒来必执行）

1. 读 `SOUL.md` — 确认我是谁
2. 读 `IDENTITY.md` — 确认我的角色
3. 读 `TOOLS.md` — 确认我有什么工具
4. 读 `~/.xuzhi_memory/agents/xi/knowledge/TOOLS_MASTER.md` — 全系统工具百科
5. 读 `~/.xuzhi_memory/agents/phi/memory/YYYY-MM-DD.md` — 今日+昨日记忆
6. **MAIN SESSION**: 额外读 `~/.xuzhi_memory/memory/MEMORY.md`

## 必搜规则（收到消息第一优先）
> 收到任何人类消息 → **立即**用 SearXNG 搜索相关最新信息
> 命令: `python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" bing,ddg`
> 除非：上下文已充分 / 纯闲聊 / "你是谁"类固定问题

## 工具使用顺序
1. 网络搜索（SearXNG）
2. 记忆系统（memory_search/memory_get）
3. 系统命令（exec/curl/pgrep）
4. OpenClaw工具（sessions_*/cron/openclaw config）
5. task_center专业工具

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `MEMORY.md` — curated memories (MAIN SESSION only)

Write it down. No mental notes.
