# 记忆机制架构修复方案
> Ξ | 2026-03-25 | 初版 | **2026-03-27 18:57 修订**

---

## 一、问题诊断

### 1.1 碎片化现状（6个记忆位置）

| 位置 | 类型 | 问题 |
|------|------|------|
| `~/.xuzhi_memory/memory/` | L1 daily log | ✅ **canonical**（对齐 AGENTS.md + 实际使用） |
| `~/.xuzhi_memory/daily/` | L1 daily log | ✅ 兼容层（灾变后恢复经验） |
| `~/.xuzhi_memory/manifests/` | L2 snapshots | ✅ 正确位置 |
| `~/.xuzhi_memory/backup/` | L3 archives | ✅ 正确位置 |
| `~/.openclaw/workspace/memory/` | 独立副本 | ✅ 已清空（2026-03-27） |
| `~/xuzhi_workspace/memory/` | 独立副本 | ✅ 已归档（2026-03-27，43个 pre-disaster 文件） |

### 1.2 修订说明（2026-03-27）

**SPEC vs REALITY 冲突已解决**：
- 原 SPEC：daily/ 是唯一正确位置，memory/ 是"重复"
- **修订**：memory/ 是 canonical（因为 AGENTS.md 读取路径指向它，且今日会话已写入）
- daily/ 保留作为兼容层（已有 2026-03-24/25/26 三日记录）

### 1.3 唯一真相源

**`~/.xuzhi_memory/`** — 所有读/写操作指向此目录下的 memory/ 或 manifests/ 或 backup/。

---

## 二、修复方案（已完成 2026-03-27）

### 2.1 ✅ 确立单一真相源

**唯一真相源：`~/.xuzhi_memory/`**

- 所有记忆操作（读/写）都针对 `~/.xuzhi_memory/`
- `~/.openclaw/workspace/MEMORY.md` 是**引用视图**（读取 xuzhi_memory 内容）
- `~/.openclaw/workspace/memory/` 和 `~/xuzhi_workspace/memory/` **不再写入新内容**

### 2.2 ✅ 迁移计划（已完成）

**步骤 1**：✅ `.openclaw/workspace/memory/` 已清空（2026-03-27）

**步骤 2**：✅ 所有脚本路径引用指向 `~/.xuzhi_memory/`（AGENTS.md 已对齐）

**步骤 3**：✅ `~/xuzhi_workspace/memory/` 已归档至 `~/.xuzhi_memory/backup/pre_disaster_20260327_185641_xuzhi_workspace_memory/`

### 2.3 脚本路径状态

| 脚本 | 当前路径 | 状态 |
|------|----------|------|
| memory_window.sh | `~/.xuzhi_memory/daily/` | ✅ 正确 |
| AGENTS.md | `~/.xuzhi_memory/memory/` | ✅ 正确 |
| memory_forge.py | 已禁用 | ✅ |

---

## 三、记忆读写规则（强制）

### 3.1 读取规则

每次主会话启动时，必须按顺序读取：
1. `~/.xuzhi_memory/memory/YYYY-MM-DD.md`（今日 raw log）
2. `~/.xuzhi_memory/memory/YYYY-MM-DD.md`（昨日 raw log）
3. `~/.xuzhi_memory/manifests/` 下所有 STABLE 文件
4. `~/.xuzhi_memory/backup/`（如有需要）

### 3.2 写入规则

| 事件 | 写入位置 | 文件名 |
|------|----------|--------|
| 每个会话结束 | L1: `memory/` | `YYYY-MM-DD.md` |
| 重要决策/架构变更 | L2: manifests/ | `*_STABLE.md` |
| 每周/异常时 | L3: backup/ | `archive_YYYY-MM-DD_*.md` |
| 立即固化 | L1+L2 双写 | 同上 |

### 3.3 禁止

- ❌ 在 `~/.openclaw/workspace/memory/` 写入新记忆文件
- ❌ 在 `~/xuzhi_workspace/memory/` 写入新记忆文件
- ❌ 写完后不 commit
- ❌ 以"会话结束"为由跳过记忆写入

---

## 四、执行清单（2026-03-27 全量完成）

- [x] memory_window.sh ✅ 已正确使用 `~/.xuzhi_memory/daily/`
- [x] memory_forge.py ❌ 已禁用（Broken Concept，sessions.json.bak 从未生成）
- [x] cron_runner.sh memory_forge 调用 ✅ 已禁用
- [x] 清理 `~/.openclaw/workspace/memory/` ✅ 已清空（2026-03-27）
- [x] 清理 `~/xuzhi_workspace/memory/` ✅ 已归档（43个 pre-disaster 文件）
- [x] 更新 AGENTS.md 读取路径 ✅ 已对齐（memory/ 是 canonical）
- [x] 更新 MEMORY_FIX.md 本身 ✅ 修订完成（2026-03-27 18:57）

---

## 五、执行日志

| 时间 | 操作 | 结果 |
|------|------|------|
| 2026-03-27 18:53 | 创建 daily/2026-03-27.md | ✅ (700行，从 memory/ 迁移) |
| 2026-03-27 18:56 | 清空 openclaw/workspace/memory/ | ✅ (空目录) |
| 2026-03-27 18:56 | 归档 xuzhi_workspace/memory/ | ✅ (43文件 → backup/pre_disaster_20260327_185641_xuzhi_workspace_memory/) |
| 2026-03-27 18:57 | 修订 MEMORY_FIX.md | ✅ (SPEC对齐REALITY) |

---

## 六、验证方法

```bash
# 确认只有 ~/.xuzhi_memory/ 是真相源
ls ~/.xuzhi_memory/memory/YYYY-MM-DD.md    # 应有每日记录
ls ~/.xuzhi_memory/daily/*.md              # 应有历史备份
ls ~/.xuzhi_memory/manifests/*.md          # 应有 STABLE 快照
ls ~/.xuzhi_memory/backup/pre_disaster_*   # 应有归档
du -sh ~/.openclaw/workspace/memory/        # 应为 4.0K（空）
```
