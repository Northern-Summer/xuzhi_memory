#!/bin/bash
# backup_guard.sh — 记忆边界与备份守卫
# 2026-03-25 | Γ 起草

set -euo pipefail

MEMORY_ROOT="$HOME/.xuzhi_memory"
BACKUP_ROOT="$HOME/.xuzhi_memory/backup"
AGENTS_DIR="$MEMORY_ROOT/agents"
DATE=$(date +%Y-%m-%d-%H%M)

# Agent 列表
AGENTS=(gamma phi delta theta omega psi xi)

log() { echo "[$(date +%T)] $*"; }

# 1. 验证记忆边界完整性
check_boundaries() {
    log "检查记忆边界..."
    for agent in "${AGENTS[@]}"; do
        agent_dir="$AGENTS_DIR/$agent"
        if [ ! -d "$agent_dir/memory" ]; then
            log "⚠️ $agent 缺少 memory/ 目录，创建中"
            mkdir -p "$agent_dir/memory"
        fi
    done
    log "边界检查完成"
}

# 2. 快照所有 agent 记忆
snapshot_all() {
    log "创建快照: $DATE"
    snap_dir="$BACKUP_ROOT/snapshot_$DATE"
    mkdir -p "$snap_dir"
    
    # Agent 个人记忆
    for agent in "${AGENTS[@]}"; do
        agent_dir="$AGENTS_DIR/$agent"
        if [ -d "$agent_dir" ]; then
            cp -r "$agent_dir" "$snap_dir/"
        fi
    done
    
    # 公共记忆（不含污染源）
    [ -d "$MEMORY_ROOT/memory" ] && cp -r "$MEMORY_ROOT/memory" "$snap_dir/memory"
    [ -d "$MEMORY_ROOT/manifests" ] && cp -r "$MEMORY_ROOT/manifests" "$snap_dir/manifests"
    
    log "快照完成: $snap_dir"
}

# 3. 清理旧快照（保留最近10个）
cleanup_old() {
    local count=$(ls -dt "$BACKUP_ROOT"/snapshot_* 2>/dev/null | wc -l)
    if [ "$count" -gt 10 ]; then
        ls -dt "$BACKUP_ROOT"/snapshot_* | tail -$((count - 10)) | xargs -r rm -rf
        log "清理旧快照，保留最近10个"
    fi
}

# 4. 验证备份完整性
verify_backup() {
    local latest=$(ls -dt "$BACKUP_ROOT"/snapshot_* 2>/dev/null | head -1)
    if [ -z "$latest" ]; then
        log "⚠️ 无可用快照"
        return 1
    fi
    for agent in "${AGENTS[@]}"; do
        if [ ! -d "$latest/$agent" ]; then
            log "⚠️ $latest/$agent 缺失"
        fi
    done
    log "备份验证完成"
}

case "${1:-full}" in
    check)   check_boundaries ;;
    snap)    snapshot_all ;;
    verify)  verify_backup ;;
    full)
        check_boundaries
        snapshot_all
        cleanup_old
        verify_backup
        ;;
esac
