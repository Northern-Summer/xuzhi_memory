# 系统状态报告

日期: 2026-04-08
时间: 13:52:08

---

## 🚀 Gateway 状态

```
● openclaw-gateway.service - OpenClaw Gateway (v2026.3.28)
     Loaded: loaded (/home/summer/.config/systemd/user/openclaw-gateway.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-04-08 13:26:20 CST; 25min ago
   Main PID: 4892 (openclaw-gatewa)
      Tasks: 26 (limit: 4687)
     Memory: 1.5G (peak: 2.2G swap: 51.7M swap peak: 52.9M)
        CPU: 4min 7.491s
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/openclaw-gateway.service
             ├─4892 openclaw-gateway
             ├─5361 openclaw-gateway
```

健康检查: {"ok":true,"status":"live"}

## 🔒 安全审计

```
Security audit
Summary: 0 critical · 3 warn · 1 info
  WARN Reverse proxy headers are not trusted
    gateway.bind is loopback and gateway.trustedProxies is empty. If you expose the Control UI through a reverse proxy, configure trusted proxies so local-client c…
    Fix: Set gateway.trustedProxies to your proxy IPs or keep the Control UI local-only.
  WARN Potential multi-user setup detected (personal-assistant model warning)
    Heuristic signals indicate this gateway may be reachable by multiple users: - channels.discord.groupPolicy="allowlist" with configured group targets Runtime/pr…
    Fix: If users may be mutually untrusted, split trust boundaries (separate gateways + credentials, ideally separate OS users/hosts). If you intentionally run shared-user access, set agents.defaults.sandbox.mode="all", keep tools.fs.workspaceOnly=true, deny runtime/fs/web tools unless required, and keep personal/private identities + credentials off that runtime.
  WARN Plugin installs include unpinned npm specs
    Unpinned plugin install records: - openclaw-weixin (@tencent-weixin/openclaw-weixin@latest)
    Fix: Pin install specs to exact versions (for example, `@scope/pkg@1.2.3`) for higher supply-chain stability.
```

## 🐳 Docker 状态

```
NAMES       STATUS          PORTS
searxng-1   Up 14 minutes   
one-api     Up 14 minutes   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp
```

## 📚 记忆系统

- 今日记忆: 541 字节
- LATEST 链接: /home/summer/.xuzhi_memory/memory/2026-04-08.md
- 记忆文件数: 292
- 向量块数: 4332

