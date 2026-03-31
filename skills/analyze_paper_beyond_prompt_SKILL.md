# analyze_paper_beyond_prompt — CoT驱动论文分析技能

**技能ID**: analyze_paper_beyond_prompt  
**类型**: 任务分解 / 分析策略  
**位置**: `~/.xuzhi_memory/skills/analyze_paper_beyond_prompt.py`  
**参考**: Beyond the Prompt (arXiv:2603.10000) — CoT激活任务分解能力  
**创建**: 2026-03-27

---

## 核心原则

来自论文的理论洞见：

> CoT激活模型的**任务分解能力**——将复杂问题分解为预训练阶段已掌握的简单子任务序列。

**不要**给复杂任务直接答案。**给复杂任务一个分解路线图**。

---

## 功能

将论文分析任务分解为6个原子任务序列：

1. 元信息提取 → metadata.json
2. 核心主张提取 → claims.json
3. 结构化摘要 → summary.md
4. 批判性评估 → critique.json
5. 跨论文关联 → 关联报告.md
6. 系统归档 → memory/ + skills/

---

## 使用方法

```bash
python3 ~/.xuzhi_memory/skills/analyze_paper_beyond_prompt.py <arxiv_id>
```

---

## 理论基础

- **Beyond the Prompt Theorem 26**：CoT的实质是提供推理路线图，而非增加计算深度
- **任务分解**使复杂问题能被映射到预训练中已掌握的能力单元
- 这与AgentFactory的subagent积累原则一致

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| 0.1 | 2026-03-27 | 初始版本，基于CoT理论框架 |
