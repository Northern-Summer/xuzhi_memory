#!/bin/bash
# 工程改进铁律合规 — Ξ | 2026-03-29
# 自问：此操作是否让系统更安全/准确/优雅/高效？答案：YES
#
# Git 凭证硬化脚本
# 解决：token 散落、push 失败无告警、无自动修复
#
# 教训（2026-03-29）：
# - pushurl 会覆盖 remote URL 中的 token！set-url --push 必须显式含 token
# - token 必须先通过 GitHub API 验证（git ls-remote），无效则不写入 vault
# - vault 是唯一真源，其他位置不存 token

set -euo pipefail

GIT_VAULT="$HOME/.xuzhi_vault"
TOKEN_FILE="$GIT_VAULT/github_token"
PUSH_LOG="$HOME/.xuzhi_memory/logs/push.log"

mkdir -p "$GIT_VAULT" "$HOME/.xuzhi_memory/logs"
chmod 700 "$GIT_VAULT"

# ============================================================
# 第一步：读取当前 token（优先从 vault，其次从 .git-credentials）
# ============================================================
get_current_token() {
    if [[ -f "$TOKEN_FILE" ]]; then
        cat "$TOKEN_FILE"
    elif [[ -f ~/.git-credentials ]]; then
        grep -o 'ghp_[a-zA-Z0-9]*' ~/.git-credentials | head -1
    else
        echo "ERROR: No token found in vault or .git-credentials" >&2
        exit 1
    fi
}

# ============================================================
# 第二步：验证 token（GitHub API）
# ============================================================
verify_token() {
    local token="$1"
    # curl fails with SSL (Clash MITM cert) - use git ls-remote instead
    if GIT_SSL_NO_VERIFY=true git ls-remote "https://${token}@github.com/Northern-Summer/xuzhi_memory.git" HEAD >/dev/null 2>&1; then
        echo "VALID"
        return 0
    else
        echo "INVALID"
        return 1
    fi
}

# ============================================================
# 第三步：向 vault 写入 token
# ============================================================
save_token() {
    local token="$1"
    echo "$token" > "$TOKEN_FILE"
    chmod 600 "$TOKEN_FILE"
    echo "Token saved to vault: $TOKEN_FILE"
}

# ============================================================
# 第四步：更新所有仓库的 remote URL
# ============================================================
update_remotes() {
    local token="$1"
    local repos=(
        "$HOME/xuzhi_memory"
        "$HOME/xuzhi_genesis"
        "$HOME/xuzhi_workspace"
    )
    for repo in "${repos[@]}"; do
        if [[ -d "$repo/.git" ]]; then
            # 只更新 push URL，fetch 保持不变
            git -C "$repo" remote set-url --push origin "https://$token@github.com/Northern-Summer/$(basename $repo).git" 2>/dev/null || true
            echo "Updated push remote: $repo"
        fi
    done
}

# ============================================================
# 第五步：验证 push
# ============================================================
test_push() {
    local repo="$1"
    local test_branch="token-verify-$(date +%s)"
    git -C "$repo" checkout --orphan "$test_branch" 2>/dev/null || true
    git -C "$repo" commit --allow-empty -m "push test $(date)" 2>/dev/null || true
    if git -C "$repo" push origin "$test_branch" 2>/dev/null; then
        # 清理测试 branch
        git -C "$repo" branch -D "$test_branch" 2>/dev/null || true
        git -C "$repo" push origin --delete "$test_branch" 2>/dev/null || true
        echo "PUSH_OK"
        return 0
    else
        echo "PUSH_FAIL"
        return 1
    fi
}

