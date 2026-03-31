#!/bin/bash
# 工程改进铁律合规 — Ξ | 2026-03-29
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
#
# OpenClaw 升级后验证脚本
# 执行时机：升级完成后立即执行
# 检查：记忆完整性、cron配置、agents人格、网关状态

set -euo pipefail

echo "=========================================="
echo "OpenClaw 升级后验证"
echo "=========================================="
echo ""

NEW_VERSION=$(openclaw --version 2>/dev/null | head -1)
echo "当前版本: $NEW_VERSION"
echo ""

# 1. 检查 Gateway
echo "【1/6】Gateway 状态"
if curl -sf --connect-timeout 5 http://localhost:18789/health > /dev/null 2>&1; then
    echo "  ✅ Gateway 运行正常"
else
    echo "  ❌ Gateway 无响应"
fi

# 2. 检查记忆完整性（核心！）
echo ""
echo "【2/6】记忆完整性检查"
MEMORY_FILES=(
    "$HOME/.xuzhi_memory/MEMORY.md"
    "$HOME/.xuzhi_memory/memory/2026-03-28.md"
    "$HOME/.xuzhi_memory/memory/2026-03-29.md"
)
for f in "${MEMORY_FILES[@]}"; do
    if [[ -f "$f" ]]; then
        lines=$(wc -l < "$f")
        echo "  ✅ $(basename $f): ${lines}行"
    else
        echo "  ❌ $(basename $f): 文件丢失！"
    fi
done

# 3. 检查 SOUL.md 和 IDENTITY.md（人格文件）
echo ""
echo "【3/6】人格文件检查"
SOUL="$HOME/.openclaw/workspace/SOUL.md"
IDENTITY="$HOME/.openclaw/workspace/IDENTITY.md"
[[ -f "$SOUL" ]] && echo "  ✅ SOUL.md" || echo "  ❌ SOUL.md 丢失！"
[[ -f "$IDENTITY" ]] && echo "  ✅ IDENTITY.md" || echo "  ❌ IDENTITY.md 丢失！"
# Also check xi-specific copies
XISOUL="$HOME/.xuzhi_memory/agents/xi/SOUL.md"
[[ -f "$XISOUL" ]] && echo "  ✅ xi/SOUL.md" || echo "  ❌ xi/SOUL.md 丢失！"

# 4. 检查 cron jobs
echo ""
echo "【4/6】Cron 任务检查"
if [[ -f "$HOME/.openclaw/cron/jobs.json" ]]; then
    count=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/cron/jobs.json')); print(len(d.get('jobs',[])))" 2>/dev/null)
    echo "  ✅ jobs.json: $count 个任务注册"
    # Check for our critical jobs
    python3 -c "
import json
d=json.load(open('$HOME/.openclaw/cron/jobs.json'))
names = [j['name'] for j in d.get('jobs',[])]
for n in ['memory_checkpoint_5min', 'xi_pulse_research', 'memory_checkpoint_hourly']:
    mark = '✅' if n in names else '❌'
    print(f'  {mark} {n}')
" 2>/dev/null
else
    echo "  ❌ jobs.json 不存在"
fi

# 5. 检查 Git 仓库状态
echo ""
echo "【5/6】Git 仓库状态"
for repo in ~/.xuzhi_memory ~/xuzhi_genesis ~/xuzhi_workspace; do
    name=$(basename $repo)
    git -C "$repo" remote -v | grep origin | head -1 | awk '{print "  " $0}'
done

# 6. 检查 OpenClaw 控制界面
echo ""
echo "【6/6】Channels 状态"
openclaw channels status 2>/dev/null | grep -E "enabled|running|error" | head -5

echo ""
echo "=========================================="
echo "验证完成 $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""
echo "如发现 ❌ 项，立即报告。"
echo ""
echo "测试指令："
echo "  openclaw sessions list"
echo "  openclaw channels status"
echo "  curl http://localhost:18789/health"
