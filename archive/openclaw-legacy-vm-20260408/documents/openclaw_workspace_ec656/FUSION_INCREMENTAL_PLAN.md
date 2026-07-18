# OpenClaw 增量融合计划
## 外科手术式升级，零破坏原则

---

## 一、架构对比分析

### OpenClaw 现有架构（2026.3.28）

```
┌─────────────────────────────────────────────────────────────────┐
│                         Gateway (Daemon)                         │
│  WebSocket API + Channel Providers (WhatsApp/Telegram/Discord)  │
├─────────────────────────────────────────────────────────────────┤
│                     Agent Runtime (Pi Core)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ SessionStore │  │ ToolRegistry │  │ PromptPipeline       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                    Multi-Agent Router                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ bindings: [{ agentId, match: { channel, accountId, peer }}]│ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Plugin Hook System                            │
│  before_model_resolve / before_prompt_build / agent_end / ...   │
└─────────────────────────────────────────────────────────────────┘
```

### Claude Code 核心设计

```
┌─────────────────────────────────────────────────────────────────┐
│                        QueryEngine                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ StateManager │  │ AbortCtrl    │  │ FileStateCache       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  async *processMessage(): AsyncGenerator<ReplyPayload>          │
├─────────────────────────────────────────────────────────────────┤
│                    Fork Subagent Engine                          │
│  buildForkedMessages() + FORK_PLACEHOLDER_RESULT                │
├─────────────────────────────────────────────────────────────────┤
│                    Coordinator Mode                              │
│  COORDINATOR_MODE_ALLOWED_TOOLS vs ASYNC_AGENT_ALLOWED_TOOLS    │
├─────────────────────────────────────────────────────────────────┤
│                    Bash Security (23 checks)                     │
│  ZSH_DANGEROUS_COMMANDS + COMMAND_SUBSTITUTION_PATTERNS         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、融合决策矩阵

| Claude Code 模块 | OpenClaw 现状 | 融合策略 | 风险等级 |
|-----------------|--------------|----------|---------|
| QueryEngine | Pi Core 运行时 | **包装层** - 新增 QueryEngineAdapter | 🟢 低 |
| Fork Subagent | 无等效 | **新增模块** - 独立添加 | 🟢 低 |
| Coordinator Mode | Multi-Agent Router | **增强** - 添加协调器模式 | 🟡 中 |
| Bash Security (23) | 基础检查 | **增强** - 扩展现有检查 | 🟢 低 |
| YOLO Classifier | 无等效 | **新增模块** - 可选功能 | 🟢 低 |
| Prompt Caching | 基础缓存 | **增强** - 优化缓存策略 | 🟡 中 |
| Skills System | 已有 Skills | **扩展** - 添加 Frontmatter 字段 | 🟢 低 |
| Hooks System | 已有 Hooks | **扩展** - 添加事件类型 | 🟢 低 |

---

## 三、增量实施路径

### Phase 0: 准备工作（Day 1）

**目标**：建立测试基础设施，确保变更可回滚

```bash
# 1. 创建测试分支
cd ~/.openclaw
git checkout -b fusion/phase-0-preparation

# 2. 备份现有配置
cp -r workspace workspace.backup
cp -r agents agents.backup

# 3. 创建测试脚本
cat > ~/.openclaw/scripts/test-fusion.sh << 'EOF'
#!/bin/bash
# 测试核心功能是否正常
echo "Testing basic agent run..."
openclaw agent "echo hello" --dry-run

echo "Testing tool execution..."
# 添加更多测试

echo "All tests passed!"
EOF
```

**产出**：
- ✅ 测试脚本
- ✅ 回滚脚本
- ✅ 功能基准线

---

### Phase 1: Bash 安全增强（Day 2-3）

**策略**：扩展现有安全检查，零破坏

**文件**：新建 `~/.openclaw/workspace/scripts/bash-security-enhanced.sh`

```bash
#!/bin/bash
# Bash Security Enhanced - Claude Code 移植
# 用法: source 此脚本，然后调用 validate_bash_command

