# OSINT 情报搜索最佳策略框架
> Ξ | 2026-03-29 | 固化自 2026-03-24 Λ 提案

---

## 核心公式：F⊕C⊗D

### F — Focus Funnel（聚焦漏斗）
```
需求 → 种子节点（最佳实践触发器）
```
- 第一轮搜索：精准关键词，找到该领域的标志性项目/论文
- 种子节点 = 领域公认最好的工作（有 citations / 有官方 code / 有社区复现）

### C — Clue Network（线索扩散网络）
7条扩散路径（每条都是独立验证通道）：
1. **论文引用** → 找被引次数高的
2. **作者主页** → 看作者还做了哪些相关工作
3. **官方代码仓库** → README 里提到的依赖和基准
4. **社区复现** → GitHub trending / starred
5. **平台讨论** → Reddit / HN / StackOverflow 的反馈
6. **术语链** → 从已知术语扩展到相关子领域
7. **对比论文** → Related Work 里提到的竞争方法

### D — Discriminator（判别锚点）
三个锚点，至少通过 2 个：
1. **权威性**：是否是顶会/顶刊/知名团队？
2. **实践性**：是否有可运行的代码/demo？
3. **社区性**：是否被广泛使用、复现、讨论？

### ⊙ — 迭代饱和即止
- 2-3 轮迭代
- 新发现节点 < 2 个 → 立即停止
- 边际收益递减 → 强制退出

---

## AI4S 项目验证标准

**核心原则：不验证 = 幻觉。写了不可复刻的项目比没写更糟糕。**

### 验证等级

| 等级 | 含义 | 标记 |
|------|------|------|
| ⭐ 可复现 | 代码存在 + 依赖清晰 + 可本地运行 | 写进 AI4S.md |
| 🔒 仅论文 | 论文质量高但无官方代码 | 单独列"仅论文"节 |
| ❌ 不可用 | 代码存在但不可运行（依赖缺失/平台锁定/已停更>1年）| 排除 |

### AI4S 项目必查项
1. **官方 GitHub 存在？** （不是 arxiv 链接，是真实的 github.com/... 仓库）
2. **最后更新 <= 18 个月？** （超过 18 个月 = 已停更，不适合作为活跃工具）
3. **有可读 README？** （无 README = 无法复现）
4. **依赖是否可安装？** （pip install / conda / docker 有任意一个即可）
5. **stars 社区验证？** （stars > 100 = 有人用过）

### AI4S 搜索三步法
```
Step 1: 搜索 "[领域] [顶级团队] official code github"
        例: "DeepMind AlphaFold official code github"
        
Step 2: 搜 "site:github.com [paper title]" 
        例: "site:github.com DeepSeek-Prover-V2"
        
Step 3: 验证 D 锚点（权威性/实践性/社区性）
        每条 ≥2 通过才写入
```

---

## 引擎矩阵（按任务类型选择）

| 任务类型 | 引擎选择 |
|----------|----------|
| 精确技术问题 | arxiv (优先) |
| 开源代码追踪 | GitHub direct search |
| 权威技术文档 | SearXNG → wiki → brave |
| 中文行业动态 | 微信搜索 |
| 事实核查 | ddg → bing 交叉验证 |

---

## URL 白名单（AI4S 用）
- ✅ `github.com` — 代码仓库
- ✅ `arxiv.org` — 论文
- ✅ `huggingface.co` — 模型
- ✅ `pypi.org` — Python 包
- ❌ `zhihu.com` — 低质量中文（不单独引用）
- ❌ `juejin.cn` — 低质量中文

---

## 饱和即止判断
```
if new_valid_projects < 2:
    stop_searching()
elif iteration >= 3:
    stop_searching()
elif marginal_gain_decreasing():
    stop_searching()
```

---

## 固化记录
- 2026-03-29：首次从 daily/2026-03-24.md 提取并固化
- 下次校准：2026-04-01
