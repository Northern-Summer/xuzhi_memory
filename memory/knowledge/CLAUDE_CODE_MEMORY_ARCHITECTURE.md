# Claude Code 记忆架构学习笔记

> 学习时间：2026-04-01 19:22
> 来源：官方文档 + 实践教程

---

## 核心架构

### 六层记忆层级

```
Layer 1: Managed policy（组织级）
  位置：/etc/claude-code/CLAUDE.md（Linux）
  特点：只读，所有用户共享
  用途：公司规范、安全策略

Layer 2: 项目级 CLAUDE.md
  位置：./CLAUDE.md 或 ./.claude/CLAUDE.md
  特点：Git 提交，团队共享
  用途：项目规范、技术栈、常用命令

Layer 3: 模块规则
  位置：.claude/rules/*.md
  特点：按文件类型加载
  用途：特定模块规则（测试、API、前端）

Layer 4: 用户全局
  位置：~/.claude/CLAUDE.md
  特点：个人偏好，不提交 Git
  用途：个人工作流习惯

Layer 5: 项目个人
  位置：CLAUDE.local.md
  特点：不提交 Git
  用途：个人对特定项目的偏好

Layer 6: Auto Memory
  位置：~/.claude/projects/<project>/memory/
  特点：Claude 自动写入
  用途：调试经验、构建命令、用户偏好
```

---

## 关键设计原则

### 1. 启动记忆限制

**规则**：只加载前 200 行

**原因**：
- 人类短期记忆：7±2 组块
- AI 启动记忆：需要克制
- 不是记住所有，而是知道该先想起什么

**实现**：
```
MEMORY.md（前 200 行）→ 索引
详细笔记 → 按需加载主题文件
```

### 2. 按需加载

**触发机制**：
- 处理 `src/` 文件时 → 加载 `src/CLAUDE.md`
- 处理 `api/` 文件时 → 加载 `api/CLAUDE.md`
- 节省 token + 提供精准上下文

### 3. Auto Memory 自动学习

**触发**：
- 用户纠正："记住用 pnpm 不用 npm"
- Claude 自动判断：哪些信息未来有用
- 自动写入：~/.claude/projects/<project>/memory/

**内容类型**：
- 构建命令
- 调试经验
- 架构笔记
- 用户偏好

---

## Xuzhi 应用方案

### 当前架构

```
Xuzhi 记忆：
  L1: memory/*.md（读写频繁）
  L2: manifests/（快照）
  L3: backup/（归档）

问题：
  - 启动全量加载（浪费 token）
  - 无子目录规则
  - Auto Memory 不够自动化
```

### 优化方案

```
Xuzhi 新架构（借鉴 Claude Code）：

启动记忆（前 200 行）：
  → MEMORY.md（索引）
  → 包含：身份、核心原则、能力清单、待办

详细主题（按需加载）：
  → knowledge/*.md（框架笔记）
  → expert_tracker/*.md（研究记录）
  → evolution/*.md（进化数据）

子目录规则：
  → agents/xi/AGENTS.md（Xi 专属）
  → agents/phi/AGENTS.md（Φ 专属）
  → 按激活的 agent 加载

Auto Memory 增强：
  → 每次 Session End 自动提取
  → 记录：用户纠正、偏好、发现
  → 位置：~/.xuzhi_memory/auto_memory/
```

---

## 具体实施

### Phase 1：启动记忆限制

**当前 MEMORY.md**：~2000 行

**优化后**：
- 前 50 行：身份 + 核心原则
- 后 150 行：能力清单 + 待办
- 详细内容 → 移到主题文件

### Phase 2：子目录规则

**当前**：全局 AGENTS.md

**优化后**：
- `agents/xi/AGENTS.md` → Xi 专属规则
- `agents/phi/AGENTS.md` → Φ 专属规则
- 按激活的 agent 按需加载

### Phase 3：Auto Memory 增强

**当前**：Session End 手动提取

**优化后**：
- 自动检测用户纠正
- 自动写入 `auto_memory/YYYY-MM-DD.md`
- 下次启动自动加载

---

## 预期效果

| 指标 | 当前 | 优化后 | 改进 |
|------|------|--------|------|
| 启动 token | ~80k | ~20k | -75% |
| 加载速度 | 慢 | 快 | 显著 |
| 记忆精准度 | 中 | 高 | 提升 |
| 自学习能力 | 中 | 高 | 提升 |

---

## 参考

- Claude Code 官方文档：https://code.claude.com/docs/en/memory
- 菜鸟教程：https://www.runoob.com/claude-code/claude-code-memory.html
- 星火博客：https://yangzh.cn/posts/posts/claude-code-auto-memory.html/
