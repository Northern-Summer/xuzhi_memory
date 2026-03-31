#!/bin/bash
# 工程改进铁律合规 — Ξ | 2026-03-29
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
#
# OpenClaw 升级前备份脚本
# 执行时机：每次升级前
# 备份内容：
#   1. .openclaw/agents/（人格配置 + 会话状态）
#   2. .openclaw/cron/（定时任务配置）
#   3. .openclaw/openclaw.json（主配置）
#   4. .xuzhi_vault/（token vault）
#   5. 各仓库最新状态确认
#
# 保留策略：最近3次备份

set -euo pipefail

BACKUP_ROOT="$HOME/.xuzhi_backups"
TIMESTAMP=$(date +%Y%m%d_%H%M)
BACKUP_DIR="$BACKUP_ROOT/pre_upgrade_$TIMESTAMP"
LOG="$BACKUP_DIR/backup_manifest.txt"

mkdir -p "$BACKUP_DIR"

echo "=== OpenClaw 升级前备份 ===" | tee "$LOG"
echo "时间: $(date)" | tee -a "$LOG"
echo "当前版本: $(openclaw --version 2>/dev/null | head -1)" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# 1. 备份 agents 目录
echo "1. 备份 agents/ ..." | tee -a "$LOG"
AGENTS_BACKUP="$BACKUP_DIR/agents.tar.gz"
tar -czf "$AGENTS_BACKUP" \
    --exclude='*.jsonl' \
    --exclude='sessions' \
    -C "$HOME" .openclaw/agents/ 2>/dev/null && echo "  ✅ agents/ (不含sessions)" | tee -a "$LOG" \
    || echo "  ⚠️ agents/ 备份失败" | tee -a "$LOG"

# 2. 备份 cron jobs
echo "2. 备份 cron 配置 ..." | tee -a "$LOG"
CRON_BACKUP="$BACKUP_DIR/cron_jobs.json"
cp "$HOME/.openclaw/cron/jobs.json" "$CRON_BACKUP" 2>/dev/null && echo "  ✅ jobs.json" | tee -a "$LOG" \
    || echo "  ⚠️ cron 备份失败" | tee -a "$LOG"

# 3. 备份 openclaw.json
echo "3. 备份 openclaw.json ..." | tee -a "$LOG"
CONFIG_BACKUP="$BACKUP_DIR/openclaw.json"
cp "$HOME/.openclaw/openclaw.json" "$CONFIG_BACKUP" 2>/dev/null && echo "  ✅ openclaw.json" | tee -a "$LOG" \
    || echo "  ⚠️ config 备份失败" | tee -a "$LOG"

# 4. 备份 vault（token）
echo "4. 备份 vault ..." | tee -a "$LOG"
VAULT_BACKUP="$BACKUP_DIR/vault.tar.gz"
tar -czf "$VAULT_BACKUP" "$HOME/.xuzhi_vault/" 2>/dev/null && echo "  ✅ .xuzhi_vault/" | tee -a "$LOG" \
    || echo "  ⚠️ vault 备份失败" | tee -a "$LOG"

# 5. 确认 git repos 最新
echo "5. Git 仓库状态确认 ..." | tee -a "$LOG"
for repo in ~/.xuzhi_memory ~/xuzhi_genesis ~/xuzhi_workspace; do
    name=$(basename $repo)
    pending=$(git -C "$repo" log --oneline origin/master..HEAD 2>/dev/null | wc -l)
    status=$(git -C "$repo" status --short 2>/dev/null | wc -l)
    echo "  $name: pending_commits=$pending, untracked=$status" | tee -a "$LOG"
done

# 6. 备份 memory L1 最新两天
echo "6. 备份 memory L1 ..." | tee -a "$LOG"
MEM_BACKUP="$BACKUP_DIR/memory_l1.tar.gz"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d yesterday +%Y-%m-%d)
tar -czf "$MEM_BACKUP" \
    "$HOME/.xuzhi_memory/memory/$TODAY.md" \
    "$HOME/.xuzhi_memory/memory/$YESTERDAY.md" \
    "$HOME/.xuzhi_memory/MEMORY.md" \
    2>/dev/null && echo "  ✅ memory L1 ($TODAY + $YESTERDAY)" | tee -a "$LOG" \
    || echo "  ⚠️ memory L1 备份失败" | tee -a "$LOG"

# 7. 清理旧备份（保留最近3次）
echo "7. 清理旧备份 ..." | tee -a "$LOG"
ls -dt "$BACKUP_ROOT"/pre_upgrade_* 2>/dev/null | tail -n +4 | while read old; do
    echo "  🗑️ 删除: $old" | tee -a "$LOG"
    rm -rf "$old"
done

echo "" | tee -a "$LOG"
echo "=== 备份完成 ===" | tee -a "$LOG"
echo "备份目录: $BACKUP_DIR" | tee -a "$LOG"
echo "总大小: $(du -sh "$BACKUP_DIR" | cut -f1)" | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "升级后如需回滚:" | tee -a "$LOG"
echo "  tar -xzf $BACKUP_DIR/agents.tar.gz -C ~/" | tee -a "$LOG"
echo "  cp $BACKUP_DIR/jobs.json ~/.openclaw/cron/" | tee -a "$LOG"
echo "  cp $BACKUP_DIR/openclaw.json ~/.openclaw/" | tee -a "$LOG"
