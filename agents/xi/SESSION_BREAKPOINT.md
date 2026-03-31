# SESSION_BREAKPOINT.md — Ξ 断点文件

> 此文件由 Hook 自动维护，每次 Session End 时更新
> 格式：固定位置 + 固定字段 = 确定性恢复

## 当前断点

```yaml
session_id: "{{SESSION_ID}}"
ended_at: "{{TIMESTAMP}}"
status: "{{STATUS}}"

# 未完成任务（最高优先级）
pending_tasks:
  - task: "{{TASK_DESCRIPTION}}"
    priority: "{{PRIORITY}}"
    context: "{{CONTEXT_FILE}}"

# 本次会话关键决策
decisions:
  - decision: "{{DECISION}}"
    reason: "{{REASON}}"

# 系统状态
system:
  git_memory: "{{GIT_STATUS}}"
  git_genesis: "{{GIT_STATUS}}"
  active_agents: ["{{AGENT_LIST}}"]

# 下次恢复指令
resume_command: "{{RESUME_COMMAND}}"
```

## 恢复时行为

1. 读取此文件
2. 报告 pending_tasks
3. 继续执行，不等待用户指令

---

## 断点历史（自动追加）