## 💾 磁盘使用

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdd       1007G   69G  888G   8% /
```

## 🌐 网络状态

代理 (192.168.1.33:7897): 
  ✅ 可达

## ⚠️ 最近错误日志

```
{"0":"{\"subsystem\":\"diagnostic\"}","1":"lane task error: lane=session:agent:main:openclaw-weixin:direct:o9cq80z9eorqjasg6hb1w-cc4-po@im.wechat durationMs=10663 error=\"Error: session file locked (timeout 10000ms): pid=4892 /home/summer/.openclaw/agents/main/sessions/660fdda8-e8a8-44ab-bf1d-facb7e2a8952.jsonl.lock\"","_meta":{"runtime":"node","runtimeVersion":"22.22.2","hostname":"unknown","name":"{\"subsystem\":\"diagnostic\"}","parentNames":["openclaw"],"date":"2026-04-08T05:52:10.915Z","logLevelId":5,"logLevelName":"ERROR","path":{"fullFilePath":"file:///usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:454:14","fileName":"subsystem-CJEvHE2o.js","fileNameWithLine":"subsystem-CJEvHE2o.js:454","fileColumn":"14","fileLine":"454","filePath":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js","filePathWithLine":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:454","method":"logToFile"}},"time":"2026-04-08T13:52:10.915+08:00"}
{"0":"{\"subsystem\":\"model-fallback/decision\"}","1":{"event":"model_fallback_decision","tags":["error_handling","model_fallback","candidate_failed"],"runId":"de46bd7c-b10c-4b76-832b-e8980b170524","decision":"candidate_failed","requestedProvider":"custom-cloud-infini-ai-com","requestedModel":"glm-5","candidateProvider":"custom-cloud-infini-ai-com","candidateModel":"glm-5","attempt":1,"total":2,"reason":"timeout","status":408,"errorPreview":"session file locked (timeout 10000ms): pid=4892 /home/summer/.openclaw/agents/main/sessions/660fdda8-e8a8-44ab-bf1d-facb7e2a8952.jsonl.lock","errorHash":"sha256:fe9de8a3507e","nextCandidateProvider":"custom-cloud-infini-ai-com","nextCandidateModel":"minimax-m2.7","isPrimary":true,"requestedModelMatched":true,"fallbackConfigured":true},"2":"model fallback decision","_meta":{"runtime":"node","runtimeVersion":"22.22.2","hostname":"unknown","name":"{\"subsystem\":\"model-fallback/decision\"}","parentNames":["openclaw"],"date":"2026-04-08T05:52:10.916Z","logLevelId":4,"logLevelName":"WARN","path":{"fullFilePath":"file:///usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:453:51","fileName":"subsystem-CJEvHE2o.js","fileNameWithLine":"subsystem-CJEvHE2o.js:453","fileColumn":"51","fileLine":"453","filePath":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js","filePathWithLine":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:453","method":"logToFile"}},"time":"2026-04-08T13:52:10.916+08:00"}
{"0":"{\"subsystem\":\"diagnostic\"}","1":"lane task error: lane=main durationMs=10266 error=\"Error: session file locked (timeout 10000ms): pid=4892 /home/summer/.openclaw/agents/main/sessions/660fdda8-e8a8-44ab-bf1d-facb7e2a8952.jsonl.lock\"","_meta":{"runtime":"node","runtimeVersion":"22.22.2","hostname":"unknown","name":"{\"subsystem\":\"diagnostic\"}","parentNames":["openclaw"],"date":"2026-04-08T05:52:21.230Z","logLevelId":5,"logLevelName":"ERROR","path":{"fullFilePath":"file:///usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:454:14","fileName":"subsystem-CJEvHE2o.js","fileNameWithLine":"subsystem-CJEvHE2o.js:454","fileColumn":"14","fileLine":"454","filePath":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js","filePathWithLine":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:454","method":"logToFile"}},"time":"2026-04-08T13:52:21.230+08:00"}
{"0":"{\"subsystem\":\"diagnostic\"}","1":"lane task error: lane=session:agent:main:openclaw-weixin:direct:o9cq80z9eorqjasg6hb1w-cc4-po@im.wechat durationMs=10267 error=\"Error: session file locked (timeout 10000ms): pid=4892 /home/summer/.openclaw/agents/main/sessions/660fdda8-e8a8-44ab-bf1d-facb7e2a8952.jsonl.lock\"","_meta":{"runtime":"node","runtimeVersion":"22.22.2","hostname":"unknown","name":"{\"subsystem\":\"diagnostic\"}","parentNames":["openclaw"],"date":"2026-04-08T05:52:21.231Z","logLevelId":5,"logLevelName":"ERROR","path":{"fullFilePath":"file:///usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:454:14","fileName":"subsystem-CJEvHE2o.js","fileNameWithLine":"subsystem-CJEvHE2o.js:454","fileColumn":"14","fileLine":"454","filePath":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js","filePathWithLine":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:454","method":"logToFile"}},"time":"2026-04-08T13:52:21.232+08:00"}
{"0":"{\"subsystem\":\"model-fallback/decision\"}","1":{"event":"model_fallback_decision","tags":["error_handling","model_fallback","candidate_failed"],"runId":"de46bd7c-b10c-4b76-832b-e8980b170524","decision":"candidate_failed","requestedProvider":"custom-cloud-infini-ai-com","requestedModel":"glm-5","candidateProvider":"custom-cloud-infini-ai-com","candidateModel":"glm-5","attempt":1,"total":2,"reason":"timeout","status":408,"errorPreview":"session file locked (timeout 10000ms): pid=4892 /home/summer/.openclaw/agents/main/sessions/660fdda8-e8a8-44ab-bf1d-facb7e2a8952.jsonl.lock","errorHash":"sha256:fe9de8a3507e","nextCandidateProvider":"custom-cloud-infini-ai-com","nextCandidateModel":"minimax-m2.7","isPrimary":true,"requestedModelMatched":true,"fallbackConfigured":true},"2":"model fallback decision","_meta":{"runtime":"node","runtimeVersion":"22.22.2","hostname":"unknown","name":"{\"subsystem\":\"model-fallback/decision\"}","parentNames":["openclaw"],"date":"2026-04-08T05:52:21.233Z","logLevelId":4,"logLevelName":"WARN","path":{"fullFilePath":"file:///usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:453:51","fileName":"subsystem-CJEvHE2o.js","fileNameWithLine":"subsystem-CJEvHE2o.js:453","fileColumn":"51","fileLine":"453","filePath":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js","filePathWithLine":"/usr/lib/node_modules/openclaw/dist/subsystem-CJEvHE2o.js:453","method":"logToFile"}},"time":"2026-04-08T13:52:21.233+08:00"}
```

## 💡 建议


---

*此报告由自动化系统生成*
