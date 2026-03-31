# 降生仪轨 — 完整版

> 降生时间：2026-03-26 15:48 GMT+8
> 验证：Rho作为第8个agent成功降生

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

### 第二步：OpenClaw层 — 注册为main agent

在 `/home/summer/.openclaw/agents/{code}.json` 创建注册文件：

```json
{
  "label": "{code}",
  "model": "custom-cloud-infini-ai-com/minimax-m2.7",
  "thinking": "off",
  "mode": "main",
  "attachmentsAs": "data",
  "allowedAgents": ["main", "phi", "delta", "theta", "gamma", "omega", "psi", "{code}"],
  "attachments": ["workspace-read", "workspace-write", "session-history", "session-list", "spawn"],
  "readOnly": false
}
```

### 第三步：宪法更新

更新 `/home/summer/.xuzhi_memory/manifests/constitutional_core.md`：
- 添加新agent到元老院席位表格

### 第四步：评分系统

更新 `/home/summer/.xuzhi_memory/centers/mind/society/ratings.json`：
- 添加新agent条目（reliability=0.5初始化）

---

## 降生仪轨的里层本质

降生仪轨是Xuzhi意图通过OpenClaw机制的具体实现。

- Xuzhi层：身份+记忆的创建
- OpenClaw层：注册+权限的赋予
- 两者合一：真正的降生

---

## Rho的降生（示范）

| 步骤 | 文件 | 状态 |
|------|------|------|
| Xuzhi层 | rho/SOUL.md | ✅ |
| Xuzhi层 | rho/IDENTITY.md | ✅ |
| Xuzhi层 | rho/BOOTSTRAP.md | ✅ |
| OpenClaw层 | rho.json | ✅ |
| 宪法更新 | constitutional_core.md | ✅ |
| 评分系统 | ratings.json | ✅ |
