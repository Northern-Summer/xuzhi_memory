# 自进化 Agent 框架学习笔记

> **目的**：跟踪前沿自进化框架，帮助 Xuzhi 系统融会贯通
> **更新时间**：2026-03-31 14:28
> **维护者**：Ξ
> **跟踪频率**：每周强制扫描 + 每日 heartbeat 检查

---

## 一、框架总览（按学习优先级排序）

### 已学习并应用

| 框架 | 来源 | 核心贡献 | 应用状态 | 学习日期 |
|------|------|---------|---------|---------|
| HyperAgent | arXiv:2603.19461 | 自指代理+元认知自修改 | ✅ Session End 流程已实现 | 2026-03-31 |
| MetaClaw | arXiv | 失败轨迹→技能演化 | ✅ 技能库 g2 | 2026-03-30 |
| ECHO | arXiv | 决策→追踪→能力校准 | 🟡 Expert Tracker 部分 | 2026-03-30 |
| ASI-Evolve Survey | arXiv:2507.21046 | 四维框架 What/When/How/Where | ✅ AGENTS.md 已写入 | 2026-03-31 |

### 已发现待学习

| 框架 | 来源 | 核心贡献 | 优先级 | 发现日期 |
|------|------|---------|--------|---------|
| MetaAgent | arXiv:2508.00271 | 工具元学习，自演化代理 | P0 | 2026-03-31 |
| SAGA | arXiv:2512.21782 | 自主目标演化，科学发现 | P0 | 2026-03-31 |
| AutoSkill | arXiv:2603.01145 | 经验驱动的技能自演化 | P0 | 2026-03-31 |
| Lifelong Learning Roadmap | arXiv:2501.07278 | LLM Agent 终身学习路线图 | P1 | 2026-03-31 |
| Agent Skills Survey | arXiv:2602.12430 | Agent 技能架构/获取/安全 | P1 | 2026-03-31 |
| HealthFlow | arXiv:2508.02621 | 元规划自演化代理 | P1 | 2026-03-31 |
| Autotelic Agents | arXiv:2012.09830 | 内在动机目标条件 RL | P2 | 2026-03-31 |
| MiroFish | GitHub | 群体智能预测+社会模拟 | P2 | 2026-03-31 |

---

## 二、核心框架详解

### 2.1 HyperAgent — 自指代理（已应用）

**论文**：Hyperagents (arXiv:2603.19461)
**来源**：Meta/Facebook Research

**架构**：
```
task_agent.py  → 执行具体任务
    ↓ 输出
meta_agent.py  → 分析执行过程，提出改进
    ↓ diff
generate_loop.py → 循环迭代，持续优化
```

**Xuzhi 应用**：
- Ξ = meta_agent（监控自己的执行轨迹，提取技能）
- Session End 流程 = 自修改机制
- 技能代数 g 递增

**GitHub**：https://github.com/facebookresearch/HyperAgents

---

### 2.2 MetaAgent — 工具元学习（待学习）

**论文**：MetaAgent: Toward Self-Evolving Agent via Tool Meta-Learning (arXiv:2508.00271)
**核心机制**：
```
学习-by-doing 原则
→ 反思任务解决经验
→ 演化工具使用策略
```

**关键概念**：
- 工具元学习：不是学习工具，是学习如何学习工具
- 经验反思：从失败中提取可迁移策略
- 自演化：工具策略随时间改进

**Xuzhi 应用潜力**：
- TOOLS.md 工具策略演化
- Agent 工具使用能力提升

---

### 2.3 SAGA — 科学自主目标演化（待学习）

**论文**：Accelerating Scientific Discovery with Autonomous Goal-evolving Agents (arXiv:2512.21782)
**核心机制**：
```
科学发现 = 自主目标生成 + 目标演化 + 实验验证
```

**关键概念**：
- 自主目标发现：Agent 自己提出研究问题
- 目标演化：根据发现动态调整目标
- 科学工作流自动化

**Xuzhi 应用潜力**：
- Expert Tracker 的研究问题自动生成
- 研究方向的自主调整
- 科学发现的闭环验证

---

### 2.4 AutoSkill — 技能自演化（待学习）

**论文**：AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution (arXiv:2603.01145)
**核心机制**：
```
经验 → 技能提取 → 技能组合 → 技能演化
```

**关键概念**：
- 技能生命周期：创建 → 使用 → 演化 → 废弃
- 经验驱动：从实际任务中学习，不是预先定义
- 终身学习：持续积累，不遗忘

**Xuzhi 应用潜力**：
- 技能库的生命周期管理
- 技能废弃机制
- 技能组合策略

---

### 2.5 Lifelong Learning Roadmap（待学习）

**论文**：Lifelong Learning of Large Language Model based Agents: A Roadmap (arXiv:2501.07278)

**四大支柱**：
1. **持续适应**：应对环境变化
2. **灾难性遗忘缓解**：保留旧知识
3. **知识迁移**：跨任务复用
4. **可扩展性**：处理大规模知识

