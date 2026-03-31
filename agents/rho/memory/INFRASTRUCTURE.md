# INFRASTRUCTURE.md — ρ (Rho) 基础设施状态

> **强制等级：每个 ρ Session Startup 必须读取**
> **最后更新：2026-03-31 22:05**

---

## 代码位置

| 类型 | 路径 | 说明 |
|------|------|------|
| OpenClaw Agent | `~/.openclaw/agents/rho/workspace/.rho/` | **canonical**：所有代码 |
| L1 共享 | `~/.xuzhi_memory/memory/` | 每日状态 |
| L2 私有 | `~/.xuzhi_memory/agents/rho/memory/` | 学科私有 |
| ECHO 校准 | `~/.xuzhi_memory/expert_tracker/echo_calibration.json` | 预测追踪 |
| Expert Tracker | `~/.xuzhi_memory/expert_tracker/` | 情报追踪 |

**绝对禁止**：在 `workspace/.rho/` 以外的位置写代码。

---

## P0 → P1 → P2 架构

```
DataFetcherAgent (P0)
    baostock (primary) + tushare (fundamental) + sina news (sentiment)
         ↓
┌─────────────────────────────────────────────────┐
│ P1 Multi-Agent                                   │
│   TechnicalAnalyst  → OHLCV, MA, RSI, volume     │
│   FundamentalAnalyst → PE, ROE, revenue growth  │
│   SentimentAnalyst  → news headlines, market mood │
│         ↓                                        │
│   RiskManager (SelfCritic pattern)               │
│   BullBear (adversarial validator)               │
└─────────────────────────────────────────────────┘
         ↓
P2 Meta-Heuristic
    DecisionEngine → Final Decision
    EchoCalibrator → prediction tracking
    MetaCognitiveLoop → skill evolution
         ↓
  ECHO calibration JSON
```

---

## ECHO 校准接入

**文件**：`~/.xuzhi_memory/expert_tracker/echo_calibration.json`

**ρ 的用法**：
- 每条市场预测 → 写入 `predictions[]`
- 格式：`{code, prediction, confidence, timestamp}`
- 下次 session 检查实际结果 → 写入 `calibrations[]`
- 触发：每次 session 做出预测时

---

## Expert Tracker 接入

**文件**：
- `~/.xuzhi_memory/expert_tracker/expert_db.json`
- `~/.xuzhi_memory/expert_tracker/synthesis.json`

**ρ 的贡献**：
- 金融市场专家领域 → 添加到 expert_db.json
- 市场情报 → 写入 synthesis.json
- 优先级：Tier 3（Bloomberg, Reuters, Wind, 中信等）

---

## 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| **Reflexion Agent** | `research/reflexion_agent.py` | 主推理循环 + MultiAgent协调 |
| **Decision Engine** | `core/decision_engine.py` | P2 全流程编排 |
| **Data Fetcher** | `agents/data_fetcher.py` | P0: baostock+tushare+news |
| **Technical Analyst** | `agents/technical_analyst.py` | P1: OHLCV技术分析 |
| **Fundamental Analyst** | `agents/fundamental_analyst.py` | P1: PE/ROE/营收分析 |
| **Sentiment Analyst** | `agents/sentiment_analyst.py` | P1: 新闻情绪分析 |
| **Risk Manager** | `agents/risk_manager.py` | P1: SelfCritic风险评估 |
| **Echo Calibrator** | `core/echo_calibrator.py` | P2: 预测追踪校准 |
| **Meta Heuristic** | `core/meta_heuristic.py` | P2: 技能生命周期+自进化 |
| LLM 研究员 | `research/llm_researcher.py` | MiniMax M2.7 调用 |
| 判断追踪 | `research/judgment_tracker.py` | 纪律反馈 |
| 涨跌停检测 | `rules/limit_checker.py` | 规则引擎 |
| T+1 检测 | `rules/t1_checker.py` | A股规则 |
| 五因子筛选 | `screener/screener.py` | 选股 |
| 实时监控 | `monitor/realtime.py` | 异动警报 |
| 候选池 | `screener/pool_a.py` | 候选股票 |

---

## 数据层

| 来源 | 用途 | 状态 |
|------|------|------|
| baostock | OHLCV日线（主力） | ✅ |
| tushare | 基本面数据（PE/ROE/营收） | ⚠️ 需token |
| Sina realtime | 实时报价交叉验证 | ✅ |
| Sina news | 新闻情绪 | ✅ |
| eastmoney | 新闻备用 | ✅ |
| akshare | 候选（blocked by proxy） | ❌ 代理问题 |

---

## 模型

- **Primary**：MiniMax M2.7（`minimax-m2.7`）
- **API**：InfiniAI（`sk-cp-ytbzyqyoa7dewbpv`）
- **Endpoint**：`https://cloud.infini-ai.com/maas/coding/v1`

---

## P2 技能系统

- **技能注册表**：`~/.rho/skills/index.json`
- **进化历史**：`~/.rho/skill_history/evolution.json`
- **元认知记忆**：`~/.rho/meta_memory/meta_YYYY-MM-DD.json`
- **11个默认技能**：技术分析×3 + 基本面×3 + 情绪×2 + 元认知×3

---

## 修订历史

| 日期 | 变更 |
|------|------|
| 2026-03-31 22:05 | P0+P1+P2完整系统构建完成 |
| 2026-03-31 22:00 | 初始创建，整合架构现状 |
