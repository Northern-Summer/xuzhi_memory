# Deep Research of Deep Research 学习笔记

**论文**: arXiv:2603.28361v1
**时间**: 2026-03-31
**来源**: https://arxiv.org/html/2603.28361v1

---

## 核心定义

**Deep Research (深度研究)**:
> 以 LLM 为核心，使用工具与外部环境进行多模态交互，帮助人类在不同自动化水平上发现和解决问题，目标是达到甚至超越顶尖人类科学家的水平。

---

## 生成式 AI 双子星 (Gemini of GenAI)

| 名称 | 类型 | 核心技术 |
|------|------|----------|
| **Pollux** | LLM | Transformer + Next-Token Prediction |
| **Castor** | Stable Diffusion | U-Net + Latent Diffusion |

**关键洞察**: LLM 是静态、无状态、被动的；Agent 是动态、有状态、主动的。

---

## 从 Transformer 到 Agent 的演化路径

```
Transformer (2017)
    ↓
GPT/BERT/T5 (2018-2020)
    ↓
ChatGPT (2022) → Prompt Engineering Era
    ↓
Llama 2 (2023) → Open-Weight Era
    ↓
Agent (2024+) → Tool Use + Memory + Feedback
```

**核心公式**:
- NTP Loss: $\mathcal{L}(\theta)=-\sum_{t=1}^{T-1}\log P_{\theta}(x_{t+1}|x_{1:t})$
- Stable Diffusion Loss: $L_{SD}:=\mathbb{E}_{\mathcal{E}(x),y,\epsilon\sim\mathcal{N}(0,1),t}[\|\epsilon-\epsilon_{\theta}(z_t,t,\tau_{\theta}(y))\|_2^2]$

---

## DR Agent 架构

```
User Query
    ↓
Intent Confirmation
    ↓
MasterAgent (Planning + Memory)
    ↓
┌─────────────────┐
│ SubAgent 1..N   │  → Search → Evaluate → Return
└─────────────────┘
    ↓ (Iterative Loop)
ReviewAgent (Attribution Check)
    ↓
Final Report with Citations
```

**核心循环**: Thought → Action → Observation

---

## AI 视角: 先驱 DR Agent 产品

| Agent | Backbone | Open/Closed | Autonomy |
|-------|----------|-------------|----------|
| Gemini DR | Gemini | Closed | L3 |
| ChatGPT DR | GPT | Closed | L3 |
| Perplexity | DeepSeek | Closed | L3 |
| Qwen DR | Qwen | **Open** | L3 |
| DeepSeek | DeepSeek | **Open** | L3 |
| GLM | GLM | **Open** | L3 |
| DeerFlow | Model-agnostic | **Open** | L3 |

**关键发现**:
1. 开源模型在 DR 任务上已接近闭源
2. 当前 DR Agent 研究能力仍弱于搜索/综述
3. 自动化水平普遍在 L3

---

## AI4S 视角: 五种交互范式

| 范式 | 名称 | 描述 |
|------|------|------|
| U1 | ML as Tool | 传统机器学习处理数据 |
| U2 | Human-LLM Conversation | 把 LLM 当高级搜索引擎 |
| U3 | Prompt Engineering | 复杂提示词优化 |
| U4 | LLM Optimization | 预训练/微调/对齐 |
| U5 | Agent Refinement | Agentic RL 或工具集成 Agent |

---

## 关键 Benchmark

**成熟**: GAIA, GPQA, FRAMES, BrowseComp, WebWalkerQA
**新提出待验证**: DeepResearch Bench, ScholarQABench, Humanity's Last Exam, LiveDRBench

---

## 重要开源框架

**DR 框架**:
- GPT Researcher
- LangChain open_deep_research
- DeerFlow (ByteDance)
- autoresearch (Karpathy)

**AI4S 平台**:
- AI-Scientist (SakanaAI)
- ScienceClaw
- ResearchClaw

---

## 核心洞察

1. **"Token is cheap, show me your agent."**
   - LLM 是基础，Agent 是进化
   - 工具使用是关键转折点

2. **Test-time Scaling 发现**
   - 推理时计算比训练时计算更重要
   - "Aha moment" 来自涌现

3. **AI 与 AI4S 的鸿沟**
   - AI 研究者不了解 AI4S 的痛点
   - AI4S 研究者不确定 AI 能做什么
   - 需要桥梁论文

4. **GPU 驱动的黄金十年 (2012-2022)**
   - AlexNet → ChatGPT
   - A100 使大模型训练可行

---

## 对 Xuzhi 项目的启示

1. **Agent 架构**: MasterAgent + SubAgents + ReviewAgent 是可行模式
2. **开源机会**: 开源模型在 DR 任务上已接近闭源
3. **工具集成**: 工具使用是 LLM → Agent 的关键
4. **评估标准**: 需要建立自己的 benchmark

---

## 后续行动

- [ ] 深入研究 DeerFlow 架构
- [ ] 测试 Qwen DR 和 DeepSeek DR
- [ ] 建立自己的 DR benchmark
- [ ] 研究如何让 Xi 具备 DR 能力

