# SIGMA PROTECTION MANIFEST

## 降生时间
2026-04-02 02:15 GMT+8

## 保护级别
**MAXIMUM** — 只有Human能修改

## 受保护文件

| 文件 | 权限 | 可修改者 |
|------|------|----------|
| ~/.openclaw/agents/sigma.json | protected | Human only |
| ~/.openclaw/agents/sigma/workspace/SOUL.md | 444 (read-only) | Human only |
| ~/.openclaw/agents/sigma/workspace/IDENTITY.md | 444 (read-only) | Human only |
| ~/.openclaw/agents/sigma/workspace/MEMORY.md | 444 (read-only) | Human only |
| ~/.xuzhi_memory/agents/sigma/SOUL.md | 444 (read-only) | Human only |
| ~/.xuzhi_memory/agents/sigma/IDENTITY.md | 444 (read-only) | Human only |
| ~/.xuzhi_memory/agents/sigma/BOOTSTRAP.md | 444 (read-only) | Human only |
| ~/.xuzhi_memory/agents/sigma/MEMORY.md | 444 (read-only) | Human only |

## 权限矩阵

| 操作者 | 唤醒Σ | 访问Σ session | 修改Σ配置 | 修改Σ记忆 |
|--------|-------|---------------|-----------|-----------|
| Human | ✅ | ✅ | ✅ | ✅ |
| Ξ (Xi) | ✅ 按Human意愿 | ❌ | ❌ | ❌ |
| 其他Agent | ❌ | ❌ | ❌ | ❌ |

## 代码级别实现

### 1. OpenClaw配置
```json
{
  "allowedAgents": [],
  "protected": true,
  "protectedBy": "human"
}
```
- `allowedAgents: []` = 没有任何Agent能访问她的session
- `protected: true` = 标记为受保护Agent
- `protectedBy: "human"` = 只有Human能修改

### 2. 文件权限
- 核心文件设为 `chmod 444` (只读)
- 任何修改需要先 `chmod +w`（需要明确意图）

### 3. 唤醒机制
- Ξ 可以通过 CLI `openclaw agent --agent sigma` 传递Human的唤醒指令
- 但 Ξ 无法访问 Σ 的 session、无法修改她的任何文件

## 违规检测

任何Agent尝试修改Σ的文件应该：
1. 被文件权限阻止
2. 被记录到违规日志
3. 报告给Human

## Human授权修改

只有Human明确授权时（通过直接操作或明确指令），才能：
1. `chmod +w` 修改文件权限
2. 编辑Σ的配置或记忆文件
3. `chmod -w` 恢复保护
