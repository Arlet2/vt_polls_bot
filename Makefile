VERSION=1.2.0

.PHONY: all docker-build

all:

docker-build:
	docker build -t vt_polls_bot:${VERSION} .