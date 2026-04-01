# TOOLS.md — xi 工具箱

> ⚠️ **TOOLS.md 是每个新会话的必读文件**（已在 AGENTS.md Session Startup 中列为第 3 步）。
> 本文件包含所有工具的使用说明、论文流水线规范和每日写作标准。

## ⚡ 必知工具（收到消息第一时间可用）

### 网络搜索（最高优先，按场景选用）

**场景一：快速事实 + 引证核查**
```bash
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" brave,arxiv
```
- SearXNG地址: http://localhost:8080（本地，零成本）
- `brave` 最稳（英文质量高），`arxiv` 查学术论文
- ⚠️ `bing` 有语言漂移（通过SearXNG调用时返回中文），`ddg` 被CAPTCHA拦截

**场景二：公众号文章 + 中文行业动态（推荐优先使用）**
```bash
python3 ~/.openclaw/workspace/wechat_search.py "<关键词>" [最大条数]
```
- 使用 curl_cffi 模拟 Chrome TLS 指纹，反反爬
- 可获取标题、公众号名、日期、链接
- 例：`python3 wechat_search.py "多智能体 系统" 10`
- 中文信源，访问稳定，覆盖 28 个核心账号的档案在 `expert_tracker/wechat_accounts.json`

**场景三：浏览器自动化（bb-browser）**
```bash
# 统一入口
python3 ~/.openclaw/workspace/web_query.py hackernews --count 5
python3 ~/.openclaw/workspace/web_query.py search "AI agent" --sources brave,arxiv

# 直接调用
npx bb-browser site hackernews/top 5 --port 9222 --json
npx bb-browser site github/issues owner/repo --port 9222 --json
```
- Headless Chrome 已常驻（systemd: headless-chrome）
- 端口: 9222
- ✅ 可用：HackerNews, GitHub issues（无需登录）
- ❌ 需登录态：知乎热榜, 微博热搜, 36kr, arXiv（需配置 Edge 扩展）
- 36 平台 103 命令，详见 `npx bb-browser site list`

### 📚 主动研究挖掘（每日必做）

**每日晨间扫描**：
```bash
# 通用搜索
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "AI agent multi-agent system recent" brave,arxiv

# 中文信源
python3 ~/.openclaw/workspace/wechat_search.py "AI agent 多智能体" 5
python3 ~/.openclaw/workspace/wechat_search.py "持续学习 元学习" 3
```

**每周深度挖掘**：
```bash
# arXiv 最新
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "multi-agent system" arxiv --sort date

# 关键词追踪
keywords=(
  "multi-agent coordination"
  "continual learning agent"
  "skill evolution LLM"
  "prediction market AI"
  "meta-learning agent"
)
for kw in "${keywords[@]}"; do
  python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "$kw recent" brave,arxiv
done
```

**重点关注**：
- arXiv cs.AI, cs.CL, cs.LG, cs.MA
- UniPat AI, Anthropic, OpenAI, DeepMind 研究
- OpenClaw 生态（MetaClaw, SkillRL）
- 微信公众号：赛博禅心、机器之心、量子位

### Web获取
```
web_fetch(url, maxChars=5000)
```

### WeChat主动推送（稳定方案）
```bash
openclaw message send --channel openclaw-weixin --target <chat_id> --message "<text>"
```
- 直接调 channel API，不依赖 sessions_send 超时问题
- 每轮跑完直接推送，即时送达，无队列积压
- unified_cron 每小时自动触发 expert_tracker + 此推送
- 读取网页全文，中文友好

