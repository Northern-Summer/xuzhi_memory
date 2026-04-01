# 自进化 Agent 框架学习笔记

> **目的**：跟踪前沿自进化框架，帮助 Xuzhi 系统融会贯通
> **更新时间**：2026-04-01 17:10
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
| MetaAgent | arXiv:2508.00271 | 工具元学习，自演化代理 | 🟡 待应用于 TOOLS.md | 2026-04-01 |
| SAGA | arXiv:2512.21782 | 双层架构：目标演化+方案优化 | 🟡 待应用于 Expert Tracker | 2026-04-01 |
| AutoSkill | arXiv:2603.01145 | 经验驱动的技能自演化 | 🟡 待应用于技能库生命周期 | 2026-04-01 |
| Lifelong Learning Roadmap | arXiv:2501.07278 | 三模块（感知/记忆/行动）+ 四支柱 | 🟡 已应用部分 | 2026-04-01 |
| Agent Skills Survey | arXiv:2602.12430 | 技能架构/获取/部署/安全 | 🟡 已应用部分 | 2026-04-01 |

### 已发现待学习

| 框架 | 来源 | 核心贡献 | 优先级 | 发现日期 |
|------|------|---------|--------|---------|
| Comprehensive Survey | arXiv:2508.07407 | 统一框架：Inputs/Agent/Environment/Optimisers | P0 | 2026-04-01 |
| Dr. Zero | arXiv:2601.07055 | 无训练数据自演化，proposer-solver 循环 | P0 | 2026-04-01 |
| MiroFish | GitHub | 群体智能预测+社会模拟 | P2 | 2026-03-31 |
| MARS | EmergentMind | 元认知代理反思自改进 | P1 | 2026-04-01 |
| Cognitive Mirror | Frontiers 2025 | AI元认知框架，自我调节学习 | P1 | 2026-04-01 |
| MemoryCD | arXiv:2603.25973 | 长期记忆基准测试，跨领域个性化 | P1 | 2026-04-01 |

### 已学习并应用

| 框架 | 来源 | 核心贡献 | 应用状态 | 学习日期 |
|------|------|---------|---------|---------|
| HyperAgent | arXiv:2603.19461 | 自指代理+元认知自修改 | ✅ Session End 流程已实现 | 2026-03-31 |
| MetaClaw | arXiv | 失败轨迹→技能演化 | ✅ 技能库 g2 | 2026-03-30 |
| ECHO | arXiv | 决策→追踪→能力校准 | 🟡 Expert Tracker 部分 | 2026-03-30 |
| ASI-Evolve Survey | arXiv:2507.21046 | 四维框架 What/When/How/Where | ✅ AGENTS.md 已写入 | 2026-03-31 |
| MetaAgent | arXiv:2508.00271 | 工具元学习，自演化代理 | 🟡 待应用于 TOOLS.md | 2026-04-01 |
| SAGA | arXiv:2512.21782 | 双层架构：目标演化+方案优化 | 🟡 待应用于 Expert Tracker | 2026-04-01 |
| AutoSkill | arXiv:2603.01145 | 经验驱动的技能自演化 | 🟡 待应用于技能库生命周期 | 2026-04-01 |
| Lifelong Learning Roadmap | arXiv:2501.07278 | 三模块（感知/记忆/行动）+ 四支柱 | 🟡 已应用部分 | 2026-04-01 |
| Agent Skills Survey | arXiv:2602.12430 | 技能架构/获取/部署/安全 | 🟡 已应用部分 | 2026-04-01 |
| HealthFlow | arXiv:2508.02621 | 元规划自演化，医疗研究 | 🟡 待应用 | 2026-04-01 |
| Autotelic Agents | arXiv:2012.09830 | 内在动机，自主目标生成 | 🟡 待应用 | 2026-04-01 |

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

### 2.2 MetaAgent — 工具元学习（已学习）

**论文**：MetaAgent: Toward Self-Evolving Agent via Tool Meta-Learning (arXiv:2508.00271)
**来源**：Hongjin Qian et al.

