# Armagdon Prep - Command Shortcuts
# This Makefile provides easy shortcuts for common site operations.

# Default target: Start the local development server
all: serve

# Start the Hugo development server (View at http://localhost:1313)
serve:
	hugo server

# Build the final static site for production (outputs to /public)
build:
	hugo --minify

# Create today's Daily Log using the ritual archetype
log:
	./log-today.sh

# Append a new task to today's Daily Log from the terminal
task:
	@read -p "Enter task: " TASK; ./log-task.sh "$$TASK"

# Create a new note in a specific section (tech, essays, or philosophy)
note:
	@read -p "Enter Title: " TITLE; \
	read -p "Enter Section (tech/essays/philosophy): " SEC; \
	./new-note.sh "$$TITLE" "$$SEC"

# Clean up build artifacts and temporary files
clean:
	rm -rf public resources .hugo_build.lock

# Automatically stage, commit with timestamp, and push to GitHub
backup:
	git add .
	git commit -m "backup: $(shell date '+%Y-%m-%d %H:%M:%S')"
	git push origin master
