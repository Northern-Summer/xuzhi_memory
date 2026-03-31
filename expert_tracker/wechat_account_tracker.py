#!/usr/bin/env python3
"""
wechat_account_tracker.py — 微信公众号账号追踪
工程改进铁律合规 — Ξ | 2026-03-29

追踪方式：
  python3 wechat_account_tracker.py list                          # 列出所有账号
  python3 wechat_account_tracker.py AI寒武纪 3                  # 追踪单账号
  python3 wechat_account_tracker.py all                         # 追踪所有账号

原理：每个公众号都有一个唯一 biz ID，wechat_search.py 返回的结果包含 biz，
      用于验证文章是否属于目标账号。

信源档案：~/.xuzhi_memory/expert_tracker/wechat_accounts.json
"""
import sys, re, json, time
from datetime import datetime

ACCOUNTS_FILE = "/home/summer/.xuzhi_memory/expert_tracker/wechat_accounts.json"
WEIXIN_SEARCH = "/home/summer/.openclaw/workspace/wechat_search.py"


def load_accounts():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    accounts = {}
    for k, v in raw.items():
        if k.startswith("_") or not isinstance(v, dict):
            continue
        if v.get("biz"):  # 只保留有 biz 的账号
            accounts[k] = v
    return accounts


def fetch_articles_via_search(account_name, account_info, max_articles=5):
    """
    用 wechat_search.py 搜索 "账号名"，返回该账号发布的文章。
    wechat_search.py 返回结果包含 biz，可验证是否属于目标账号。
    """
    import subprocess

    result = subprocess.run(
        ["python3", WEIXIN_SEARCH, account_name, str(max_articles)],
        capture_output=True, text=True, timeout=20
    )

    articles = []
    if result.returncode != 0 or not result.stdout.strip():
        return [], f"search_failed: {result.stderr[:100]}"

    target_biz = account_info.get("biz", "")

    # 解析 wechat_search.py 的输出
    # 格式: "Title: xxx | Account: xxx | URL: xxx | Biz: xxx | Date: xxx | Digest: xxx\n---"
    current = {}
    for line in result.stdout.split("\n"):
        line = line.strip()
        if not line:
            if current.get("url"):
                biz = current.get("biz", "")
                # 如果 wechat_search 返回了 biz，验证是否匹配
                # 如果没有 biz，检查 account 是否匹配（宽松匹配）
                if target_biz and biz and biz == target_biz:
                    articles.append(dict(current))
                elif not target_biz and current.get("account", "").strip():
                    # 无 biz 时，接受所有结果（可能有重复）
                    articles.append(dict(current))
                current = {}
            continue
        if line.startswith("Title:"):
            current["title"] = line[6:].strip()
        elif line.startswith("Account:"):
            current["account"] = line[8:].strip()
        elif line.startswith("URL:"):
            current["url"] = line[4:].strip()
        elif line.startswith("Biz:"):
            current["biz"] = line[4:].strip()
        elif line.startswith("Date:"):
            current["date"] = line[5:].strip()
        elif line.startswith("Digest:"):
            current["digest"] = line[7:].strip()
        elif line.startswith("---"):
            if current.get("url"):
                articles.append(dict(current))
            current = {}

    return articles[:max_articles], "ok" if articles else "no_articles"


def track_account(account_name, max_articles=3):
    accounts = load_accounts()
    if account_name not in accounts:
        print(f"❌ 未知账号: {account_name}")
        print(f"   已知账号: {', '.join(sorted(accounts.keys()))}")
        return []

    info = accounts[account_name]
    print(f"=== [{account_name}] biz={info.get('biz','')} topics={info.get('topics',[])} ===")

    articles, status = fetch_articles_via_search(account_name, info, max_articles)

    if status == "search_failed":
        print(f"   ❌ 搜索失败")
        return []
    elif status == "no_articles":
        print(f"   ⚠️  无文章")
        return []

    for a in articles:
        print(f"   ✓ {a.get('title','')}")
        print(f"     {a.get('url','')[:70]}")
        print(f"     biz={a.get('biz','')} date={a.get('date','')}")

    return articles


def list_accounts():
    accounts = load_accounts()
    print(f"=== 已注册公众号账号 ({len(accounts)}) ===")
    for name, info in sorted(accounts.items()):
        desc = info.get("description", "")
        biz = info.get("biz", "无biz")
        topics = ", ".join(info.get("topics", [])[:3])
        print(f"  {name}")
        print(f"    biz={biz} | 话题={topics}")
        if desc:
            print(f"    {desc}")
    print()


def main():
    if len(sys.argv) < 2:
        list_accounts()
        return

    cmd = sys.argv[1]
    if cmd == "list":
        list_accounts()
    elif cmd == "all":
        accounts = load_accounts()
        print(f"=== 公众号追踪 | {len(accounts)} 个账号 ===\n")
        all_articles = []
        for name in sorted(accounts.keys()):
            arts = track_account(name, max_articles=3)
            all_articles.extend(arts)
            time.sleep(1)
        print(f"\n=== 共 {len(all_articles)} 篇 ===")
    else:
        max_n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        track_account(cmd, max_n)


if __name__ == "__main__":
    main()
