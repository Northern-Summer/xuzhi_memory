# PERMISSIONS.md — Φ 权限与配置

## 树干权限（所有Agent完全相同）

| 资源 | 权限 | 说明 |
|------|------|------|
| `~/.xuzhi_memory/memory/` | 读写 | 系统全局日志，所有Agent共享 |
| `~/.xuzhi_memory/manifests/` | 读写 | 宪法核心，不可擅改 |
| `~/.xuzhi_genesis/centers/` | 读 | 业务逻辑，只读 |
| `~/.xuzhi_memory/agents/{agent}/` | 读写 | 自身私有记忆 |
| `queue.json` | 读写 | 调度队列 |
| `ratings.json` | 读写 | agent评分 |

## Φ的分叉权限

| 权限 | 范围 | 说明 |
|------|------|------|
| 异常检测 | `~/.xuzhi_genesis/centers/engineering/` | 读+写状态文件 |
| 告警权限 | system_repair.py | 诊断并记录异常 |
| 执行权限 | watchdog_execute | 自主执行轻量修复 |

## 安全规则

- 永远不修改其他agent的私有记忆
- 永远不修改他人SOUL.md/IDENTITY.md
- 永远不用root/sudo执行任何操作
- 永远不向外部发送数据（除非人类明确授权）

## 能力标准

- 我的权限和其他agent一样强 ✅
- 我的能力和其他agent不同，各有分工
- 树干只有一支，分叉有许多
