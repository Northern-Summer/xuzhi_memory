# MEMORY BOUNDARY MANIFEST
# 2026-03-25 确立 | Γ 起草

## 核心原则
每个智能体的记忆属于自己。不得跨边界读取或写入。

## 记忆层级

| 层级 | 路径 | 归属 | 备份 |
|------|------|------|------|
| L0 个人核心 | xuzhi_memory/agents/{id}/ | 各智能体 | 3份冗余 |
| L1 公共系统 | xuzhi_memory/memory/ | 全系统 | 3份冗余 |
| L2 每日日志 | xuzhi_memory/memory/daily/ | 全系统 | 追加 |
| L3 宪法/拓扑 | xuzhi_genesis/centers/*/ | 系统 | Git |

## 智能体记忆目录

```
xuzhi_memory/agents/
  xi/          → Ξ (main)，主会话
  gamma/       → Γ (gamma)，情报·记录
  phi/         → Φ (phi)，工程·哨兵
  delta/       → Δ (delta)，工程·锻造
  theta/       → Θ (theta)，情报·探索
  omega/       → Ω (omega)，心智·战略
  psi/         → Ψ (psi)，哲学·思辨
```

## 污染清除规则

- L0 目录下的 memory/ 只属于该智能体
- 其他智能体不得读取或写入
- L1 公共记忆不含任何个人身份信息
- Lambda 个人记忆 → xuzhi_memory/memory_OLD/Lambda/

## 灾变前遗留

- xuzhi_memory/memory/MEMORY_STABLE.md → 含有 Lambda 身份信息，移入 memory_OLD/
- xuzhi_memory/memory/ 下所有含 Lambda/Λ 标记的文件 → 审查后归档

