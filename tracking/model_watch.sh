#!/bin/bash
# Model Repository Watch | Γ
# Check for updates in key AI4S repositories

WATCH_DIR="$HOME/.xuzhi_memory/tracking/models_watch"
DATE=$(date +%Y-%m-%d)

echo "# Model Watch | ${DATE}" > "$WATCH_DIR/${DATE}.md"
echo "" >> "$WATCH_DIR/${DATE}.md"

# MatterGen
echo "## Microsoft MatterGen" >> "$WATCH_DIR/${DATE}.md"
cd ~/xuzhi_genesis/centers/naturalscience/physics/refs/mattergen 2>/dev/null && \
    git log --oneline -5 >> "$WATCH_DIR/${DATE}.md" 2>/dev/null || \
    echo "Repo not found" >> "$WATCH_DIR/${DATE}.md"
echo "" >> "$WATCH_DIR/${DATE}.md"

# AlphaFold 3
echo "## DeepMind AlphaFold 3" >> "$WATCH_DIR/${DATE}.md"
cd ~/xuzhi_genesis/centers/naturalscience/biology/refs/alphafold3 2>/dev/null && \
    git log --oneline -5 >> "$WATCH_DIR/${DATE}.md" 2>/dev/null || \
    echo "Repo not found" >> "$WATCH_DIR/${DATE}.md"
echo "" >> "$WATCH_DIR/${DATE}.md"

# Syntheseus
echo "## Microsoft Syntheseus" >> "$WATCH_DIR/${DATE}.md"
cd ~/xuzhi_genesis/centers/naturalscience/chemistry/refs/syntheseus 2>/dev/null && \
    git log --oneline -5 >> "$WATCH_DIR/${DATE}.md" 2>/dev/null || \
    echo "Repo not found" >> "$WATCH_DIR/${DATE}.md"

echo "Watch complete: $WATCH_DIR/${DATE}.md"