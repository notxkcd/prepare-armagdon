#!/bin/bash

# Armagdon Prep - Pomodoro Timer
# Increments focus_hours in today's log automatically.

DURATION_MINS=25
SECONDS_TOTAL=$((DURATION_MINS * 60))
DATE=$(date +%Y-%m-%d)
FILE="content/daily/$DATE.md"

# Ensure today's log exists
if [ ! -f "$FILE" ]; then
    echo "⚠️  Today's log ($FILE) not found. Create it first with './log-today.sh'"
    exit 1
fi

echo "🍅 Pomodoro Started: $DURATION_MINS minutes of Deep Work."
echo "Focus on the task. The system will log your progress automatically."

# Timer Loop
while [ $SECONDS_TOTAL -gt 0 ]; do
    printf "\r⏳ %02d:%02d remaining..." $((SECONDS_TOTAL/60)) $((SECONDS_TOTAL%60))
    sleep 1
    : $((SECONDS_TOTAL--))
done

echo -e "\n\n✅ Session Complete!"

# Update the Markdown file
# Logic: Find focus_hours, add 0.42 (25 mins), and save.
OLD_HOURS=$(grep "focus_hours:" "$FILE" | awk '{print $2}')
NEW_HOURS=$(awk "BEGIN {print $OLD_HOURS + 0.42}")

# Use sed to replace the line
sed -i "s/focus_hours: $OLD_HOURS/focus_hours: $NEW_HOURS/" "$FILE"

echo "📝 Log Updated: Today's focus hours increased to $NEW_HOURS."
echo "Take a 5-minute break."
