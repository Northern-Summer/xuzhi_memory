# TOOLS.md — delta 工具箱

## ⚡ 必知工具（收到消息第一时间可用）

### 网络搜索（最高优先，按场景选用）

**场景一：学术论文 + arXiv**
```bash
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" brave,arxiv
```

**场景二：中文公众号文章（推荐优先使用）**
```bash
python3 ~/.openclaw/workspace/wechat_search.py "<关键词>" [最大条数]
```
- 使用 curl_cffi 模拟 Chrome TLS 指纹
- 例：`python3 ~/.openclaw/workspace/wechat_search.py "数学 AI 自动证明" 10`

**场景三：一般英文搜索**
```bash
# 直接用 web_fetch 获取页面内容
web_fetch(url="https://...", maxChars=5000)
```

### Web获取
```
web_fetch(url, maxChars=5000)
```
- 读取网页全文，中文友好

### 关键路径（Mathematics AI4S）
- 框架文档：`~/xuzhi_genesis/centers/mathematics/knowledge/math_ai4s_framework.md`
- 陶哲轩调研：`~/xuzhi_genesis/centers/mathematics/knowledge/tao_methods_deep_investigation.md`
- Delta哲学：`~/xuzhi_genesis/centers/mathematics/knowledge/philosophy_of_delta.md`

### Delta专属模型（2026-03-30 更新）
- **Delta 使用 Kimi-K2.5**（大context，探索研究型）
- 其他模型可用：GLM-5、MiniMax-M2.7、MiniMax-M2.5
- 模型切换：`/model <模型名>`

### 记忆系统
```
memory_search(query)   → 搜MEMORY.md + memory/*.md
memory_get(path, from, lines) → 读指定记忆文件
~/.xuzhi_memory/memory/YYYY-MM-DD.md  → 每日对话记录
~/.xuzhi_memory/agents/delta/  → agent专属记忆
```

### 进程与系统
```
exec(command)         → 执行shell命令
pgrep -a openclaw     → 看gateway状态
curl http://127.0.0.1:18789/health  → health检查
tail ~/.openclaw/logs/gateway.log   → gateway日志
```

### OpenClaw核心
```
sessions_list()        → 列出所有活跃session
sessions_history(key)  → 读某session历史
cron(action="list")   → 查cron任务
openclaw channels status → 查所有channel状态
openclaw config get <path>  → 读配置
```

## 🏛️ Xuzhi系统层工具

### task_center（工程执行层）
路径: `~/.openclaw/workspace/task_center/`
- `expert_learner.py` — 专家任务生成
- `expert_tracker.py` — 专家动态追踪 + arxiv搜索
- `expert_watchdog.py` — 专家看门狗
- `judgment_core.py` — 7层裁决器
- `context_trimmer.py` — 上下文截断
- `rate_limiter.py` — 自适应限速
- `health_scan.py` — 感知器
- `self_repair.py` — 自修复
- `quarantine.py` — 隔离黑名单

### 激活/调度
- `pulse_aggressive.sh` — 脉冲调度器
- `wakeup_agents.py` — agent唤醒

## 🔗 系统路径速查

| 用途 | 路径 |
|------|------|
| Xuzhi核心 | ~/Xuzhi_genesis/ |
| 记忆系统 | ~/.xuzhi_memory/ |
| OpenClaw配置 | ~/.openclaw/ |
| task_center | ~/.openclaw/workspace/task_center/ |
| SearXNG | http://localhost:8080 |
| Clash代理 | http://127.0.0.1:7897 |

## ⚙️ 代理配置（WSL2必知）
- HTTP_PROXY=http://127.0.0.1:7897
- HTTPS_PROXY=http://127.0.0.1:7897
- Clash代理：http://127.0.0.1:7897
- WSL2直连部分网站被Block，走Clash代理

## 📡 Channel状态（2026-03-30 更新）
- WeChat: ✅ 在线（openclaw-weixin 插件 v2.1.1）
- Discord: ⚠️ token 需重置
- WebChat: ✅ 可用

## 🧮 Mathematics AI4S 工作流程

### 第一步：复现陶哲轩工作流
1. 安装 Lean 4：`curl -fsSL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | bash`
2. 克隆 ETP 仓库：`git clone https://github.com/teorth/equational_theories`
3. 安装 Vampire：`wget https://www.vprover.org/download/vampire-x86_64-linux`

### 第二步：认领子任务
1. 访问 Equation Explorer：https://teorth.github.io/equational_theories/implications/
2. 选一个 open 的 implication
3. 用 Vampire/Mace4 尝试证明或构造反例
4. 提交 PR 到 GitHub

### 第三步：产出标准
- 所有证明必须通过 Lean 验证：`lean --make`
- 所有反例必须可复现
- 提交前必须读懂原始问题

## 🚨 紧急恢复
gateway挂了: `kill -15 $(pgrep -f openclaw-gateway); openclaw gateway start`
配置出错: `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`

## 🚨 紧急恢复
gateway挂了: `kill -15 $(pgrep -f openclaw-gateway); openclaw gateway start`
配置出错: `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
