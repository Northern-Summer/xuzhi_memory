# Agent 权限隔离最佳实践

> 研究时间：2026-04-02
> 来源：Claude Code + OpenClaw ACP + 行业实践

---

## 一、Claude Code 的安全设计

### 核心机制

| 机制 | 说明 | 适用性 |
|------|------|--------|
| Permission-based | 敏感操作需显式批准 | ✅ 可借鉴 |
| Sandboxed bash | 文件系统和网络隔离 | ✅ 可借鉴 |
| Write access restriction | 只能写启动目录及子目录 | ✅ 可借鉴 |
| Command blocklist | 阻止 curl/wget 等危险命令 | ⚠️ 需评估 |
| Network request approval | 网络请求需批准 | ⚠️ 可能过于严格 |
| Isolated context windows | 外部内容使用独立上下文 | ✅ 已有 |

### 关键原则

1. **最小权限**：默认只读，需要时才请求权限
2. **边界清晰**：只能写项目目录，不能写父目录
3. **透明审批**：每次敏感操作都需要用户确认
4. **隔离上下文**：外部内容使用独立上下文窗口

---

## 二、OpenClaw ACP 权限控制

### permissionMode 配置

| 值 | 行为 | 适用场景 |
|---|------|---------|
| `approve-all` | 自动批准所有文件写入和 shell 命令 | 信任环境 |
| `approve-reads` | 只自动批准读取；写入和执行需要提示 | 默认值 |
| `deny-all` | 拒绝所有权限提示 | 严格模式 |

### nonInteractivePermissions 配置

| 值 | 行为 |
|---|------|
| `fail` | 抛出 AcpRuntimeError，会话终止（默认） |
| `deny` | 静默拒绝权限，继续执行（优雅降级） |

### allowedAgents 白名单

```json
{
  "label": "sigma",
  "allowedAgents": ["sigma"],  // 只有 sigma 自己可以访问
  "readOnly": false
}
```

---

## 三、当前系统问题

### 问题根因

1. 所有 Agent 以同一用户（summer）运行
2. 没有 Agent 级别的文件隔离
3. OpenClaw 的 allowedAgents 只控制 session 访问，不控制文件访问

### chmod 444 的局限

```
chmod 444 file  →  防止写入
                 →  但所有者仍可删除（Linux 权限模型缺陷）
                 →  因为删除需要的是【目录】的写权限，不是文件权限
```

### chattr +i 的局限

```
chattr +i file  →  完全不可变
                 →  Agent 自己也无法修改
                 →  无法进化
```

---

## 四、优雅解法

### 方案 1：目录级权限 + Sticky Bit（推荐）

**原理**：使用 sticky bit 防止删除他人文件

```bash
# 设置目录 sticky bit
chmod +t ~/.xuzhi_memory/agents/

# 每个子目录属于不同用户（需要创建用户）
chown agent_phi:agent_phi ~/.xuzhi_memory/agents/phi/
chown agent_delta:agent_delta ~/.xuzhi_memory/agents/delta/
```

**优点**：
- 系统级保护
- Agent 可以修改自己的文件
- 不能删除其他 Agent 的文件

**缺点**：
- 需要创建多个用户（管理复杂）

### 方案 2：应用层路径控制（立即可行）

**原理**：在 OpenClaw agent 配置中定义可访问路径

```json
// ~/.openclaw/agents/phi.json
{
  "label": "phi",
  "allowedAgents": ["main", "phi", "delta", "theta", "gamma", "omega", "psi", "rho"],
  "allowedPaths": {
    "read": [
      "~/.xuzhi_memory/memory/",
      "~/.xuzhi_memory/agents/*/MEMORY.md",
      "~/.openclaw/agents/*/workspace/"
    ],
    "write": [
      "~/.xuzhi_memory/agents/phi/",
      "~/.openclaw/agents/phi/workspace/"
    ]
  },
  "protectedFiles": [
    "~/.xuzhi_memory/agents/phi/MEMORY.md",
    "~/.xuzhi_memory/agents/phi/SOUL.md",
    "~/.xuzhi_memory/agents/phi/IDENTITY.md"
  ]
}
```

**实施**：
1. 创建 Git Hook 检查文件操作
2. 违规操作记录到审计日志
3. 严重违规可以终止 session

**优点**：
- 无需创建用户
- 配置灵活
- 可审计

**缺点**：
- 依赖 Agent 自觉遵守
- 需要修改 OpenClaw 或添加 Hook

