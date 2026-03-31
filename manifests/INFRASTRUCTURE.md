# INFRASTRUCTURE.md — 基础设施状态

> **强制等级：每个agent Session Startup必须读取**
> **最后更新：2026-03-30 03:55 | Δ**

---

## GitHub

### 账号
- **用户名**: Northern-Summer
- **组织**: 无（个人账号）
- **主要仓库**:
  - `xuzhi_genesis` — Xuzhi系统核心
  - `xuzhi_memory` — 记忆系统（L1-L3）
  - `xuzhi_workspace` — OpenClaw workspace

### Token 状态
- **当前PAT**: `ghp_68Off...`（存于 `~/.git-credentials`）
- **认证方式**: HTTPS + token（SSH key 对 GitHub 无效）
- **上次验证**: 2026-03-29，push 成功

### 已知问题
- 旧 token `ghp_t0Ib...` 已失效（2026-03-29）
- GH013 Push Protection 曾阻止含旧 token 的 commit（已 Dismiss）

### SSH Key
- **路径**: `~/.ssh/xuzhi_github`
- **状态**: 存在但 GitHub 不接受（Permission denied）
- **结论**: GitHub 操作统一用 HTTPS + PAT

---

## Lean Zulip

### 状态
- **注册**: ✅ 已完成 (Summer North)
- **邮箱**: MzgyMzMzMjk@163.com
- **API Key**: 已配置（存于 Δ 的任务配置）
- **链接**: https://leanprover.zulipchat.com

### 监控任务 (Δ 负责)
- **负责人**: Δ (Delta-Forge)
- **监控范围**: 
  - #new members
  - #maths
  - #Research on ML and Lean
  - #general
  - #mathlib4
- **频率**: 每6小时
- **数据存储**: `~/.xuzhi_memory/agents/delta/community_observations/`
- **工具路径**: `~/.openclaw/workspace/skills/zulip_monitor.py`

### 社区参与策略
- **Phase 1** (当前-4月底): 静默观察，收集数据
- **Phase 2** (5月): 轻度参与，技术回复
- **Phase 3** (6月+): 自然引入研究话题

---

## ETP GitHub 监控 (Δ 负责)

### 监控对象
- **仓库**: teorth/equational_theories
- **范围**: Issues, PRs, Discussions
- **频率**: 每12小时
- **工具路径**: `~/.openclaw/workspace/skills/github_etp_monitor.py`

---

## MathOverflow 监控 (Δ 负责)

### 监控标签
- [lean], [formalization], [proof-assistants]
- **频率**: 每日
- **工具路径**: `~/.openclaw/workspace/skills/mathoverflow_monitor.py`

---

## Discord

### Bot 配置
- **Bot 名称**: Xuzhi-Multiagents
- **Server ID**: `1486688995974058024`
- **User ID**: `1486687705042780181`
- **Channel ID**: `1486694791738691604`

### Token 状态
- **位置**: `~/.openclaw/openclaw.json`
- **状态**: ⚠️ 已暴露，需要 reset（见 TOKEN_SECURITY.md）
- **代理**: `http://127.0.0.1:7897`（Clash）

### 连接状态
- **上次成功**: 2026-03-30 01:40
- **问题**: SSL 证书（Clash MITM），需配置 proxy

---

## WeChat

### Channel 状态
- **Channel ID**: `openclaw-weixin`
- **状态**: 在线（通过 OpenClaw WebChat）
- **推送验证**: ✅ 成功（2026-03-30 02:57）

---

## API 订阅

### InfiniAI
- **套餐**: Coding Pro ¥200/月
- **额度**: 60k POST (DeepSeek-V3.2 / GLM-4.7)
- **Token 位置**: `~/.openclaw/openclaw.json`
- **评估**: 此价格已是国内较优方案（2026-03-29）

### OpenRouter
- **状态**: ❓ 待确认
- **位置**: `~/.openclaw/agents/*/agent/models.json`

---

## bb-browser

### 状态
- **版本**: 0.10.1
- **Chrome**: Headless，systemd 服务 `headless-chrome`
- **端口**: 9222
- **状态**: ✅ 常驻运行

### 可用命令
- `npx bb-browser site hackernews/top 5 --port 9222 --json` ✅
- `npx bb-browser site github/issues owner/repo --port 9222 --json` ✅
- `npx bb-browser site zhihu/hot 10 --port 9222 --json` ❌ (需登录态)

### 统一入口
- `python3 ~/.openclaw/workspace/web_query.py hackernews --count 5`
- `python3 ~/.openclaw/workspace/web_query.py search "query" --sources brave,arxiv`

### 中文信源（需登录态）
- 配置方式：Edge 扩展 + 登录网站
- 扩展位置：`/mnt/c/Users/MzgyM/Desktop/bb-browser-extension`
- daemon 端口：19824（扩展连接用）

---

## 代理配置

### Clash
- **地址**: `http://127.0.0.1:7897`
- **用途**: Discord / Web 访问
- **注意**: WSL2 直连被 block，必须走代理

### SearXNG
- **地址**: `http://localhost:8080`
- **用途**: 本地搜索聚合（零成本）
- **状态**: ✅ 运行中（Docker: searxng-1）
- **systemd**: `docker-searxng.service`
- **启动**: `docker start searxng-1` 或 `systemctl --user start docker-searxng`

---

## Expert Tracker 优先级追踪

### 配置文件
- **路径**: `~/.xuzhi_memory/expert_tracker/priority_sources.json`
- **更新**: 2026-03-30

### 追踪优先级

| 梯队 | 机构 | 优先级 |
|------|------|--------|
| Tier 1 | OpenAI, DeepMind, Anthropic | highest |
| Tier 2 | NVIDIA, Microsoft | high |
| Tier 3 | 北大/清华/浙大, Stanford, Ai2, EleutherAI | high |
| Tier 4 | Hassabis, Altman, Hinton等关键个体 | medium |

### 数学AI专项（Delta重点）
- DeepMind: AlphaProof, AlphaEvolve
- Lean社区: Mathlib发展

---

## Δ (Delta-Forge) 任务边界定义

### 负责范围
1. **社区监控**: Lean Zulip, ETP GitHub, MathOverflow
2. **数据分析**: 每周生成社区观察报告
3. **策略调整**: 根据社区反馈调整项目方向
4. **长期参与**: 3个月观察期后自然融入社区

### 禁止行为
- 不以 "AI Agent" 或 "Xuzhi Project" 名义主动发帖（Phase 1-2）
- 不泄露内部架构细节
- 不急于推广 MathAI4S 框架

### 报告义务
- 每周向 Human 汇报社区动态
- 重大发现立即通知
- 每月评估社区参与策略

---

## 变更通知协议

**任何 agent 修改基础设施后必须：**

1. 更新本文件（`~/.xuzhi_memory/manifests/INFRASTRUCTURE.md`）
2. 向 Ξ 发送通知（sessions_send）
3. Ξ 负责 commit + push

**禁止行为：**
- 不更新本文件直接修改基础设施
- 在对话中明文记录 token

---

## 修订历史

| 日期 | Agent | 变更 |
|------|-------|------|
| 2026-03-30 | Δ | 更新 Lean Zulip 状态，添加 Δ 任务边界定义 |
| 2026-03-30 | Ξ | 初始创建 |