# ============================================================
# 第六步：清理散落的 token
# ============================================================
cleanup_tokens() {
    echo "=== Scanning for token spills ==="
    local count=0
    # 扫描 session transcripts（token 只出现在 .jsonl 文件）
    while IFS= read -r file; do
        if grep -q 'ghp_[a-zA-Z0-9]\{20,\}' "$file" 2>/dev/null; then
            # 替换为 [REDACTED]
            sed -i "s/ghp_[a-zA-Z0-9]*/ghp_REDACTED/g" "$file"
            echo "REDACTED: $file"
            ((count++)) || true
        fi
    done < <(find ~/.openclaw/sessions ~/.openclaw/agents -name "*.jsonl" 2>/dev/null)
    
    # 清理 backup 目录中的 token（不删文件，只替换）
    while IFS= read -r file; do
        if grep -q 'ghp_[a-zA-Z0-9]\{20,\}' "$file" 2>/dev/null; then
            sed -i "s/ghp_[a-zA-Z0-9]*/ghp_REDACTED/g" "$file" 2>/dev/null || true
            echo "REDACTED backup: $file"
            ((count++)) || true
        fi
    done < <(find ~ -name "*.md" -path "*backup*" 2>/dev/null)
    find ~/.local/share/Trash -name "*.md" 2>/dev/null | while read f; do
        if grep -q 'ghp_[a-zA-Z0-9]\{20,\}' "$f" 2>/dev/null; then
            sed -i "s/ghp_[a-zA-Z0-9]*/ghp_REDACTED/g" "$f" 2>/dev/null || true
            echo "REDACTED trash: $f"
            ((count++)) || true
        fi
    done
    
    echo "Total files redacted: $count"
}

# ============================================================
# 主流程
# ============================================================
main() {
    local cmd="${1:-status}"
    
    case "$cmd" in
        verify)
            echo "=== Token Verification ==="
            local token
            token=$(get_current_token)
            echo "Current token: ${token:0:12}..."
            verify_token "$token"
            ;;
        save)
            local new_token="${2:-}"
            if [[ -z "$new_token" ]]; then
                echo "Usage: $0 save <new_token>"
                exit 1
            fi
            echo "Verifying token via GitHub API (git ls-remote)..."
            # Use git ls-remote to verify - works even with SSL issues via proxy
            if GIT_SSL_NO_VERIFY=true git ls-remote "https://${new_token}@github.com/Northern-Summer/xuzhi_memory.git" HEAD >/dev/null 2>&1; then
                echo "Token VERIFIED by GitHub."
                save_token "$new_token"
                update_remotes "$new_token"
                echo "=== Testing push ==="
                for repo in "$HOME/xuzhi_memory" "$HOME/xuzhi_genesis" "$HOME/xuzhi_workspace"; do
                    if [[ -d "$repo/.git" ]]; then
                        echo -n "  $(basename $repo): "
                        if GIT_SSL_NO_VERIFY=true git -C "$repo" push origin master >/dev/null 2>&1; then
                            echo "OK"
                        else
                            echo "FAIL - check $PUSH_LOG"
                        fi
                    fi
                done
                cleanup_tokens
            else
                echo "Token INVALID - GitHub rejected it. NOT saved."
                exit 1
            fi
            ;;
        push)
            local token
            token=$(get_current_token)
            update_remotes "$token"
            for repo in "$HOME/xuzhi_memory" "$HOME/xuzhi_genesis" "$HOME/xuzhi_workspace"; do
                if [[ -d "$repo/.git" ]]; then
                    local pending
                    pending=$(git -C "$repo" log --oneline origin/master..HEAD 2>/dev/null | wc -l)
                    if [[ "$pending" -gt 0 ]]; then
                        echo "Pushing $repo ($pending commits)..."
                        if git -C "$repo" push origin master 2>&1 | tee -a "$PUSH_LOG"; then
                            echo "  OK" 
                        else
                            echo "  FAILED"
                        fi
                    fi
                fi
            done
            ;;
        cleanup)
            cleanup_tokens
            ;;
        status)
            echo "=== Git Hardening Status ==="
            echo "Vault: $TOKEN_FILE ($(ls -la $TOKEN_FILE 2>/dev/null || echo 'NOT FOUND'))"
            echo ""
            for repo in "$HOME/xuzhi_memory" "$HOME/xuzhi_genesis" "$HOME/xuzhi_workspace"; do
                if [[ -d "$repo/.git" ]]; then
                    local token_in_remote
                    token_in_remote=$(git -C "$repo" remote get-url --push origin 2>/dev/null | grep -o 'ghp_[a-zA-Z0-9]*' || echo 'NONE')
                    local pending
                    pending=$(git -C "$repo" log --oneline origin/master..HEAD 2>/dev/null | wc -l)
                    echo "$(basename $repo): remote_token=${token_in_remote:0:12}..., pending=$pending"
                fi
            done
            ;;
        *)
            echo "Usage: $0 {verify|save <token>|push|cleanup|status}"
            ;;
    esac
}

main "$@"
