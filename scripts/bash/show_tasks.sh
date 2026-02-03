#!/bin/bash

# Armagdon Prep - Bash Version of Status Dashboard
# Demonstrates parsing Markdown frontmatter and body with standard tools.

DATE=$(date +%Y-%m-%d)
FILE="content/daily/$DATE.md"

if [ ! -f "$FILE" ]; then
    echo "⚠️  Today's log not found: $FILE"
    exit 1
fi

echo "=========================================="
echo "   ARMAGDON STATUS - $(date '+%A, %B %d')"
echo "=========================================="

# 1. Parse Frontmatter Metrics
echo "METRICS:"
grep -E "^(focus|learning|physical)_hours:|^status:" "$FILE" | while read -r line; do
    echo "  • $line"
done

echo ""
echo "DAILY PROTOCOL:"
# 2. Parse Body Tasks
# Looks for lines starting with "- [ ]" or "- [x]"
grep -E "^- \[.\]" "$FILE" | while read -r line; do
    if [[ $line == *"[x]"* ]]; then
        echo "  [DONE]    ${line:6}"
    else
        echo "  [PENDING] ${line:6}"
    fi
done

echo "=========================================="
