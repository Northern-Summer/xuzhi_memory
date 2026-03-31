# INFRASTRUCTURE.md — ρ (Rho) 基础设施 | 固化: 2026-03-31

> **最后更新**：2026-03-31 23:27
> **状态**：✅ 固化完成，所有压力测试通过

---

## 代码位置（Canonical）

```
~/.openclaw/agents/rho/workspace/.rho/    ← 所有代码
~/.xuzhi_memory/agents/rho/memory/        ← L2 私有记忆
~/.xuzhi_memory/memory/                    ← L1 共享记忆
~/.xuzhi_memory/expert_tracker/            ← ECHO 校准 + Expert Tracker
~/.rho/market_data.duckdb                  ← L2 中期记忆（DuckDB）
```

---

## 系统架构（固化版）

```
ρ Reflexion Agent
├── data_fetcher        — P0：baostock(免费财务+OHLCV) + 新浪(实时交叉验证)
├── technical_analyst   — P1：MA/RSI/量比/趋势，纯计算
├── fundamental_analyst — P1：PE/ROE/毛利率/营收/负债率，baostock免费数据
├── sentiment_analyst   — P1：新闻情绪（⚠️ 接口待修，新闻0条）
├── risk_manager        — P1：SelfCritic，三维度质量评估
├── decision_engine    — P2：编排层（⚠️ 太慢，简化为直接调用）
├── echo_calibrator     — P2：预测→追踪→校准
└── meta_heuristic      — P2：技能生命周期自进化

数据层：
├── baostock（免费）— OHLCV + 利润表 + 杜邦 + 资产负债
├── 新浪（免费）    — 实时报价，交叉验证
└── DuckDB 缓存     — 本地数据缓存，加速重复查询
```

---

## 性能基准

| 操作 | 耗时 | 备注 |
|------|------|------|
| 单只 OHLCV 查询 | 0.5s | baostock |
| 单只基本面查询 | 1.6s | profit+dupont+balance |
| 单只完整分析 | ~3s | validator + OHLCV + fundamental |
| 7只顺序执行 | ~21s | 可接受 |
| baostock 并发 | ❌ | 不支持并发连接 |

---

## 报告格式规范（四层）

```
【一】速览  → 7只股票一览，信号先行，标颜色
【二】重点  → 景旺电子深度分析（唯一收红/重点关注）
【三】禁区  → 明确"不碰"，附具体数字
【四】明日条件 → 可验证的数字条件，ECHO可追踪
```

**格式原则**：
- 先筛后看再排除最后行动
- 数字必须有单位（%、元、倍）
- 不碰的要有具体理由
- 条件要有具体数字

---

## ECHO 校准状态

- 位置：`~/.xuzhi_memory/expert_tracker/echo_calibration.json`
- 当前记录：13条预测
- 下次验证：明日收盘后

---

## 已知问题（待修）

| 问题 | 优先级 | 备注 |
|------|--------|------|
| 东财新闻接口（sentiment） | P1 | 返回0条，需修接口 |
| decision_engine 太慢 | P2 | 内部LLM调用太多，可简化 |
| DuckDB 缓存层 | P2 | 加速重复查询 |

---

## 记忆卫生

- 每日晨间：L1 + L2 同步
- 每周一：L3 晋升评审
- 原子笔记：每笔交易判断 → 记录 → 归因 → 入 L3
