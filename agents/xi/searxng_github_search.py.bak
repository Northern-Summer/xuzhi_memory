#!/usr/bin/env python3
"""
searxng_github_search.py — SearXNG GitHub-focused search
Uses subprocess+curl (known to work) + proper URL encoding.
工程改进铁律合规 — Ξ | 2026-03-29
自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
"""
import subprocess, re, sys, urllib.parse

SEARXNG = "http://127.0.0.1:8080"

def search(query, timeout=12):
    """
    Search via SearXNG HTML, extract GitHub URLs.
    Returns list of unique GitHub repo URLs.
    """
    encoded_q = urllib.parse.quote(query)
    url = f"{SEARXNG}/search?q={encoded_q}&format=html"
    
    cmd = ["curl", "-s", "--max-time", str(timeout), "--get", url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
        html = result.stdout
    except Exception as e:
        return [], str(e)
    
    if not html:
        return [], "Empty response"
    
    # Extract unique github.com URLs
    links = re.findall(r'href="(https?://github\.com/[^"]+)"', html)
    seen = set()
    unique = []
    BLOCKED = {"searxng/searxng", "searxng/searxng-issues"}
    for link in links:
        clean = link.split("?")[0].split("#")[0]
        # Skip searxng self-references and archive links
        if any(b in clean for b in BLOCKED):
            continue
        if clean not in seen:
            seen.add(clean)
            unique.append(clean)
    
    return unique[:10], None

def search_github(query, timeout=12):
    """Search for GitHub repos matching query."""
    links, err = search(query, timeout)
    if err:
        return [], err
    repos = [l for l in links if "github.com" in l]
    return repos[:8], None

def get_title(url, timeout=5):
    """Get repo name from GitHub URL."""
    m = re.match(r'https://github\.com/([^/]+)/([^/]+)', url)
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    return url

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "AI agent framework"
    print(f"Query: {q}")
    repos, err = search_github(q)
    if err:
        print(f"Error: {err}")
    else:
        print(f"GitHub results: {len(repos)}")
        for r in repos:
            print(f"  {get_title(r)} | {r}")
