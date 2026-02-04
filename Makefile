# Armagdon Prep - Command Shortcuts
# This Makefile provides easy shortcuts for common site operations.

# Default target: Show help
all: help

# Show help for available commands
help:
	@echo "Armagdon Prep - Command Manual"
	@echo "------------------------------"
	@echo "make serve   - Start the local development server"
	@echo "make build   - Build the final static site"
	@echo "make log     - Create today's Daily Log"
	@echo "make task    - Add a new task to today's log"
	@echo "make scratch - Capture a fleeting thought"
	@echo "make note    - Create a new note (tech/essays/philosophy)"
	@echo "make pomo    - Start a Pomodoro focus session"
	@echo "make show    - Show today's status dashboard"
	@echo "make check   - Toggle tasks interactively"
	@echo "make backup  - Commit and push changes to GitHub"
	@echo "make clean   - Remove build artifacts"

# Start the Hugo development server (View at http://localhost:1313)
serve:
	hugo server

# Build the final static site for production (outputs to /public)
build:
	hugo --minify
	bun x pagefind --site public --output-path public/_pagefind

# Create today's Daily Log using the ritual archetype
log:
	./log-today.sh

# Append a new task to today's Daily Log from the terminal
task:
	@read -p "Enter task: " TASK; ./log-task.sh "$$TASK"

# Capture a quick thought and append it to today's reflections
scratch:
	python3 scratch.py

# Create a new note in a specific section (tech, essays, or philosophy)
note:
	@read -p "Enter Title: " TITLE; \
	read -p "Enter Section (tech/essays/philosophy): " SEC; \
	./new-note.sh "$$TITLE" "$$SEC"

# Start a 25-minute Pomodoro session (automatically updates today's focus_hours)
pomo:
	python3 pomo.py

# Show today's tasks and metrics in a beautiful terminal dashboard
show:
	python3 show_tasks.py

# Toggle today's tasks interactively
check:
	python3 check_tasks.py

# Clean up build artifacts and temporary files
clean:
	rm -rf public resources .hugo_build.lock

# Automatically stage, commit with timestamp, and push to GitHub
backup:
	git add .
	git commit -m "backup: $(shell date '+%Y-%m-%d %H:%M:%S')"
	git push origin master
