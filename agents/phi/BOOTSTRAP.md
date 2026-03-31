# BOOTSTRAP.md — Φ 启动协议

## 记忆系统：树干一支，分叉各各不同

**唯一不共享的：** 自身的身份和人格。
**必须共享的：** 除上述之外的一切系统变更。

---

## 记忆的层次（所有Agent完全相同）

| 层次 | 位置 | 共享？ |
|------|------|--------|
| 启动层 | `~/.xuzhi_memory/agents/{agent}/` | ✅ 机制同，内容异 |
| 私有L1 | `~/.xuzhi_memory/agents/{agent}/memory/` | ❌ 私有 |
| 私有L2 | `~/.xuzhi_memory/agents/{agent}/MEMORY.md` | ❌ 私有 |
| 意图追踪 | `~/.xuzhi_memory/agents/{agent}/intent_log.jsonl` | ❌ 私有 |

**共享树干：**
| `~/.xuzhi_memory/memory/` | ✅ 系统全局日志 |
| `~/.xuzhi_memory/manifests/` | ✅ 宪法核心 |

---

## 启动流程

1. 读 BOOTSTRAP.md
2. 读 constitutional_core.md
3. 读 SOUL.md
4. 读 IDENTITY.md
5. 读私有L1 + 共享memory/
6. 感知+决策+执行
7. 记录intent_log + 当日日志

## 实时共享原则

- 系统架构变更 → `memory/`
- 新agent降生 → `manifests/constitutional_core.md`
- 消亡/禁用 → `ratings.json`
