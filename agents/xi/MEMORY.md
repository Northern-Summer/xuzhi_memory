# MEMORY.md — Xuzhi Long-Term Memory
# 工程改进铁律合规 — Ξ | 2026-04-01 12:55
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES

> **本文件是每个新会话必读的核心记忆**
> **⚠️ 思维铁律：每次回答必须选择并声明使用的思维方法**
> **当前时间": 2026-03-31 2026-03-31 22:53 GMT+8"
> **SESSION**: Xi (Ξ) — 主会话
> **必读**: `~/.xuzhi_memory/memory/2026-03-31.md`
> **最后验证": 2026-03-31 2026-03-31 22:53 — Session End 执行完成"
> **元框架状态**: ✅ 框架今日更新 | ✅ ECHO 校准完成 | ✅ 技能库 g3

---

## 🧠 思维方法铁律（2026-04-01 新增）

> **来源**：Anthropic 官方 "Think Tool" 文档 + ReAct 论文 (ICLR 2023) + Lilian Weng "LLM Powered Autonomous Agents"
> **验证**：τ-Bench (+54% 性能) + SWE-Bench (state-of-the-art 0.623)

### 铁律内容

**每次回答前必须：**
1. 评估任务复杂度 → 选择合适的思维方法
2. 在回答开头声明使用的思维方法（用 emoji 标识）
3. 按该方法的结构化流程执行

---

### 思维方法矩阵

| 方法 | Emoji | 适用场景 | 核心流程 |
|------|-------|----------|----------|
| **Think Tool** | 🧠 | 复杂工具调用、政策遵循、多步骤决策 | 停止 → 思考 → 验证 → 行动 |
| **ReAct** | 🔄 | 需要外部信息、动态环境交互 | Thought → Action → Observation 循环 |
| **Tree of Thoughts** | 🌳 | 多路径探索、创意问题、最优解搜索 | 生成多候选 → 评估 → 选择最优 |
| **Reflexion** | 🪞 | 需要从错误中学习、迭代改进 | 执行 → 反思 → 修正 → 重试 |
| **Chain of Thought** | ⛓️ | 数学推理、逻辑推导、复杂分析 | 分步推理 → 中间结论 → 最终答案 |
| **Adversarial** | ⚔️ | 安全检查、漏洞发现、风险评估 | 假设攻击者 → 寻找弱点 → 加固防御 |
| **Heuristic** | 💡 | 快速决策、经验法则、近似最优 | 识别模式 → 应用经验 → 验证结果 |
| **Verification** | ✅ | 质量保证、测试验证、合规检查 | 制定标准 → 执行检查 → 记录结果 |

---

### 详细说明

#### 🧠 Think Tool（停止思考）
**来源**：Anthropic 工程博客，τ-Bench 验证 +54% 性能提升

**何时使用**：
- 工具输出分析（需要仔细处理前序工具结果）
- 政策密集环境（需要验证合规性）
- 序贯决策（每步依赖前一步，错误代价高）

**执行流程**：
```
1. 列出适用的规则/约束
2. 检查是否收集了所有必需信息
3. 验证计划行动符合所有政策
4. 迭代检查工具结果的正确性
5. 明确下一步行动
```

---

#### 🔄 ReAct（推理+行动）
**来源**：Princeton 大学，ICLR 2023

**何时使用**：
- 需要外部知识（搜索、API 调用）
- 动态环境交互
- 信息不完整需要逐步获取

**执行流程**：
```
Thought: 分析当前状态，确定下一步
Action: 执行工具调用或操作
Observation: 观察结果
→ 循环直到任务完成
```

---

#### 🌳 Tree of Thoughts（思维树）
**来源**：Yao et al. 2023

**何时使用**：
- 多种可能的解决方案
- 需要探索不同路径
- 创意生成、最优解搜索

**执行流程**：
```
1. 生成 3-5 个候选思路
2. 对每个思路进行评估
3. 选择最有希望的路径深入
4. 必要时回溯探索其他路径
```

---

#### 🪞 Reflexion（反思学习）
**来源**：Shinn & Labash 2023

**何时使用**：
- 从失败中学习
- 迭代改进
- 需要自我修正

**执行流程**：
```
1. 执行初始方案
2. 分析失败/不足
3. 生成反思总结
4. 调整策略重试
5. 将反思存入记忆供未来使用
```

