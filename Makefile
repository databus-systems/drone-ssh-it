.PHONY: docker

IMAGE ?= plugins/drone-ssh

docker:
		docker build --rm -t $(IMAGE) .

