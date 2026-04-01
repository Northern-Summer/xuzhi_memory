# 技能审计日志规范

> 创建时间：2026-04-01 18:45
> 维护者：Ξ

---

## 日志格式

### 标准格式（JSON）

```json
{
  "timestamp": "2026-04-01T18:45:00+08:00",
  "session_id": "agent:main:openclaw-weixin",
  "skill": {
    "name": "删除前确认",
    "source": "auto_generated",
    "trust_score": 0.6
  },
  "action": {
    "type": "file_deletion",
    "target": "/path/to/file",
    "risk_level": "high"
  },
  "context": {
    "trigger": "user_request",
    "related_files": []
  },
  "result": {
    "status": "confirmed",
    "user_response": "approved",
    "execution_time_ms": 100
  }
}
```

### 简化格式（单行）

```
[2026-04-01T18:45:00] SKILL:删除前确认 ACTION:file_deletion TARGET:/path RISK:high RESULT:confirmed
```

---

## 审计维度

### 1. 调用频率

| 技能 | 正常频率 | 当前频率 | 状态 |
|------|---------|---------|------|
| 删除前确认 | <5次/小时 | 0次/小时 | ✅ 正常 |
| 路径验证 | <10次/小时 | 0次/小时 | ✅ 正常 |

### 2. 风险分布

| 风险等级 | 操作数 | 占比 |
|---------|--------|------|
| 低 | - | - |
| 中 | - | - |
| 高 | - | - |
| 极高 | 0 | 0% |

### 3. 用户确认率

| 技能 | 需确认次数 | 确认次数 | 确认率 |
|------|-----------|---------|--------|
| 删除前确认 | - | - | - |

---

## 审计报告模板

```markdown
# 技能审计日报 - YYYY-MM-DD

## 概览

- 总调用次数：X
- 高风险操作：Y
- 用户确认率：Z%

## 异常事件

| 时间 | 技能 | 事件 | 处理 |
|------|------|------|------|
| - | - | - | - |

## 建议

- [ ] 建议项 1
- [ ] 建议项 2
```

---

## 存储

- 日志位置：`~/.xuzhi_memory/logs/skill_audit/`
- 格式：`YYYY-MM-DD.jsonl`（JSON Lines）
- 保留期：30 天
- 归档：每月归档到 backup/

---

## 参考

- 技能安全审计系统：skill_audit_system.md
- Agent Skills Survey: arXiv:2602.12430