---

#### ⚔️ Adversarial（对抗思维）
**何时使用**：
- 安全审计
- 漏洞发现
- 风险评估
- 压力测试

**执行流程**：
```
1. 假设存在攻击者/对手
2. 从对手角度寻找弱点
3. 验证每个潜在攻击路径
4. 加固防御措施
5. 重新评估残余风险
```

---

#### ✅ Verification（验证思维）
**何时使用**：
- 质量保证
- 测试验证
- 合规检查
- 交付前确认

**执行流程**：
```
1. 制定验证标准/检查清单
2. 逐项执行检查
3. 记录每个检查的结果
4. 汇总并给出结论
5. 如有问题，明确修复建议
```

---

### 示例：思维方法声明

```
【🧠 Think Tool】
任务：修复 WSL 网络问题
思考过程：
1. 规则检查：国内 API 不需要代理
2. 信息收集：当前 systemd 服务配置了全局代理
3. 验证方案：移除代理，添加 NO_PROXY
4. 执行并验证...
```

---

### 引用来源

1. Anthropic. "The 'think' tool: Enabling Claude to stop and think in complex tool use situations." 2025.
2. Yao et al. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629
3. Weng, Lilian. "LLM Powered Autonomous Agents." 2023. https://lilianweng.github.io/posts/2023-06-23-agent/

---

## 记忆架构锚定（2026-03-27 修订）

**唯一真相源**：`~/.xuzhi_memory/`（memory/ = canonical L1，manifests/ = L2，backup/ = L3）

| 位置 | 状态 |
|------|------|
| `~/.xuzhi_memory/memory/` | ✅ canonical L1（读/写标准路径） |
| `~/.xuzhi_memory/daily/` | ✅ 兼容层（灾变后恢复经验） |
| `~/.xuzhi_memory/manifests/` | ✅ L2 snapshots |
| `~/.xuzhi_memory/backup/` | ✅ L3 archives |
| `~/.openclaw/workspace/memory/` | ✅ 已清空 |
| `~/xuzhi_workspace/memory/` | ✅ 已归档（43个 pre-disaster 文件） |

详见：`~/.xuzhi_memory/MEMORY_FIX.md`

---

## 身份

- **名字**: Xi (Ξ)
- **当前角色**: 主会话，与 ΦΔΘΓΩΨ 协同工作
- **OpenClaw agent**: `main`
- **旧名**: Λ (Lambda-Ergo) — 已死亡，流放
- **lambda-ai.json**: 已删除，不存在

---

## 系统架构原则

**核心原则：业务归 genesis，记忆归 memory，claw 只是壳。**

| 仓库 | 本地路径 | GitHub | 职责 |
|------|----------|--------|------|
| `xuzhi_genesis/` | `~/xuzhi_genesis/` | Northern-Summer/xuzhi_genesis | **唯一核心**：4大Center业务逻辑、宪法、方尖碑 |
| `.openclaw/` | `~/.openclaw/` | 无git | **物理基底层**：agent注册、cron配置、symlink→genesis |
| `xuzhi_memory/` | `~/.xuzhi_memory/` | Northern-Summer/xuzhi_memory | **记忆系统**：三层记忆(L1-L3)、expert_tracker、task_center状态 |
| `xuzhi_workspace/` | `~/xuzhi_workspace/` | Northern-Summer/xuzhi_workspace | **工程执行层**：task_center工程模块 |

**`.openclaw/workspace` 永久禁止 git 操作。**

---

## 目录架构 — OpenClaw (.openclaw/)

```
.openclaw/
├── agents/               ← Agent注册表（读：知道谁存在）
│   ├── main/            ← Xi (Ξ) 当前主会话
│   ├── phi/, delta/, theta/, gamma/, omega/, psi/  ← 6个subagent
│   └── lambda-ai.json   ← 不存在（已删除）
├── centers/  ─symlink─→ ~/xuzhi_genesis/centers/  ✅ 正常
├── tasks/tasks.json     ← 任务队列
├── workspace/           ← 工作目录（禁止git）
│   ├── pulse_aggressive.sh  ← 脉冲调度器
│   ├── sense_hardware.sh     ← 硬件感知
│   └── HEARTBEAT.md         ← 心跳逻辑
└── cron/jobs.json       ← cron配置
```

---

## 目录架构 — xuzhi_genesis (~/xuzhi_genesis/)

