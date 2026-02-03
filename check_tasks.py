#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Earthy Colors
ACCENT = "#556b2f"

console = Console()

def get_today_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"content/daily/{date_str}.md"
    if not os.path.exists(path):
        console.print(f"[bold red]⚠️  Log not found:[/bold red] {path}")
        sys.exit(1)
    return path

def parse_log(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    tasks = []
    for i, line in enumerate(lines):
        match = re.match(r'^-\s+\[([ xX])\]\s+(.*)', line)
        if match:
            tasks.append({
                "line_index": i,
                "done": match.group(1).lower() == 'x',
                "name": match.group(2).strip()
            })
    return tasks, lines

def write_log(filepath, lines):
    with open(filepath, 'w') as f:
        f.writelines(lines)

def main():
    filepath = get_today_file()
    
    while True:
        tasks, lines = parse_log(filepath)
        console.clear()
        console.print(Panel(f"[bold {ACCENT}]Task Manager[/bold {ACCENT}] - {datetime.now().strftime('%A, %b %d')}", box=box.ROUNDED))
        
        table = Table(box=box.SIMPLE, header_style=f"bold {ACCENT}", border_style=ACCENT, expand=True)
        table.add_column("ID", justify="right", width=4)
        table.add_column("Status", justify="center", width=10)
        table.add_column("Task", ratio=1)

        for i, t in enumerate(tasks):
            status = "[bold green]DONE[/bold green]" if t['done'] else "[dim]PENDING[/dim]"
            style = "[strike dim]" if t['done'] else ""
            table.add_row(str(i+1), status, f"{style}{t['name']}")
        
        console.print(table)
        console.print("[dim]Enter number to toggle, 'q' to quit[/dim]")
        
        choice = console.input(f"\n[bold {ACCENT}]Action[/bold {ACCENT}]: ")
        if choice.lower() == 'q': break
        
        try:
            idx = int(choice) - 1
            selected = tasks[idx]
            line_idx = selected['line_index']
            
            # Toggle logic
            current_line = lines[line_idx]
            if selected['done']:
                lines[line_idx] = current_line.replace("[x]", "[ ]").replace("[X]", "[ ]")
            else:
                lines[line_idx] = current_line.replace("[ ]", "[x]")
            
            write_log(filepath, lines)
        except (ValueError, IndexError):
            pass

if __name__ == "__main__":
    main()
