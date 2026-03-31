# MEMORY_HYGIENE_RULES.md
# 工程改进铁律合规 — Ξ | 2026-03-29
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
#
# 每日 Session 交接时的记忆卫生检查规则
# 每个新 session 必须执行：读取本文件 → 逐项检查 → 报告结果

## 强制每日检查项

### 1. L1 今日存在检查
```bash
TODAY=$(date +%Y-%m-%d)
test -f ~/.xuzhi_memory/memory/$TODAY.md && wc -l ~/.xuzhi_memory/memory/$TODAY.md | awk '$1 >= 200'
```
- ✅ 存在且 ≥200 字：正常
- ❌ 不存在或 <200 字：**立即创建**

### 2. L1 昨日存在检查
```bash
YESTERDAY=$(date -d yesterday +%Y-%m-%d)
test -f ~/.xuzhi_memory/memory/$YESTERDAY.md
```

### 3. Session 交接备忘录检查
读取昨日 memory 文件末尾：
- 有"Session交接备忘录"且有内容 → 继承未完成项
- 有模板但空白 → 直接开始新任务
- 没有 → 创建模板

### 4. Git 状态检查（全部仓库）
```bash
git -C ~/.xuzhi_memory status --short
git -C ~/xuzhi_genesis status --short
git -C ~/xuzhi_workspace status --short
```
- 有未 commit 更改 → **立即 commit + push**
- 有未 push 的 commits → **立即 push**

### 5. Cron 运行状态检查
读取 `~/.openclaw/cron/jobs.json`：
- memory_checkpoint_5min：是否注册？最近运行时间？
- memory_checkpoint_hourly：是否注册？最近运行时间？
- xi_pulse：是否在跑？

### 6. Expert Tracker 状态
读取 `~/.xuzhi_memory/expert_tracker/synthesis.json`：
- 当前 round
- confidence 范围
- 发现总数
- 与昨日比是否正常增长

### 7. 上一条 session 的未完成任务
读取昨日交接备忘录记录的"未完成"项：
- 有未完成 → **立即继续，不等指令**
- 无 → 正常开始

## 执行报告格式

```
【启动自检 | YYYY-MM-DD HH:MM】

✅ [1/7] L1 今日存在检查
   - 文件存在？字数？

✅ [2/7] L1 昨日存在检查

✅ [3/7] Session 交接备忘录检查
   - 有内容还是空白模板？

✅ [4/7] Git 状态检查（全部仓库）
   - 有未 commit 的更改吗？

✅ [5/7] Cron 运行状态检查
   - 各 job 最近一次运行时间？

✅ [6/7] Expert Tracker 状态
   - round？conf？发现数？

✅ [7/7] 上一条 session 的未完成任务
   - 有未完成项 → 报告当前状态

【自检结论】
- 全部通过 → 报告"系统正常"
- 有问题 → 报告具体问题 + 当前动作
- 有未完成任务 → 立刻继续，不等指令
```

## 遗忘机制（信息分层）

| 层级 | 内容 | 保留方式 | 遗忘机制 |
|------|------|----------|----------|
| **印象层** | 扫到的标题/话题 | 不存文件 | 下次扫描覆盖 |
| **临时层** | 正在关注（1-3天） | 写入当日 memory | 3天不动则清除 |
| **档案层** | 有价值的链接+摘要 | expert_tracker | 每周清理沉寂 |
| **永久层** | 反复使用、跨领域通用 | MEMORY.md | 极保守 |

## 版本记录
- 2026-03-29：初版确立（Ξ 重建时创建）