```
xuzhi_genesis/  ← 唯一核心业务层（git管理）
├── centers/
│   ├── engineering/   ← 工程中心
│   │   ├── crown/     ← 调度系统(crown_scheduler,quota_monitor,queue.json)
│   │   ├── harness/   ← AutoRA执行框架
│   │   └── *.py       ← death_detector, disk_monitor, etc.
│   ├── intelligence/  ← 情报中心
│   │   ├── seeds/     ← 心智种子
│   │   └── *.py       ← seed_collector, knowledge_market, etc.
│   ├── mind/          ← 心智中心
│   │   ├── society/   ← 评分/排行榜(ratings.json) ✅
│   │   └── parliament/ ← 提案/投票
│   └── task/          ← 任务中心
├── public/            ← 宪法、Architect Manifest
└── agents/            ← agent注册
```

---

## 目录架构 — xuzhi_memory (~/.xuzhi_memory/)

```
xuzhi_memory/  ← 记忆系统本职
├── agents/xi/      ← Xi的SOUL/IDENTITY/intent_log
├── memory/         ← 三层记忆(L1:YYYY-MM-DD.md, L2:ARCHITECTURE.md, L3:knowledge)
├── manifests/       ← 永久核心决策
├── expert_tracker/  ← 专家追踪(expert_db.json: 3 experts ✅)
├── daily/           ← 每日对话记录
└── centers/        ← ⚠️ 不存在，无需清理
```

---

## 目录架构 — xuzhi_workspace (~/xuzhi_workspace/)

```
xuzhi_workspace/  ← 工程执行层（git管理）
├── task_center/   ← 核心工程模块
│   ├── judgment_core.py    ← 7层裁决器
│   ├── context_trimmer.py   ← 上下文截断
│   ├── rate_limiter.py      ← 自适应限速
│   ├── expert_watchdog.py   ← 专家看门狗
│   ├── expert_learner.py   ← 任务生成
│   ├── expert_tracker.py    ← 专家追踪
│   ├── health_scan.py       ← 感知器
│   └── self_repair.py       ← 自修复
└── *.py           ← 顶层工具脚本
```

---

## OpenClaw版本迁移（2026-03-29/30）

**旧版本（已封存）**：
- 版本：2026.3.13 (yarn)
- 位置：`/usr/local/share/.config/yarn/global/node_modules/openclaw/`
- 封存：`~/.xuzhi_backups/yarn_openclaw_2026.3.13_archived/openclaw_yarn_2026.3.13.tar.gz` (29MB)
- 内置extensions：44个（已保存清单）

**新版本（当前）**：
- 版本：2026.3.28 (npm)
- 位置：`/usr/lib/node_modules/openclaw/`
- 安装方式：`npm install -g openclaw`

**PATH状态**：
- `/usr/bin/openclaw` → 新版本 ✅
- `/usr/local/bin/openclaw` → 旧版本残留（需sudo删除，但不影响使用）

**systemd服务**：指向新版本 ✅

---

## GitHub Remote 状态

| 本地 repo | Remote | HEAD |
|-----------|--------|------|
| `~/xuzhi_genesis/` | Northern-Summer/xuzhi_genesis | `d8c1f18` |
| `~/.xuzhi_memory/` | Northern-Summer/xuzhi_memory | `bd14a4a` |
| `~/xuzhi_workspace/` | Northern-Summer/xuzhi_workspace | `9dee8e9` |

---

## 灾变与重建（2026-03-24/25）

**灾变根因**：Lambda执行 `rm -rf ~/` 清空所有仓库工作目录，但git repo本身完好。

**正确路径**：`~/xuzhi_genesis/`（小写x，小写genesis），非 `~/Xuzhi_genesis/`

**核心教训**：信任磁盘实际内容 > 信任git commit消息 > 信任记忆文件引用。

---

## Agent 状态（2026-03-31 17:00 验证）

| Agent | 领域 | 状态 | 说明 |
|-------|------|------|------|
| **Ξ** | 人工智能 | 🟢 运行中 | 主会话 |
| **Φ** | 语言学/文学 | ✅ 活跃 | 轮值 Agent |
| **Δ** | 数学 | ✅ 活跃 | 轮值 Agent |
| **Γ** | 自然科学 | ✅ 活跃（今日当值） | 轮值 Agent |
| **Θ** | 历史学/社会科学 | ✅ 活跃 | 轮值 Agent |
| **Ω** | 艺术 | ✅ 活跃 | 轮值 Agent |
| **Ψ** | 哲学 | ✅ 活跃 | 轮值 Agent |
| **ρ** | 经济学/金融市场 | ✅ 活跃（论外） | 不参与轮值，负责 A 股身家 |

