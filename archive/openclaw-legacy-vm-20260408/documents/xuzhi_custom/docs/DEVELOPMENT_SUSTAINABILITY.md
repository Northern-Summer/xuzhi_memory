# 开发可持续性规范 v1.0

> **目的**：确保每次开发都为后续开发带来便利，而非破坏
> **创建时间**：2026-04-01
> **创建者**：Ξ

---

## 核心原则

### 1. 分离原则

**官方层** vs **自定义层** 必须严格分离：

| 层级 | 路径 | 内容 | 升级影响 |
|------|------|------|----------|
| 官方层 | `/usr/lib/node_modules/openclaw/` | OpenClaw 核心 | npm update 会覆盖 |
| 用户配置层 | `~/.openclaw/` | 用户配置、hooks | npm update 不会覆盖 |
| 自定义层 | `~/.xuzhi_custom/` | 自定义脚本、文档 | 完全独立 |
| 记忆层 | `~/.xuzhi_memory/` | 所有记忆数据 | 完全独立 |

**结论**：
- 自定义代码放在 `~/.xuzhi_custom/` 或 `~/.openclaw/hooks/`
- 永远不要修改 `/usr/lib/node_modules/openclaw/` 内的文件

### 2. 备份原则

**每次重大操作前必须备份**：

```bash
# 升级前
~/.openclaw/workspace/upgrade-protection.sh backup

# 升级后
npm update -g openclaw

# 恢复
~/.openclaw/workspace/upgrade-protection.sh restore

# 验证
~/.openclaw/workspace/upgrade-protection.sh verify
```

### 3. 文档原则

**每个功能必须有文档**：

| 功能类型 | 文档位置 |
|----------|----------|
| 系统架构 | `MEMORY.md` |
| 启动规程 | `AGENTS.md` |
| 工具使用 | `TOOLS.md` |
| Hook | `HOOK.md`（每个 Hook 目录内） |
| 开发规范 | `~/.xuzhi_custom/docs/` |

---

## 当前系统状态（2026-04-01）

### 已实现的保护机制

1. ✅ **Symlink 隔离**
   - `~/.openclaw/workspace/MEMORY.md` → `~/.xuzhi_memory/agents/xi/MEMORY.md`
   - `~/.openclaw/workspace/AGENTS.md` → `~/.xuzhi_memory/agents/xi/AGENTS.md`
   - 升级不会影响 symlink 指向的内容

2. ✅ **Hook 系统**
   - `~/.openclaw/hooks/` 存放自定义 Hook
   - 升级不会覆盖（managed hooks 目录）

3. ✅ **记忆系统**
   - `~/.xuzhi_memory/` 独立于 OpenClaw 安装目录
   - 升级完全不影响记忆数据

4. ✅ **断点文件**
   - `SESSION_BREAKPOINT.md` 自动维护
   - 确保任意断点可恢复

### 待完善项

1. 🟡 **~/.xuzhi_custom/** 刚创建，待充实
2. 🟡 **AI4S Weekly cron** 有 error，待修复
3. 🟡 **Hook 触发验证** 待测试

---

## 升级检查清单

**每次 npm update -g openclaw 前必须执行**：

```
[ ] 1. 运行 upgrade-protection.sh backup
[ ] 2. Git commit 所有未提交更改
[ ] 3. Git push 到远程
[ ] 4. npm update -g openclaw
[ ] 5. 运行 upgrade-protection.sh restore
[ ] 6. 运行 upgrade-protection.sh verify
[ ] 7. 测试 /new 触发 Hook
[ ] 8. 检查记忆系统正常
```

---

## 未来开发指南

### 添加新功能时

1. **代码放哪里？**
   - Hook → `~/.openclaw/hooks/<hook-name>/`
   - 脚本 → `~/.xuzhi_custom/scripts/`
   - 文档 → `~/.xuzhi_custom/docs/`

2. **如何确保不破坏现有功能？**
   - 新增文件，不修改现有文件（除非必要）
   - 使用 symlink 而非复制
   - 写文档说明依赖关系

3. **如何确保可回滚？**
   - Git commit 前 review 变更
   - 保留 upgrade-protection.sh 备份

### 修改现有功能时

1. **先读取现有文件**
2. **备份后再修改**
3. **测试后才能 commit**
4. **更新相关文档**

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-01 | 初始创建 |
