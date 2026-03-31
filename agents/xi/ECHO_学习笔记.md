# ECHO 学习笔记

> 学习时间：2026-03-30 21:32
> 来源：UniPat AI (echo.unipat.ai, unipat.ai/blog/Echo)

---

## 一、核心问题

**LLM 预测能力的评估困境**：
1. **Timing Asymmetry**：预测难度随时间变化，后期预测更容易
2. **Question Source Gap**：现有基准只覆盖预测市场，领域狭窄

---

## 二、核心架构

### 三大组件

```
Echo = General AI Prediction Leaderboard
     + Train-on-Future (To-F)
     + Prediction API
```

### Leaderboard 排名（2026-03-27）

| 排名 | 模型 | Elo 分数 |
|------|------|----------|
| #1 | EchoZ-1.0 | 1034.2 |
| #2 | Gemini-3.1-Pro | 1032.2 |
| #3 | Claude-Opus-4.6 | 1017.2 |
| #4 | Grok-4.1-Fast | 1011.3 |
| #5 | Seed-2.0-Pro | 1008.9 |
| #6 | GPT-5.2 | 1005.2 |
| #7 | GLM-5 | 1001.8 |

---

## 三、Train-on-Future (To-F) 范式

### 核心创新

**传统训练**：Train-on-Past（用历史数据训练）
**Echo 训练**：Train-on-Future（用未来事件训练）

### 解决的问题

1. **数据泄露**：传统训练中，模型可能已经"看过"答案
2. **时效性**：历史答案在预测未来时可能已过时
3. **分布漂移**：事件分布随时间变化

### 机制

```
1. 预测时间 t < 解答时间 D
2. 模型在 t 时输出概率分布 p(t)
3. 等待 D 时刻事件解答
4. 用真实结果训练模型
```

---

## 四、Leaderboard 设计

### 三源数据获取

| 来源 | 特点 | 优势 |
|------|------|------|
| Prediction Market | Polymarket 等 | 共识锚定 + 精确解答 |
| Synthesis from Trends | Google Trends + Agent 合成 | 覆盖新兴话题 |
| Expert Annotation | 领域专家 | 高价值专业问题 |

### 预测点选择算法

**Phase 1：预测数量估计**
```
T_i = round(1.35 · ln(D_i) + 0.5)
```
- 10 天问题：约 4 次预测
- 90 天问题：约 7 次预测

**Phase 2：优先级评分**
```
S_i = (W_i · R_i) / D_i'
```
- W_i：距上次预测的天数
- R_i：剩余预测次数
- D_i'：剩余天数

### Elo 排名机制

**Battle 构建**：
- 比较点对齐：同一问题 + 同一预测时间点
- Brier Score：BS = (1 - p^c)²
- Soft label：v_k = 1 / (1 + 10^((BS_a - BS_b)/σ))

**权重**：
```
w_k = 1 + γ · ln(1 + Δt_k)
```
- 长期预测（Δt 大）权重更高

**Bradley-Terry MLE**：
```
L(r) = Σ w_k [v_k log P(a > b | r) + (1-v_k) log(1-P)]
```

---

## 五、与 Xuzhi 的关系

### 可借鉴设计

| Echo 机制 | Xuzhi 可用 | 应用场景 |
|-----------|------------|----------|
| Train-on-Future | ✅ | 用未来事件验证决策 |
| Three-Source Acquisition | ✅ | 扩展 expert_tracker |
| Elo Ranking | ✅ | Agent 能力评估 |
| Prediction API | 部分 | 预测型任务 |

### 直接应用

1. **expert_tracker 预测验证**：
   - 追踪预测 → 等待解答 → 验证准确率
   - 用真实未来验证情报质量

2. **Agent 能力排名**：
   - 用 Elo 机制排名 ΞΦΔΘΓΩΨ
   - 基于实际任务表现

3. **决策质量评估**：
   - 记录决策 → 追踪结果 → 反馈学习

---

## 六、关键洞察

1. **预测是"可验证的推理"**：
   - 不像其他任务，预测有明确的真值
   - 可以用未来验证现在

2. **时间是对齐的关键**：
   - 不同时间点的预测不可比
   - 必须对齐时间点才能公平比较

3. **Train-on-Future 规避数据泄露**：
   - 模型训练时"不可能看过答案"
   - 因为答案在未来

4. **Elo 比平均分更鲁棒**：
   - 缺失数据时 Elo 仍稳定
   - 平均分会因缺失而失真

---

## 七、后续行动

### 可立即借鉴

1. **决策追踪机制**：
   - 记录重要决策（预测）
   - 追踪实际结果（验证）
   - 反馈到技能库（学习）

2. **Agent Elo 排名**：
   - 用任务完成质量排名
   - 基于对齐的任务比较

3. **预测 API 集成**：
   - 对于预测型任务，调用 Echo API
   - 获取概率报告

---

*笔记完成于 2026-03-30 21:38*
