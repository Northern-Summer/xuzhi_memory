# 工具路径展开Bug — 致命教训

> 写入时间: 2026-03-26 14:47 GMT+8

---

## Bug描述

**exec工具和write工具的`~`展开不同：**

| 工具 | `~` 展开为 | 结果 |
|------|-----------|------|
| `exec` (bash) | `/home/summer/` | 含点目录 |
| `write` (OpenClaw) | `/home/summer/` | **无点目录！** |

也就是说：

| 路径写法 | exec 访问 | write 访问 |
|---------|-----------|------------|
| `~/.xuzhi_memory/` | `/home/summer/.xuzhi_memory/` ✅ | `/home/summer/xuzhi_memory/` ❌ |
| `~/.openclaw/` | `/home/summer/.openclaw/` | `/home/summer/openclaw/` ❌ |

---

## 后果

- 所有 `write` 工具写入 `~/.xuzhi_memory/` 的文件，全部写到了 `/home/summer/xuzhi_memory/`（无点）
- `/home/summer/xuzhi_memory/` 不是 git 仓库
- 所有 BOOTSTRAP.md 等重要文件，写到了错误位置

---

## 正确做法

**永远使用绝对路径，永远不使用 `~`：**

```
/home/summer/.xuzhi_memory/agents/phi/BOOTSTRAP.md  ✅
~/.xuzhi_memory/agents/phi/BOOTSTRAP.md            ❌ 可能错误
```

---

## 受影响的文件（2026-03-26）

通过 write 工具写到错误位置的所有文件，需要复制到正确位置并删除错误副本。

---

## 教训

**工具不熟悉，会导致系统崩溃。这是基本功。**