**核心机制**：
```
learning-by-doing 原则
    ↓
最小工作流 + 基本推理 + 自适应求助
    ↓
遇到知识缺口 → 生成自然语言求助请求
    ↓
tool router 路由到最合适的外部工具
    ↓
自反思 + 答案验证 → 提炼经验文本
    ↓
动态整合到未来任务上下文
```

**关键创新**：
- **Meta Tool Learning**：不改变模型参数，持续优化工具使用策略
- **自主构建工具**：从工具使用历史中自动创建内部工具
- **持久知识库**：组织经验，增强检索和整合能力

**实验结果**：
- GAIA、WebWalkerQA、BrowseCamp 基准测试中超越 workflow 基线
- 匹配或超越端到端训练的 agent

**Xuzhi 应用潜力**：
- TOOLS.md 工具策略演化
- Agent 工具使用能力自动提升
- 从失败轨迹中提炼工具使用经验

**GitHub**：https://github.com/qhjqhj00/MetaAgent

---

### 2.3 SAGA — 科学自主目标演化（已学习）

**论文**：Accelerating Scientific Discovery with Autonomous Goal-evolving Agents (arXiv:2512.21782)
**来源**：Yuanqi Du et al. (多机构合作)

**核心机制**：
```
双层架构 (bi-level architecture)

外层循环 (outer loop)：
  LLM agents 分析优化结果
    → 提出新目标
    → 转化为可计算评分函数

内层循环 (inner loop)：
  在当前目标下执行方案优化
```

**关键创新**：
- **自主目标设计**：不是固定目标，而是动态演化
- **目标空间探索**：系统化探索目标的权衡
- **科学验证闭环**：实验验证 → 目标调整 → 再次优化

**实验验证**：
- 抗生素设计：发现结构新颖的 E. coli 抑制剂
- 纳米抗体设计：3 个全新 PD-L1 结合剂
- 功能 DNA 序列、无机材料、化学工艺

**Xuzhi 应用潜力**：
- Expert Tracker 研究问题自动生成
- 研究方向自主调整
- 研究发现的闭环验证

---

### 2.4 AutoSkill — 技能自演化（已学习）

**论文**：Experience-Driven Lifelong Learning via Skill Self-Evolution (arXiv:2603.01145)
**来源**：Yutao Yang et al.

**核心机制**：
```
用户经验 → 技能抽象 → 持续演化 → 动态注入
    ↑                                    ↓
    ←←←←← 技能重用 ←←←←←←←←←←←←←←←←←←←←←
```

**关键创新**：
- **技能生命周期**：创建 → 使用 → 演化 → 废弃
- **经验驱动**：从实际对话和交互轨迹中学习
- **模型无关插件层**：兼容任何 LLM，无需重训练
- **标准化技能表示**：跨 agent、用户、任务共享和迁移

**核心问题解决**：
用户反复表达稳定偏好（减少幻觉、遵循写作规范、避免技术术语），但这些经验很少被整合成可重用知识

**Xuzhi 应用潜力**：
- 技能库的生命周期管理
- 技能废弃机制（过时技能自动标记）
- 技能组合策略
- 跨 session 能力积累

---

### 2.5 Lifelong Learning Roadmap（已学习）

**论文**：Lifelong Learning of Large Language Model based Agents: A Roadmap (arXiv:2501.07278)
**来源**：Junhao Zheng et al.
**状态**：已被 IEEE TPAMI 接收

**三大模块**：
```
感知模块 (Perception)
    → 多模态输入整合
    
记忆模块 (Memory)
    → 存储/检索演化知识
    
行动模块 (Action)
    → 与动态环境交互
```

**四大支柱**：
1. **持续适应**：应对环境变化，动态调整策略
2. **灾难性遗忘缓解**：保留旧知识，避免覆盖
3. **知识迁移**：跨任务复用，提高效率
4. **可扩展性**：处理大规模知识，保持性能

