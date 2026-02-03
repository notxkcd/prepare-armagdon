#!/bin/bash

# Armagdon Prep - Bash Version of Focus Loop
# Robust parsing and updating using sed and bc.

DATE=$(date +%Y-%m-%d)
FILE="content/daily/$DATE.md"
POMO_INC=0.42

play_alert() {
    # Try paplay with 80% volume
    if paplay --volume=52428 /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga 2>/dev/null; then
        return
    fi
    # Try aplay
    if aplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null; then
        return
    fi
    # Fallback to bell
    for i in {1..3}; do
        echo -e "\a"
        sleep 0.2
    done
}

while true; do
    if [ ! -f "$FILE" ]; then echo "Log not found."; exit 1; fi
    clear
    echo "--- Bash Focus Loop ---"
    
    # List tasks with numbers
    mapfile -t TASKS < <(grep -E "^- [ ] " "$FILE" | sed 's/^- [ ] //')
    
    if [ ${#TASKS[@]} -eq 0 ]; then
        echo "No pending tasks found."
        exit 0
    fi

    for i in "${!TASKS[@]}"; do
        echo "$((i+1))) ${TASKS[$i]}"
    done
    echo "q) Quit"

    read -p "Select task #: " CHOICE
    if [[ $CHOICE == "q" ]]; then break; fi
    
    IDX=$((CHOICE-1))
    TASK_NAME="${TASKS[$IDX]}"
    
    # Determine Metric
    METRIC="focus_hours"
    if [[ $TASK_NAME == *"Ruck"* ]]; then METRIC="physical_hours"
elif [[ $TASK_NAME == *"Interview"* ]]; then METRIC="learning_hours"
fi

    echo "Focusing on: $TASK_NAME"
    
    # 25 Minute Timer
    SEC=$((25 * 60))
    while [ $SEC -gt 0 ]; do
        printf "\r⏳ %02d:%02d remaining..." $((SEC/60)) $((SEC%60))
        sleep 1
        ((SEC--))
    done
    echo -e "\n✅ Done!"
    play_alert

    # Update File
    NOW=$(date +%H:%M)
    # 1. Update Hour Metric (using bc for math)
    OLD_VAL=$(grep "^$METRIC:" "$FILE" | cut -d' ' -f2)
    NEW_VAL=$(echo "$OLD_VAL + $POMO_INC" | bc)
    sed -i "s/^$METRIC: $OLD_VAL/$METRIC: $NEW_VAL/" "$FILE"
    
    # 2. Update Task Line
    sed -i "/- [ ] $TASK_NAME/ s/$/ 🍅/" "$FILE"
    sed -i "/- [ ] $TASK_NAME/ s/\[ \] /\[ \] [$NOW] /" "$FILE"

    echo "Log updated. Press Enter to continue..."
    read
done