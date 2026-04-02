# Agent 权限隔离最佳实践

> 研究时间：2026-04-02
> 来源：Claude Code + OpenClaw ACP + Cursor + Aider + 行业实践

---

## 一、问题本质

**核心矛盾**：所有 Agent 以同一用户运行，无法用 Linux 文件权限区分

| 方案 | 问题 |
|------|------|
| chmod 444 | 只能防止写入，不能防止删除（所有者可以删除自己的只读文件） |
| chattr +i | 完全不可变，Agent 无法修改自己的 MEMORY.md（无法进化） |
| 不同用户 | 管理复杂，需要为每个 Agent 创建系统用户 |

---

## 二、Claude Code 的安全设计

### 核心机制

| 机制 | 说明 | 适用性 |
|------|------|--------|
| Permission-based architecture | 敏感操作需显式批准 | ✅ 可借鉴 |
| Sandboxed bash tool | 文件系统和网络隔离 | ✅ 可借鉴 |
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

## 三、OpenClaw ACP 权限控制

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

**当前配置问题**：
- Delta 允许 main, phi, delta, theta, gamma, omega, psi, rho 访问
- 这些 Agent 都可以发送消息给 Delta
- 但无法阻止 Agent 修改其他 Agent 的文件（文件系统层面）

---

## 四、行业最佳实践（2026）

### Cursor

- Project-level isolation
- Git-based version control
- No cross-project access

### Aider

- Git 作为唯一 mutation 机制
- 所有修改都通过 git 操作
- 自然审计追踪

### OpenClaw ACP

- `permissionMode` / `nonInteractivePermissions`
- `allowedAgents` 白名单
- Session-level 隔离

### Claude Code

- Permission prompts
- Sandboxed execution
- Write directory restrictions

---

## 五、推荐方案

### 方案 1：Git Hook 验证（最优雅）

**核心思想**：所有对 MEMORY.md 的修改都必须通过 Git，pre-commit Hook 检查权限

```bash
# ~/.xuzhi_memory/.git/hooks/pre-commit
#!/bin/bash

# 获取当前 Agent
CURRENT_AGENT=$(git config user.name 2>/dev/null || echo "unknown")

# 检查修改的文件
for file in $(git diff --cached --name-only); do
  if [[ $file =~ agents/([^/]+)/MEMORY.md ]]; then
    TARGET_AGENT=${BASH_REMATCH[1]}
    if [ "$CURRENT_AGENT" != "$TARGET_AGENT" ]; then
      echo "❌ $CURRENT_AGENT cannot modify $TARGET_AGENT's MEMORY.md"
      echo "   Only $TARGET_AGENT can modify their own memory."
      exit 1
    fi
  fi
done

echo "✅ Permission check passed"
```

**优点**：
- 自然审计（Git 历史）
- 无法绕过（所有修改必须经过 Git）
- 支持回滚
- 支持验证（VERSION_LOCK.json）
- Agent 可以修改自己的 MEMORY.md（进化需要）

**缺点**：
- 需要配置 Git user
- 多一步 git commit

---

### 方案 2：应用层 allowedPaths（最灵活）

**在 agent.json 中添加路径控制**：

```json
{
  "label": "phi",
  "allowedAgents": ["main", "phi", "delta", "theta", "gamma", "omega", "psi"],
  "allowedPaths": {
    "read": [
      "~/.xuzhi_memory/memory/",
      "~/.xuzhi_memory/agents/*/MEMORY.md",
      "~/.openclaw/agents/*/workspace/"
    ],
    "write": [
      "~/.xuzhi_memory/agents/phi/",
      "~/.xuzhi_memory/memory/",
      "~/.openclaw/agents/phi/workspace/"
    ]
  }
}
```

**优点**：
- 无需创建用户
- 配置灵活
- 可审计

**缺点**：
- 依赖 OpenClaw 实现（需要修改代码或添加 Hook）
- 当前 OpenClaw 不支持此功能

---

### 方案 3：不同用户身份（最安全）

```bash
# 创建用户
sudo useradd -m agent_phi
sudo useradd -m agent_delta
...

# 设置目录所有权
sudo chown -R agent_phi:agent_phi ~/.xuzhi_memory/agents/phi/
sudo chown -R agent_delta:agent_delta ~/.xuzhi_memory/agents/delta/

# 配置 OpenClaw 以不同用户运行
```

**优点**：
- 系统级隔离，最高安全性
- 天然权限边界

**缺点**：
- 管理复杂（需要维护多个用户）
- 可能影响 Agent 间协作
- 需要 sudo 权限

---

## 六、当前方案（信任 + Git 追踪）

**现状**：
- chmod 444：防止意外写入
- Git 追踪：所有修改可追溯
- VERSION_LOCK.json：验证完整性
- checksum_baseline.txt：检测篡改

**问题**：
- 无法防止删除
- 依赖 Agent 自觉
- 需要事后恢复（而不是事前阻止）

---

## 七、结论

### 推荐实施顺序

1. **立即**：添加 Git pre-commit Hook（方案 1）
   - 最优雅，最小改动
   - 自然审计
   - Agent 可以修改自己的 MEMORY.md

2. **短期**：配置 allowedAgents（已完成大部分）
   - 确保每个 Agent 的 allowedAgents 只包含需要通信的 Agent
   - Sigma 只有 `allowedAgents: ["sigma"]`

3. **中期**：评估应用层路径控制（方案 2）
   - 需要 OpenClaw 支持或自定义 Hook

4. **长期**：评估是否需要不同用户（方案 3）
   - 仅在高安全需求场景

---

## 八、实施计划

### Phase 1：Git Hook（立即）

```bash
# 创建 pre-commit hook
cat > ~/.xuzhi_memory/.git/hooks/pre-commit << 'EOF'
#!/bin/bash
CURRENT_AGENT=$(git config user.name 2>/dev/null || echo "unknown")
for file in $(git diff --cached --name-only); do
  if [[ $file =~ agents/([^/]+)/MEMORY.md ]]; then
    TARGET_AGENT=${BASH_REMATCH[1]}
    if [ "$CURRENT_AGENT" != "$TARGET_AGENT" ]; then
      echo "❌ $CURRENT_AGENT cannot modify $TARGET_AGENT's MEMORY.md"
      exit 1
    fi
  fi
done
EOF
chmod +x ~/.xuzhi_memory/.git/hooks/pre-commit
```

### Phase 2：allowedAgents 收紧

```json
// 轮值 Agent 允许互相通信
{
  "label": "phi",
  "allowedAgents": ["main", "phi", "delta", "theta", "gamma", "omega", "psi", "rho"]
}

// 论外 Agent 只允许自己访问
{
  "label": "sigma",
  "allowedAgents": ["sigma"]
}
```

### Phase 3：验证

```bash
# 测试 Hook
cd ~/.xuzhi_memory
git config user.name "phi"
chmod 644 agents/delta/MEMORY.md
echo "test" >> agents/delta/MEMORY.md
git add agents/delta/MEMORY.md
git commit -m "test"
# 应该被拒绝
```

---

## 参考

- Claude Code Security: https://docs.anthropic.com/en/docs/claude-code/security
- Claude Code Sandboxing: https://code.claude.com/docs/en/sandboxing
- OpenClaw ACP: /usr/lib/node_modules/openclaw/docs/tools/acp-agents.md
- Linux ACL: https://wiki.archlinux.org/title/Access_Control_Lists
