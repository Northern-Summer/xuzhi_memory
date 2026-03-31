# 系统架构规范 v1.0 — 统领一切

> 状态：2026-03-31 创建
> 维护者：Ξ
> 用途：统御整个系统的变化，新增功能时必须遵守

---

## 一、文件位置规范（最高优先级）

### 1.1 Agent 配置文件

| 文件类型 | 规范位置 | 读取优先级 | 说明 |
|----------|----------|------------|------|
| Agent 注册 | `~/.openclaw/agents/<agent>.json` | 唯一 | OpenClaw 读取 |
| AGENTS.md | `~/.openclaw/agents/<agent>/workspace/AGENTS.md` | 1 | OpenClaw 注入 |
| AGENTS.md (备用) | `~/.xuzhi_memory/agents/<agent>/AGENTS.md` | 2 | 仅用于 git 追踪 |
| SOUL.md | `~/.xuzhi_memory/agents/<agent>/SOUL.md` | 唯一 | 身份定义 |
| IDENTITY.md | `~/.xuzhi_memory/agents/<agent>/IDENTITY.md` | 唯一 | 角色定义 |
| HEARTBEAT.md | `~/.openclaw/agents/<agent>/workspace/HEARTBEAT.md` | 唯一 | 心跳指令 |
| MEMORY.md | `~/.xuzhi_memory/agents/<agent>/MEMORY.md` | 唯一 | 长期记忆 |

**冲突规则**：
- workspace/ 下的文件优先级高于 xuzhi_memory/
- 两者内容不同时，以 workspace/ 为准，但需同步到 xuzhi_memory/

### 1.2 记忆文件

| 文件类型 | 规范位置 | 说明 |
|----------|----------|------|
| 共享 L1 | `~/.xuzhi_memory/memory/YYYY-MM-DD.md` | 所有 agent 共享 |
| 私有 L1 | `~/.xuzhi_memory/agents/<agent>/memory/` | 各 agent 独立 |
| L2 规范 | `~/.xuzhi_memory/manifests/` | 架构/宪法/规范 |
| L3 归档 | `~/.xuzhi_memory/backup/` | 灾难恢复 |

### 1.3 脚本文件

| 脚本类型 | 规范位置 | 说明 |
|----------|----------|------|
| 系统脚本 | `~/xuzhi_genesis/scripts/` | 记忆同步、健康检查等 |
| Agent 专用 | `~/.xuzhi_memory/agents/<agent>/scripts/` | 各 agent 私有脚本 |
| Cron 脚本 | `~/xuzhi_genesis/scripts/cron/` | 定时任务 |

**禁止**：同一脚本存在多个位置（如 agent_registration.sh 有 4 个版本）

---

## 二、Agent 轮值规范

### 2.1 轮值计算

```bash
TODAY=$(date +%-d)
ON_DUTY=$((TODAY % 7))
# 0=phi, 1=delta, 2=gamma, 3=theta, 4=omega, 5=psi, 6=xi
```

### 2.2 HEARTBEAT.md 标准模板

**所有 agent 的 HEARTBEAT.md 必须以轮值检查开头：**

```markdown
# HEARTBEAT.md — <Agent名称>

## 轮值检查（最高优先级）

```bash
TODAY=$(date +%-d)
ON_DUTY=$((TODAY % 7))
# 0=phi, 1=delta, 2=gamma, 3=theta, 4=omega, 5=psi, 6=xi
# 我的轮值日: <数字>

if [ $ON_DUTY -ne <我的轮值日> ]; then
  echo "非轮值日，返回 HEARTBEAT_OK"
  exit 0
fi
```

## 检查清单
- 确认自己仍在运行
- 检查上次心跳以来是否有新消息或任务
- 有紧急事项需要报告则报告，否则回复 HEARTBEAT_OK
```

### 2.3 当前轮值映射

| Agent | 轮值日 | 数字 |
|-------|--------|------|
| Φ (phi) | 周日 | 0 |
| Δ (delta) | 周一 | 1 |
| Γ (gamma) | 周二 | 2 |
| Θ (theta) | 周三 | 3 |
| Ω (omega) | 周四 | 4 |
| Ψ (psi) | 周五 | 5 |
| Ξ (xi/main) | 周六 | 6 |

