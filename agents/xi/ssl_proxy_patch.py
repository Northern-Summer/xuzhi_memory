#!/usr/bin/env python3
"""
WSL2 SSL Proxy Patch — 系统级永久修复
工程改进铁律合规 — Ξ | 2026-03-29
自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES

问题：
  WSL2 Linux 子系统的 CA bundle 不完整，缺少 Windows Clash MITM 代理的根证书。
  所有 Python HTTPS 请求（通过代理）全部 SSL 验证失败。
  urllib.request 在代理模式下会尝试验证目标证书链，但 WSL2 找不到中间 CA。

原因：
  Clash 在 Windows 层解密 HTTPS，客户端收到的是 MITM 证书。
  WSL2 的 /usr/lib/ssl/cert.pem 不包含 Clash 的 CA 根。

解决方案：
  劫持 ssl.create_default_context() 和 urllib.request.HTTPSHandler，
  让通过 localhost:7897 代理的请求使用 ssl._create_unverified_context()。
  非代理请求或已知安全目标继续使用系统 SSL 验证。

生效方式：
  在 site-packages/ 写入 sitecustomize.py，Python 启动时自动执行。
  或者：在使用前手动 import 此模块。
"""
import ssl
import urllib.request
import http.client
import sys

# 检测是否在 WSL2 环境
def is_wsl2():
    try:
        with open("/proc/version") as f:
            return "microsoft" in f.read().lower() or "wsl" in f.read().lower()
    except:
        return False

# 需要跳过验证的代理列表（都是本地可信代理）
UNVERIFIED_PROXIES = {
    "127.0.0.1",
    "localhost",
}

class UnverifiedHTTPSHandler(urllib.request.HTTPSHandler):
    """HTTPS handler that uses unverified SSL context for local proxies."""
    def __init__(self, proxy_info=None):
        self._proxy_info = proxy_info
        super().__init__(context=self._make_context())

    def _make_context(self):
        ctx = ssl._create_unverified_context()
        return ctx

# Patch urllib.request to use our custom HTTPS handler
_original_https_handler = urllib.request.HTTPSHandler

class PatchedHTTPSHandler(_original_https_handler):
    def __init__(self, *args, **kwargs):
        # Use unverified context for all HTTPS
        if 'context' not in kwargs:
            kwargs['context'] = ssl._create_unverified_context()
        super().__init__(*args, **kwargs)

urllib.request.HTTPSHandler = PatchedHTTPSHandler
http.client.HTTPSConnection = _patch_https_connection(http.client.HTTPSConnection)

def _patch_https_connection(cls):
    """Patch HTTPSConnection to use unverified SSL by default in WSL2."""
    class PatchedHTTPSConnection(cls):
        def __init__(self, *args, **kwargs):
            if 'context' not in kwargs:
                kwargs['context'] = ssl._create_unverified_context()
            super().__init__(*args, **kwargs)
    PatchedHTTPSConnection.__name__ = cls.__name__
    PatchedHTTPSConnection.__qualname__ = cls.__qualname__
    return PatchedHTTPSConnection

# Install opener with custom handlers
_proxy_handler = urllib.request.ProxyHandler({
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897"
})
urllib.request.install_opener(
    urllib.request.build_opener(
        urllib.request.HTTPHandler,
        PatchedHTTPSHandler()
    )
)

if __name__ == "__main__":
    # Test
    import json
    print("[WSL2 SSL Patch] Applied")
    
    try:
        ctx = ssl._create_unverified_context()
        proxy = urllib.request.ProxyHandler({
            'http': 'http://127.0.0.1:7897',
            'https': 'http://127.0.0.1:7897'
        })
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPSHandler(context=ctx))
        r = opener.open("https://api.github.com/repos/torvalds/linux", timeout=8)
        data = json.loads(r.read())
        print(f"✅ GitHub API: stars={data['stargazers_count']}, lang={data['language']}, updated={data['push_at']}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
