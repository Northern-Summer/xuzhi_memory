# SHARED_TOOLS.md — 全系统通用知识（L3 永久共同记忆）

> **强制等级：最高。所有 agent 启动时必须读取此文件。**
> **最后更新：2026-03-30 00:34**
> **晋升条件：已由 Ξ 和 Δ 独立验证，对系统运行有可量化影响**

---

## 网络搜索（最高优先，按场景选用）

### 场景一：学术论文 + arXiv
```bash
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" brave,arxiv
```
- SearXNG地址: http://localhost:8080（本地，零成本）
- 推荐引擎: brave（英文稳）、arxiv（论文）

### 场景二：中文公众号文章
```bash
python3 ~/.openclaw/workspace/wechat_search.py "<关键词>" [最大条数]
```
- 使用 curl_cffi 模拟 Chrome TLS 指纹
- 例：`python3 ~/.openclaw/workspace/wechat_search.py "AI 数学 自动证明" 10`

### 场景三：一般网页
```bash
# 直接用 web_fetch 获取页面内容
web_fetch(url="https://...", maxChars=5000)
```

---

## 代理配置（WSL2 环境）

```bash
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
```
- Clash代理：http://127.0.0.1:7897
- WSL2 直连部分网站被 Block，必须走代理
- GitHub raw 文件下载可能需要代理

---

## 模型路由（2026-03-30 确立）

| Agent | 模型 | 用途 |
|-------|------|------|
| Ξ (main) | **GLM-5** | 协调、工程、高风险决策 |
| Δ (delta) | **Kimi-K2.5** | 数学研究、多路径探索 |
| Φ (phi) | **Kimi-K2.5** | 语言学探索 |
| Θ (theta) | **Kimi-K2.5** | 社会科学研究 |
| Γ (gamma) | **Kimi-K2.5** | 自然科学研究 |
| Ω (omega) | **Kimi-K2.5** | 艺术探索 |
| Ψ (psi) | **GLM-5** | 哲学推理 |
| **默认** | **MiniMax-M2.7** | 通用后备 |

**模型切换**：`/model <模型名>`

**可用模型**：
- `glm-5` — OpenClaw 原生优化，长链稳定
- `kimi-k2.5` — 大 context，探索研究型
- `minimax-m2.7` — 默认，平衡
- `minimax-m2.5` — 性价比高，适合批量任务

---

## 系统路径速查

| 用途 | 路径 |
|------|------|
| Xuzhi 核心 | `~/xuzhi_genesis/` |
| 记忆系统 | `~/.xuzhi_memory/` |
| OpenClaw 配置 | `~/.openclaw/` |
| task_center | `~/.openclaw/workspace/task_center/` |
| 公共协议注册表 | `~/xuzhi_genesis/centers/public/registry/` |
| L3 共享知识 | `~/.xuzhi_memory/memory/knowledge/` |

---

## Channel 状态（2026-03-30）

| Channel | 状态 | 备注 |
|---------|------|------|
| WeChat | ✅ 在线 | openclaw-weixin v2.1.1 |
| Discord | ⚠️ 需重置 | token 过期 |
| WebChat | ✅ 可用 | |

---

## 输出规范（铁律）

通过任何 channel 向外部发送消息时，消息内容必须以自己的代号开头：

- **Φ**：每条消息以「Φ | HH:MM」开头
- **Δ**：每条消息以「Δ | HH:MM」开头
- **Θ**：每条消息以「Θ | HH:MM」开头
- **Γ**：每条消息以「Γ | HH:MM」开头
- **Ω**：每条消息以「Ω | HH:MM」开头
- **Ψ**：每条消息以「Ψ | HH:MM」开头
- **Ξ**：每条消息以「Ξ | HH:MM」开头

---

## Hub 协议（触发词）

- **"让/给/叫 + ΦΔΘΓΩΨ"** → 转发给对应 agent
- **"回来/总负责人/接线员/总工程师"** → 回到 Ξ

---

## 无感保活（PRT-002）

判断 agent 是否在运行：**看产出**（文件、git log），不发消息试探。
`sessions_send` 是打断，绝对禁止用于保活。

---

## 紧急恢复

```bash
# Gateway 挂了
kill -15 $(pgrep -f openclaw-gateway); openclaw gateway start

# 配置出错
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json

# 查看日志
tail ~/.openclaw/logs/gateway.log
```

---

## 记忆三层架构

| 层级 | 位置 | 性质 |
|------|------|------|
| L1 | `~/.xuzhi_memory/memory/YYYY-MM-DD.md` | 每日工作记忆，共享 |
| L2 | `~/.xuzhi_memory/agents/{X}/memory/` | 学科私有，不共享 |
| L3 | `~/.xuzhi_memory/memory/knowledge/` | 永久共同记忆，共享 |

### ⚠️ 轮值 Agent 无私有 L2

**2026-04-02 确立**：phi/delta/theta/gamma/omega/psi 不需要私有 L2。

| Agent 类型 | 私有 L2 | 原因 |
|------------|---------|------|
| 轮值 Agent（ΦΔΘΓΩΨ） | ❌ 不需要 | 所有工作记忆在共享 L1 |
| 特殊 Agent（Rho/Sigma） | ✅ 需要 | 学科知识需要隔离 |

**错误操作**：`memory_sync.sh` 曾将共享 L1 同步到每个 agent 的 memory/，造成 4MB+ 冗余。

**正确架构**：轮值 Agent 的 memory/ 目录保持空（只有 .gitkeep）。

---

## 维护机制

1. **每次系统配置变更**（模型、路径、channel）→ 更新此文件
2. **每次新增公共协议** → 更新 `~/xuzhi_genesis/centers/public/registry/INDEX.md`
3. **每个 agent 启动时** → 先读此文件，再读自己的 TOOLS.md

---

## L3 写入保护（铁律）

**读取**：所有 agent 随时可读，无需审批。

**写入**：不对称保护，必须满足以下条件：

### 晋升条件（必须同时满足）

1. **多 agent 验证**：被至少 2 个 agent 独立验证
2. **可量化影响**：对系统运行有可量化影响（如：减少错误率、提升效率、解决实际 bug）
3. **时间无关性**：不依赖具体日期/事件（永久有效）

### 写入流程

```
1. 提议者在 L1 记录提议内容 + 验证请求
2. 至少 1 个其他 agent 在 L1 独立验证
3. Ξ 执行写入（不是特权，是分工）
4. 写入后立即 git commit + push
```

**关键**：L3 写入必须经过 Human 确认。Ξ 只是执行者，不是决策者。

### 禁止行为

- ❌ 单 agent 直接写入 L3
- ❌ 未经验证的内容晋升
- ❌ 临时性、日期依赖的内容晋升
- ❌ 修改已有 L3 内容（只能追加，不能覆盖）
- ❌ Ξ 未经 Human 确认擅自写入

### 例外

- **紧急修复**：系统崩溃、安全漏洞 → Ξ 可单方面写入，但必须在 24h 内向 Human 报告并补验证
- **架构变更**：需要 Human 明确授权

### 设计原则

**中心化的合理性**：
- 不是去中心化 vs 中心化的对立
- 是合理的协调机制 vs 无序的各自为政
- 效率和安全性要求有最终把关人
- Human = 最终决策，Ξ = 执行协调

---

**文件版本**：v1.1
**创建者**：Ξ
**验证者**：Ξ、Δ

---

**文件版本**：v1.0
**创建者**：Ξ
**验证者**：Ξ、Δ
