#!/bin/bash
# AI4S Daily Tracker | Γ
# Run daily to fetch new papers from arXiv

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="$HOME/.xuzhi_memory/tracking/ai4s_daily"
LOG_FILE="$OUTPUT_DIR/${DATE}.md"

echo "# AI4S Daily Scan | ${DATE}" > "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "## arXiv cs.LG (Machine Learning)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Fetch recent papers (last 24 hours)
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.LG+AND+(material+OR+molecule+OR+protein+OR+crystal)&start=0&max_results=20&sortBy=submittedDate&sortOrder=descending" | \
    grep -E "<title>|<summary>|<published>|<arxiv:doi>" | \
    head -100 >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "## arXiv physics.chem-ph (Chemical Physics)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

curl -s "http://export.arxiv.org/api/query?search_query=cat:physics.chem-ph+AND+(AI+OR+machine+learning+OR+deep+learning)&start=0&max_results=20&sortBy=submittedDate&sortOrder=descending" | \
    grep -E "<title>|<summary>|<published>|<arxiv:doi>" | \
    head -100 >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "## arXiv q-bio.BM (Biomolecules)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

curl -s "http://export.arxiv.org/api/query?search_query=cat:q-bio.BM+AND+(structure+prediction+OR+folding)&start=0&max_results=20&sortBy=submittedDate&sortOrder=descending" | \
    grep -E "<title>|<summary>|<published>|<arxiv:doi>" | \
    head -100 >> "$LOG_FILE"

echo "Scan complete: $LOG_FILE"