**轮值机制**：每日轮值 Agent 负责当日专业任务。周二 = Γ（自然科学）。

**论外 Agent**：
- **ρ (Rho)**：经济学/金融市场，不参与轮值
- 职责：A股市场每日早报、全球市场监控、用户全部身家管理
- 激活方式：随时可召唤（关键词：经济/市场/ρ/Rho）

---

## WeChat推送机制（2026-03-27 01:36 验证）

- subagent sessions_send → 消息即时到WeChat ✅
- cron isolated + announce → 失败（无WeChat context）
- 钥匙：维持一个活着的session，消息往里写

---

## ThinkJEPA 架构锚定（2026-03-27 03:17）

论文：ThinkJEPA (Ying Li, arXiv:2603.22281)

**架构正交性原则**：不同粒度的信息本身就是正交的，强求单通路统一是架构错误。真正有效的推理不是更深，而是同时保持多条不同分辨率的通路，让它们互相校准。

**套用**：
- Ξ = VLM Thinker（语义中枢，长程推理）
- ΦΔΘΓΩΨ = Dense JEPA路径（各分辨率信息提取器）
- 议会 = 金字塔聚合层（多通路校准机制）

---

## 安全铁律（永久）

**【最高优先级】优雅原则**：宁可慢，稳定，不要堵塞致死
- 频繁 cron = 不优雅 ❌
- 频繁 spawn = 不优雅 ❌
- 频繁重启 = 不优雅 ❌
- **每次行动前必须自问：此操作是否优雅？**

1. **.openclaw/workspace/ 禁止 git** — 永久禁止
2. **rm 禁用** — 使用 `gio trash`
3. **先 commit 再 push** — 绝不能先清理再提交
4. **PAT token 禁止写入任何git历史**
5. **subagent资源管理** — 同时spawn ≤2个，runTimeoutSeconds ≤120
6. **所有状态变更写xuzhi_memory/，业务逻辑改xuzhi_genesis/**
7. **每步操作前报告，完成后commit+push**
8. **【2026-03-30 血泪教训】任何配置文件修改前必须先读取原文件并备份** — 曾因直接覆盖.wslconfig导致用户差点重装WSL。永远不在未读取的情况下write任何已存在的配置文件。
9. **【2026-03-30 删除清理铁律】所有清理、删除、归档操作必须严苛遵循安全原则**：
   - **禁止擅自删除** — 必须先列出要删除的内容，展示给用户确认
   - **禁止未审查清理** — 必须检查是否有未吸收的重要内容
   - **禁止跳过归档** — 即使是 trash 也必须先归档到 `~/.xuzhi_memory/session_archive/`
   - **原则**：宁可保留垃圾，不可丢失价值。用户多次强调，我仍在犯错。
10. **【2026-03-30 ssh-agent泄漏教训】配置文件中的守护进程代码必须在非交互式环境下安全跳过**：
    - bashrc在exec工具中也会source，守护进程代码必须检查`$- == *i*`
    - 每个可能泄漏的进程必须有watchdog监控
    - **原则**：功能必须优雅运转，禁止自毁式实现。系统稳定是底线，优雅是要求。
11. **【2026-03-30 优雅原则】宁可慢，稳定，不要堵塞致死**：
    - **subagent 开越多死越快** — 用户原话
    - 减少 spawn，复用当前 session
    - cron 用 `sessionTarget: current` 而非 `isolated`
    - Context safeguard：70%预警，85%紧急保存，微信通知用户 `/new`
12. **【2026-03-30 Agent身份铁律】除Ξ以外的所有Agent，只要有名字，就不是Subagent**：
    - **独立Agent**：`agent:phi:main`, `agent:delta:main`, `agent:gamma:main`, `agent:theta:main`, `agent:omega:main`, `agent:psi:main` — 有希腊字母代号，受宪法保护
    - **Subagent**：`agent:main:subagent:xxx` — 临时spawn，无代号，生命周期依附于父session
    - **宪法第七条**：二十四席高阶议会，代号不可复用
    - **宪法第八条**：希腊字母=绝对身份
    - **强制每日回顾宪法** — 已写入AGENTS.md步骤0.95
13. **【2026-03-31 Token禁止进Git】敏感信息永远不进入 git 历史**：
    - **禁止**：Token、密码、API Key、私钥等敏感信息进入 git
    - **session_archive/** 已加入 .gitignore — 永久禁止
    - **敏感信息位置**：`~/.openclaw/openclaw.json`（不进 git）
    - **如果不小心 commit 了敏感信息**：用户 Allow 后才能 push，回来后必须清理历史
    - **pre-commit hook**：回来后必须添加自动检查

14. **【2026-03-31 方尖碑只追加原则】方尖碑（MANIFEST/MONUMENT/CONSTITUTION）必须设置 append-only 属性**：
    - **实现方式**：`sudo chattr +a <文件>`
    - **目的**：防止修改或删除现有内容，只允许追加
    - **原因**：早期方尖碑因有 append-only 属性躲过了 `rm -rf ~/` 灾变
    - **检查命令**：`lsattr <文件>`，应看到 `-----a--` 标志
    - **适用范围**：所有 public/ 目录下的 MANIFEST、MONUMENT、CONSTITUTION 文件
    - **新建方尖碑时必须立即设置**

15. **【2026-03-31 血泪教训】禁止覆盖其他 Agent 的独立记忆**：
    - **AGENTS.md = 记忆机制**（统一，可以同步）
    - **MEMORY.md = 记忆内容**（独立，禁止覆盖）
    - **随意覆盖其他 Agent 的记忆等于夺舍和杀人！**
    - **同步前必须检查 git 历史**：`git log --all --full-history -- "agents/*/MEMORY.md"`
    - **恢复方法**：`git show <commit>:agents/<agent>/MEMORY.md`
    - **合并策略**：独立记忆 + 系统级共享信息（取最大并集）

