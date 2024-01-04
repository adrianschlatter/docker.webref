VERSION := 0.1

webref-$(VERSION).tar.gz: Dockerfile config/requirements.txt Makefile
	docker build -t webref:$(VERSION) .
	docker save webref:$(VERSION) | gzip > webref-$(VERSION).tar.gz

up: webref-$(VERSION).tar.gz
	VERSION=$(VERSION) docker compose up --detach

clean:
	VERSION=$(VERSION) docker-compose down --rmi all --volumes --remove-orphans
	rm -f webref-$(VERSION).tar.gz
