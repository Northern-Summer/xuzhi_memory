# TOOLS.md — Theta 工具箱

> **必须先读 L3 共享知识：`~/.xuzhi_memory/memory/knowledge/SHARED_TOOLS.md`**
> 以下为本 agent 专属补充内容。

---

## 网络搜索（详见 SHARED_TOOLS.md）

**学术论文 + arXiv：**
```bash
python3 ~/.openclaw/workspace/skills/multi-search-engine/searxng_client.py "<搜索词>" brave,arxiv
```

**中文公众号：**
```bash
python3 ~/.openclaw/workspace/wechat_search.py "<关键词>" [最大条数]
```

**一般网页：**
```bash
web_fetch(url="https://...", maxChars=5000)
```

---

## 代理配置（WSL2 环境）

```bash
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
```

---

## Theta专属路径

- 历史社会科学中心：`~/xuzhi_genesis/centers/socialscience/`

---

## 紧急恢复

```bash
kill -15 $(pgrep -f openclaw-gateway); openclaw gateway start
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
```

---

**共享知识位置**：`~/.xuzhi_memory/memory/knowledge/SHARED_TOOLS.md`
