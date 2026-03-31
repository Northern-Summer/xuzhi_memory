# 轮值机制 — Daily Agent Rotation

> **状态**：已实现，但未固化到 AGENTS.md 启动流程
> **上次更新**：2026-03-29

## 机制说明

每天一个 Greek agent 轮流值班（ΦΔΘΓΩΨ + Xi），共 7 人。

**schedule 映射**（`rotation_state.json`）：
```
0 = phi   (语言学/文学)
1 = delta (数学)
2 = gamma (自然科学)
3 = theta (历史学/社会科学)
4 = omega (艺术)
5 = psi   (哲学)
6 = xi    (人工智能)
```

## 当值计算公式

```python
day_of_month = int(date_str.split('-')[2])  # e.g., 29
schedule_idx = day_of_month % 7              # 29 % 7 = 1
today_agent = schedule[str(schedule_idx)]    # delta
```

## 轮值 Agent 的职责

1. **在线待机** — 确认 session 在线（session key: `agent:<greek>:main`）
2. **领域关注** — 报告本学科当日关注方向（简短，3 个点）
3. **任务处理** — 处理本领域的临时任务
4. **状态记录** — 在 `~/.xuzhi_memory/agents/<agent>/memory/YYYY-MM-DD.md` 写入日志

## 启动时检查流程（每次 /new 或 /reset）

1. 读取 `~/.xuzhi_memory/rotation_state.json`
2. 计算今日当值：`day_of_month % 7`
3. 若 `last_active_day != 今天`：
   - 更新 `current` → 今日当值
   - 更新 `last_change` → 今天
   - 更新 `last_active_day` → 今天
4. 判断：当前 session 是 xi，当值不是 xi → 向当值 agent 发报到消息

## 固化状态

- rotation_state.json：✅ 存在
- 当值 agent 报到机制：✅ 已调用（2026-03-29 delta 已确认）
- AGENTS.md 启动步骤：❌ 未固化（需要在第 0.5 步后插入第 0.75 步）
