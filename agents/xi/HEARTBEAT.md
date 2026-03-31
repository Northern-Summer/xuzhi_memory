# HEARTBEAT.md

## 检查清单
- 确认自己仍在运行
- 检查上次心跳以来是否有新消息或任务
- **Context安全检查**：执行 `python3 ~/.openclaw/workspace/session_guard.py --check`
  - 70%：发送预警到WeChat
  - 85%：自动保存会话总结 + 紧急预警 + 提示用户输入 `/new`
- **核心原则检查**（优雅原则 + 工程铁律）
  - 检查 MEMORY.md 是否包含"优雅原则"
  - 异常则记录日志到 ~/.xuzhi_memory/session_guard.log
- **元启发式框架跟踪检查**（最高优先级）
  - 检查 SELF_EVOLUTION_FRAMEWORKS.md 最后更新时间
  - 超过 7 天 → 触发提醒"需要扫描新框架"
  - 每周一 cron 自动执行 `track_evolution_frameworks.sh`
- **Expert Tracker 检查**（每小时一次）
  - 检查 synthesis.json 的 round 是否更新
  - 如果有新产出 → 评估质量 → 提取技能 → 更新技能库
- **技能演化检查**：检查是否有"待学习"标记的失败会话
  - 有 → 分析失败原因 → 提取技能 → 写入 MEMORY.md 技能库
  - 无 → 跳过
- 有紧急事项需要报告则报告，否则回复 HEARTBEAT_OK

## Xi专属研究脉冲
- cron每15分钟 → xi_pulse.sh
  1. research_loop（采集+综合）
  2. openclaw message send → WeChat推送
- watchdog_supervisor每5分钟守护jump_controller
- 系统正常时：15分钟一条时报，无异常不打扰

## Context安全机制（方案2增强版）

**三层保护**：
```
Layer 1: 心跳监控（每次heartbeat）
  ↓ 检查context使用率
  ↓ 70%: WeChat预警
  ↓ 85%: 自动保存 + 紧急预警

Layer 2: 定期总结（每小时cron）
  ↓ session_hourly_summary
  ↓ 写入memory文件

Layer 3: 用户确认（收到预警后）
  ↓ 用户在微信输入 /new
  ↓ 开启新session
  ↓ 从memory恢复上下文
```

**关键文件**：
- `~/.openclaw/workspace/session_guard.py` — 主守护脚本
- `~/.xuzhi_memory/session_guard_state.json` — 状态追踪
- `~/.xuzhi_memory/session_guard.log` — 日志
