all: serve

serve:
	hugo server

build:
	hugo --minify

log:
	./log-today.sh

clean:
	rm -rf public resources .hugo_build.lock
