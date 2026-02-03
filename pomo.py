#!/usr/bin/env python3
import os
import re
import time
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.live import Live
from rich import box

# Configuration
DURATION_MINS = 25
BREAK_MINS = 5
POMO_INCREMENT = 0.42  # 25 mins in hours

# Earthy Colors (matching the Hugo theme)
ACCENT = "#556b2f"  # Muted Green
TEXT = "#2d2a26"    # Soft Black
PAPER = "#fcfbf9"   # Warm White

console = Console()

def get_today_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"content/daily/{date_str}.md"
    if not os.path.exists(path):
        console.print(f"[bold red]⚠️  Today's log not found:[/bold red] {path}")
        console.print("[yellow]Run 'make log' first.[/yellow]")
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
            # Clean name from previous tomatoes for matching
            clean_name = raw_name.replace("🍅", "").strip()
            
            # Determine metric category
            category = "focus_hours"
            if any(k in clean_name for k in ["Ruck", "Exercise", "Gym", "Physical"]):
                category = "physical_hours"
            elif any(k in current_section or k in clean_name for k in ["Interview", "Programming", "Study", "Learn"]):
                category = "learning_hours"
            
            tasks.append({
                "name": clean_name,
                "category": category,
                "line": line.strip(),
                "section": current_section
            })
            
    return tasks, lines

def update_file(filepath, task_name, metric, lines):
    now_time = datetime.now().strftime("%H:%M")
    new_lines = []
    found_task = False
    new_val = 0.0
    
    for line in lines:
        # 1. Update Metrics in Frontmatter
        if line.startswith(f"{metric}:"):
            try:
                current_val = float(line.split(":")[1].strip())
                new_val = round(current_val + POMO_INCREMENT, 2)
                line = f"{metric}: {new_val}\n"
            except ValueError:
                pass
        
        # 2. Update Task Line (Timestamp and Tomato)
        # We use a loose match for the task name to handle existing tomatoes/timestamps
        if task_name in line and not found_task:
            # Replace or add timestamp [HH:MM]
            if re.search(r'\[[0-9]{2}:[0-9]{2}\]', line):
                line = re.sub(r'\[[0-9]{2}:[0-9]{2}\]', f'[{now_time}]', line)
            else:
                line = line.replace("- [ ] ", f"- [ ] [{now_time}] ")
            
            # Append Tomato
            line = line.rstrip() + " 🍅\n"
            found_task = True
            
        new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    return new_val

def run_timer(duration_mins, description, color):
    total_seconds = duration_mins * 60
    
    with Progress(
        TextColumn("[bold]{task.description}"),
        BarColumn(bar_width=None, complete_style=color, finished_style=color),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task(description, total=total_seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)

def main():
    console.clear()
    console.print(Panel(f"[bold {ACCENT}]Armagdon Prep[/bold {ACCENT}] - Integrated Pomodoro", box=box.ROUNDED))
    
    filepath = get_today_file()
    tasks, original_lines = parse_log(filepath)
    
    if not tasks:
        console.print("[bold red]❌ No tasks found in today's log.[/bold red]")
        return

    table = Table(title="Today's Protocol", box=box.SIMPLE, header_style=f"bold {ACCENT}", border_style=ACCENT)
    table.add_column("ID", justify="right", style="dim")
    table.add_column("Task", ratio=1)
    table.add_column("Category", style="italic")

    for i, t in enumerate(tasks):
        table.add_row(str(i+1), t['name'], t['category'].replace('_', ' ').title())
    
    console.print(table)
    
    try:
        choice = console.input(f"\n[bold {ACCENT}]Select task number[/bold {ACCENT}] (or 'q' to quit): ")
        if choice.lower() == 'q': return
        idx = int(choice) - 1
        selected = tasks[idx]
    except (ValueError, IndexError):
        console.print("[bold red]Invalid selection.[/bold red]")
        return

    # Check for multi-cycle
    cycles = 4 if "2 Hours" in selected['name'] or "2 hours" in selected['name'] else 1
    
    console.print(f"\n[bold]Target:[/bold] {selected['name']}")
    console.print(f"[bold]Metric:[/bold] {selected['category'].replace('_', ' ').title()}")
    console.print(f"[bold]Cycles:[/bold] {cycles}\n")
    
    for c in range(cycles):
        label = f"Session {c+1}/{cycles}"
        run_timer(DURATION_MINS, label, ACCENT)
        
        # Update file after every successful session
        new_val = update_file(filepath, selected['name'], selected['category'], original_lines)
        # Re-read lines for next iteration update
        with open(filepath, 'r') as f: original_lines = f.readlines()
        
        console.print(f"\n[bold green]✅ Session Complete![/bold green]")
        console.print(f"📝 {selected['category']} updated to [bold]{new_val}h[/bold]")

        if c < cycles - 1:
            console.print(f"\n[bold {ACCENT}]Starting Break...[/bold {ACCENT}]")
            run_timer(BREAK_MINS, "Break", "blue")
            console.print("\n[bold]Break finished.[/bold]")
            input("Press Enter to start next session...")

    console.print(Panel(f"[bold {ACCENT}]Protocol Satisfied.[/bold {ACCENT}]\nGo well.", box=box.DOUBLE))

if __name__ == "__main__":
    main()