
---

## 🔥 GitHub Push 失败根因（2026-03-29 更新版）

**痼疾**：每天都要修，云端提交流程需要大修。

**历史教训链**：
1. ghp_t0Ib... — token 失效 → 被 revoke
2. ghp_68Off... — token 存在但 GitHub 不认（从未真正工作或被 org 审查 block）
3. ghp_MMmBK... — 当前有效 token（2026-03-29 验证）

**根因一（已修复）**：`git remote set-url --push origin <URL>` 如果之前存在 `pushurl`，新的 URL 不会自动覆盖它。pushurl 覆盖了含 token 的 URL，导致 push 用裸 URL 发请求 → 401。
- xuzhi_memory 的 pushurl = `https://github.com/Northern-Summer/xuzhi_memory.git`（无 token）
- 正确做法：先删 pushurl，或显式 set-url --push 含 token 的 URL

**根因二（已修复）**：token 散落在 40+ 文件（session transcripts、backup、Trash）

**正确方案（永久固化）**：
```bash
# 唯一可信源：~/.xuzhi_vault/github_token（600 权限）
# 使用 git_hardening.sh：
bash ~/.xuzhi_memory/bin/git_hardening.sh save <new_token>

# 验证流程：git ls-remote 测试 → 有效才写入 vault → 更新所有 remote → test push
# 三仓库 repo 名：xuzhi_memory（无点），xuzhi_genesis，xuzhi_workspace
```

**git_hardening.sh 固化检查点**：
- token 验证：GIT_SSL_NO_VERIFY=true git ls-remote（不用 curl，curl 有 SSL 问题）
- 无效 token → 绝不写入 vault，退出并报错
- pushurl bug 已修复（显式设置含 token 的 push URL）
- 旧 token 散落自动清理（session transcripts、backup 文件 redact）

**Human 手动操作**：去 github.com/settings/tokens → Generate new token → 发给 Xi

---

## 🔥 2026-03-27 重大教训：系统漏洞修复

### Session Startup 严重漏洞（已修复）
**问题**：TOOLS.md 不在 Session Startup 必读列表，导致工具链从未被自动调用
**修复**：
- AGENTS.md 新增第3步：读取 TOOLS.md
- TOOLS.md 新增卷首标注，声明其为必读文件
- 论文流水线规范写入 TOOLS.md（永久有效）

### 网络搜索强制规范（2026-03-27 确立）
- 搜索是**强制步骤**，不是可选项
- 每次论文写作必须：开写前搜索 → 引用前验证 → 完成后对照
- 命令：`python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" bing,ddg`

### 自评 Rubric（2026-03-27 建立）
| 维度 | submittable门槛 |
|------|-----------------|
| 论证结构 | ≥3分 |
| 文献综述（含2024-2026新文献） | ≥3分 |
| 句式机器感 | ≥3分 |
| 实验支撑 | ≥3分 |
| 格式规范 | ≥3分 |
| **均分** | **≥4.0** |

### 每日论文目标（永久）
- 主目标：1篇完整可投稿论文（完整结构）
- 底线：1篇草稿 → expert_tracker/papers_v2/
- 降级：博客发布 + 问题日志记录
- 连续3天均分<4.0 → 系统性检修

### 今日核心教训（永久记忆）
> 今天写了8版论文，但全程没有调用一次网络搜索。
> 这是系统性失职，不是"忘了"。
> TOOLS.md不在必读列表 = 工具链永远不会被自动调用。
> 修复后，任何新会话都会先读TOOLS.md，然后才能启动。
