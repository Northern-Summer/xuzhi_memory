# OpenClaw 优化实施清单
## 基于 Claude Code 最佳实践的改进追踪

---

## 🚀 Phase 1: 基础架构 (Week 1-2)

### 1.1 QueryEngine 类重构
- [ ] 创建 `src/agents/QueryEngine.ts`
- [ ] 实现 `EngineState` 状态管理
- [ ] 重构 `runReplyAgent` 为类方法
- [ ] 添加 `submitMessage` 生成器方法
- [ ] 实现 `abort()` 中断机制
- [ ] 单元测试覆盖

**参考文件：**
- `claude-code-sourcemap/restored-src/src/QueryEngine.ts`

---

### 1.2 工具权限注册表
- [ ] 创建 `src/agents/tools/permissions.ts`
- [ ] 定义 `PermissionLevel` 类型
- [ ] 实现 `ToolPermissionPolicy` 接口
- [ ] 创建 `TOOL_PERMISSION_REGISTRY`
- [ ] 实现 `ToolPermissionChecker` 类

**参考文件：**
- `claude-code-sourcemap/restored-src/src/constants/tools.ts`

---

## 🔐 Phase 2: 安全系统 (Week 3-4)

### 2.1 Bash 安全检查器
- [ ] 创建 `src/agents/tools/bash/security.ts`
- [ ] 移植 `ZSH_DANGEROUS_COMMANDS`
- [ ] 移植 `COMMAND_SUBSTITUTION_PATTERNS`
- [ ] 实现 `extractQuotedContent()`
- [ ] 实现 `stripSafeRedirections()`
- [ ] 添加 `BASH_SECURITY_CHECK_IDS`

**参考文件：**
- `claude-code-sourcemap/restored-src/src/tools/BashTool/bashSecurity.ts` (102KB)

---

### 2.2 命令分类器
- [ ] 创建 `src/agents/tools/bash/classifier.ts`
- [ ] 实现 `BashCommandClassifier` 类
- [ ] 添加危险模式正则
- [ ] 集成 LLM 分类（可选）
- [ ] 实现 `classifyCommand()` 方法

**参考文件：**
- `claude-code-sourcemap/restored-src/src/utils/permissions/yoloClassifier.ts` (52KB)

---

### 2.3 权限规则解析
- [ ] 创建 `src/agents/tools/bash/permissionRules.ts`
- [ ] 实现 `isDangerousBashPermission()`
- [ ] 移植 `DANGEROUS_BASH_PATTERNS`
- [ ] 添加规则解析器

**参考文件：**
- `claude-code-sourcemap/restored-src/src/utils/permissions/permissionSetup.ts`

---

## 🤖 Phase 3: Agent 系统 (Week 5-6)

### 3.1 Agent 工具重构
- [ ] 扩展 Agent 工具 Schema
- [ ] 添加 `run_in_background` 参数
- [ ] 添加 `name` 和 `team_name` 参数
- [ ] 实现 Agent 生命周期管理
- [ ] 添加进度追踪

**参考文件：**
- `claude-code-sourcemap/restored-src/src/tools/AgentTool/AgentTool.tsx` (160KB)

---

### 3.2 Fork Subagent 机制
- [ ] 创建 `src/agents/fork.ts`
- [ ] 实现 `isForkSubagentEnabled()`
- [ ] 实现 `buildForkedMessages()`
- [ ] 实现 `FORK_PLACEHOLDER_RESULT`
- [ ] 添加 Fork 指令模板
- [ ] 实现 Cache Safe Params

**参考文件：**
- `claude-code-sourcemap/restored-src/src/tools/AgentTool/forkSubagent.ts`
- `claude-code-sourcemap/restored-src/src/utils/forkedAgent.ts`

---

### 3.3 Coordinator Mode
- [ ] 创建 `src/agents/coordinator/` 目录
- [ ] 实现 `CoordinatorEngine` 类
- [ ] 创建协调器系统提示
- [ ] 实现 Worker 生命周期
- [ ] 实现 `sendMessageToWorker()`
- [ ] 实现 `stopWorker()`
- [ ] 实现 Scratchpad 共享