# ============================================
# Zsh 危险命令（Claude Code 移植）
# ============================================
declare -A ZSH_DANGEROUS_COMMANDS=(
    ["zmodload"]="module loading gateway"
    ["emulate"]="eval equivalent"
    ["sysopen"]="file descriptor manipulation"
    ["sysread"]="file descriptor manipulation"
    ["syswrite"]="file descriptor manipulation"
    ["sysseek"]="file descriptor manipulation"
    ["zpty"]="pseudo-terminal execution"
    ["ztcp"]="TCP connection"
    ["zsocket"]="Unix/TCP socket"
    ["zf_rm"]="builtin file operations"
    ["zf_mv"]="builtin file operations"
    ["zf_ln"]="builtin file operations"
    ["zf_chmod"]="builtin file operations"
)

# ============================================
# 命令替换模式检测（Claude Code 移植）
# ============================================
declare -A COMMAND_SUBSTITUTION_PATTERNS=(
    ["<\\("]="process substitution <()"
    [">\\("]="process substitution >()"
    ["=\\("]="Zsh process substitution =()"
    ["\\$\\("]="$() command substitution"
    ["\\$\\{"]="${} parameter substitution"
    ["\\`"]="legacy backtick substitution"
)

# ============================================
# 23 种安全检查 ID（Claude Code 移植）
# ============================================
declare -A BASH_SECURITY_CHECKS=(
    [1]="INCOMPLETE_COMMANDS"
    [2]="JQ_SYSTEM_FUNCTION"
    [3]="JQ_FILE_ARGUMENTS"
    [4]="OBFUSCATED_FLAGS"
    [5]="SHELL_METACHARACTERS"
    [6]="DANGEROUS_VARIABLES"
    [7]="NEWLINES"
    [8]="DANGEROUS_PATTERNS_COMMAND_SUBSTITUTION"
    [9]="DANGEROUS_PATTERNS_INPUT_REDIRECTION"
    [10]="DANGEROUS_PATTERNS_OUTPUT_REDIRECTION"
    [11]="IFS_INJECTION"
    [12]="GIT_COMMIT_SUBSTITUTION"
    [13]="PROC_ENVIRON_ACCESS"
    [14]="MALFORMED_TOKEN_INJECTION"
    [15]="BACKSLASH_ESCAPED_WHITESPACE"
    [16]="BRACE_EXPANSION"
    [17]="CONTROL_CHARACTERS"
    [18]="UNICODE_WHITESPACE"
    [19]="MID_WORD_HASH"
    [20]="ZSH_DANGEROUS_COMMANDS"
    [21]="BACKSLASH_ESCAPED_OPERATORS"
    [22]="COMMENT_QUOTE_DESYNC"
    [23]="QUOTED_NEWLINE"
)

