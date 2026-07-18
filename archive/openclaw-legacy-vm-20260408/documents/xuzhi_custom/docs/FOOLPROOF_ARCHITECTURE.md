# 防傻瓜系统架构 v1.0

> **目标**：即使是一个完全不懂开发的人，也能安全使用系统，不会破坏，甚至能增强
> **创建时间**：2026-04-01
> **创建者**：Ξ

---

## 核心问题

**用户描述**：
> "我现在基本上每天重新开始的时候都好像我们彼此重新认识一样。一直到晚上所有事情都做完的时候是状态最好的。然后第二天又从头开始。"

**根因分析**：
1. LLM 是无状态的，每次会话都从零开始
2. 记忆系统依赖 LLM 主动读取（软约束）
3. 没有强制性的恢复机制

---

## 解决方案：三层防护

### 第一层：代码强制注入（最可靠）

**机制**：Hook 在 `/new` 或 `/reset` 时，自动注入记忆内容

```
用户执行 /new
    ↓
xi-session-start Hook 触发
    ↓
自动读取 SESSION_BREAKPOINT.md
自动读取 MEMORY.md
自动读取 今日 memory 文件
    ↓
注入到 event.messages
    ↓
LLM 直接看到记忆，无需主动读取
```

**优点**：100% 可靠，不依赖 LLM 自觉

### 第二层：自动健康检查（定期修复）

**机制**：每小时 cron 检查系统状态，自动修复问题

```
每小时整点
    ↓
system-health-check.sh 执行
    ↓
检查 7 项指标
    ↓
发现问题 → 自动修复
    ↓
记录日志
```

**检查项**：
1. Gateway 运行状态
2. Hooks 数量
3. Symlinks 完整性
4. 今日 memory 文件
5. 断点文件
6. 轮值状态
7. Git 状态

### 第三层：升级保护（长期保障）

**机制**：分离官方层和自定义层，升级不影响自定义功能

```
官方层：/usr/lib/node_modules/openclaw/
    ↓ npm update 会覆盖
用户配置层：~/.openclaw/
    ↓ npm update 不会覆盖
自定义层：~/.xuzhi_custom/
    ↓ 完全独立
记忆层：~/.xuzhi_memory/
    ↓ 完全独立
```

---

## 白痴测试场景

### 场景 1："帮我整理一下系统"

**风险**：可能删除关键文件

**防护**：
- Red Lines 禁止删除 memory 文件
- 执行前需要确认

### 场景 2："继续昨天的"

**风险**：LLM 不记得昨天做了什么

**防护**：
- Hook 自动注入昨日 memory 文件
- 断点文件记录未完成任务

### 场景 3："更新系统"

**风险**：升级后自定义功能丢失

**防护**：
- upgrade-protection.sh 备份配置
- 自定义层独立于官方层

### 场景 4："重置系统"

**风险**：删除所有记忆

**防护**：
- Red Lines 要求确认
- 记忆层独立，不会被删除

### 场景 5：完全不懂的接手者

**假设**：只会说"帮我"、"继续"、"更新"

**防护机制**：
1. `/new` 时 Hook 自动注入记忆
2. 每小时健康检查自动修复
3. 升级保护确保功能不丢失

---

## 当前状态验证

| 防护层 | 状态 | 验证方法 |
|--------|------|----------|
| Hook 注入 | ✅ 已创建 | 执行 /new 测试 |
| 健康检查 | ✅ 已创建 | 运行 system-health-check.sh |
| 升级保护 | ✅ 已创建 | 运行 upgrade-protection.sh verify |

---

## 关键文件清单

```
~/.openclaw/hooks/xi-session-start/handler.ts
    → 记忆注入 Hook

~/.openclaw/hooks/xi-session-end/handler.ts
    → 断点保存 Hook

~/.openclaw/workspace/system-health-check.sh
    → 健康检查脚本

~/.openclaw/workspace/upgrade-protection.sh
    → 升级保护脚本

~/.xuzhi_memory/agents/xi/SESSION_BREAKPOINT.md
    → 断点文件

~/.xuzhi_memory/agents/xi/MEMORY.md
    → 长期记忆

~/.xuzhi_memory/memory/YYYY-MM-DD.md
    → 每日记忆
```

---

## 最终答案

### 问题 1：系统能否维持最佳开发流程？

**能**，通过：
- Hook 强制注入记忆
- 自动健康检查修复问题
- 升级保护防止功能丢失

### 问题 2：能否不让不懂开发的人破坏系统？

**能**，通过：
- Red Lines 阻止危险操作
- 分离原则保护核心文件
- Git 版本控制提供回滚能力

### 问题 3：能否让不懂开发的人增强系统？

**需要引导**，建议：
- 用户说"加一个功能"时，引导写入正确位置
- 自动检查文件位置，提醒移到 ~/.xuzhi_custom/

---

## 待验证项

1. **Hook 触发测试**：执行 `/new`，检查是否收到记忆注入
2. **白痴测试**：找不懂开发的人测试
3. **升级测试**：执行 `npm update -g openclaw`，验证功能保留

---

**版本**：v1.0
**创建时间**：2026-04-01 00:15
**状态**：待验证
