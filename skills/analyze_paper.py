#!/usr/bin/env python3
"""
analyze_paper.py — Xuzhi PaperMind 分析脚本模板
参考：AgentFactory (arXiv:2603.18000) 可执行技能原则
位置：~/.xuzhi_memory/skills/analyze_paper.py

使用方法：
    python3 ~/.xuzhi_memory/skills/analyze_paper.py <arxiv_id> [output_dir]

输出：
    - {arxiv_id}_report.md      # 结构化分析报告
    - {arxiv_id}_claims.json    # 核心主张列表
    - {arxiv_id}_metadata.json  # 元信息

每篇论文分析流程：
    1. 解析输入（arxiv ID 或 URL）
    2. 获取摘要（web_fetch arxiv abs页面）
    3. 生成结构化报告（PaperMind工作流）
    4. 输出claims + metadata
"""

import sys
import json
import re
import subprocess
from pathlib import Path

# === 配置 ===
SKILLS_DIR = Path.home() / ".xuzhi_memory" / "skills"
OUTPUT_DIR = Path.home() / ".xuzhi_memory" / "memory" / "papers"

# === PaperMind 工作流 ===

def extract_arxiv_id(input_str: str) -> str:
    """从URL或直接ID提取arxiv编号"""
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+)',
        r'(\d+\.\d+)',
    ]
    for p in patterns:
        m = re.search(p, input_str)
        if m:
            return m.group(1)
    return input_str.strip()

def fetch_abstract(arxiv_id: str) -> dict:
    """使用web_fetch获取摘要"""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    # 此处调用实际web_fetch工具（通过subprocess调用Python脚本或API）
    # 简化版：返回占位符
    return {
        "url": url,
        "arxiv_id": arxiv_id,
        "title": "",  # 需从实际fetch中提取
        "authors": [],
        "abstract": "",
        "submitted": "",
    }

def extract_metadata(text: str) -> dict:
    """从页面文本提取元信息"""
    # 简化版：正则提取标题、作者
    title_match = re.search(r'<title>([^<]+)</title>', text)
    return {
        "title": title_match.group(1) if title_match else "Unknown",
    }

def analyze_claims(abstract: str) -> list:
    """提取核心主张（简化版，实际需要更复杂NLP）"""
    # 这里应实现主张提取逻辑
    return []

def generate_report(metadata: dict, claims: list) -> str:
    """生成PaperMind格式报告"""
    report = f"""# 论文分析报告：{metadata.get('title', 'Unknown')}

## 元信息
- **arXiv**: {metadata.get('arxiv_id')}
- **作者**：{', '.join(metadata.get('authors', []))}

## 结构化摘要
（待填充）

## 核心主张
"""
    for i, c in enumerate(claims, 1):
        report += f"{i}. {c}\n"
    return report

def main():
    if len(sys.argv) < 2:
        print("用法: python3 analyze_paper.py <arxiv_id_or_url>")
        sys.exit(1)
    
    arxiv_id = extract_arxiv_id(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 步骤1：获取摘要
    data = fetch_abstract(arxiv_id)
    
    # 步骤2：提取claims
    claims = analyze_claims(data["abstract"])
    
    # 步骤3：生成报告
    report = generate_report(data, claims)
    
    # 步骤4：保存
    report_file = output_dir / f"{arxiv_id}_report.md"
    claims_file = output_dir / f"{arxiv_id}_claims.json"
    
    report_file.write_text(report)
    claims_file.write_text(json.dumps(claims, ensure_ascii=False, indent=2))
    
    print(f"✓ 分析完成: {report_file}")

if __name__ == "__main__":
    main()
