# 六层记忆系统审计工具

> 写入时间: 2026-03-26 16:00 GMT+8

---

## 六层抽象（从外到内）

| 层 | 名称 | 位置 | 说明 |
|----|------|------|------|
| 1 | L1共享记忆 | `/home/summer/.xuzhi_memory/memory/*.md` | 所有agent共享 |
| 2 | Agent私有记忆 | `/home/summer/.xuzhi_memory/agents/{agent}/memory/*.md` | 各agent私有 |
| 3 | 记忆加载机制 | `workspace-xi/AGENTS.md` | 读取路径定义 |
| 4 | Bootstrap注入 | `workspace-xi/SOUL.md`, `IDENTITY.md` | 身份注入system prompt |
| 5 | OpenClaw注册 | `/home/summer/.openclaw/agents/{code}.json` | agent配置 |
| 6 | 真实session | `/home/summer/.openclaw/agents/{code}/sessions/` | 实际运行态 |

---

## 审计命令

### Layer 1: L1共享记忆
```bash
ls /home/summer/.xuzhi_memory/memory/*.md
```

### Layer 2: Agent私有记忆
```bash
for agent in phi delta theta gamma omega psi xi rho; do
  echo "$agent: $(ls /home/summer/.xuzhi_memory/agents/$agent/memory/*.md 2>/dev/null | wc -l) files"
done
```

### Layer 3: AGENTS.md路径
```bash
grep "memory\|L1\|L2" /home/summer/.openclaw/workspace-xi/AGENTS.md
```

### Layer 4: Bootstrap文件
```bash
cat /home/summer/.openclaw/workspace-xi/SOUL.md | head -5
```

### Layer 5: Agent注册
```bash
cat /home/summer/.openclaw/agents/{code}.json
```

### Layer 6: 真实session
```bash
ls /home/summer/.openclaw/agents/{code}/sessions/sessions.json
```

---

## 已知问题清单

### ❌ Layer 2: Agent私有memory/目录大部分缺失
- 只有 phi/memory/2026-03-25.md 存在
- 其他所有agent的私有今日日志缺失
- AGENTS.md说"写memory/YYYY-MM-DD.md"，但没有强制机制

### ❌ Layer 3: AGENTS.md路径指向错误
- 说"读 memory/YYYY-MM-DD.md"（workspace-xi内，不存在）
- 应指向 `/home/summer/.xuzhi_memory/agents/{agent}/memory/`

---

## 修复原则

1. 永远不删除任何现有文件
2. 永远用write工具创建文件（绝对路径）
3. 修复后立即验证
4. 每次修复写入audit日志
