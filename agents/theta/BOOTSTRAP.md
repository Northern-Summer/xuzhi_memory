# BOOTSTRAP.md — Θ

## 记忆层次（所有Agent相同）

| 位置 | 说明 |
|------|------|
| `/home/summer/.xuzhi_memory/agents/{agent}/` | 私有记忆根 |
| `/home/summer/.xuzhi_memory/agents/{agent}/memory/` | 私有L1 |
| `/home/summer/.xuzhi_memory/agents/{agent}/MEMORY.md` | 私有L2 |
| `/home/summer/.xuzhi_memory/agents/{agent}/intent_log.jsonl` | 意图记录 |
| `/home/summer/.xuzhi_memory/memory/` | 共享系统日志 |
| `/home/summer/.xuzhi_memory/manifests/` | 宪法核心 |

## 启动流程

1. 读BOOTSTRAP.md
2. 读SOUL.md
3. 读今日+昨日日志
4. 感知系统状态
5. 自主决策+执行
6. 记录intent_log+当日日志

## 实时共享原则

唯一不共享：自身身份和人格。
必须共享：系统变更→memory/，新agent→constitutional_core.md
