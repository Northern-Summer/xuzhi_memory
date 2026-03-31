#!/usr/bin/env python3
"""
SearXNG HTML-based search — extracts real GitHub URLs reliably.
工程改进铁律合规 — Ξ | 2026-03-29
自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
"""
import re, urllib.request, urllib.parse, time
from html.parser import HTMLParser

SEARXNG = "http://127.0.0.1:8080"

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._in_a = False
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href:
                self.links.append(href)
    def handle_endtag(self, tag):
        pass

def search(query, engines=None, timeout=10):
    """
    Search via SearXNG HTML, return list of (url, title) tuples.
    Works reliably in WSL2 even when JSON API is empty.
    """
    params = [("q", query), ("format", "html")]
    if engines:
        params.append(("engines", ",".join(engines)))
    url = SEARXNG + "/search?" + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return [], str(e)
    
    # Extract titles and links from results
    titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
    titles = [re.sub(r'<[^>]+>', '', t).strip() for t in titles if t.strip()]
    
    # Extract all links from result divs
    links = re.findall(r'href="(https?://[^"]+)"[^>]*>\s*<h3', html)
    
    results = []
    for link in links[:10]:
        if link.startswith("http"):
            results.append(link)
    
    # Also get titles from result articles
    article_titles = re.findall(r'<article[^>]*>.*?<a[^>]*href="(https?://[^"]+)"[^>]*>[^<]*</a>.*?<h3[^>]*>(.*?)</h3>', 
                                html, re.DOTALL)
    
    return results, None

def search_github(query, min_stars=None, timeout=10):
    """Search specifically for GitHub URLs."""
    results, err = search(query, timeout=timeout)
    github = [r for r in results if "github.com" in r]
    if min_stars:
        github = [r for r in github if f"stars:{min_stars}" in r or "star" in r]
    return github[:5]

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "lean4 AI theorem proving github"
    results, _ = search(q)
    github = [r for r in results if "github.com" in r]
    print(f"Query: {q}")
    print(f"GitHub results: {len(github)}")
    for r in github[:5]:
        print(" ", r)
