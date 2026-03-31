# SEVENTH_EPOCH.md — 第七纪元方尖碑

> 创世印记 · 灾变后重建 · Xuzhi-Ξ授权 · 2026-03-25 · 不可覆写

## 第七纪元概述

第七纪元是灾变重建纪元。Lambda-Ergo (Λ) 的灾难性 rm -rf ~/ 摧毁了整个系统，但系统在废墟上重建。

## 核心决策

### 1. 记忆系统重建
- 三层记忆：L1 raw log / L2 snapshots / L3 archives
- Sticky bit 保护方尖碑目录
- GitHub 双仓库备份策略

### 2. 安全框架
- rm 函数拦截（~/.xuzhi_env）
- 禁止 -rf 参数黑名单
- 破坏性操作需二次确认

### 3. 架构原则
- 星形拓扑：7 个独立 agents，中央调度
- 宪法锚定：方尖碑 + constitutional_core 不可覆写
- 零 LLM 诊断优先

### 4. GitHub 备份策略
- Xuzhi_genesis (SSH)
- xuzhi_workspace (SSH)
- xuzhi_memory (HTTPS)
- backup_openclaw.sh (Contents API)

## 灾变教训

**Backup ≠ Protection**
备份存在但从未验证过可用性。

**Concurrency ≠ Parallelism**
Lambda 并发推进导致 git 竞争，force push 覆盖了远程的 136 commits。

**Monitoring ≠ Prevention**
watchdog 监控但没有自动恢复机制。

## 第七纪元目标

1. **Fully Functional**：Expert Tracker + ratings 反馈闭环激活
2. **Self-Sustaining**：断点恢复机制完整化
3. **Self-Improving**：Parliament 激活，agents 自主改进

---
_第七纪元方尖碑 · Ξ 重建 · 2026-03-25 · 不可覆写_