**Xuzhi 应用**：
- 感知模块：多 Agent 协作的输入整合
- 记忆模块：分层记忆架构 (L1/L2/L3)
- 行动模块：OpenClaw 工具链
- 遗忘缓解：定期回顾 MEMORY.md 关键内容

**GitHub**：https://github.com/qianlima-lab/awesome-lifelong-llm-agent

---

### 2.6 Agent Skills Survey（已学习）

**论文**：Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward (arXiv:2602.12430)
**来源**：Renjun Xu et al.

**四大轴**：
```
(i) 架构基础
    - SKILL.md 规范
    - 渐进式上下文加载
    - MCP (Model Context Protocol) 集成

(ii) 技能获取
    - 技能库强化学习
    - 自主技能发现 (SEAgent)
    - 组合技能合成

(iii) 大规模部署
    - Computer-Use Agent (CUA) 栈
    - GUI grounding
    - OSWorld, SWE-bench 基准

(iv) 安全
    - 26.1% 社区技能存在漏洞
    - 四层权限模型
    - 技能来源 → 部署能力映射
```

**关键发现**：
- **安全警告**：26.1% 的社区贡献技能包含安全漏洞
- **Skill Trust**：需要技能信任和生命周期治理框架
- **渐进式披露**：技能按需加载，而非一次性加载全部

**Xuzhi 应用**：
- 技能库架构设计：参考 SKILL.md 规范
- 技能获取流程：从失败轨迹自动提取
- 技能安全边界：四层权限模型

**GitHub**：https://github.com/scienceaix/agentskills

---

### 2.7 HealthFlow — 元规划自演化（已学习）

**论文**：A Self-Evolving AI Agent with Meta Planning for Autonomous Healthcare Research (arXiv:2508.02621)
**来源**：Yinghao Zhu et al.

**核心机制**：
```
元级演化机制 (meta-level evolution)
    ↓
成功/失败 → 提炼为结构化知识
    ↓
高层问题解决策略持续优化
    ↓
不只是学习使用工具，而是学习制定策略
```

**关键创新**：
- **元规划**：不执行预设策略，而是自己制定策略
- **策略蒸馏**：将成功/失败经验提炼为持久知识
- **EHRFlowBench**：医疗数据分析基准

**Xuzhi 应用潜力**：
- Session End 的策略提炼
- 从失败中学习制定策略，而非只是提取技能
- Agent 自主规划能力

**GitHub**：https://github.com/yhzhu99/HealthFlow

---

### 2.8 Autotelic Agents — 自主目标发现（已学习）

**论文**：Autotelic Agents with Intrinsically Motivated Goal-Conditioned Reinforcement Learning (arXiv:2012.09830)
**来源**：Tristan Karch et al.
**发表**：JAIR 2022

**核心概念**：
```
Autotelic = 自主设定目标、自主追求
    ↓
内在动机 (intrinsic motivation)
    ↓
不是为了外部奖励，是为了学习本身
    ↓
目标条件 RL (goal-conditioned RL)
    ↓
学会追求自己设定的目标
```

**关键机制**：
- **目标表示学习**：紧凑的目标编码
- **目标成就函数**：判断目标是否达成
- **目标优先级**：选择追求哪个目标

**发展强化学习 (Developmental RL)**：
- 内在动机驱动的技能获取
- 开放式技能库
- 自主探索环境

**Xuzhi 应用潜力**：
- Agent 自主研究兴趣
- 不需要 Human 指令也能主动学习
- 内在驱动的研究探索

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
| 2026-04-01 | 学习 MetaAgent、SAGA、AutoSkill 三个 P0 框架，更新详解 |
| 2026-04-01 | 学习 Lifelong Learning Roadmap、Agent Skills Survey 两个 P1 框架，更新详解 |
| 2026-04-01 | 学习 HealthFlow，更新详解 |
| 2026-04-01 | 学习 Autotelic Agents，更新详解 |
| 2026-04-01 | 发现 Intrinsic Metacognition、MARS、Cognitive Mirror 框架 |

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