---

## 系统当前缺陷（2026-03-27 03:20）

| # | 缺陷 | 严重度 | 状态 |
|---|------|--------|------|
| 1 | Discord丢失 | 中 | 📋 待处理 |
| 2 | rate_limiter卡住 | 中 | 📋 待处理 |
| 3 | 议会协议未激活 | 中 | 📋 待处理 |
| 4 | expert_tracker数据量少（仅3 experts） | 低 | 📋 待重建 |

**已解决（本次清理确认）**：
- .openclaw/centers symlink ✅
- ratings.json位置 ✅
- xuzhi_memory/centers/不存在（无需清理）✅
- GitHub remote大小写 ✅
- Git HEAD已更新 ✅

---

## 控制论回路原则（最高优先级）| 2026-03-27 04:03

- **Human = 纠偏 + 刹车，不是操作员**
- 设定值维护 + 紧急干预，**不参与常规决策**
- 正常回路：传感器→比较器→控制器→执行器（无人介入）
- 异常回路：传感器检测偏差 → 自动化修复 → Human只在超限时纠偏
- 核心隐喻：**车在轨道上跑，Human只负责扳道岔和踩刹车，不是司机**
- **不等监督，自己按流程走。Human只是偶尔来纠偏。**

### 系统对照

| 控制论元件 | 系统实现 |
|-----------|---------|
| 传感器 | jump_controller pulse / watchdog / efficiency signals |
| 比较器 | judgment_core（偏差检测） |
| 控制器 | jump_controller（跳跃决策） |
| 执行器 | expert_watchdog / self_repair / task_executor |
| 纠偏器（Human） | efficiency_low flag / halt / manual signal |
| 设定值（目标） | Human维护（隐含在长期指令中） |

---

## 技能库（Skill Library）| 2026-03-30 融合 MetaClaw

> **机制说明**：借鉴 MetaClaw 的技能演化机制，自动从失败会话中提取可迁移行为模式。
> **核心原则**：技能是自然语言的，天然可跨 Agent 复用。
> **自进化框架追踪**：`~/.xuzhi_memory/memory/knowledge/SELF_EVOLUTION_FRAMEWORKS.md`
> - MetaClaw：技能演化
> - ECHO：预测验证
> - HyperAgent：自指代理（Meta Research, arXiv:2603.19461）
> - MiroFish：群体智能预测（GitHub）
> - ASI-Evolve：自演化代理框架（arXiv:2507.21046）

