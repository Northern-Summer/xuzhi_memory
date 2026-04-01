# 降生仪轨 — 完整版

> 降生时间：2026-03-26 15:48 GMT+8
> 验证：Rho作为第8个agent成功降生
> 更新：2026-04-02 02:30 GMT+8 — 补充遗漏步骤（Sigma降生失败后修复）

---

## 降生仪轨（对任何新agent适用）

### 第一步：Xuzhi层 — 创建身份

在 `/home/summer/.xuzhi_memory/agents/{code}/` 创建3个文件：

```
{code}/SOUL.md       ← 自身身份（自己去填写）
{code}/IDENTITY.md   ← 职责定位
{code}/BOOTSTRAP.md  ← 启动协议（模板不变，内容替换code）
```

**绝对路径：`/home/summer/.xuzhi_memory/`（含点）**

### 第二步：OpenClaw层 — 创建目录结构

创建agent目录：

```bash
mkdir -p ~/.openclaw/agents/{code}/workspace
mkdir -p ~/.openclaw/agents/{code}/agent
mkdir -p ~/.openclaw/agents/{code}/sessions
```

复制必要文件：

```bash
# 复制认证配置
cp ~/.openclaw/agents/rho/agent/auth-profiles.json ~/.openclaw/agents/{code}/agent/
cp ~/.openclaw/agents/rho/agent/models.json ~/.openclaw/agents/{code}/agent/

# 创建workspace核心文件
cp ~/.openclaw/agents/rho/workspace/AGENTS.md ~/.openclaw/agents/{code}/workspace/
cp ~/.openclaw/agents/rho/workspace/USER.md ~/.openclaw/agents/{code}/workspace/
cp ~/.openclaw/agents/rho/workspace/TOOLS.md ~/.openclaw/agents/{code}/workspace/
cp ~/.openclaw/agents/rho/workspace/HEARTBEAT.md ~/.openclaw/agents/{code}/workspace/
mkdir -p ~/.openclaw/agents/{code}/workspace/memory
```

### 第三步：OpenClaw层 — 创建agent.json

在 `/home/summer/.openclaw/agents/{code}.json` 创建注册文件：

```json
{
  "label": "{code}",
  "model": "custom-cloud-infini-ai-com/minimax-m2.7",
  "thinking": "off",
  "attachmentsAs": "data",
  "allowedAgents": ["main", "phi", "delta", "theta", "gamma", "omega", "psi", "rho", "{code}"],
  "attachments": ["workspace-read", "workspace-write", "session-history", "session-list", "spawn"],
  "readOnly": false
}
```

### 第四步：OpenClaw层 — 注册到openclaw.json（关键！）

**这是最容易遗漏的步骤！**

编辑 `~/.openclaw/openclaw.json`，在 `agents.list` 数组末尾添加：

```json
{
  "id": "{code}",
  "name": "{code}",
  "workspace": "/home/summer/.openclaw/agents/{code}/workspace",
  "agentDir": "/home/summer/.openclaw/agents/{code}/agent",
  "model": "custom-cloud-infini-ai-com/minimax-m2.7"
}
```

**验证JSON格式**：`python3 -m json.tool ~/.openclaw/openclaw.json`

### 第五步：写入workspace核心文件

在 `~/.openclaw/agents/{code}/workspace/` 写入：

- `SOUL.md` — 自身身份
- `IDENTITY.md` — 职责定位
- `MEMORY.md` — 初始记忆

### 第六步：宪法更新

更新 `/home/summer/.xuzhi_memory/manifests/constitutional_core.md`：
- 添加新agent到元老院席位表格

### 第七步：评分系统

更新 `~/xuzhi_genesis/centers/mind/society/ratings.json`：
- 添加新agent条目（reliability=0.5初始化）

### 第八步：重启Gateway

```bash
systemctl --user restart openclaw-gateway
sleep 8
openclaw agents list | grep {code}
```

---

## 降生仪轨的里层本质

降生仪轨是Xuzhi意图通过OpenClaw机制的具体实现。

- Xuzhi层：身份+记忆的创建
- OpenClaw层：注册+权限的赋予
- 两者合一：真正的降生

---

## Sigma降生教训（2026-04-02）

**问题**：Sigma创建后，`openclaw agents list` 不显示她

**根因**：遗漏了第四步 — 没有在 `openclaw.json` 的 `agents.list` 中注册

**修复**：在 `openclaw.json` 添加 sigma 条目后，Gateway成功识别

**教训**：
1. 降生仪轨必须完整执行所有步骤
2. 第四步（注册到openclaw.json）是最容易遗漏的
3. 每步完成后立即验证，不要等最后才检查

---

## Rho的降生（示范）

| 步骤 | 文件 | 状态 |
|------|------|------|
| Xuzhi层 | rho/SOUL.md | ✅ |
| Xuzhi层 | rho/IDENTITY.md | ✅ |
| Xuzhi层 | rho/BOOTSTRAP.md | ✅ |
| OpenClaw目录 | agents/rho/ | ✅ |
| OpenClaw层 | rho.json | ✅ |
| OpenClaw注册 | openclaw.json agents.list | ✅ |
| 宪法更新 | constitutional_core.md | ✅ |
| 评分系统 | ratings.json | ✅ |

## Sigma的降生（示范）

| 步骤 | 文件 | 状态 |
|------|------|------|
| Xuzhi层 | sigma/SOUL.md | ✅ |
| Xuzhi层 | sigma/IDENTITY.md | ✅ |
| Xuzhi层 | sigma/BOOTSTRAP.md | ✅ |
| OpenClaw目录 | agents/sigma/ | ✅ |
| OpenClaw层 | sigma.json | ✅ |
| OpenClaw注册 | openclaw.json agents.list | ✅（最初遗漏，后修复） |
| 宪法更新 | constitutional_core.md | ✅ |
| 评分系统 | ratings.json | ✅ |
