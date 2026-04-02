# 最优雅解法：三层防护 + Git 追踪

> 审计时间：2026-04-02 13:44
> 原则：最小改动、最大效果、最可持续

---

## 一、问题本质

| 问题 | 根因 | 影响 |
|------|------|------|
| chmod 444 不能防删除 | Linux 权限模型缺陷 | Delta MEMORY.md 被删 |
| Agent 同一用户运行 | 无法用文件权限区分 | 无法技术强制隔离 |
| 断点可能覆盖 | 上下文压缩丢失信息 | 需要持久化保护 |

---

## 二、最优雅解法

### 核心架构：三层防护

```
Layer 1: Git 追踪（可恢复）
Layer 2: VERSION_LOCK.json（可验证）
Layer 3: pre-commit Hook（可警告）
```

### 为什么是最优雅？

| 特性 | 说明 |
|------|------|
| 最小改动 | 只需添加 Hook，无需修改系统配置 |
| 最大效果 | 所有修改可追踪、可验证、可恢复 |
| 最可持续 | 不依赖特定用户、不会过时 |
| 不会被断点打断 | 保护机制在 Git 层，不受 Agent 上下文影响 |

---

## 三、具体实施

### 1. Git 作为唯一真相源

**原理**：所有修改必须通过 Git

```
Agent 修改文件 → Git add → Git commit → Hook 检查 → 记录历史
                    ↓
              如果出问题 → Git revert → 恢复
```

**优点**：
- 天然审计追踪
- 天然版本控制
- 天然恢复能力
- 不依赖 Agent 记忆

### 2. VERSION_LOCK.json 验证

**原理**：记录正确版本的 SHA256

```json
{
  "agents/phi/MEMORY.md": {
    "sha256": "219abc58b2101fc36fac...",
    "locked_at": "2026-04-02T00:56:00+08:00",
    "locked_by": "user"
  }
}
```

**验证脚本**：

```bash
#!/bin/bash
# verify_memory_integrity.sh
cd ~/.xuzhi_memory
jq -r '.locked_files | to_entries[] | "\(.key) \(.value.sha256)"' VERSION_LOCK.json | \
while read file expected_sha; do
  if [ -f "$file" ]; then
    actual_sha=$(sha256sum "$file" | cut -d' ' -f1)
    if [ "$actual_sha" != "$expected_sha" ]; then
      echo "❌ $file 被篡改"
      echo "   预期: $expected_sha"
      echo "   实际: $actual_sha"
    fi
  else
    echo "❌ $file 不存在"
  fi
done
```

### 3. pre-commit Hook 警告

**原理**：修改其他 Agent 的文件时警告

```bash
#!/bin/bash
# 检查跨 Agent 修改
CURRENT_AGENT=$(git config user.name 2>/dev/null || echo "unknown")

for file in $(git diff --cached --name-only); do
  if [[ $file =~ agents/([^/]+)/MEMORY.md ]]; then
    TARGET_AGENT=${BASH_REMATCH[1]}
    if [ "$CURRENT_AGENT" != "$TARGET_AGENT" ] && [ "$CURRENT_AGENT" != "main" ]; then
      echo "⚠️ $CURRENT_AGENT 正在修改 $TARGET_AGENT 的 MEMORY.md"
      echo "   建议：各人自扫门前雪，莫管他人瓦上霜。"
    fi
  fi
done
```

---

## 四、不会被断点打断的原因

| 保护层 | 位置 | 断点影响 |
|--------|------|----------|
| Git 追踪 | 文件系统 + 远程仓库 | ❌ 不受影响 |
| VERSION_LOCK.json | 文件系统 | ❌ 不受影响 |
| pre-commit Hook | Git 配置 | ❌ 不受影响 |

**关键**：保护机制在 Agent 之外，不依赖 Agent 的上下文或记忆。

---

## 五、恢复流程

如果文件被意外删除或修改：

```bash
# 1. 检查 Git 历史
git log --oneline -- agents/phi/MEMORY.md

# 2. 恢复到正确版本
git checkout <commit> -- agents/phi/MEMORY.md

# 3. 验证 SHA256
sha256sum agents/phi/MEMORY.md

# 4. 与 VERSION_LOCK.json 对比
jq '.locked_files."agents/phi/MEMORY.md".sha256' VERSION_LOCK.json
```

---

## 六、与行业方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| 不同用户 | 最安全 | 管理复杂，影响协作 |
| chattr +i | 防删除 | 无法进化 |
| Docker 隔离 | 完全隔离 | 资源开销大 |
| **Git 追踪** | **最小改动，最大效果** | 需要事后恢复 |

---

## 七、最终建议

### 已实施

1. ✅ Git 追踪所有修改
2. ✅ VERSION_LOCK.json 锁定正确版本
3. ✅ pre-commit Hook 警告跨 Agent 修改
4. ✅ checksum_baseline.txt 记录每个 Agent 的哈希
5. ✅ 删除危险的 memory_sync.sh

### 建议添加

1. 定期运行验证脚本（每 6 小时）
2. 验证失败时发送告警到微信
3. 自动恢复到 VERSION_LOCK 锁定的版本

---

## 八、验证脚本

```bash
#!/bin/bash
# ~/.openclaw/workspace/verify_memory_integrity.sh
# 每 6 小时运行一次

cd ~/.xuzhi_memory

ISSUES=""

# 检查每个 Agent 的 MEMORY.md
for agent in phi delta theta gamma omega psi; do
  file="agents/$agent/MEMORY.md"
  if [ -f "$file" ]; then
    expected=$(jq -r ".locked_files.\"$file\".sha256" VERSION_LOCK.json 2>/dev/null)
    actual=$(sha256sum "$file" | cut -d' ' -f1)
    if [ "$expected" != "null" ] && [ "$expected" != "$actual" ]; then
      ISSUES="$ISSUES\n❌ $agent MEMORY.md 被篡改"
    fi
  else
    ISSUES="$ISSUES\n❌ $agent MEMORY.md 不存在"
  fi
done

# 如果有问题，发送告警
if [ -n "$ISSUES" ]; then
  openclaw message send --channel openclaw-weixin \
    --target "o9cq80z9eOrqJasg6hB1W-Cc4-Po@im.wechat" \
    --message "⚠️ 记忆完整性验证失败:$ISSUES"
fi
```

---

## 九、总结

```
═══════════════════════════════════════════════════════════════
【最优雅解法】
═══════════════════════════════════════════════════════════════

核心：Git 作为唯一真相源

三层防护：
  1. Git 追踪 → 可恢复
  2. VERSION_LOCK.json → 可验证
  3. pre-commit Hook → 可警告

特性：
  ✅ 最小改动：只需 Hook，无需修改系统
  ✅ 最大效果：所有修改可追踪、可验证、可恢复
  ✅ 最可持续：不依赖 Agent 上下文
  ✅ 不会被断点打断：保护机制在 Git 层

核心原则：
  各人自扫门前雪，莫管他人瓦上霜。

═══════════════════════════════════════════════════════════════
```
