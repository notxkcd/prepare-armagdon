#!/bin/bash

# Armagdon Prep - Daily Logger
# Usage: ./log-today.sh

DATE=$(date +%Y-%m-%d)
FILE="content/daily/$DATE.md"

if [ -f "$FILE" ]; then
    echo "⚠️  Log for today already exists at: $FILE"
    echo "Opening it now..."
else
    echo "📝 Creating new Daily Log for $DATE..."
    hugo new "$FILE" > /dev/null
    echo "✅ Created: $FILE"
fi

# Optional: Open in default editor (uncomment if desired)
# $EDITOR "$FILE"

echo "To edit, run: nano $FILE"
