#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from rich.console import Console

console = Console()
ACCENT = "#556b2f"

def get_today_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = f"content/daily/{date_str}.md"
    if not os.path.exists(path):
        console.print("[bold red]Today's log not found.[/bold red]")
        sys.exit(1)
    return path

def main():
    filepath = get_today_file()
    note = console.input(f"[bold {ACCENT}]Capture Thought[/bold {ACCENT}]: ")
    
    if not note.strip():
        return

    timestamp = datetime.now().strftime("%H:%M")
    entry = f"\n* {timestamp} - {note}\n"

    with open(filepath, 'a') as f:
        f.write(entry)
    
    console.print(f"\n[bold {ACCENT}]✔ Site Updated.[/bold {ACCENT}] Thought appended to {os.path.basename(filepath)}.")

if __name__ == "__main__":
    main()

