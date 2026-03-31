#!/usr/bin/env python3
"""
fetch_arxiv_abstract.py — 从 arxiv.org 提取论文摘要
使用 web_fetch（OpenClaw 内置），不依赖 curl

用法:
  python3 fetch_arxiv_abstract.py 2603.22281
  python3 fetch_arxiv_abstract.py 2603.22281 2603.18000

工程改进铁律合规 — Ξ | 2026-03-27
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
"""
import sys
import json
import subprocess
import re

def fetch_abstract(arxiv_id: str) -> dict:
    """抓取单篇 arxiv 论文的摘要"""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    try:
        result = subprocess.run(
            ["python3", "-c", f"""
import subprocess
result = subprocess.run(['curl', '-s', '--connect-timeout', '10', '-H', 'User-Agent: Mozilla/5.0', '{url}'], capture_output=True, text=True, timeout=15)
print(result.stdout)
"""],
            capture_output=True,
            text=True,
            timeout=20
        )
        html = result.stdout
        
        # 提取 meta citation_abstract
        match = re.search(r'<meta name="citation_abstract" content="([^"]*)"', html, re.DOTALL)
        if match:
            abstract = match.group(1)
            # HTML entity decode
            abstract = abstract.replace('&#39;', "'").replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            return {"arxiv_id": arxiv_id, "abstract": abstract, "status": "ok"}
        
        # 备用：从 HTML 中提取
        match2 = re.search(r'class="abstract mathjax">\s*<p>(.*?)</p>', html, re.DOTALL)
        if match2:
            abstract = match2.group(1)
            abstract = re.sub(r'<[^>]+>', '', abstract).strip()
            return {"arxiv_id": arxiv_id, "abstract": abstract, "status": "ok_fallback"}
        
        return {"arxiv_id": arxiv_id, "abstract": None, "status": "not_found", "html_snippet": html[:500]}
    
    except Exception as e:
        return {"arxiv_id": arxiv_id, "abstract": None, "status": "error", "error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("用法: fetch_arxiv_abstract.py <arxiv_id> [arxiv_id ...]")
        print("例: fetch_arxiv_abstract.py 2603.22281 2603.18000")
        sys.exit(1)
    
    arxiv_ids = sys.argv[1:]
    results = []
    
    for aid in arxiv_ids:
        aid = aid.strip()
        if not aid:
            continue
        result = fetch_abstract(aid)
        results.append(result)
        
        if result["status"] == "ok" or result["status"] == "ok_fallback":
            abstract_preview = result["abstract"][:200] + "..." if len(result["abstract"]) > 200 else result["abstract"]
            print(f"✅ {aid}: {abstract_preview}")
        else:
            print(f"❌ {aid}: {result['status']}")
    
    # 输出 JSON 供程序消费
    print(f"\n--- JSON OUTPUT ({len(results)} papers) ---")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
