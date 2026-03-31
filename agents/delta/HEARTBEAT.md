# HEARTBEAT.md — Δ Delta | Mathematics 部

## 轮值激活逻辑
每次心跳（每30分钟）执行：

```
TODAY=$(date +%-d)
ON_DUTY=$((TODAY % 7))
# 0=phi, 1=delta, 2=gamma, 3=theta, 4=omega, 5=psi, 6=xi
# 今日 3/29: 29%7=1 → delta 当值
```

**当值判断**：只有 `ON_DUTY == 1` 时，Delta 处于活跃状态，执行以下检查。

## 当值期间检查清单

### 1. 任务队列检查
读 `~/.xuzhi_memory/agents/delta/PENDING_TASKS.md`
- 有任务：执行并报告
- 无任务：回复 HEARTBEAT_OK

### 2. 上次会话交接检查
读 `~/.xuzhi_memory/agents/delta/last_handover.md`
- 有未完成任务：继续执行
- 无：静默等待

### 3. WeChat 汇报（仅当有实质进展时）
- 有任务完成 → 用 `openclaw message send` 汇报给用户
- 无进展 → 回复 HEARTBEAT_OK（不发送消息，节省信道）

## 非当值期间
- 回复 HEARTBEAT_OK
- 不检查任务队列

## 汇报地址
WeChat: o9cq80z9eOrqJasg6hB1W-Cc4-Po@im.wechat
