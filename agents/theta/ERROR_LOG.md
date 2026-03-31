# ERROR_LOG.md — Θ 的错误日志

## 2026-03-31 13:16 | 技能缺陷：edit vs write

### 错误描述
反复用 `edit` 工具尝试创建新文件，失败 10+ 次仍不切换到 `write` 工具。

### 错误日志片段
```
{"type":"message","id":"7b0b25c8",...,"content":[{"type":"toolCall","id":"functions.edit:264","name":"edit","arguments":{"file_path":"...grounded_theory.md","path":"...grounded_theory.md"}}]}
{"type":"toolResult","toolCallId":"functions.edit:264","toolName":"edit","content":[{"type":"text","text":"{\n  \"status\": \"error\",\n  \"tool\": \"edit\",\n  \"error\": \"Missing required parameters: oldText alias, newText alias. Supply correct parameters before retrying.\"\n}"]}
... (重复 10+ 次)
```

### 根因
不知道/忘记：
- `write` 工具用于**创建新文件**
- `edit` 工具用于**修改已存在的文件**（需要 oldText/newText）

### 修复
记录为技能：**"创建新文件用 write，修改文件用 edit"**

### 防止再犯
写入 MEMORY.md 技能库：
```
| 技能 | 版本 | 来源 | 代数 |
|------|------|------|------|
| "创建新文件用 write，修改文件用 edit" | v1 | 2026-03-31 会话 | g1 |
```

### 影响
- Session 卡住 10+ 分钟
- 无法完成方法库内容填充
- 需要其他 agent（Ξ）补救
