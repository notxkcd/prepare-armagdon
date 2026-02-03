#!/usr/bin/env python3
import os
import re
import time
import sys
from datetime import datetime

# Configuration
DURATION_MINS = 25
BREAK_MINS = 5
POMO_INCREMENT = 0.42  # 25 mins in hours

def get_today_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"content/daily/{date_str}.md"
    if not os.path.exists(path):
        print(f"⚠️  Today's log not found: {path}")
        print("Run 'make log' first.")
        sys.exit(1)
    return path

def parse_log(filepath):
    tasks = []
    current_section = ""
    
    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Detect Sections
        header_match = re.match(r'^##\s+\d+\.\s+([^(\n]+)', line)
        if header_match:
            current_section = header_match.group(1).strip()
        
        # Detect Tasks: - [ ] [HH:MM] Task Name
        task_match = re.match(r'^-\s+\[[ xX]\]\s+(\[[0-9]{2}:[0-9]{2}\])?\s*(.*)', line)
        if task_match:
            raw_name = task_match.group(2).strip()
            # Determine metric category
            category = "focus_hours"
            if "Ruck" in raw_name or "Exercise" in raw_name:
                category = "physical_hours"
            elif "Interview" in current_section or "Programming" in raw_name:
                category = "learning_hours"
            
            tasks.append({
                "name": raw_name,
                "category": category,
                "line": line.strip()
            })
            
    return tasks, lines

def update_file(filepath, task_name, metric, lines):
    now_time = datetime.now().strftime("%H:%M")
    new_lines = []
    found_task = False
    
    for line in lines:
        # 1. Update Metrics in Frontmatter
        if line.startswith(f"{metric}:"):
            current_val = float(line.split(":")[1].strip())
            new_val = round(current_val + POMO_INCREMENT, 2)
            line = f"{metric}: {new_val}\n"
        
        # 2. Update Task Line (Timestamp and Tomato)
        if task_name in line and not found_task:
            # Replace or add timestamp [HH:MM]
            if "[" in line and "]" in line and any(c.isdigit() for c in line.split(']')[0]):
                line = re.sub(r'\[[0-9]{2}:[0-9]{2}\]', f'[{now_time}]', line)
            else:
                line = line.replace("- [ ] ", f"- [ ] [{now_time}] ")
            
            # Append Tomato
            line = line.strip() + " 🍅\n"
            found_task = True
            
        new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    return new_val

def run_timer(duration_mins, label):
    seconds = duration_mins * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\r⏳ {label}: {timer} remaining...", end="")
        time.sleep(1)
        seconds -= 1
    print("\n✅ Session Complete!")

def main():
    filepath = get_today_file()
    tasks, original_lines = parse_log(filepath)
    
    if not tasks:
        print("❌ No tasks found in today's log.")
        return

    print("\n--- Armagdon Pomodoro ---")
    for i, t in enumerate(tasks):
        print(f"{i+1}) {t['name']}")
    
    try:
        choice = input("\nSelect task number (or 'q' to quit): ")
        if choice.lower() == 'q': return
        idx = int(choice) - 1
        selected = tasks[idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Check for multi-cycle
    cycles = 4 if "2 Hours" in selected['name'] or "2 hours" in selected['name'] else 1
    
    print(f"\n🚀 Starting {cycles} session(s) for: {selected['name']}")
    
    for c in range(cycles):
        run_timer(DURATION_MINS, f"Session {c+1}/{cycles}")
        new_val = update_file(filepath, selected['name'], selected['category'], original_lines)
        # Re-read lines for next iteration update
        with open(filepath, 'r') as f: original_lines = f.readlines()
        
        if c < cycles - 1:
            run_timer(BREAK_MINS, "Break")
            input("\nPress Enter to start next session...")

    print(f"\n🏁 Finished. Today's {selected['category']} is now {new_val}h")

if __name__ == "__main__":
    main()
