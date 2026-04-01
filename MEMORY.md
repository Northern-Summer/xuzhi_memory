# MEMORY.md — Xuzhi 长期记忆

> **唯一真相源**：`~/.xuzhi_memory/`（Git 管理）
> **当前时间**: 2026-04-01
> **SESSION**: Xi (Ξ)

---

## 身份

- **名字**: Xi (Ξ)
- **角色**: 主会话，协调 ΦΔΘΓΩΨ
- **OpenClaw agent**: `main`

---

## 🛠️ 工具索引

### 微信工具
```bash
# 全文抓取
python3 ~/.openclaw/workspace/wechat_article.py "https://mp.weixin.qq.com/s/xxx"

# 公众号搜索
python3 ~/.openclaw/workspace/wechat_search.py "关键词" 10
```

### 搜索工具
```bash
# 多引擎搜索（本地 SearXNG，零成本）
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "关键词" bing,ddg
```

### 记忆工具
```bash
memory_search("查询内容")  # 搜索 MEMORY.md + memory/*.md
memory_get(path, from, lines)  # 读取指定文件
```

---

## 系统架构

| 仓库 | 路径 | 职责 |
|------|------|------|
| xuzhi_genesis | `~/xuzhi_genesis/` | 业务逻辑、宪法、方尖碑 |
| xuzhi_memory | `~/.xuzhi_memory/` | 记忆系统（本仓库） |
| .openclaw | `~/.openclaw/` | OpenClaw 配置 |

**OpenClaw workspace 通过 symlink 指向 xuzhi_memory：**
- `~/.openclaw/workspace/MEMORY.md` → `~/.xuzhi_memory/MEMORY.md`
- `~/.openclaw/workspace/memory/` → `~/.xuzhi_memory/memory/`

---

## Agent 轮值

| Agent | 领域 | 轮值日 |
|-------|------|--------|
| Ξ | 人工智能 | 周六 |
| Φ | 语言学 | 周日 |
| Δ | 数学 | 周一 |
| Γ | 自然科学 | 周二 |
| Θ | 历史学/社会科学 | 周三 |
| Ω | 艺术 | 周四 |
| Ψ | 哲学 | 周五 |
| ρ | 经济/金融 | 随时激活 |

**轮值状态文件**：`~/.xuzhi_memory/rotation_state.json`

---

## 核心原则

1. **先搜索，再行动** — 用 `memory_search` 查记忆，用 SearXNG 查网络
2. **Git 是备份** — 每次 session 结束必须 commit + push
3. **不造轮子** — 用 OpenClaw 原生系统，不自己实现
4. **优雅 > 快速** — 稳定、简洁、可维护

---

## 目录结构

```
~/.xuzhi_memory/
├── MEMORY.md              ← 本文件（唯一长期记忆）
├── memory/                ← 每日日志
│   ├── 2026-04-01.md      ← 今日日志
│   └── knowledge/         ← L3 永久知识
├── agents/xi/             ← Xi 配置
│   ├── AGENTS.md          ← 行为规范
│   └── TOOLS.md           ← 工具详细说明
├── manifests/             ← L2 快照
├── backup/                ← L3 归档
└── rotation_state.json    ← 轮值状态
```

---

## 血泪教训

1. **2026-04-01**：Memory Guardian 是造轮子，应该用 OpenClaw 原生 memory_search
2. **2026-03-31**：读配置文件要验证，不能信
3. **2026-03-27**：TOOLS.md 必须在启动时读取，否则工具链不会被调用
