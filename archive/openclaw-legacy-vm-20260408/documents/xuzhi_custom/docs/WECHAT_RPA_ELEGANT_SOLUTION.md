# 微信文章抓取优雅方案

## 目标

**一次配置，永久有效**：
- Agent 只需要发送链接
- 自动下载并输出到共享目录
- 无需人工干预

---

## 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                    微信文章抓取服务                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   WSL (Agent)                      Windows (RPA 服务)           │
│   ───────────                      ──────────────────           │
│                                                                 │
│   1. 写入链接                      监听目录                      │
│      ↓                               ↓                          │
│   /mnt/c/Users/.../queue/     →    检测新文件                   │
│      xxx.url                        ↓                          │
│                                    打开浏览器                    │
│                                    抓取内容                      │
│                                    OCR/复制                     │
│                                    ↓                           │
│   2. 读取内容              ←       写入输出                     │
│      ↓                                                          │
│   /mnt/c/Users/.../output/                                      │
│      xxx.md                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 实现方案

### 方案 A：WeChat-Article-Exporter + 目录监听（最简单）

**配置一次**：
1. 下载 WeChat-Article-Exporter
2. 配置自动监听模式
3. 设置输入/输出目录

**使用方式**：
```bash
# Agent 操作
echo "https://mp.weixin.qq.com/s/xxx" > /mnt/c/Users/.../queue/article.url

# 等待输出
cat /mnt/c/Users/.../output/article.md
```

**优点**：配置最简单
**缺点**：需要 WeChat-Article-Exporter 支持监听模式

### 方案 B：Python RPA 服务（最灵活）

**Windows 端服务**（一次配置）：

```python
# wechat_rpa_service.py
# 运行: python wechat_rpa_service.py
# 开机自启: 添加到 Windows 任务计划程序

import time
import os
from pathlib import Path
import pyautogui
import webbrowser
from PIL import Image
import pytesseract
import subprocess

QUEUE_DIR = Path(r"C:\Users\MzgyM\wechat_rpa\queue")
OUTPUT_DIR = Path(r"C:\Users\MzgyM\wechat_rpa\output")
PROCESSED_DIR = Path(r"C:\Users\MzgyM\wechat_rpa\processed")

def ensure_dirs():
    for d in [QUEUE_DIR, OUTPUT_DIR, PROCESSED_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def get_article_content(url):
    """RPA 抓取微信文章"""
    # 1. 打开浏览器
    webbrowser.open(url)
    time.sleep(8)  # 等待加载
    
    # 2. 全选复制（Ctrl+A, Ctrl+C）
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    
    # 3. 获取剪贴板内容
    import subprocess
    result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], 
                          capture_output=True, text=True)
    content = result.stdout
    
    # 4. 关闭标签页
    pyautogui.hotkey('ctrl', 'w')
    
    return content

def process_file(url_file):
    """处理单个 URL 文件"""
    url = url_file.read_text().strip()
    print(f"处理: {url}")
    
    try:
        content = get_article_content(url)
        
        # 写入输出
        output_file = OUTPUT_DIR / f"{url_file.stem}.md"
        output_file.write_text(content, encoding='utf-8')
        print(f"完成: {output_file}")
        
        # 移动到已处理
        url_file.rename(PROCESSED_DIR / url_file.name)
        
    except Exception as e:
        print(f"失败: {e}")
        error_file = OUTPUT_DIR / f"{url_file.stem}.error"
        error_file.write_text(str(e), encoding='utf-8')

def main():
    ensure_dirs()
    print("微信 RPA 服务启动...")
    print(f"监听目录: {QUEUE_DIR}")
    
    while True:
        # 检查队列
        url_files = list(QUEUE_DIR.glob("*.url"))
        
        for url_file in url_files:
            process_file(url_file)
        
        time.sleep(5)  # 每 5 秒检查一次

if __name__ == "__main__":
    main()
```

**Agent 端使用**：

```python
# wechat_rpa_client.py (在 WSL 中运行)

from pathlib import Path
import time
import uuid

QUEUE_DIR = Path("/mnt/c/Users/MzgyM/wechat_rpa/queue")
OUTPUT_DIR = Path("/mnt/c/Users/MzgyM/wechat_rpa/output")

def fetch_wechat_article(url, timeout=60):
    """
    抓取微信文章
    返回: 文章内容或 None
    """
    task_id = str(uuid.uuid4())[:8]
    
    # 1. 写入队列
    queue_file = QUEUE_DIR / f"{task_id}.url"
    queue_file.write_text(url)
    
    # 2. 等待输出
    output_file = OUTPUT_DIR / f"{task_id}.md"
    error_file = OUTPUT_DIR / f"{task_id}.error"
    
    start = time.time()
    while time.time() - start < timeout:
        if output_file.exists():
            return output_file.read_text(encoding='utf-8')
        if error_file.exists():
            raise Exception(error_file.read_text(encoding='utf-8'))
        time.sleep(2)
    
    raise TimeoutError("抓取超时")

# 使用示例
if __name__ == "__main__":
    url = "https://mp.weixin.qq.com/s/cJGWji1XeOEXgYGvIxGCtA"
    content = fetch_wechat_article(url)
    print(content[:500])
```

---

## 配置步骤（一次配置）

### Step 1: 创建目录结构

```powershell
# Windows PowerShell
mkdir C:\Users\MzgyM\wechat_rpa\queue
mkdir C:\Users\MzgyM\wechat_rpa\output
mkdir C:\Users\MzgyM\wechat_rpa\processed
```

### Step 2: 安装依赖

```powershell
pip install pyautogui pillow pytesseract pyperclip

# 安装 Tesseract OCR
# 下载: https://github.com/UB-Mannheim/tesseract/wiki
```

### Step 3: 创建服务脚本

将上面的 `wechat_rpa_service.py` 保存到 `C:\Users\MzgyM\wechat_rpa\`

### Step 4: 配置开机自启

```powershell
# 创建任务计划
schtasks /create /tn "WeChatRPA" /tr "python C:\Users\MzgyM\wechat_rpa\wechat_rpa_service.py" /sc onstart /rl highest
```

### Step 5: 立即启动服务

```powershell
python C:\Users\MzgyM\wechat_rpa\wechat_rpa_service.py
```

---

## Agent 使用方式

```python
# 集成到 wechat_search.py

def fetch_full_article(url):
    """获取微信文章全文"""
    from wechat_rpa_client import fetch_wechat_article
    return fetch_wechat_article(url)

# 使用
articles = search_wechat("Claude Code")
for article in articles:
    content = fetch_full_article(article['url'])
    print(content)
```

---

## 优雅性评估

| 指标 | 评分 | 说明 |
|------|------|------|
| 一次配置 | ⭐⭐⭐⭐⭐ | 配置后永久有效 |
| 自动化程度 | ⭐⭐⭐⭐⭐ | 完全自动，无需人工 |
| 可靠性 | ⭐⭐⭐⭐ | 依赖浏览器，可能需要维护 |
| 跨平台 | ⭐⭐⭐ | WSL + Windows 协作 |
| 可维护性 | ⭐⭐⭐⭐ | 简单的文件交互 |

---

## 总结

**回答你的问题**：是的，可以做到一次配置永久有效。

**核心设计**：
1. Windows 端：后台服务监听目录
2. Agent 端：写入链接 → 读取输出
3. 通过共享目录通信，无需网络端口

**时间投入**：初始配置 30 分钟，之后永久自动运行。

---

*Created: 2026-04-01*
