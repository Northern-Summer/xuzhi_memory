#!/usr/bin/env python3
"""
analyze_paper_beyond_prompt.py — 基于CoT理论的任务分解分析
参考：Beyond the Prompt (arXiv:2603.10000) — CoT激活任务分解能力

核心原则：
- 不要给复杂问题直接答案
- 给复杂问题一个分解路线图
- 将复杂任务映射到预训练阶段已掌握的能力单元

使用方法：
    python3 analyze_paper_beyond_prompt.py <arxiv_id>
"""

import sys
import re
from pathlib import Path

# === 论文分析的任务分解框架 ===

TASK_DECOMPOSITION_TEMPLATE = """
## 任务分解路线图

对于这篇论文的完整分析，将其分解为以下原子任务：

### 原子任务1：元信息提取
- 输入：arxiv URL/ID
- 执行：提取标题、作者、机构、提交日期
- 输出：metadata.json

### 原子任务2：核心主张提取
- 输入：论文摘要 + 全文
- 执行：识别论文明确提出的贡献点（每个附带证据位置）
- 输出：claims.json

### 原子任务3：结构化摘要生成
- 输入：论文全文
- 执行：按背景/方法/结果/结论四部分生成摘要
- 输出：summary.md

### 原子任务4：批判性评估
- 输入：论文全文 + claims
- 执行：评估实验设计/可复现性/结论支持度
- 输出：critique.json

### 原子任务5：跨论文关联
- 输入：claims + 现有知识库
- 执行：与已有论文建立连接，识别模式和矛盾
- 输出：关联报告.md

### 原子任务6：系统归档
- 输入：所有分析产物
- 执行：写入memory/ + 更新skills/ + commit
- 输出：归档确认
"""

def decompose_analysis_task(arxiv_id: str) -> dict:
    """将论文分析任务分解为原子任务序列"""
    return {
        "task_id": arxiv_id,
        "decomposition": [
            {"step": 1, "name": "元信息提取", "input": f"arxiv.org/abs/{arxiv_id}", "output": "metadata.json"},
            {"step": 2, "name": "核心主张提取", "input": "摘要+全文", "output": "claims.json"},
            {"step": 3, "name": "结构化摘要", "input": "全文", "output": "summary.md"},
            {"step": 4, "name": "批判性评估", "input": "全文+claims", "output": "critique.json"},
            {"step": 5, "name": "跨论文关联", "input": "claims+知识库", "output": "关联报告.md"},
            {"step": 6, "name": "系统归档", "input": "所有产物", "output": "memory/ + skills/"},
        ],
        "total_steps": 6,
        "principle": "给复杂任务分解路线图，而非直接要求输出"
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 analyze_paper_beyond_prompt.py <arxiv_id>")
        sys.exit(1)
    
    arxiv_id = sys.argv[1]
    plan = decompose_analysis_task(arxiv_id)
    
    print(f"=== 论文分析任务分解 ===")
    print(f"arxiv: {arxiv_id}")
    print(f"原则: {plan['principle']}")
    print(f"\n分解为 {plan['total_steps']} 个原子任务:\n")
    for step in plan["decomposition"]:
        print(f"  Step {step['step']}: {step['name']}")
        print(f"    输入: {step['input']} → 输出: {step['output']}")
    print(f"\n{TASK_DECOMPOSITION_TEMPLATE}")

if __name__ == "__main__":
    main()