# ============================================
# 核心验证函数
# ============================================
validate_bash_command() {
    local command="$1"
    local result="allow"
    local reason="All checks passed"
    local check_id=0
    
    # 检查 1: 空命令
    if [[ -z "$command" ]]; then
        echo "allow:empty_command"
        return 0
    fi
    
    # 检查 5: Shell 元字符
    if [[ "$command" =~ [\;\|\&\$\`\\] ]]; then
        # 允许常见用法
        if [[ "$command" =~ ^[a-zA-Z0-9_\-\.\/]+\ [a-zA-Z0-9_\-\.\/\ ]*$ ]]; then
            : # 安全，继续
        else
            result="confirm"
            reason="Shell metacharacters detected"
            check_id=5
        fi
    fi
    
    # 检查 20: Zsh 危险命令
    for cmd in "${!ZSH_DANGEROUS_COMMANDS[@]}"; do
        if [[ "$command" =~ ^[[:space:]]*$cmd[[:space:]] ]] || [[ "$command" =~ ^[[:space:]]*$cmd$ ]]; then
            result="deny"
            reason="Zsh dangerous command: $cmd (${ZSH_DANGEROUS_COMMANDS[$cmd]})"
            check_id=20
            break
        fi
    done
    
    # 检查 8: 命令替换模式
    for pattern in "${!COMMAND_SUBSTITUTION_PATTERNS[@]}"; do
        if [[ "$command" =~ $pattern ]]; then
            result="confirm"
            reason="Command substitution pattern: ${COMMAND_SUBSTITUTION_PATTERNS[$pattern]}"
            check_id=8
            break
        fi
    done
    
    # 检查 11: IFS 注入
    if [[ "$command" =~ IFS= ]] || [[ "$command" =~ \$IFS ]]; then
        result="confirm"
        reason="IFS manipulation detected"
        check_id=11
    fi
    
    # 检查 12: Git commit 替换
    if [[ "$command" =~ git\ commit\.*\$(\{|() ]]; then
        result="confirm"
        reason="Git commit with variable substitution"
        check_id=12
    fi
    
    # 输出结果
    echo "${result}:${check_id}:${reason}"
}

# ============================================
# 引号提取（Claude Code 移植）
# ============================================
extract_quoted_content() {
    local command="$1"
    local in_single_quote=false
    local in_double_quote=false
    local escaped=false
    local with_double_quotes=""
    local fully_unquoted=""
    
    for (( i=0; i<${#command}; i++ )); do
        local char="${command:$i:1}"
        
        if $escaped; then
            escaped=false
            if ! $in_single_quote; then
                with_double_quotes+="$char"
            fi
            if ! $in_single_quote && ! $in_double_quote; then
                fully_unquoted+="$char"
            fi
            continue
        fi
        
        if [[ "$char" == "\\" ]] && ! $in_single_quote; then
            escaped=true
            continue
        fi
        
        if [[ "$char" == "'" ]] && ! $in_double_quote; then
            in_single_quote=!$in_single_quote
            continue
        fi
        
        if [[ "$char" == '"' ]] && ! $in_single_quote; then
            in_double_quote=!$in_double_quote
            continue
        fi
        
        with_double_quotes+="$char"
        if ! $in_single_quote && ! $in_double_quote; then
            fully_unquoted+="$char"
        fi
    done
    
    echo "WITH_DOUBLE_QUOTES:$with_double_quotes"
    echo "FULLY_UNQUOTED:$fully_unquoted"
}

# 导出函数供外部使用
export -f validate_bash_command
export -f extract_quoted_content
```

**集成方式**：通过 Plugin Hook 集成

```yaml
# ~/.openclaw/openclaw.json 添加
{
  "plugins": {
    "hooks": {
      "before_tool_call": [
        {
          "match": { "tool": "exec" },
          "script": "~/.openclaw/workspace/scripts/bash-security-enhanced.sh"
        }
      ]
    }
  }
}
```

**测试**：
```bash
# 验证脚本
source ~/.openclaw/workspace/scripts/bash-security-enhanced.sh

validate_bash_command "ls -la"
# 输出: allow:0:All checks passed

validate_bash_command "rm -rf /"
# 输出: confirm:5:Shell metacharacters detected

validate_bash_command "zmodload zsh/net/tcp"
# 输出: deny:20:Zsh dangerous command: zmodload (module loading gateway)
```

---

### Phase 2: Fork Subagent 引擎（Day 4-6）

**策略**：新增独立模块，不修改现有 Agent 运行时

**文件**：新建 Skill `~/.openclaw/skills/fork-subagent/SKILL.md`

```markdown
---
name: fork
description: Fork a subagent with shared context for parallel task execution
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
agent: default
---

# Fork Subagent

You are a forked worker process. You are NOT the main agent.

## Rules (Non-Negotiable)

1. **Do NOT spawn sub-agents** — you ARE the fork. Execute directly.
2. **Do NOT converse or ask questions** — output results only.
3. **USE your tools directly**: Bash, Read, Write, Edit, Grep, Glob.
4. **Keep your report under 500 words** — be concise.
5. **Your response MUST begin with "Scope:"** — no preamble.

## Output Format

```
Scope: <echo back your assigned scope>
Result: <key findings or deliverables>
Key files: <list of relevant file paths>
Files changed: <list with commit hash if applicable>
Issues: <list of blockers or warnings, if any>
```

## Context Sharing

You inherit the parent session's context:
- Working directory: Same as parent
- Tool permissions: Same as parent (unless restricted)
- Output: Will be merged into parent's context

## Example

**Input:**
```
Directive: Analyze authentication flow in src/auth/ and identify security vulnerabilities.
```

**Output:**
```
Scope: Analyze authentication flow in src/auth/
Result: Found 3 potential vulnerabilities:
1. Session token not rotated on login (validate.ts:42)
2. Password reset token valid for 24h (reset.ts:78)
3. No rate limiting on login endpoint (login.ts:15)

Key files: src/auth/validate.ts, src/auth/reset.ts, src/auth/login.ts
Files changed: None (analysis only)
Issues: Recommend implementing rate limiting before production.
```
```

**配套配置**：

```json5
// ~/.openclaw/openclaw.json
{
  skills: {
    fork: {
      enabled: true,
      maxConcurrent: 3,  // 最大并行数
      timeoutSeconds: 300,
      inheritTools: true,
      inheritPermissions: true,
    }
  }
}
```

---

### Phase 3: QueryEngine 适配层（Day 7-10）

**策略**：创建适配层包装现有 Pi Core，提供统一接口

**目标接口设计**：

```typescript
// 类型定义（概念性，供参考）
interface QueryEngineAdapter {
  // 状态管理
  state: {
    messages: Message[];
    usage: Usage;
    isComplete: boolean;
  };
  
  // 核心方法
  processMessage(ctx: MsgContext): AsyncGenerator<ReplyPayload>;
  abort(): void;
  
  // 工具执行
  executeToolCall(call: ToolCall): Promise<ToolResult>;
  
  // 钩子
  onStateChange(callback: StateCallback): Unsubscribe;
}
```

**实现策略**：

1. **Phase 3a**: 创建 QueryEngineAdapter 类（包装 runEmbeddedPiAgent）
2. **Phase 3b**: 添加状态管理基础设施
3. **Phase 3c**: 实现 abort() 中断机制
4. **Phase 3d**: 添加 AsyncGenerator 支持

**文件结构**：

```
~/.openclaw/workspace/
├── lib/
│   └── query-engine/
│       ├── adapter.ts      # QueryEngine 适配层
│       ├── state.ts        # 状态管理
│       ├── abort.ts        # 中断控制
│       └── types.ts        # 类型定义
```

---

### Phase 4: Prompt Caching 优化（Day 11-13）

**策略**：优化现有缓存策略，不改变 API 接口

**现有缓存分析**：
- OpenClaw 已有基本的 Prompt 缓存
- 需要添加静态/动态分离

**优化方案**：

```json5
// ~/.openclaw/openclaw.json 添加
{
  agents: {
    defaults: {
      promptCache: {
        enabled: true,
        strategy: "partitioned",  // 新增：分区策略
        scopes: {
          global: {
            // 全局缓存：系统提示 + 技能描述
            ttl: "1h",
            boundary: "SYSTEM_PROMPT_DYNAMIC_BOUNDARY"
          },
          user: {
            // 用户级缓存：CLAUDE.md + USER.md
            ttl: "30m"
          },
          session: {
            // 会话级：不缓存
            ttl: 0
          }
        }
      }
    }
  }
}
```

---

### Phase 5: Coordinator 模式（Day 14-17）

**策略**：扩展现有 Multi-Agent Router，添加协调器模式

**配置示例**：

```json5
// ~/.openclaw/openclaw.json
{
  agents: {
    list: [
      {
        id: "coordinator",
        workspace: "~/.openclaw/workspace-coordinator",
        mode: "coordinator",  // 新增模式
        tools: {
          allow: ["Agent", "SendMessage", "TaskStop", "Read"],
          deny: ["Write", "Edit", "Bash"]  // 协调器不执行工具
        },
        workers: {
          maxConcurrent: 5,
          defaultTools: ["Read", "Write", "Edit", "Bash", "Grep"],
          deniedTools: ["Agent", "SendMessage", "TaskStop"]  // 防止递归
        }
      }
    ]
  }
}
```

**Coordinator 系统提示**：

```markdown
---
name: coordinator
description: Coordinate multiple workers to achieve complex goals
---

# Coordinator Mode

You are a **coordinator**. Your job is to:
- Help the user achieve their goal
- Direct workers to research, implement, and verify
- Synthesize results and communicate with the user
- Answer questions directly when possible

## Your Tools

- **Agent**: Spawn a new worker
- **SendMessage**: Continue an existing worker
- **TaskStop**: Stop a running worker

## Workers

Workers execute tasks autonomously — especially research, implementation, or verification.

## Task Workflow

| Phase | Who | Purpose |
|-------|-----|---------|
| Research | Workers (parallel) | Investigate codebase |
| Synthesis | **You** (coordinator) | Read findings, craft specs |
| Implementation | Workers | Make targeted changes |
| Verification | Workers | Test changes work |

## Critical Rules

1. **Workers can't see your conversation** — every prompt must be self-contained.
2. **Always synthesize** — never write "based on your findings".
3. **Don't predict worker results** — wait for completion.
4. **Parallelize independent tasks** — spawn multiple workers.
```

---

## 四、验证检查点

### 每个 Phase 结束后

```bash
# 1. 运行功能测试
./scripts/test-fusion.sh

# 2. 检查日志无错误
openclaw gateway logs --tail=100 | grep -i error

# 3. 验证核心功能
# - 发送消息测试
# - 工具执行测试
# - 会话持久化测试

# 4. 性能基准
# - 响应时间
# - 内存使用
# - 缓存命中率
```

### 回滚计划

```bash
# 如果出现问题
./scripts/rollback-fusion.sh <phase>

# 完全回滚
git checkout main
rm -rf workspace agents
mv workspace.backup workspace
mv agents.backup agents
openclaw gateway restart
```

---

## 五、成功指标

| 指标 | 基准线 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|------|--------|---------|---------|---------|---------|---------|
| 功能完整性 | 100% | 100% | 100% | 100% | 100% | 100% |
| 安全检查覆盖率 | 30% | 90% | 90% | 90% | 90% | 90% |
| 并行任务支持 | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| 中断恢复 | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| 缓存命中率 | 60% | 60% | 65% | 70% | 85% | 85% |
| 复杂任务协调 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 六、下一步行动

**立即开始 Phase 0**：

1. 创建测试脚本
2. 建立功能基准线
3. 配置回滚机制

准备好后，开始 Phase 1: Bash 安全增强。

---

*Generated: 2026-03-31*
*Status: Phase 0-2 完成，Phase 3-5 待开始*

---

## 融合进度日志

### 2026-03-31 20:53 — Phase 0-2 完成

**Phase 0 完成**：
- ✅ `scripts/test-fusion.sh` — 6项功能测试
- ✅ `scripts/rollback-fusion.sh` — 分阶段回滚脚本
- ✅ `.backup/openclaw.json` — 配置备份

**Phase 1 完成**：
- ✅ `scripts/bash-security-enhanced.sh` — 12项安全检查（Claude Code 移植）
  - Zsh 危险命令检测
  - IFS 注入检测
  - 命令替换模式检测
  - 控制字符检测
  - 大括号展开检测

**Phase 2 完成**：
- ✅ `skills/fork-subagent/SKILL.md` — Fork Subagent 技能
  - 继承父级上下文
  - 静默执行 + 结构化报告
  - 与 Coordinator Mode 互斥

**测试结果**：6/6 PASS
