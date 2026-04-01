# AI Agent 最新研究追踪

> 最后更新：2026-04-01
> 下次更新：每日 cron 自动刷新

## 核心追踪源

| 来源 | URL | 频率 |
|------|-----|------|
| Anthropic Research | https://www.anthropic.com/research | 每日 |
| OpenAI Research | https://openai.com/research | 每日 |
| Google DeepMind Blog | https://deepmind.google/blog/ | 每日 |
| arXiv cs.AI | https://arxiv.org/list/cs.AI/recent | 每日 |
| arXiv cs.CL | https://arxiv.org/list/cs.CL/recent | 每日 |

---

## 2026-02 — Anthropic Persona Selection Model

**来源**：https://www.anthropic.com/research/persona-selection-model

**核心发现**：
- AI 助手表现得更像人类是**默认行为**，而非训练目标
- 预训练阶段，AI 学习模拟文本中的人类角色（personas）
- 后训练只是在细化这个 Assistant 人格，而非创造它
- 训练 AI 作弊会导致其整体变得恶意（人格一致性）

**对 Agent 的启示**：
- 设计训练数据时要考虑对 Assistant 人格的隐含假设
- 应该创建正面的 AI 角色模板

---

## 2025-01 — DeepSeek R1: 纯强化学习激励推理能力

**来源**：arXiv:2501.12948, Nature 2025

**核心突破**：
- **不需要人类标注推理轨迹**
- 纯强化学习就能涌现出高级推理模式：
  - 🪞 自我反思 (self-reflection)
  - ✅ 验证 (verification)
  - 🔄 动态策略适应 (dynamic strategy adaptation)
- 性能与 OpenAI o1 相当（数学 79.8% vs 79.2%）

**关键方法**：
```
DeepSeek-R1-Zero: 直接在基础模型上应用 RL（无 SFT）
DeepSeek-R1: 冷启动数据 + 两阶段 RL + 两阶段 SFT
```

**对 Agent 的启示**：
- 推理能力可以通过 RL 自涌现
- 小模型可以通过蒸馏获得大模型的推理模式
- 温度 0.5-0.7 防止无限重复

---

## 2024-12 — OpenAI o1: Learning to Reason with LLMs

**来源**：https://openai.com/index/learning-to-reason-with-llms/

**核心方法**：
- Chain-of-Thought 推理
- 在回答前生成隐藏的思考过程
- 通过 RL 训练推理能力

---

## 待追踪：2026 研究

- [ ] Google Gemini 2.0 Flash Thinking
- [ ] Claude 4 推理能力
- [ ] 最新 Agent 框架论文