---

## 三、新增功能检查清单

### 3.1 新增 Agent 时

```markdown
[ ] 1. 创建 ~/.openclaw/agents/<agent>.json
[ ] 2. 创建 ~/.openclaw/agents/<agent>/workspace/ 目录
[ ] 3. 创建 workspace/AGENTS.md（必须以自己名字开头）
[ ] 4. 创建 workspace/HEARTBEAT.md（包含轮值检查）
[ ] 5. 创建 ~/.xuzhi_memory/agents/<agent>/ 目录
[ ] 6. 创建 SOUL.md（身份定义）
[ ] 7. 创建 IDENTITY.md（角色定义）
[ ] 8. 创建 memory/ 目录
[ ] 9. 添加到轮值映射表
[ ] 10. 运行健康检查验证
```

### 3.2 新增脚本时

```markdown
[ ] 1. 确定脚本类型（系统/Agent专用/Cron）
[ ] 2. 放入规范位置（见 1.3）
[ ] 3. 检查是否与现有脚本重复
[ ] 4. 添加注释：用途、触发条件、依赖
[ ] 5. 添加到本文档的"脚本清单"
```

### 3.3 新增配置项时

```markdown
[ ] 1. 确定配置类型（Agent级/系统级）
[ ] 2. 确定存储位置（json/md/shell变量）
[ ] 3. 检查是否与现有配置冲突
[ ] 4. 更新相关文档
[ ] 5. 测试配置读取优先级
```

### 3.4 修改现有功能时

```markdown
[ ] 1. 搜索所有相关文件（见搜索命令）
[ ] 2. 列出所有需要修改的位置
[ ] 3. 确保所有位置同步修改
[ ] 4. 更新本文档（如有架构变化）
[ ] 5. 运行健康检查验证
```

---

## 四、搜索命令（快速定位）

```bash
# 搜索所有 AGENTS.md
find ~/.openclaw ~/.xuzhi_memory -name "AGENTS.md" -type f

# 搜索所有 HEARTBEAT.md
find ~ -name "HEARTBEAT.md" -type f 2>/dev/null | grep -v ".cache"

# 搜索特定 Agent 的所有文件
ls -la ~/.openclaw/agents/<agent>/workspace/
ls -la ~/.xuzhi_memory/agents/<agent>/

# 检查脚本重复
find ~ -name "*.sh" -type f 2>/dev/null | xargs -I{} basename {} | sort | uniq -c | sort -rn | head -10

# 检查配置冲突
for f in ~/.openclaw/agents/*.json; do echo "--- $(basename $f) ---"; grep '"model"' "$f"; done
```

---

## 五、配置优先级（冲突时）

```
1. OpenClaw 注入（workspace/ 下的文件）
   ↓
2. Git 追踪（xuzhi_memory/ 下的文件）
   ↓
3. 环境变量
   ↓
4. 硬编码默认值
```

---

## 六、禁止行为

- ❌ 在 xuzhi_memory 创建与 workspace 相同的文件但不同步
- ❌ 同一脚本存在多个位置
- ❌ 新增 Agent 时不添加轮值检查
- ❌ 修改配置时不检查所有相关文件
- ❌ 跳过健康检查

---

## 七、定期一致性检查

**频率**：每周一 09:00（cron）

**检查项**：
1. AGENTS.md 是否有两个版本且不同
2. HEARTBEAT.md 是否缺少轮值检查
3. 脚本是否有重复
4. 配置是否有冲突

**脚本**：`~/xuzhi_genesis/scripts/system_consistency_check.sh`

---

## 八、脚本清单

| 脚本 | 位置 | 用途 |
|------|------|------|
| memory_sync.sh | ~/xuzhi_genesis/scripts/ | 记忆同步 |
| memory_health_check.sh | ~/xuzhi_genesis/scripts/ | 记忆健康检查 |
| memory_push.sh | ~/xuzhi_genesis/scripts/ | 一键推送 |
| system_consistency_check.sh | ~/xuzhi_genesis/scripts/ | 系统一致性检查（待创建） |

---

## 九、变更日志

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-03-31 | 创建本文档 | 解决反复搜查问题 |

---

**本文档是系统的最高规范，所有变更必须遵守。**
