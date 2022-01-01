PROJECT = $(shell basename $(shell pwd))
ID = hatvillage/${PROJECT}

build:
	docker build \
		--tag ${ID} .

run:
	docker run \
		--name ${PROJECT} \
		--hostname ${PROJECT}-dev \
		--volume $(shell pwd):/opt/${PROJECT} \
		--volume ${HOME}/.ssh:/root/.ssh \
		--interactive \
		--tty \
		--rm \
		${ID} \
		bash

ci:
	docker run --rm ${ID} test