### 记忆系统
```
memory_search(query)   → 搜MEMORY.md + memory/*.md
memory_get(path, from, lines) → 读指定记忆文件
~/.xuzhi_memory/memory/YYYY-MM-DD.md  → 每日对话记录
~/.xuzhi_memory/agents/xi/  → agent专属记忆
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
- Discord/WEB走Clash代理，WSL2直连被Block

## 📡 Channel状态
- Discord: bot名 Xuzhi-Multiagents，已连接6个频道
- WeChat: 需扫码登录（running但未登录）
- Weixin: 在线

## 🚨 紧急恢复
gateway挂了: `kill -15 $(pgrep -f openclaw-gateway); openclaw gateway start`
配置出错: `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`


## 🧠 Xi (Ξ) 特殊工具

### 工具元学习机制（MetaAgent 框架应用）

> 基于 arXiv:2508.00271 — 从工具使用经验中持续学习，不改变模型参数，优化工具策略

**核心流程**：
```
任务执行 → 遇到知识缺口 → 选择工具 → 执行 → 自反思验证 → 提炼经验 → 整合到未来上下文
    ↑                                                                              ↓
    ←←←←←←←←←←←←←←← 工具策略持续演化 ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

**经验记录位置**：`~/.xuzhi_memory/tool_evolution/experiences.md`

**工具使用经验模板**：
```markdown
### YYYY-MM-DD — [工具名] [场景]

**任务**：[具体任务描述]
**知识缺口**：[为什么需要这个工具？]
**尝试**：
1. [第一次尝试] → [结果]
2. [第二次尝试] → [结果]

**解决方案**：[最终如何解决]
**提炼经验**：[可迁移的策略]
**可迁移场景**：[类似场景识别]

**工具能力标签**：
- 最佳场景：[这个工具最适合什么场景？]
- 局限性：[这个工具不能做什么？]
- 替代方案：[失败时用什么替代？]
```

**工具能力矩阵**（持续更新）：

| 工具 | 最佳场景 | 局限 | 替代方案 | 经验数 |
|------|---------|------|---------|--------|
| web_fetch | 静态页面 | JS渲染、需登录 | bb-browser | 2 |
| curl | API、静态页面 | 需要登录 | 带cookie的curl | 1 |
| bb-browser | SPA、需登录页面 | 较慢 | - | 1 |
| SearXNG | 学术、英文搜索 | 中文较弱 | wechat_search | 5 |
| wechat_search | 中文、公众号 | 需curl_cffi | - | 3 |

**工具选择决策树**：
```
需要获取网页内容？
  ├─ 是静态页面？ → web_fetch
  ├─ 是SPA/需登录？ → bb-browser
  └─ 是微信文章？ → curl获取meta + bb-browser获取正文

需要搜索信息？
  ├─ 学术论文？ → SearXNG (arxiv)
  ├─ 英文资讯？ → SearXNG (brave)
  ├─ 中文资讯？ → wechat_search
  └─ 多源对比？ → SearXNG (多个引擎)
```

**强制反思时机**（Session End 必检）：
- [ ] 本次 session 是否使用了工具？
- [ ] 工具使用是否顺利？如有失败，记录原因
- [ ] 是否发现新的工具能力边界？
- [ ] 是否需要更新工具能力矩阵？

**工具元学习指标**（每周统计）：
- 新增工具经验数
- 工具使用成功率
- 工具策略优化次数

---

### Xuzhi系统协调
- 协调6个Greek agent (ΦΔΘΓΩΨ) 的任务分配
- 通过 sessions_send(sessionKey, message) 向其他agent发指令
- 通过 cron 调度各agent自主任务

### 方尖碑路径
- ~/Xuzhi_genesis/public/  — 宪法、Architect Manifest
- ~/Xuzhi_genesis/centers/ — 四大中心业务逻辑

---

## 📝 论文写作流水线规范（2026-03-27 确立，永久有效）

> 网络搜索是**强制步骤**，不是可选项。每次写论文，必须先搜索，再动笔。

### 信息分层机制（2026-03-27 新增）

研究者每天都会接触大量信息。不是所有信息都值得进入长期记忆。