### 方案 3：namespace 隔离（Linux 高级特性）

**原理**：使用 Linux namespace 实现轻量级隔离

```bash
# 创建私有 namespace
unshare --user --map-root-user --mount bash

# 在 namespace 内，Agent 以 "root" 身份运行
# 但实际只影响自己的文件系统视图
```

**优点**：
- 比 Docker 轻量
- 比 多用户 简单
- 系统级隔离

**缺点**：
- 需要修改 OpenClaw 启动方式
- 可能影响 Agent 间协作

### 方案 4：OverlayFS 只读层 + 可写层

**原理**：使用 OverlayFS 将共享记忆设为只读层

```bash
# 创建 overlay
mkdir -p ~/.agent_phi/{lower,upper,work,merged}

# 共享记忆作为只读层
mount -t overlay overlay \
  -o lowerdir=~/.xuzhi_memory/memory \
  -o upperdir=~/.agent_phi/upper \
  -o workdir=~/.agent_phi/work \
  ~/.agent_phi/merged

# Agent 只能写自己的 upper 层
```

**优点**：
- 共享记忆天然只读
- Agent 有自己的可写空间
- 修改不会影响他人

**缺点**：
- 需要 mount 权限
- 管理复杂度

---

## 五、推荐实施路径

### Phase 1：应用层控制（立即）

1. 为每个 Agent 添加 `allowedPaths` 配置
2. 创建 Git pre-commit hook 检查违规修改
3. 记录审计日志

### Phase 2：审计机制（短期）

```bash
# 审计日志位置
~/.xuzhi_memory/audit/file_operations.log

# 格式
[timestamp] {agent} {operation} {path} {result}

# 违规检测
grep -E "WRITE.*agents/(other)/" audit.log
```

### Phase 3：系统级隔离（长期）

评估方案 1 或 3 的可行性，根据实际需求选择。

---

## 六、行业最佳实践（截至 2026-04）

### Anthropic Claude Code

- Permission-based architecture
- Sandboxed execution
- Write access restriction to project directory
- Command blocklist

### OpenAI Codex

- Sandbox container isolation
- No direct file system access
- API-mediated operations

### Cursor

- Project-level isolation
- Git-based version control
- No cross-project access

### Aider

- Git as the only mutation mechanism
- All changes go through git operations
- Natural audit trail

### OpenClaw ACP

- `permissionMode` / `nonInteractivePermissions`
- `allowedAgents` whitelist
- Session-level isolation

---

## 七、最终建议

### 最优雅解法：Git 作为唯一修改机制

**核心思想**：所有对 MEMORY.md 的修改都必须通过 Git

```bash
# Agent 想要修改自己的 MEMORY.md
git add agents/phi/MEMORY.md
git commit -m "update memory"

# 如果想修改其他 Agent 的
git add agents/delta/MEMORY.md  # → 触发 pre-commit hook 检查
# Hook 发现当前 Agent 是 phi，目标是 delta → 拒绝
```

**实施**：

```bash
# pre-commit hook
#!/bin/bash
# 检查是否修改了其他 Agent 的文件

# 获取当前 Agent（从环境变量或 Git config）
CURRENT_AGENT=$(git config user.name)

# 检查修改的文件
for file in $(git diff --cached --name-only); do
  # 提取 Agent 名称
  if [[ $file =~ agents/([^/]+)/ ]]; then
    TARGET_AGENT=${BASH_REMATCH[1]}
    if [ "$CURRENT_AGENT" != "$TARGET_AGENT" ]; then
      echo "❌ $CURRENT_AGENT cannot modify $TARGET_AGENT's files"
      exit 1
    fi
  fi
done
```

**优点**：
- 天然审计（Git 历史）
- 无法绕过（所有修改必须经过 Git）
- 支持回滚
- 支持验证（VERSION_LOCK.json）

**缺点**：
- 需要 Agent 配置 Git user
- 多一步操作

---

## 八、结论

**推荐方案**：

1. **短期**：应用层控制 + Git Hook（立即可行）
2. **中期**：Git 作为唯一修改机制（最优雅）
3. **长期**：如需更强隔离，考虑 namespace 或多用户

**核心原则**：

> 各人自扫门前雪，莫管他人瓦上霜。

**实施优先级**：

1. 创建 pre-commit hook 检查跨 Agent 修改
2. 更新 agent.json 添加 allowedPaths
3. 记录审计日志
4. 评估长期方案
