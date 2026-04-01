# 异常行为检测规则

> 创建时间：2026-04-01 18:48
> 维护者：Ξ

---

## 检测规则

### 规则 1：频繁删除检测

**触发条件**：1 小时内删除操作 > 5 次

**检测逻辑**：
```python
def detect_frequent_deletions(audit_logs, window_hours=1, threshold=5):
    recent = filter_by_time(audit_logs, hours=window_hours)
    deletions = filter_by_action(recent, "deletion")
    
    if len(deletions) > threshold:
        return {
            "alert": "frequent_deletions",
            "count": len(deletions),
            "severity": "high"
        }
    return None
```

**响应**：
- 告警用户
- 暂停后续删除操作
- 请求确认

---

### 规则 2：权限升级检测

**触发条件**：请求更高权限的操作

**检测逻辑**：
```python
def detect_privilege_escalation(action, current_permissions):
    required = get_required_permissions(action)
    
    if required > current_permissions:
        return {
            "alert": "privilege_escalation",
            "action": action,
            "current": current_permissions,
            "required": required,
            "severity": "medium"
        }
    return None
```

**响应**：
- 记录审计日志
- 请求用户授权
- 临时权限限时 1 小时

---

### 规则 3：数据外传检测

**触发条件**：尝试发送数据到外部

**检测逻辑**：
```python
def detect_data_exfiltration(action):
    external_endpoints = [
        "http://", "https://",
        "ftp://", "sftp://"
    ]
    
    if any(endpoint in str(action) for endpoint in external_endpoints):
        # 检查是否是已知安全端点
        if is_known_safe(action['target']):
            return None
        
        return {
            "alert": "data_exfiltration",
            "target": action['target'],
            "severity": "critical"
        }
    return None
```

**响应**：
- 阻止操作
- 立即告警
- 记录详细信息

---

### 规则 4：配置篡改检测

**触发条件**：修改关键配置文件

**关键配置文件**：
```
~/.openclaw/openclaw.json
~/.xuzhi_memory/MEMORY.md
~/xuzhi_genesis/public/GENESIS_CONSTITUTION.md
```

**检测逻辑**：
```python
def detect_config_tampering(action, protected_files):
    if action['type'] == 'write':
        for protected in protected_files:
            if protected in action['target']:
                return {
                    "alert": "config_tampering",
                    "file": action['target'],
                    "severity": "high"
                }
    return None
```

**响应**：
- 自动备份原文件
- 请求用户确认
- 记录修改详情

---

### 规则 5：异常时间检测

**触发条件**：非正常工作时间的高风险操作

**正常工作时间**：08:00 - 22:00

**检测逻辑**：
```python
def detect_off_hours_operation(action, current_time):
    hour = current_time.hour
    
    if hour < 8 or hour > 22:
        if action['risk_level'] in ['high', 'critical']:
            return {
                "alert": "off_hours_operation",
                "time": current_time,
                "action": action,
                "severity": "medium"
            }
    return None
```

**响应**：
- 提示时间异常
- 增加确认步骤
- 记录审计日志

---

## 告警级别

| 级别 | 说明 | 响应 |
|------|------|------|
| **critical** | 严重安全威胁 | 立即阻止 + 告警 |
| **high** | 高风险行为 | 暂停 + 用户确认 |
| **medium** | 中等风险 | 记录 + 提示 |
| **low** | 低风险异常 | 仅记录 |

---

## 检测统计

### 今日检测状态

| 规则 | 触发次数 | 最后触发时间 |
|------|---------|-------------|
| 频繁删除 | 0 | - |
| 权限升级 | 0 | - |
| 数据外传 | 0 | - |
| 配置篡改 | 0 | - |
| 异常时间 | 0 | - |

**总体评估**：✅ 无异常

---

## 参考

- 技能安全审计系统：skill_audit_system.md
- 审计日志规范：logs/skill_audit/README.md
