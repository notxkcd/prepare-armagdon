#!/usr/bin/env python3
import os
import re
import sys
import tty
import termios
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich import box

# Earthy Colors
ACCENT = "#556b2f"
TEXT = "#2d2a26"

console = Console()

def get_today_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"content/daily/{date_str}.md"
    if not os.path.exists(path):
        console.print(f"[bold red]Today's log not found.[/bold red]")
        sys.exit(1)
    return path

def parse_log(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    tasks = []
    for i, line in enumerate(lines):
        # Surgical regex: captures the exact checkbox and the rest of the line
        match = re.match(r'^(\s*-\s+\[)([ xX])(\]\s+)(.*)', line)
        if match:
            tasks.append({
                "line_index": i,
                "done": match.group(2).lower() == 'x',
                "prefix": match.group(1),
                "suffix": match.group(3),
                "name": match.group(4).strip()
            })
    return tasks, lines

def write_log(filepath, lines):
    with open(filepath, 'w') as f:
        f.writelines(lines)

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b': # Escape sequence
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def generate_table(tasks, cursor_idx):
    table = Table(box=box.SIMPLE, header_style=f"bold {ACCENT}", border_style=ACCENT, expand=True)
    table.add_column(" ", width=2)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Task", ratio=1)

    for i, t in enumerate(tasks):
        pointer = f"[bold {ACCENT}]>[/bold {ACCENT}]" if i == cursor_idx else " "
        status = "[bold green]DONE[/bold green]" if t['done'] else "[dim]PENDING[/dim]"
        name_style = "[strike dim]" if t['done'] else ""
        row_style = f"bold {TEXT} on #e8eade" if i == cursor_idx else ""
        
        table.add_row(pointer, status, f"{name_style}{t['name']}", style=row_style)
    return table

def main():
    filepath = get_today_file()
    cursor_idx = 0
    
    tasks, lines = parse_log(filepath)
    if not tasks:
        console.print("[yellow]No tasks found in today's log.[/yellow]")
        return

    with Live(generate_table(tasks, cursor_idx), console=console, screen=True, auto_refresh=False) as live:
        while True:
            live.update(generate_table(tasks, cursor_idx), refresh=True)
            key = get_char()
            
            if key in ('k', '\x1b[A'): # Up
                cursor_idx = (cursor_idx - 1) % len(tasks)
            elif key in ('j', '\x1b[B'): # Down
                cursor_idx = (cursor_idx + 1) % len(tasks)
            elif key in (' ', '\r'): # Toggle
                t = tasks[cursor_idx]
                new_status = " " if t['done'] else "x"
                # Surgical replacement at the exact line index
                lines[t['line_index']] = f"{t['prefix']}{new_status}{t['suffix']}{t['name']}\n"
                write_log(filepath, lines)
                tasks, lines = parse_log(filepath) # Re-sync
            elif key.lower() == 'q' or key == '\x03': # Quit
                break

    console.print(f"\n[bold {ACCENT}]✔ Site Updated.[/bold {ACCENT}] Changes synced to {os.path.basename(filepath)}.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
