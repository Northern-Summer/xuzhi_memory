# MetaClaw 深度学习笔记

> 学习时间：2026-03-30 21:21
> 来源：arXiv:2603.17187 + GitHub aiming-lab/MetaClaw

---

## 一、核心问题

**LLM Agent 的静态困境**：
- Agent 部署后保持静态，用户需求不断演变
- 任务分布漂移（task distribution drift）
- 现有方法各有限制：
  - Memory-based：存储原始轨迹，冗余且无法提取可迁移模式
  - Skill-based：静态技能库，不与权重优化协调
  - RL-based：小规模或离线设置，忽略数据有效性问题

**MetaClaw 的解决方案**：持续元学习框架，联合维护基础 LLM 策略 θ 和可复用行为技能库 S。

---

## 二、核心架构

### Meta-Model 定义

```
ℳ = (θ, S)
```

- θ：基础 LLM 策略参数
- S = {s₁, s₂, ..., sₖ}：技能指令库

**推理时**：
```
a ~ πθ(·|τ, Retrieve(S, τ))
```
Retrieve(S, τ) 通过嵌入检索选择最相关的技能。

### 双时间尺度互补机制

| 机制 | 时间尺度 | 操作对象 | 是否需要 GPU |
|------|----------|----------|--------------|
| Skill-driven Fast Adaptation | 秒级 | S（技能库） | 否（LLM 分析） |
| Opportunistic Policy Optimization | 分钟-小时级 | θ（模型权重） | 是（云 LoRA） |

---

## 三、Skill-Driven Fast Adaptation

### 核心公式

```
S_{g+1} = S_g ∪ E(S_g, D_g^{sup})
```

- E：技能演化器（LLM）
- D_g^{sup}：失败轨迹（support set）
- g：技能代数

### 特点

1. **无梯度设计**：技能库存在于离散自然语言空间
2. **零停机时间**：通过 prompt 注入，不修改模型参数
3. **双重角色**：
   - 元参数：跨任务流积累行为知识
   - 适应基础：推理时检索任务相关技能

### 示例技能

```
"verify file path before reading"
"confirm before destructive commands"
"check session context before cleanup"
```

---

## 四、Opportunistic Policy Optimization

### 核心公式

```
θ_{t+1} = θ_t + α ∇_θ E_{(τ,ξ,g')~B}[R(πθ(·|τ, S_{g'}))]
```

- B：RL buffer，只包含 query data
- R：Process Reward Model (PRM) 分数
- g'：轨迹收集时的技能代数

### 关键设计

1. **数据门控**：只有 buffer 积累足够样本后才启动训练
2. **自然延迟**：策略优化通常落后技能演化数天
3. **后适应优化**：优化 θ 使得技能驱动适应产生更强的后适应行为

---

## 五、Skill Generation Versioning

### 问题

轨迹 (τ_i, ξ_i) 触发 S_g → S_{g+1} 演化时：
- 该轨迹的奖励 r_i 反映的是 S_g 下的表现
- 如果此轨迹进入 RL buffer，会污染梯度更新

### 解决方案

每个样本标记技能代数 g_i：

| 数据类型 | 定义 | 用途 |
|----------|------|------|
| Support set D_g^{sup} | S_g 下收集，触发演化 | 技能演化，不进入 RL buffer |
| Query set D_{g+1}^{qry} | S_{g+1} 生效后收集 | 策略优化 |

**刷新机制**：技能代数从 g → g+1 时，刷新 buffer 中所有版本 ≤ g 的样本。

---

## 六、Opportunistic Meta-Learning Scheduler (OMLS)

### 三种空闲信号

1. **Sleep window**：用户配置的睡眠时间（如 23:00-07:00）
2. **Keyboard inactivity**：系统键盘无活动
3. **Calendar occupancy**：Google Calendar 事件占用

### 原则

- 策略优化只在用户非活跃窗口触发
- 消除服务停机时间
- 用户无感知训练

---

## 七、Proxy-Based Architecture

```
User → OpenClaw/CoPaw/IronClaw → MetaClaw Proxy → LLM API
                                    ↓
                              Skill Injection
                              Trajectory Logging
                              Reward Scoring
                                    ↓
                              RL Training (async)
```

