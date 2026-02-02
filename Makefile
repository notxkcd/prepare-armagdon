all: serve

serve:
	hugo server

build:
	hugo --minify

log:
	./log-today.sh

task:
	@read -p "Enter task: " TASK; ./log-task.sh "$$TASK"

note:
	@read -p "Enter Title: " TITLE; \
	read -p "Enter Section (tech/essays/philosophy): " SEC; \
	./new-note.sh "$$TITLE" "$$SEC"

clean:
	rm -rf public resources .hugo_build.lock