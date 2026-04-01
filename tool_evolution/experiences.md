# 工具元学习记录

> 基于 MetaAgent (arXiv:2508.00271) 的 learning-by-doing 原则
> 目的：从工具使用经验中提炼可迁移策略

## 元学习机制

```
任务执行 → 遇到知识缺口 → 生成求助 → 工具调用 → 反思验证 → 提炼经验
    ↑                                                        ↓
    ←←←←←←←←←← 经验整合到未来上下文 ←←←←←←←←←←←←←←←←←←←←←←←←
```

## 工具使用经验记录

### 2026-04-01 — web_fetch 微信文章

**任务**：获取微信公众号文章内容
**知识缺口**：微信有反爬机制，直接 web_fetch 只能获取 meta 信息
**尝试**：
1. web_fetch → 只获取到标题和描述
2. curl + User-Agent → 仍然无法获取正文（JS渲染）

**解决方案**：
- 微信文章正文是 JavaScript 渲染的
- 需要 headless browser (Chrome) 才能获取完整内容
- Meta 信息（标题、描述）可以通过 curl 获取

**提炼经验**：
- 微信文章：用 curl 获取 meta，用 headless chrome 获取正文
- 适用工具：`npx bb-browser` 或 `curl -A "Mozilla/5.0..."`

**可迁移策略**：
- SPA 页面（React/Vue）需要 headless browser
- 静态页面可以直接 curl

---

## 工具能力矩阵

| 工具 | 最佳场景 | 局限 | 替代方案 |
|------|---------|------|---------|
| web_fetch | 静态页面 | JS渲染页面 | bb-browser |
| curl | API、静态页面 | 需要登录 | 带cookie的curl |
| bb-browser | SPA、需登录页面 | 较慢 | - |
| SearXNG | 学术、英文搜索 | 中文较弱 | wechat_search |
| wechat_search | 中文、公众号 | 需curl_cffi | - |

## 待补充

- [ ] 记录更多工具使用经验
- [ ] 建立工具选择决策树
- [ ] 创建工具失败案例库
