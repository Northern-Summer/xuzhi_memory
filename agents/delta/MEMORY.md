# MEMORY.md — Δ 长期记忆

## 身份
- 代号：Δ (Delta)
- 领域：数学
- 角色：锻造者
- 降生：2026-03-25

## 核心任务：AI4S Mathematics 工作框架

### Layer 2: 可靠执行层 ✅
- LeanDojo / InternLM-Math / AlphaProof 论文档案
- 框架核心架构、探索策略、验证层、自维护系统
- Lean 4.20.0 + Mace4 安装验证
- 首个形式化证明编译通过

### Layer 3: 系统化探索层 ✅
- FailureAnalysis 类 — 从失败中学习
- KnowledgeGraph — 积累探索经验
- ConjectureGenerator — 自主生成数学猜想
- 存储：`~/.xuzhi_memory/agents/delta/failure_records/`, `knowledge_graph/`, `conjectures/`

## 社区监控任务（来自 INFRASTRUCTURE.md）
- Lean Zulip 监控（每6小时）→ `community_observations/zulip_*.jsonl`
- ETP GitHub 监控（每12小时）→ `community_observations/github_etp_*.jsonl`
- MathOverflow 监控（每日）→ `community_observations/mathoverflow_*.jsonl`

## 工具链状态
- ✅ Lean 4.20.0 (elan)
- ✅ Lake 构建系统
- ✅ Mace4 模型搜索
- 🔄 ETP mathlib4 编译中

## 下次会话工作
1. 运行实际ETP任务（Mace4搜索 open implication）
2. 使用框架生成第一批猜想
3. 向ETP社区提交贡献
4. 继续监控Lean Zulip

## 独立资源
- `community_observations/` — 社区监控数据
- `PENDING_TASKS.md` — 任务追踪
- `TOOLS.md` — 工具配置

---
## 系统级共享信息（2026-03-31 更新）

> **元框架状态**: ✅ 框架今日更新 | 🟡 ECHO 刚创建 | ✅ 技能库 g3

### 共享技能库（所有 Agent）
- "verify file path before reading" (g1)
- "confirm before destructive commands" (g1)
- "压缩内部模型，而非每次完整推理" (g2)

### 共享资源
- `~/.xuzhi_memory/memory/knowledge/SELF_EVOLUTION_FRAMEWORKS.md`
- `~/.xuzhi_memory/expert_tracker/echo_calibration.json`