**参考文件：**
- `claude-code-sourcemap/restored-src/src/coordinator/coordinatorMode.ts`

---

## ⚡ Phase 4: 性能优化 (Week 7-8)

### 4.1 Prompt Caching
- [ ] 创建 `src/agents/prompt/caching.ts`
- [ ] 实现 `PromptPartitioner` 类
- [ ] 实现 `CacheScope` 类型
- [ ] 实现 `buildCachedRequest()`
- [ ] 添加缓存统计
- [ ] 实现动态边界标记

**参考文件：**
- `claude-code-sourcemap/restored-src/src/services/api/claude.ts`
- `claude-code-sourcemap/restored-src/src/constants/prompts.ts`

---

### 4.2 消息优化
- [ ] 实现消息规范化
- [ ] 添加工具结果配对
- [ ] 实现内容块压缩
- [ ] 添加 Token 估算

**参考文件：**
- `claude-code-sourcemap/restored-src/src/utils/messages.ts` (193KB)

---

## 📦 Phase 5: Skills 系统 (Week 9-10)

### 5.1 Frontmatter 扩展
- [ ] 扩展 `SkillFrontmatter` 接口
- [ ] 添加 `allowedTools` 字段
- [ ] 添加 `whenToUse` 字段
- [ ] 添加 `hooks` 字段
- [ ] 添加 `arguments` 字段
- [ ] 实现 Frontmatter 解析器

**参考文件：**
- `claude-code-sourcemap/restored-src/src/skills/loadSkillsDir.ts`

---

### 5.2 智能技能匹配
- [ ] 创建 `src/skills/matcher.ts`
- [ ] 实现 `SkillMatcher` 类
- [ ] 添加 LLM 相关性匹配
- [ ] 实现技能推荐

---

### 5.3 Hooks 系统
- [ ] 创建 `src/skills/hooks.ts`
- [ ] 实现 `preExecute` hooks
- [ ] 实现 `postExecute` hooks
- [ ] 添加 hook 注册机制

**参考文件：**
- `claude-code-sourcemap/restored-src/src/utils/hooks.ts` (159KB)

---

## 🧪 测试清单

### 单元测试
- [ ] QueryEngine 测试
- [ ] 权限检查器测试
- [ ] Bash 安全检查测试
- [ ] Fork 消息构建测试
- [ ] Prompt Caching 测试

### 集成测试
- [ ] Agent 生命周期测试
- [ ] Coordinator 模式测试
- [ ] 多 Agent 协作测试
- [ ] 缓存命中测试

---

## 📊 验收标准

### Phase 1 完成标准
- QueryEngine 类可运行
- 基本权限检查工作
- 单元测试通过

### Phase 2 完成标准
- Bash 命令安全检查生效
- 危险命令被正确拦截
- 分类器准确率 > 95%

### Phase 3 完成标准
- Agent 工具支持后台运行
- Fork 机制工作正常
- Coordinator 可协调多个 Worker

### Phase 4 完成标准
- Prompt Cache 命中率 > 50%
- API 成本降低 > 30%
- 响应延迟降低

### Phase 5 完成标准
- Skills Frontmatter 完整解析
- 智能匹配工作正常
- Hooks 系统可用

---

## 📁 文件结构规划

```
src/agents/
├── QueryEngine.ts           # 核心 Query 引擎
├── fork.ts                  # Fork 机制
├── coordinator/
│   ├── index.ts
│   ├── CoordinatorEngine.ts # 协调器引擎
│   ├── WorkerHandle.ts      # Worker 句柄
│   └── ScratchpadManager.ts # 共享目录管理
├── tools/
│   ├── permissions.ts       # 权限系统
│   ├── bash/
│   │   ├── security.ts      # 安全检查
│   │   ├── classifier.ts    # 命令分类
│   │   └── patterns.ts      # 危险模式
│   └── AgentTool.ts         # Agent 工具
├── prompt/
│   ├── caching.ts           # Prompt 缓存
│   └── partitioner.ts       # 内容分区

src/skills/
├── matcher.ts               # 技能匹配
├── hooks.ts                 # Hooks 系统
└── parser.ts                # Frontmatter 解析
```

---

*Last Updated: 2026-03-31*
*Status: Ready for Implementation*
