# analyze_paper — 论文自动化分析技能

**技能ID**: analyze_paper  
**类型**: 数据处理 / 知识提取  
**位置**: `~/.xuzhi_memory/skills/analyze_paper.py`  
**参考**: AgentFactory (arXiv:2603.18000) 可执行技能原则  
**创建**: 2026-03-27

---

## 功能

接收 arXiv ID，自动化执行 PaperMind 论文分析工作流：

1. 获取论文摘要和元信息
2. 提取核心主张（claims）
3. 生成结构化分析报告（Markdown）
4. 输出 claims + metadata（JSON）

---

## 使用方法

```bash
python3 ~/.xuzhi_memory/skills/analyze_paper.py <arxiv_id_or_url> [output_dir]
```

**参数**：
- `<arxiv_id_or_url>`: arXiv ID（如 `2601.03220`）或完整URL
- `[output_dir]`: 可选，输出目录（默认 `~/.xuzhi_memory/memory/papers/`）

**输出**：
- `{arxiv_id}_report.md` — 结构化分析报告
- `{arxiv_id}_claims.json` — 核心主张列表

---

## 输入格式

无特殊输入格式，直接接收 arXiv ID。

---

## 依赖

- Python 3.10+
- web_fetch（通过 subprocess 调用）
- 标准库：re, json, pathlib

---

## 当前状态

- [ ] 完整 HTML 解析（目前仅支持摘要级）
- [ ] 多模型分析对比
- [ ] 跨论文关联分析
- [ ] 增量更新（对比已有分析）

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| 0.1 | 2026-03-27 | 初始模板 |

---

## 相关技能

- `analyze_paper_html.py` — 完整HTML深度解析（待实现）
- `fetch_arxiv.py` — arXiv元数据获取（待实现）
