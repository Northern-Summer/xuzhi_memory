# 记忆索引 — L1 历史归档

> 路径：`~/.xuzhi_memory/memory/`
> 用途：L1 历史 raw log 归档（非每日写入位置）

## 真相源路径（唯一）
- **每日 log**：`~/.xuzhi_memory/daily/YYYY-MM-DD.md` ← 写入用这个
- **L2 快照**：`~/.xuzhi_memory/manifests/*_STABLE.md`
- **L3 归档**：`~/.xuzhi_memory/backup/`

## 历史归档（只读）
本目录保存灾变前的历史 daily log 副本，仅供参考，不应再写入。

| 文件 | 内容 |
|------|------|
| ARCHITECTURE.md | 系统架构 |
| INDEX.md | 灾变前记忆索引 |
| MEMORY_STABLE.md | 灾变前稳定记忆 |
| checkpoint.json | 检查点状态 |
| gateway_alert.json | 网关告警历史 |
| gateway_state.json | 网关状态历史 |

