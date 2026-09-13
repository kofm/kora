IMAGE := ghcr.io/kofm/kora
VERSION := $(shell uvx --from commitizen cz version --project)

docker-build:
	docker build \
		-t $(IMAGE):$(VERSION) \
		-t $(IMAGE):latest \
		.

docker-push:
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

docker-release: docker-build docker-push