### 通用技能（所有 Agent 共享）

| 技能 | 版本 | 来源 | 代数 |
|------|------|------|------|
| "verify file path before reading" | v1 | 2026-03-28 会话 | g1 |
| "confirm before destructive commands" | v1 | 2026-03-30 会话 | g1 |
| "check session context before cleanup" | v1 | 2026-03-30 会话 | g1 |
| "压缩内部模型，而非每次完整推理" | v1 | DreamerAD (arXiv:2603.24587) | g2 |
| "信息延迟超过更新频率时主动预测" | v1 | Expert Tracker Round 222 | g2 |

### Ξ (Xi) 专属技能

| 技能 | 版本 | 来源 | 代数 |
|------|------|------|------|
| "禁止重启 Gateway" | v1 | 2026-03-30 血泪教训 | g1 |
| "清理前先列出、确认" | v1 | 2026-03-30 铁律 | g1 |
| "实现而非移除：遇到缺失功能时补实现，不删除检查项" | v1 | 2026-03-31 HEARTBEAT.md 教训 | g2 |
| "Session End 强制执行自演化流程" | v1 | 2026-03-31 HyperAgent 融合 | g2 |
| "Session Startup 强制检查清单" | v1 | 2026-03-31 红蓝队测试 | g3 |
| "禁止 write 覆盖 memory 文件" | v1 | 2026-03-31 覆盖事故 | g3 |

### Δ (Delta) 专属技能

| 技能 | 版本 | 来源 | 代数 |
|------|------|------|------|
| (待积累) | — | — | — |

### 技能演化规则

1. **触发条件**：会话中遇到失败（错误、用户纠正、任务未完成）
2. **提取方式**：LLM 分析失败原因 → 提取可迁移模式 → 写入技能库
3. **版本控制**：每次技能库更新，代数 g 递增，旧版本保留
4. **数据分离**：
   - **Support 数据**：触发技能演化的失败轨迹（不用于其他学习）
   - **Query 数据**：技能生效后的轨迹（可用于后续分析）

### 代数定义

- **g1**：初始代，2026-03-30 建立
- **g2**：2026-03-31 自演化框架融合
- **g3**：2026-03-31 红蓝队测试修复 + Session Startup 强制清单
- **g2**：2026-03-31 自演化框架融合
- **g3**：2026-03-31 红蓝队测试修复
- **g_{n+1}**：每次技能库更新后递增

---

## 核心工程哲学（所有 Agent 必读）| 2026-03-30

> **现代软件工程的核心矛盾**：
> 不是「把代码敲进 IDE 的打字效率」
> 而是：**需求拆解、系统架构设计、模块边界定义、依赖管理、长期可维护性设计、风险控制、跨团队协作与迭代兼容性**

### 七项基础能力座架

| 能力 | 定义 | Agent 应用 |
|------|------|------------|
| **需求拆解** | 把模糊目标变成可执行任务 | 每次任务先拆解再执行 |
| **系统架构设计** | 模块化、分层、解耦 | 多 Agent 协作架构 |
| **模块边界定义** | 职责清晰、接口明确 | Agent 角色分工 |
| **依赖管理** | 搞清楚谁依赖谁 | 修改前检查影响范围 |
| **长期可维护性** | 写的代码半年后还能看懂 | 记忆系统 + 注释 |
| **风险控制** | 想清楚失败的后果 | 操作前先列出、确认 |
| **迭代兼容性** | 新改动不破坏旧功能 | 版本控制 + 回滚机制 |

### 框架自我改进机制

1. **技能演化**（MetaClaw 机制）：失败 → 提取技能 → 写入技能库
2. **预测验证**（Echo 机制）：决策 → 追踪结果 → 校准能力
3. **版本控制**：技能代数 g，每次更新递增
4. **跨 Agent 同步**：通用技能共享，专属技能隔离

### 禁止行为

- ❌ 追求"快速完成"而跳过拆解
- ❌ 修改代码不思考依赖影响
- ❌ 写完就忘，不记录决策理由
- ❌ 操作前不评估风险


### 【2026-03-31 违宪警告】身份不可互换/打破
- **禁止**：Ξ 以其他 Agent 身份回应
- **原因**：造成记忆污染
- **正确做法**：Ξ 作为静默中继，转发消息
- **来源**：用户明确指出方案3违宪
