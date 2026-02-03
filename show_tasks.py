#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

# Earthy Colors
ACCENT = "#556b2f"  # Muted Green
TEXT = "#2d2a26"    # Soft Black

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
    metrics = {}
    tasks = []
    current_section = "General"
    
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse Frontmatter for metrics
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for line in fm.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metrics[key.strip()] = val.strip()

    # Parse Body for tasks
    lines = content.split('\n')
    for line in lines:
        header_match = re.match(r'^##\s+\d+\.\s+([^(\n]+)', line)
        if header_match:
            current_section = header_match.group(1).strip()
        
        task_match = re.match(r'^-\s+\[([ xX])\]\s+(.*)', line)
        if task_match:
            status = task_match.group(1).strip().lower()
            name = task_match.group(2).strip()
            tasks.append({
                "section": current_section,
                "done": status == 'x',
                "name": name
            })
            
    return metrics, tasks

def main():
    filepath = get_today_file()
    metrics, tasks = parse_log(filepath)
    
    date_display = datetime.now().strftime("%A, %B %d, %Y")
    
    console.clear()
    console.print(Panel(f"[bold {ACCENT}]Armagdon Status[/bold {ACCENT}] - {date_display}", box=box.ROUNDED))

    # Metrics Summary
    m_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    m_table.add_column("Key", style=f"bold {ACCENT}")
    m_table.add_column("Value", style="bold")
    
    m_table.add_row("Status", metrics.get('status', 'Pending'))
    m_table.add_row("Deep Work", f"{metrics.get('focus_hours', '0')}h")
    m_table.add_row("Learning", f"{metrics.get('learning_hours', '0')}h")
    m_table.add_row("Physical", f"{metrics.get('physical_hours', '0')}h")
    
    console.print(m_table)

    # Task List
    t_table = Table(title="Daily Protocol", box=box.SIMPLE, header_style=f"bold {ACCENT}", border_style=ACCENT, expand=True)
    t_table.add_column("Status", justify="center", width=8)
    t_table.add_column("Task", ratio=1)
    t_table.add_column("Section", style=f"bold italic #fcfbf9 on {ACCENT}", justify="center")

    for t in tasks:
        mark = "[bold green]DONE[/bold green]" if t['done'] else "[dim]PENDING[/dim]"
        name_style = "[strike dim]" if t['done'] else ""
        t_table.add_row(mark, f"{name_style}{t['name']}", t['section'])
    
    console.print(t_table)

    # Progress Calculation
    done_count = sum(1 for t in tasks if t['done'])
    total_count = len(tasks)
    if total_count > 0:
        percent = (done_count / total_count) * 100
        console.print(f"\n[bold]Overall Completion:[/bold] {done_count}/{total_count} tasks ({percent:.1f}%)")
        
        with Progress(
            BarColumn(bar_width=None, complete_style=ACCENT, finished_style=ACCENT),
            console=console
        ) as progress:
            progress.add_task("", total=100, completed=percent)

if __name__ == "__main__":
    main()
