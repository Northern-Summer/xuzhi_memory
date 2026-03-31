#!/usr/bin/env python3
"""
fetch_missing_abstracts.py — 抓取 changes.json 中缺失的论文摘要
工程改进铁律合规 — Ξ | 2026-03-28
自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES

每次运行：
1. 读取 changes.json 的所有 arxiv IDs
2. 对比 abstracts.json 中已有的 ID
3. 对缺失的批量抓取（每批5条，间隔2秒）
4. 追加到 abstracts.json
"""
import urllib.request
import json
import re
import time
from pathlib import Path

HOME = Path.home()
CHANGES_FILE = HOME / ".xuzhi_memory" / "expert_tracker" / "changes.json"
ABSTRACT_FILE = HOME / ".xuzhi_memory" / "expert_tracker" / "abstracts.json"
FETCH_LOG = HOME / ".xuzhi_memory" / "expert_tracker" / "abstract_fetch.log"

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def extract_arxiv_ids(changes_file):
    """从 changes.json 提取所有 arxiv ID"""
    data = json.loads(changes_file.read_text())
    ids = set()
    for item in data.get("changes", []):
        url = item.get("new_url", "")
        match = re.search(r'(\d+\.\d+)', url)
        if match:
            ids.add(match.group(1))
    return ids

def load_existing_abstracts(abstract_file):
    """加载已有 abstract 的 ID 集合"""
    if not abstract_file.exists():
        return set()
    try:
        data = json.loads(abstract_file.read_text())
        if isinstance(data, list):
            return {item["arxiv_id"] for item in data}
        return set(data.keys())
    except Exception:
        return set()

def fetch_abstract(arxiv_id):
    """抓取单篇摘要"""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8")
        
        m = re.search(r'<meta name="citation_abstract" content="([^"]*)"', html, re.DOTALL)
        if m:
            abstract = m.group(1)
            abstract = (abstract
                .replace('&#39;', "'").replace('&amp;', '&')
                .replace('&lt;', '<').replace('&gt;', '>')
                .replace('&quot;', '"').replace('&#x27;', "'")
                .replace('&nbsp;', ' '))
            return {"arxiv_id": arxiv_id, "abstract": abstract, "status": "ok"}
        
        # 备用：从 HTML 提取
        m2 = re.search(r'class="abstract mathjax">\s*<p>(.*?)</p>', html, re.DOTALL)
        if m2:
            raw = re.sub(r'<[^>]+>', '', m2.group(1)).strip()
            return {"arxiv_id": arxiv_id, "abstract": raw, "status": "ok_fallback"}
        
        return {"arxiv_id": arxiv_id, "abstract": None, "status": "not_found"}
    
    except Exception as e:
        return {"arxiv_id": arxiv_id, "abstract": None, "status": "error", "error": str(e)}

def main():
    changes_ids = extract_arxiv_ids(CHANGES_FILE)
    existing_ids = load_existing_abstracts(ABSTRACT_FILE)
    missing = sorted(changes_ids - existing_ids)
    
    if not missing:
        print(f"✅ 全部 {len(existing_ids)} 篇已有摘要，无需抓取")
        return
    
    print(f"需要抓取: {len(missing)} 篇 | 已有: {len(existing_ids)} 篇")
    
    # 读 abstracts.json
    if ABSTRACT_FILE.exists():
        try:
            existing_data = json.loads(ABSTRACT_FILE.read_text())
            if isinstance(existing_data, list):
                abstracts = existing_data
            else:
                abstracts = existing_data
        except Exception:
            abstracts = []
    else:
        abstracts = []
    
    # 批量抓取（每批5条，间隔2秒）
    BATCH = 5
    fetched = 0
    failed = []
    
    for i in range(0, len(missing), BATCH):
        batch = missing[i:i+BATCH]
        for aid in batch:
            print(f"  [{i+fetched+1}/{len(missing)}] fetching {aid}...", end=" ", flush=True)
            result = fetch_abstract(aid)
            if result["status"] == "ok":
                # 从 changes.json 获取标题
                changes_data = json.loads(CHANGES_FILE.read_text())
                title = None
                for c in changes_data.get("changes", []):
                    if aid in c.get("new_url", ""):
                        title = c.get("new_title", "")
                        break
                result["title"] = title or f"arXiv:{aid}"
                abstracts.append(result)
                print("OK")
            else:
                print(f"FAIL ({result.get('status')})")
                failed.append(aid)
            time.sleep(2)  # 礼貌间隔
        
        # 每批后写一次（防止中途崩溃丢数据）
        ABSTRACT_FILE.write_text(json.dumps(abstracts, indent=2, ensure_ascii=False))
        print(f"  💾 已保存 {len(abstracts)} 篇")
        
        if i + BATCH < len(missing):
            time.sleep(5)  # 批次间暂停
    
    # 写日志
    log_entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_missing": len(missing),
        "fetched": len(missing) - len(failed),
        "failed": failed
    }
    if FETCH_LOG.exists():
        try:
            log_data = json.loads(FETCH_LOG.read_text())
            if not isinstance(log_data, list):
                log_data = [log_data]
        except Exception:
            log_data = []
    else:
        log_data = []
    log_data.append(log_entry)
    FETCH_LOG.write_text(json.dumps(log_data, indent=2, ensure_ascii=False))
    
    print(f"\n✅ 完成: 抓取 {len(missing)-len(failed)}/{len(missing)} | 失败 {len(failed)}")

if __name__ == "__main__":
    main()