### 优势

1. **无需本地 GPU**：通过云 LoRA 训练
2. **透明集成**：对上游 Agent 无侵入
3. **异步处理**：服务、奖励建模、训练完全解耦

---

## 八、实验结果

### MetaClaw-Bench

- 934 个问题，44 个模拟工作日
- 每天是顺序、反馈驱动的多轮 CLI 任务会话

### 关键结果

| 模型 | 基线 | +Skills | +Full |
|------|------|---------|-------|
| Kimi-K2.5 | 21.4% | — | 40.6% |
| GPT-5.2 | 41.1% | — | — |

- Skill-driven 适应：相对提升 32.2%
- 端到端任务完成：8.25× 提升
- 文件检查完成：185% 提升

### AutoResearchClaw

- 23 阶段自主研究流水线
- 仅技能注入：复合鲁棒性提升 18.3%

---

## 九、与 Xuzhi 系统的关系

### 直接相关性

| MetaClaw 组件 | Xuzhi 对应 | 状态 |
|---------------|------------|------|
| Skill Library S | MEMORY.md + skills/ | 已存在 |
| Proxy Architecture | OpenClaw | 已使用 |
| Skill Evolver E | 可实现 | 待集成 |
| OMLS | cron + heartbeat | 部分实现 |
| RL Training | — | 未实现 |

### 可借鉴的设计

1. **技能演化机制**：
   - 当前：手动写入 MEMORY.md
   - 改进：LLM 自动分析失败会话，提取技能

2. **支持/查询分离**：
   - 当前：所有对话混在一起
   - 改进：标记"触发学习"的会话 vs 普通会话

3. **机会主义调度**：
   - 当前：cron 固定调度
   - 改进：检测用户空闲窗口再训练

4. **版本化机制**：
   - 当前：无版本控制
   - 改进：技能代数标记，避免过期数据污染

---

## 十、部署选项

### 三种模式

| 模式 | 功能 | 资源需求 |
|------|------|----------|
| skills_only | 技能注入 + 自动摘要 | 轻量，无 GPU |
| rl | skills + 在线 RL | RL 后端 (Tinker/MinT) |
| madmax | rl + 智能调度 | RL 后端 + 日历集成 |

### 一键安装（OpenClaw）

```bash
curl -LO https://github.com/aiming-lab/MetaClaw/releases/download/v0.4.0/metaclaw-plugin.zip
unzip metaclaw-plugin.zip -d ~/.openclaw/extensions
openclaw plugins enable metaclaw-openclaw && openclaw gateway restart
```

---

## 十一、关键论文引用

1. **SkillRL**: Xia et al., "SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning"
2. **ReAct**: Yao et al., 2022
3. **Reflexion**: Shinn et al., 2023
4. **EXPEL**: Zhao et al., 2024
5. **MAML**: Finn et al., 2017

---

## 十二、后续行动建议

### 短期（可立即实施）

1. **技能提取自动化**：
   - 分析失败会话 → 提取技能 → 写入技能库
   - 可用现有 LLM 实现

2. **版本标记**：
   - 为 MEMORY.md 中的技能添加"生效日期"和"来源会话"

### 中期（需要工程）

3. **支持/查询分离**：
   - 标记"触发学习"的会话
   - 区分用于技能提取的数据和用于其他用途的数据

4. **机会主义调度增强**：
   - 检测用户空闲窗口（已有 heartbeat 基础）
   - 在空闲时执行"学习任务"

### 长期（需要资源）

5. **RL 训练集成**：
   - 接入 Tinker 或 MinT
   - 实现权重热更新

---

## 十三、核心洞察

1. **两个时间尺度是互补的，不是竞争的**：
   - 快适应（技能）解决眼前问题
   - 慢优化（权重）提升长期能力

2. **技能库的双重角色**：
   - 作为元参数积累知识
   - 作为适应基础提供即时专业化

3. **数据版本化是元学习的关键**：
   - 混合使用过期数据会污染梯度
   - 支持集/查询集分离是理论基础

4. **无 GPU 也能进化**：
   - 技能注入不需要训练
   - 云 LoRA 解决训练需求

---

*笔记完成于 2026-03-30 21:35*
