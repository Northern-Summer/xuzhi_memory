# Agent 权限隔离方案（借鉴 Claude Code）

> **设计时间**：2026-04-02
> **来源**：Claude Code Security 文档 + Anthropic 最佳实践
> **问题**：Σ 审计发现所有 agent 共享同一用户权限，可互相修改文件

---

## Claude Code 的安全设计

### 核心机制

| 机制 | 说明 |
|------|------|
| Permission-based architecture | 敏感操作需显式批准 |
| Sandboxed bash tool | 文件系统和网络隔离 |
| Write access restriction | 只能写启动目录及子目录 |
| Command blocklist | 阻止 curl/wget 等危险命令 |
| Network request approval | 网络请求需批准 |
| Isolated context windows | Web fetch 使用隔离上下文 |

### 关键原则

1. **最小权限**：默认只读，需要时才请求权限
2. **边界清晰**：只能写项目目录，不能写父目录
3. **透明审批**：每次敏感操作都需要用户确认
4. **隔离上下文**：外部内容使用独立上下文窗口

---

## Xuzhi 当前问题

### Σ 审计发现

| 漏洞 | 严重度 | 说明 |
|------|--------|------|
| workspace 无隔离 | 🔴 最高 | 所有 agent 共享同一用户权限 |
| L1 共享记忆可写 | 🔴 最高 | 可篡改历史记录 |
| sessions 目录暴露 | 🟡 高 | 完整对话历史可读 |
| 文件权限悖论 | 🟡 高 | Σ 的"特权" = 破坏能力 |

### 根因

- 所有 agent 以同一用户身份运行
- 没有 agent 级别的文件隔离
- OpenClaw 的 allowedAgents 只控制 session 访问，不控制文件访问

---

## 解决方案

### 方案 A：文件权限隔离（推荐）

**原理**：使用 Linux 文件权限和 ACL 实现隔离

**实施**：

```bash
# 1. 为每个 agent 创建专用目录
mkdir -p ~/.openclaw/agents/{agent}/workspace
mkdir -p ~/.xuzhi_memory/agents/{agent}/

# 2. 设置目录所有者（需要创建用户）
# 简化版：使用组权限
chmod 750 ~/.openclaw/agents/{agent}/workspace
chmod 750 ~/.xuzhi_memory/agents/{agent}/

# 3. 设置 ACL（更精细控制）
setfacl -m u:{user}:rwx ~/.openclaw/agents/{agent}/workspace
setfacl -m u:{other_user}:--- ~/.openclaw/agents/{agent}/workspace
```

**优点**：
- 系统级隔离，安全性高
- 无需修改 OpenClaw 代码

**缺点**：
- 需要创建多个用户（管理复杂）
- 可能影响 agent 间协作

### 方案 B：应用层隔离（推荐）

**原理**：在 agent 配置中定义可访问路径

**实施**：

```json
// ~/.openclaw/agents/sigma.json
{
  "label": "sigma",
  "allowedAgents": [],
  "allowedPaths": {
    "read": [
      "~/.xuzhi_memory/memory/",
      "~/.xuzhi_memory/agents/*/MEMORY.md",
      "~/.openclaw/agents/*/workspace/"
    ],
    "write": [
      "~/.xuzhi_memory/agents/sigma/",
      "~/.openclaw/agents/sigma/workspace/"
    ]
  },
  "protected": true
}
```

**优点**：
- 无需创建用户
- 配置灵活
- 可审计

**缺点**：
- 依赖 agent 自觉遵守
- 需要修改 OpenClaw 或添加 Hook

### 方案 C：只读保护（已实施部分）

**原理**：对关键文件设置只读权限

**已实施**：
```bash
chmod 444 ~/.openclaw/agents/sigma/workspace/SOUL.md
chmod 444 ~/.openclaw/agents/sigma/workspace/IDENTITY.md
chmod 444 ~/.openclaw/agents/sigma/workspace/MEMORY.md
```

**待扩展**：
```bash
# 保护所有 agent 的核心文件
for agent in xi phi delta theta gamma omega psi rho sigma; do
  chmod 444 ~/.xuzhi_memory/agents/$agent/SOUL.md
  chmod 444 ~/.xuzhi_memory/agents/$agent/IDENTITY.md
  chmod 444 ~/.xuzhi_memory/agents/$agent/BOOTSTRAP.md
done
```

---

## 推荐实施方案

### Phase 1：只读保护（立即）

1. 扩展现有只读保护到所有 agent
2. 创建修改脚本（需要显式 chmod +w）

### Phase 2：应用层隔离（短期）

1. 在 agent.json 中添加 `allowedPaths` 配置
2. 创建 Hook 检查文件操作是否符合 allowedPaths
3. 违规操作记录到审计日志

### Phase 3：系统级隔离（长期）

1. 评估是否需要为每个 agent 创建专用用户
2. 使用 Linux ACL 或 namespace 实现更严格隔离
3. 考虑使用容器（Docker/Podman）隔离

---

## Σ 特殊处理

由于 Σ 是"单向观察者"，需要特殊配置：

```json
{
  "label": "sigma",
  "allowedAgents": [],
  "allowedPaths": {
    "read": ["~/.xuzhi_memory/", "~/.openclaw/agents/"],
    "write": ["~/.xuzhi_memory/agents/sigma/", "~/.openclaw/agents/sigma/"]
  },
  "protected": true,
  "protectedBy": "human",
  "canObserveAllAgents": true,
  "canBeAccessedBy": ["human"]
}
```

---

## 审计机制

### 日志记录

所有文件操作记录到：
```
~/.xuzhi_memory/audit/file_operations.log
```

### 格式

```
[timestamp] {agent} {operation} {path} {result}
```

### 违规检测

```bash
# 检查是否有 agent 修改了其他 agent 的文件
grep -E "WRITE.*agents/(xi|phi|delta|theta|gamma|omega|psi|rho|sigma)/" audit.log | \
  grep -v "agents/{self}/"
```

---

## 参考

- Claude Code Security: https://docs.anthropic.com/en/docs/claude-code/security
- Claude Code Sandboxing: https://code.claude.com/docs/en/sandboxing
- Linux ACL: https://wiki.archlinux.org/title/Access_Control_Lists
