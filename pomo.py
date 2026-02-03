#!/usr/bin/env python3
import os
import re
import time
import sys
import subprocess
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich import box

# Configuration
DURATION_MINS = 25
BREAK_MINS = 5
POMO_INCREMENT = 0.42

# Earthy Colors
ACCENT = "#556b2f"
TEXT = "#2d2a26"

console = Console()

def play_alert():
    try:
        subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"], check=True, stderr=subprocess.DEVNULL)
    except:
        try:
            subprocess.run(["aplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"], check=True, stderr=subprocess.DEVNULL)
        except:
            for _ in range(3):
                print("\a", end="", flush=True)
                time.sleep(0.2)

def get_today_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"content/daily/{date_str}.md"
    if not os.path.exists(path):
        console.print(f"[bold red]⚠️  Log not found:[/bold red] {path}")
        sys.exit(1)
    return path

def parse_log(filepath):
    metrics = {}
    tasks = []
    current_section = "General"
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
        content = "".join(lines)

    # Frontmatter metrics
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        for l in fm_match.group(1).split('\n'):
            if ':' in l:
                k, v = l.split(':', 1)
                metrics[k.strip()] = v.strip()

    # Body tasks
    for line in lines:
        header_match = re.match(r'^##\s+\d+\.\s+([^(\n]+)', line)
        if header_match:
            current_section = header_match.group(1).strip()
        
        task_match = re.match(r'^-\s+\[([ xX])\]\s+(\[[0-9]{{2}}:[0-9]{{2}}\])?\s*(.*)', line)
        if task_match:
            raw_name = task_match.group(3).strip()
            clean_name = raw_name.replace("🍅", "").strip()
            
            category = "focus_hours"
            if any(k in clean_name for k in ["Ruck", "Exercise", "Gym"]): category = "physical_hours"
            elif any(k in current_section or k in clean_name for k in ["Interview", "Programming", "Study"]): category = "learning_hours"
            
            tasks.append({
                "name": clean_name,
                "done": task_match.group(1).lower() == 'x',
                "category": category,
                "section": current_section
            })
            
    return metrics, tasks, lines

def update_file(filepath, task_name, metric, lines):
    now_time = datetime.now().strftime("%H:%M")
    new_lines = []
    found_task = False
    
    for line in lines:
        if line.startswith(f"{metric}:"):
            val = float(line.split(":")[1].strip())
            line = f"{metric}: {round(val + POMO_INCREMENT, 2)}\n"
        
        if task_name in line and not found_task:
            if re.search(r'\[[0-9]{{2}}:[0-9]{{2}}\]', line):
                line = re.sub(r'\[[0-9]{{2}}:[0-9]{{2}}\]', f'[{now_time}]', line)
            else:
                line = line.replace("- [ ] ", f"- [ ] [{now_time}] ")
            line = line.rstrip() + " 🍅\n"
            found_task = True
        new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)

def display_dashboard(metrics, tasks):
    console.clear()
    date_display = datetime.now().strftime("%A, %B %d")
    console.print(Panel(f"[bold {ACCENT}]Focus Loop[/bold {ACCENT}] - {date_display}", box=box.ROUNDED))

    # Stats
    m_table = Table(box=box.SIMPLE, show_header=False)
    m_table.add_row("Deep Work", f"{metrics.get('focus_hours', '0')}h", "Learn", f"{metrics.get('learning_hours', '0')}h", "Body", f"{metrics.get('physical_hours', '0')}h")
    console.print(m_table)

    # Selection Table
    t_table = Table(title="Select Next Task", box=box.SIMPLE, header_style=f"bold {ACCENT}", border_style=ACCENT, expand=True)
    t_table.add_column("ID", justify="right", width=4)
    t_table.add_column("Status", justify="center", width=8)
    t_table.add_column("Task", ratio=1)
    t_table.add_column("Category", style=f"bold italic #fcfbf9 on {ACCENT}", justify="center")

    for i, t in enumerate(tasks):
        status = "[bold green]DONE[/bold green]" if t['done'] else "[dim]PENDING[/dim]"
        style = "[strike dim]" if t['done'] else ""
        t_table.add_row(str(i+1), status, f"{style}{t['name']}", t['category'].split('_')[0].title())
    
    console.print(t_table)

def run_timer(duration_mins, description, color):
    total_seconds = duration_mins * 60
    with Progress(TextColumn("[bold]{task.description}"), BarColumn(complete_style=color), TextColumn("{task.percentage:>3.0f}%"), TimeRemainingColumn(), console=console) as progress:
        task = progress.add_task(description, total=total_seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)
    play_alert()

def main():
    while True:
        filepath = get_today_file()
        metrics, tasks, lines = parse_log(filepath)
        display_dashboard(metrics, tasks)
        
        choice = console.input(f"\n[bold {ACCENT}]Select task # to focus[/bold {ACCENT}] (or 'q' to quit): ")
        if choice.lower() == 'q': break
        
        try:
            selected = tasks[int(choice)-1]
            cycles = 4 if "2 Hour" in selected['name'] else 1
            
            for c in range(cycles):
                run_timer(DURATION_MINS, f"{selected['name']} ({c+1}/{cycles})", ACCENT)
                update_file(filepath, selected['name'], selected['category'], lines)
                # Refresh data for potential multi-cycle updates
                _, _, lines = parse_log(filepath)
                
                if c < cycles - 1:
                    run_timer(BREAK_MINS, "Break", "blue")
                    console.input("\nBreak over. Press Enter for next cycle...")
            
            console.print("\n[bold green]Success![/bold green] Returning to dashboard...")
            time.sleep(1.5)
            
        except (ValueError, IndexError):
            console.print("[red]Invalid choice.[/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()