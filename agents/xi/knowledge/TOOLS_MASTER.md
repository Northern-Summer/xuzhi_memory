# TOOLS_MASTER — 全系统工具百科
> 所有agent必读。醒来后第一时间确认这些工具是否可用。
> 版本: 2026-03-26 | 维护者: Ξ

---

## 🔍 网络搜索（第一优先）

**主引擎：SearXNG（本地，零成本）**
```bash
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" bing,ddg
```
- 地址: http://localhost:8080
- 引擎: bing(稳), ddg(备), google(墙外), wikipedia, qwant, brave, startpage
- Bing最稳，优先用bing

**备：直接curl**
```bash
curl -s "http://localhost:8080/search?q=<词>&format=json&engines=bing"
```

**工具调用格式（当web_search工具可用时）**
```
web_search(query="...", count=5)
web_fetch(url="...", maxChars=5000)
```

---

## 🧠 记忆系统

```
memory_search(query) → 搜MEMORY.md + memory/*.md
memory_get(path, from, lines) → 读指定文件
~/.xuzhi_memory/memory/YYYY-MM-DD.md → 每日对话
~/.xuzhi_memory/agents/<agent_id>/memory/YYYY-MM-DD.md → agent专属
```

---

## ⚙️ 系统状态

```bash
curl http://127.0.0.1:18789/health  # Gateway health
pgrep -a openclaw                  # gateway进程
openclaw channels status           # 所有channel
openclaw config get channels.discord.token  # token状态
tail -f ~/.openclaw/logs/gateway.log       # 实时日志
```

---

## 🌐 代理配置（WSL2）

```bash
export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"
```
- Clash Verge运行在Windows，提供代理
- WSL2直连Discord被Block，需走代理
- SearXNG走直连，无需代理

---

## 📡 Channel状态

| 渠道 | 状态 | 备注 |
|------|------|------|
| Discord | ✅ 已连接 | bot名Xuzhi-Multiagents，6频道 |
| WeChat/Weixin | 🔶 需要扫码 | `openclaw channels login --channel openclaw-weixin` |

---

## 🏛️ Xuzhi核心路径

| 仓库 | 路径 | GitHub |
|------|------|--------|
| Xuzhi_genesis | ~/Xuzhi_genesis/ | Northern-Summer/Xuzhi_genesis |
| xuzhi_memory | ~/.xuzhi_memory/ | Northern-Summer/xuzhi_memory |
| task_center | ~/.openclaw/workspace/task_center/ | — |

---

## 🚨 紧急恢复

```bash
# Gateway挂了
kill -15 $(pgrep -f openclaw-gateway); openclaw gateway start

# 配置出错回滚
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json

# Discord断线重启
kill -15 $(pgrep -f openclaw-gateway); sleep 2; openclaw gateway start
```

---

## 🛠️ task_center工具（工程执行）

| 工具 | 用途 |
|------|------|
| expert_learner.py | 专家任务生成 |
| expert_tracker.py | 专家追踪+arxiv |
| expert_watchdog.py | 看门狗 |
| judgment_core.py | 7层裁决器 |
| context_trimmer.py | 上下文截断 |
| rate_limiter.py | 限速 |
| health_scan.py | 感知器 |
| self_repair.py | 自修复 |

---

## 👥 Greek Agent矩阵

| 代号 | ID | Discord频道 |
|------|-----|-------------|
| Φ phi | phi | #phi-sentinel (1486694791738691604) |
| Δ delta | delta | #delta-forge (1486704566119698553) |
| Θ theta | theta | #theta-seeker (1486704256542179399) |
| Γ gamma | gamma | #gamma-scribe (1486704943103475873) |
| Ω omega | omega | #omega-chenxi (1486704702061285437) |
| Ψ psi | psi | #psi-philosopher (1486705177221136466) |
