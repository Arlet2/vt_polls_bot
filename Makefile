VERSION=1.3.0
SSH_PORT=1802

.PHONY: all docker-build

all:
	make docker-build
	make docker-save-image

docker-build:
	docker compose up

docker-save-image:
	docker save vt_polls_bot:${VERSION} > vt_polls_bot_${VERSION}.img

send-image: # todo: fix it
	scp -P ${SSH_PORT} vt_polls_bot_${VERSION}.img arlet@arlet.su:~/vt_polls_bot/
