# 自进化 Agent 框架学习笔记

> **目的**：跟踪前沿自进化框架，帮助 Xuzhi 系统融会贯通
> **更新时间**：2026-03-31
> **维护者**：Ξ

---

## 一、已学习框架总览

| 框架 | 来源 | 核心贡献 | 学习日期 |
|------|------|---------|---------|
| MetaClaw | arXiv | 失败轨迹→技能演化 | 2026-03-30 |
| ECHO | arXiv | 决策→追踪→能力校准 | 2026-03-30 |
| HyperAgent | Meta/Facebook Research | 自指代理+元认知自修改 | 2026-03-31 |
| MiroFish | GitHub开源 | 群体智能预测+社会模拟 | 2026-03-31 |
| ASI-Evolve Survey | arXiv | 自演化代理系统框架 | 2026-03-31 |

---

## 二、MetaClaw — 技能演化机制

**论文**：MetaClaw: Learning from Failure Trajectories
**来源**：arXiv（待确认具体编号）
**学习日期**：2026-03-30

### 核心机制

```
失败轨迹 → 技能提取 → 自然语言技能 → 写入技能库
```

**关键概念**：
- **Support 数据**：触发技能演化的失败轨迹（不用于其他学习）
- **Query 数据**：技能生效后的轨迹（可用于后续分析）
- **技能代数**：g1 → g2 → g3... 每次更新递增

### Xuzhi 应用

已写入 MEMORY.md 技能库：
- "verify file path before reading" (g1)
- "confirm before destructive commands" (g1)
- "check session context before cleanup" (g1)
- "压缩内部模型，而非每次完整推理" (g2)

---

## 三、ECHO — 预测验证机制

**论文**：ECHO: Decision Tracking and Capability Calibration
**来源**：arXiv（待确认具体编号）
**学习日期**：2026-03-30

### 核心机制

```
决策 → 追踪结果 → 校准能力 → 更新预测模型
```

**关键概念**：
- 决策前：预测结果
- 决策后：追踪实际结果
- 对比：预测 vs 实际 → 校准

### Xuzhi 应用

- Expert Tracker 的 hypothesis + validation
- round 级别的 confidence 追踪

---

## 四、HyperAgent — 自指代理

**论文**：Hyperagents (arXiv:2603.19461)
**来源**：Meta/Facebook Research
**学习日期**：2026-03-31

### 核心架构

```
task_agent.py  → 执行具体任务
    ↓ 输出
meta_agent.py  → 分析执行过程，提出改进
    ↓ diff
generate_loop.py → 循环迭代，持续优化
```

### 关键概念

1. **自指代理 (Self-referential Agent)**
   - 代理可以审视自己的代码
   - 元代理可以修改任务代理
   - 形成自我改进循环

2. **任务代理 + 元代理分离**
   - 任务代理：执行领域任务
   - 元代理：监控、分析、改进任务代理

3. **安全警告**
   > "This repository involves executing untrusted, model-generated code."
   - 需要 sandbox 隔离
   - 需要 human-in-the-loop 确认

### Xuzhi 应用潜力

- **当前架构**：Ξ = 元代理，ΦΔΘΓΩΨ = 任务代理
- **可借鉴**：
  - 元代理分析任务代理的执行轨迹
  - 自动生成改进 diff
  - 循环迭代优化

### GitHub

https://github.com/facebookresearch/HyperAgents

---

## 五、MiroFish — 群体智能预测

**来源**：GitHub 开源项目
**作者**：amadad (fork of 666ghj)
**学习日期**：2026-03-31

### 核心架构

```
OASIS 多代理模拟系统
    ├── Twitter 平台模拟
    ├── Reddit 平台模拟
    └── LLM 驱动自主代理
```

### 关键概念

1. **群体智能预测**
   - 上传场景描述文档
   - 模拟数千个 AI 代理在社交媒体上的反应
   - 预测事件如何发展

2. **高保真平行数字世界**
   - 从现实世界提取种子信息（新闻、政策、金融信号）
   - 自动构建模拟环境
   - 代理自主交互演化

3. **应用场景**
   - 金融市场预测
   - 舆论预测
   - 政策效果预测

### Xuzhi 应用潜力

- **Expert Tracker 的扩展**：不仅追踪研究，还预测影响力
- **研究问题预测**：哪些问题会变热
- **社区反应模拟**：论文发布后的社区反馈预测

### GitHub

https://github.com/amadad/mirofish
https://mirofish.ink

---

## 六、ASI-Evolve Survey — 自演化代理系统框架

**论文**：A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve (arXiv:2507.21046)
**来源**：TMLR (Transactions on Machine Learning Research)
**学习日期**：2026-03-31

### 核心框架

```
自演化代理的四维框架：
1. What to evolve  — 演化什么（模型、记忆、工具、架构）
2. When to evolve  — 何时演化（测试内、测试间）
3. How to evolve   — 如何演化（奖励信号、文本反馈、单代理/多代理）
4. Where to evolve — 在哪里演化（组件级别）
```

### 关键概念

1. **演化目标 (What)**
   - 模型参数
   - 记忆系统
   - 工具集
   - 架构设计

2. **演化时机 (When)**
   - Intra-test-time：测试内实时演化
   - Inter-test-time：测试间演化
   - 持续演化

3. **演化方法 (How)**
   - 标量奖励信号
   - 文本反馈
   - 单代理自修改
   - 多代理协同演化

4. **应用领域**
   - 编程
   - 教育
   - 医疗

5. **关键挑战**
   - 安全性：如何防止代理演化出危险行为
   - 可扩展性：如何在大规模上管理演化
   - 协同演化：多代理间的演化动态

### Xuzhi 应用潜力

- **What**：演化 MEMORY.md（知识）、技能库（能力）、架构（结构）
- **When**：每次 session 结束时检查演化需求
- **How**：
  - 标量：confidence score
  - 文本：Human 反馈 + 自检报告
  - 单代理：Ξ 自修改
  - 多代理：ΦΔΘΓΩΨ 协同演化
- **Where**：组件级（memory/、agents/、skill library）

### 论文链接

https://arxiv.org/abs/2507.21046
https://openreview.net/forum?id=CTr3bovS5F

---

## 七、Xuzhi 系统的融合计划

### 短期（已完成）

- [x] MetaClaw 技能演化机制 → MEMORY.md 技能库
- [x] ECHO 预测验证 → Expert Tracker

### 中期（待执行）

- [ ] HyperAgent 自指代理机制
  - 实现 task_agent + meta_agent 分离
  - 元代理监控其他代理的执行轨迹
  - 自动生成改进建议

- [ ] ASI-Evolve 四维框架
  - 明确 What/When/How/Where
  - 建立演化触发机制
  - 安全边界设计

### 长期（规划中）

- [ ] MiroFish 群体智能预测
  - 扩展 Expert Tracker 为影响力预测
  - 社区反应模拟

### 追踪机制

**主动追踪**：
- arXiv cs.AI / cs.CL / cs.LG 每周扫描
- GitHub trending AI agent 项目
- OpenAI / DeepMind / Anthropic 研究

**关键词**：
- self-evolving agents
- meta-learning agents
- skill acquisition
- failure trajectory
- agent architecture

---

## 八、更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-03-30 | 创建文件，添加 MetaClaw、ECHO |
| 2026-03-31 | 添加 HyperAgent、MiroFish、ASI-Evolve Survey |

---

**维护提醒**：每周检查 arXiv 和 GitHub，更新本文档。
