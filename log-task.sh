#!/bin/bash

# Armagdon Prep - Task Logger
# Usage: ./log-task.sh "Your task here"

if [ -z "$1" ]; then
    echo "Usage: ./log-task.sh \"Task description\""
    exit 1
fi

DATE=$(date +%Y-%m-%d)
FILE="content/daily/$DATE.md"

# Ensure today's log exists
if [ ! -f "$FILE" ]; then
    echo "Creating today's log first..."
    ./log-today.sh > /dev/null
fi

# Check if "## 4. Tasks" section exists, if not append it
if ! grep -q "## 4. Tasks" "$FILE"; then
    echo -e "\n## 4. Tasks" >> "$FILE"
fi

# Append the task
echo "- [ ] $1" >> "$FILE"
echo "✅ Added task to $DATE: $1"