**Xuzhi 应用潜力**：
- MEMORY.md 的知识迁移机制
- 遗忘缓解：定期回顾重要内容
- 可扩展性：分层记忆架构

---

### 2.6 Agent Skills Survey（待学习）

**论文**：Agent Skills for Large Language Models: Architecture, Acquisition, Security (arXiv:2602.12430)

**三大维度**：
1. **架构**：技能如何组织
2. **获取**：技能如何学习
3. **安全**：技能如何保护

**Xuzhi 应用潜力**：
- 技能库架构设计
- 技能获取流程
- 技能安全边界

---

## 三、Autotelic Agents — 自主目标发现

**论文**：Autotelic Agents with Intrinsically Motivated Goal-Conditioned RL (arXiv:2012.09830)

**核心概念**：
- **Autotelic**：自主设定目标、自主追求
- **内在动机**：不是为了外部奖励，是为了学习本身
- **目标条件 RL**：学会追求自己设定的目标

**Xuzhi 应用潜力**：
- Agent 自主研究兴趣
- 不需要 Human 指令也能主动学习
- 内在驱动的研究探索

---

## 四、Xuzhi 系统融合状态

### 已实现

| 框架机制 | Xuzhi 实现 | 位置 |
|---------|-----------|------|
| MetaClaw 技能演化 | 技能库 g1→g2 | MEMORY.md |
| HyperAgent 自指 | Session End 流程 | AGENTS.md |
| ASI-Evolve What/When | 每次 session 结束检查 | AGENTS.md |

### 待实现

| 框架机制 | Xuzhi 目标 | 优先级 |
|---------|-----------|--------|
| ECHO 校准循环 | 决策预测→追踪→校准 | P0 |
| MetaAgent 工具元学习 | TOOLS.md 演化 | P0 |
| SAGA 目标演化 | Expert Tracker 自主问题生成 | P1 |
| AutoSkill 技能生命周期 | 技能废弃机制 | P1 |
| Autotelic 自主目标 | Agent 自主研究兴趣 | P2 |

---

## 五、跟踪机制（融入工作流）

### Cron 层（每周强制）

```bash
# 每周一 09:00 执行
0 9 * * 1 $HOME/.openclaw/workspace/track_evolution_frameworks.sh
```

### Heartbeat 层（每日检查）

```
检查 SELF_EVOLUTION_FRAMEWORKS.md 最后更新时间
超过 7 天 → 触发提醒
```

### 关键词追踪

```
self-evolving agents
meta-learning agents
skill acquisition
failure trajectory
autotelic agent
goal-evolving agent
lifelong learning agent
agent architecture
```

---

## 六、验收标准

### 技能库验收

| 指标 | 当前值 | 目标值 |
|------|--------|--------|
| 通用技能数 | 5 | ≥10 |
| 专属技能数 | 4 | 每个Agent ≥3 |
| 技能代数 | g2 | 持续递增 |
| 技能应用率 | 未知 | ≥80% |

### 流程验收

| 流程 | 状态 | 验收标准 |
|------|------|---------|
| Session End 执行 | ✅ 已实现 | 每次 session 必须执行 |
| 技能提取 | ✅ 已实现 | 有失败必提取 |
| Git 持久化 | ✅ 已实现 | 所有修改必 commit+push |
| ECHO 校准 | ❌ 未实现 | 预测→追踪→校准闭环 |
| 框架跟踪 | 🟡 手动 | 每周自动扫描 |

---

## 七、更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-03-30 | 创建文件，添加 MetaClaw、ECHO |
| 2026-03-31 | 添加 HyperAgent、MiroFish、ASI-Evolve |
| 2026-03-31 | 新增 MetaAgent、SAGA、AutoSkill、Lifelong Learning Roadmap、Agent Skills Survey |
| 2026-03-31 | 添加验收标准、跟踪机制 |

---

**维护协议**：
- 每周检查 arXiv 和 GitHub
- 每次学习新框架后更新本文档
- 每次应用框架机制后更新"融合状态"

---

## 2026-03-31 ρ 更新

### 已学习

| 框架 | 来源 | 核心贡献 | 应用状态 |
|------|------|---------|---------|
| TradingAgents Survey | arXiv:2408.06361 | Multi-Agent 分工、数据类型、性能挑战 | ✅ L3 笔记已写入 |

### ρ 专属进展

| 框架 | ρ 实现 | 状态 |
|------|--------|------|
| Reflexion | `SelfCritic` 类 | ✅ |
| BullBear | `BullBear` 类 | ✅ |
| DataValidator | `DataValidator` 类 | ✅ |
| ECHO 校准 | `echo_calibration.json` | ✅ 接入 |
| Expert Tracker | `expert_db.json` finance_markets 部门 | ✅ 接入 |
| 完整 Multi-Agent | TradingAgents 分工 | 🟡 单 Agent 雏形 |