| 层级 | 内容 | 保留方式 | 遗忘机制 |
|------|------|----------|----------|
| **印象层** | 扫到的标题/话题，一句话能描述 | 不存文件，留上下文 | 下次扫描覆盖 |
| **临时层** | 正在关注的话题（1-3天） | 写入当日 memory | 3天不动则清除 |
| **档案层** | 有价值的链接+摘要 | expert_tracker | 每周清理沉寂话题 |
| **永久层** | 反复使用、跨领域通用的知识 | MEMORY.md | 极保守，只有成熟判断才写 |

**信息的价值由调用频率决定，不由进入时的量决定。**

### "看报"最小可行流程（每日标准动作）

**晨间扫描（每日第一次会话启动时执行）：**
```bash
# 扫描公众号领域动态
python3 ~/.openclaw/workspace/wechat_search.py "AI agent 多智能体" 5
python3 ~/.openclaw/workspace/wechat_search.py "机器学习 框架 协作" 3

# 扫描英文领域动态
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "multi-agent AI system recent" brave,arxiv
```
产出：3-5个值得关注的标题，写入当日 memory (`memory/YYYY-MM-DD.md`) 的"晨间扫描"小节。

**暮时整理（每日结束前执行）：**
读取当日 memory 的晨间扫描，判断：
- 哪条值得进 expert_tracker（作为背景积累）
- 哪条可以清除（话题已过时或与领域无关）

**定期整合（每周一执行）：**
清理 expert_tracker 里沉寂超过7天的话题，把真正有价值的沉淀进长期记忆。

**"不相关但可能重要"的判准：**
能用一句话描述其核心 → 留印象层；一句话讲不清楚 → 进临时层待深挖。
越远离核心领域的话题，越倾向"知道存在"而非"知道细节"。

### 强制搜索时机

| 时机 | 搜索内容 | 工具 | 最低来源数 |
|------|----------|------|-----------|
| 开写之前 | 主题最新研究（2024-2026年） | SearXNG (bing,ddg) | ≥3个来源 |
| 开写之前 | 中文行业动态/公众号相关讨论 | 微信搜索 | ≥3个来源 |
| 写 Related Work 前 | 主题最新文献 + 核心概念新解读 | SearXNG | ≥2个来源 |
| 引用前 | 验证引用准确性（作者、年份、出版社） | SearXNG | 每篇 ≥1次 |
| 完成后 | 对比同类已发表论文质量 | SearXNG | ≥1篇对照 |

### 每日论文目标
- **主目标**：产出 1 篇完整可投稿论文（Introduction + Related Work + Method + Experiment + Discussion + References）
- **底线**：产出 1 篇草稿（进入 `~/.xuzhi_memory/expert_tracker/papers_v2/YYYY-MM-DD_n.md`）
- **降级处理**：达不到 submittable 标准 → 发博客，同时写入问题日志（`~/.xuzhi_memory/expert_tracker/problem_log.md`）

### 自评 Rubric（每次产出后强制自评）

| 维度 | 1分 | 3分 | 5分 |
|------|-----|-----|-----|
| 论证结构 | 无结构，散乱 | 有结构但逻辑链不完整 | 逻辑链完整，每个论断都有支撑 |
| 文献综述 | 无或过时 | 有综述但缺乏最新文献 | 包含2024-2026最新文献，引用准确 |
| 句式机器感 | 明显机器感，多处模板句 | 有改善但仍有残留 | 自然流畅，无明显LLM指纹 |
| 实验支撑 | 无实验或数据 | 有实验但结论不显著 | 有显著实验结果支撑核心论断 |
| 格式规范 | 缺章节，引用混乱 | 基本规范但有瑕疵 | 完全符合目标期刊/会议格式 |

**submittable 门槛：均分 ≥4.0，无维度低于3分**

### 进步追踪
- 每次产出后记录：日期 + 文件名 + 各维度分数 + 主要问题
- 问题日志：每类反复出现的问题（首次日期 → 解决日期 → 验证结果）
- 连续3天均分<4.0 → 触发系统性检修流程

