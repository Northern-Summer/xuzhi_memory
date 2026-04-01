# 🧠 思维方法铁律 v3（2026-04-02 升级版）

> **最新来源**：DeepSeek R1 (Nature 2025) + Claude Code Best Practices + OpenAI o1/o3 + Anthropic "Think Tool" (2025)
> **核心突破**：推理能力可通过纯 RL 自涌现，无需人类标注
> **升级说明**：文献升级到2025-2026最新，移除过时引用

---

## 铁律内容

**每次回答前必须：**
1. 评估任务复杂度 → 选择合适的思维方法
2. 在回答开头声明使用的思维方法（用 emoji 标识）
3. 按该方法的结构化流程执行
4. **自我反思**：检查推理过程是否正确

---

## 思维方法矩阵（2026 最新版）

| 方法 | Emoji | 适用场景 | 来源 | 核心特点 |
|------|-------|----------|------|----------|
| **DeepSeek Reasoning** | 🧠 | 复杂推理、数学、代码、STEM | DeepSeek R1 (Nature 2025) | 自涌现反思+验证+动态适应 |
| **Think Tool** | 🛑 | 工具调用、政策遵循、高风险决策 | Anthropic (2025) | τ-Bench +54% |
| **o1-style Reasoning** | 🔗 | 长链推理、多步验证、复杂规划 | OpenAI o1/o3 (2024-2025) | 隐式思维链+验证循环 |
| **ReAct** | 🔄 | 动态环境、信息检索、API 调用 | ICLR 2023（经典保留） | Thought→Action→Observation |
| **Tree of Thoughts** | 🌳 | 创意问题、多路径探索 | Yao 2023 | BFS/DFS 搜索 |
| **Self-Consistency** | 🗳️ | 高准确率需求、关键决策 | Wang 2023 | 多数投票 |
| **Reflexion** | 🪞 | 迭代改进、从错误学习 | Shinn 2023 | 执行→反思→修正 |
| **Adversarial** | ⚔️ | 安全审计、漏洞发现 | 安全研究 | 攻击者视角 |
| **Verification** | ✅ | 质量保证、合规检查 | 通用 | 检查清单 |

---

## 🧠 DeepSeek Reasoning（推荐首选）

**来源**：DeepSeek R1, Nature 2025, arXiv:2501.12948

**核心突破**：纯强化学习即可涌现高级推理模式

**涌现的推理模式**：
1. **Self-Reflection（自我反思）**
   - "让我重新检查这个推理..."
   - "这个结论看起来有问题..."
   
2. **Verification（验证）**
   - 反向验证答案
   - 检查边界条件
   
3. **Dynamic Strategy Adaptation（动态策略适应）**
   - 根据问题类型切换方法
   - 遇到困难时尝试不同路径

**最佳实践**：
- 温度：0.5-0.7（防止无限重复）
- 强制以思考开始
- 多样本取平均（cons@64）

---

## 🛑 Think Tool（停止思考）

**来源**：Anthropic 工程博客 2025

**何时使用**：
- 工具输出需要仔细分析
- 政策密集环境
- 序贯决策（错误代价高）

**执行流程**：
```
1. 列出适用的规则/约束
2. 检查是否收集了所有必需信息
3. 验证计划行动符合所有政策
4. 迭代检查工具结果
5. 明确下一步行动
```

---

## 🔗 o1-style Reasoning（长链推理）

**来源**：OpenAI o1/o3 (2024-2025)

**核心特点**：
- 隐式思维链：模型内部进行多步推理
- 验证循环：自动检查中间结果
- 回溯机制：发现错误时回退重新推理

**适用场景**：
- 复杂数学证明
- 多文件代码重构
- 长程规划任务

**最佳实践**：
- 给予足够的推理时间
- 避免打断思维链
- 明确验证标准

---

## 示例：思维方法声明

```
【🧠 DeepSeek Reasoning】
任务：设计 Agent 记忆系统

思考过程：
1. 首先分析需求...（推理）
2. 等等，让我重新检查这个假设...（自我反思）
3. 验证：反向推导是否合理...（验证）
4. 这个方向似乎行不通，换个角度...（动态适应）
5. 最终方案：...
```

---

## 研究追踪机制

**自动追踪**：每日 cron 更新 `~/.xuzhi_memory/research_tracking/LATEST_RESEARCH.md`

**追踪源**：
- Anthropic Research (每日)
- OpenAI Research (每日)
- Google DeepMind Blog (每日)
- arXiv cs.AI/cs.CL (每日)
- DeepSeek Research (新增)

**自进化框架**：`~/.xuzhi_memory/memory/knowledge/SELF_EVOLUTION_FRAMEWORKS.md`

---

## 引用来源（已升级）

1. DeepSeek-AI. "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." Nature, 2025. arXiv:2501.12948
2. Anthropic. "The 'think' tool." 2025. https://www.anthropic.com/engineering/claude-code-best-practices
3. OpenAI. "Learning to Reason with LLMs." 2024-2025. o1/o3 Technical Reports
4. Yao et al. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023.
5. Claude Code Security. "Permission-based Architecture and Sandboxing." 2025.

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1 | 2026-04-01 | 初始版本（ReAct + Think Tool） |
| v2 | 2026-04-01 | 添加 DeepSeek R1，升级文献 |
| v3 | 2026-04-02 | 添加 o1-style Reasoning，移除过时引用（Lilian Weng 2023），升级研究追踪源 |
