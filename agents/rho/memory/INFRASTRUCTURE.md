# INFRASTRUCTURE.md — ρ 荐股系统架构

> 建立时间：2026-03-31
> 更新：2026-03-31

---

## 系统定位

ρ 只做 A 股，中短期趋势跟随。
板块偏好：科技 > 新能源（不排斥其他更好选择）。

---

## 核心架构：HyperAgent + ECHO

### 三层架构（荐股流程）

```
Task Agent (web搜索)
  ↓ 候选股列表（带理由）
Meta Agent (过滤+优先排序)
  ↓ Top 3 候选
Multi-Agent 分析（技术/基本面/情绪）
  ↓ 研判数据
BullBear 对抗验证
  ↓
SelfCritic 批判
  ↓
ECHO 记录 → 最终推荐 1 只
```

### 已有模块（.rho/）

| 目录 | 模块 | 职责 |
|------|------|------|
| `agents/` | DataFetcherAgent | P0数据获取：OHLCV + 基本面 + 新闻 |
| `agents/` | TechnicalAnalyst | 技术分析：MA、RSI、趋势、量价 |
| `agents/` | FundamentalAnalyst | 基本面分析：PE、ROE、估值信号 |
| `agents/` | SentimentAnalyst | 情绪分析：新闻情绪评分 |
| `agents/` | RiskManager | 风险管理 + SelfCritic |
| `core/` | DecisionEngine | 主流程编排（analyze()） |
| `core/` | BullBear | 多空对抗分析 |
| `core/` | EchoCalibrator | 预测追踪与校准（ECHO机制） |
| `rules/` | LimitChecker | 涨跌停/停牌/新股检测 |
| `screener/` | screener | 五因子趋势选股 |
| `data/` | sources | LLM调用（Sina/baostock封装） |

---

## 荐股入口（stock_recommender）

**位置：** `.rho/screener/stock_recommender.py`（新建）

**输入：** 无（从全市场搜索）
**输出：**
1. 候选股列表（5-10只，含搜索理由）
2. 最终推荐 1 只（最强逻辑）

### 步骤

#### Step 1: Web搜索构建候选池

使用 `web_search` 工具搜索以下内容：
```
1. "A股 今日 涨停 原因" → 找板块效应
2. "A股 科技板块 资金流入" → 找机构动向
3. "A股 机构 推荐 最新" → 找分析师共识
4. "A股 大盘 明日 展望" → 判断市场环境
```

#### Step 2: 候选股技术筛选

对每只候选股运行 `TechnicalAnalyst`，筛选条件：
- RSI < 35（超卖反弹）或 MA5 > MA10（趋势转多）
- 量比 > 0.7（非极度缩量）
- 排除 ST 股、新股（上市 < 1年）

#### Step 3: Multi-Agent 分析（Top 3）

对通过筛选的候选股运行完整分析：
```
DataFetcherAgent.fetch_all()
  → TechnicalAnalyst.analyze()
  → FundamentalAnalyst.analyze()
  → SentimentAnalyst.analyze()
  → BullBear.analyze()
  → RiskManager.assess()
  → DecisionEngine._parse_final_text()
```

#### Step 4: ECHO记录

每次推荐写入 `~/.xuzhi_memory/expert_tracker/echo_calibration.json`：
```python
EchoCalibrator().record(
    code=code, name=name,
    prediction=signal,
    confidence=confidence,
    reasoning_quality=risk_sig.get('combined_quality', 0.5),
    trend=tech_sig.get('trend', ''),
    agent_outputs={...},
)
```

---

## 输出格式

```
【候选股】（按逻辑强度排序）

1. [股票名](代码) | 搜索理由 | 板块 | 逻辑
2. ...

【最终推荐】
股票名(代码) | 置信度 | 逻辑 | 入场条件 | 止损
```

---

## ECHO校准机制

每笔推荐记录 ID，下次分析时查询近期校准统计：
```python
EchoCalibrator().get_stats(days=30)
  → {accuracy, avg_confidence, calibration_error}
```

置信度校准原则：
- 如果 calibration_error > 0.1 → 降低置信度
- ECHO 准确率 < 50% → 标注"系统需校准"

---

## 文件路径规范

| 用途 | 路径 |
|------|------|
| DuckDB市场数据 | `~/.rho/market_data.duckdb` |
| ECHO校准记录 | `~/.xuzhi_memory/expert_tracker/echo_calibration.json` |
| Expert Tracker | `~/.xuzhi_memory/expert_tracker/` |
| 每日记忆 | `~/.xuzhi_memory/agents/rho/memory/YYYY-MM-DD.md` |
| ρ工作空间 | `~/.openclaw/agents/rho/workspace/.rho/` |

---

## 已知问题（2026-03-31）

1. **B5: format_decision缺少四层格式**
   - 当前 format_decision() 只有单层结构
   - 需要重写支持【一】速览【二】重点【三】禁区【四】明日条件

2. **候选股PE数据缺失**
   - baostock基本面查询未返回2024年年报PE数据
   - 需要增强 `_baostock_fundamental` 的年报查询逻辑

3. **新浪API稳定性**
   - 新浪实时行情API偶尔超时
   - 需要降级策略：超时5秒后跳过交叉验证
