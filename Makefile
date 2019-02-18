#                                 __                 __
#    __  ______  ____ ___  ____ _/ /____  ____  ____/ /
#   / / / / __ \/ __ `__ \/ __ `/ __/ _ \/ __ \/ __  /
#  / /_/ / /_/ / / / / / / /_/ / /_/  __/ /_/ / /_/ /
#  \__, /\____/_/ /_/ /_/\__,_/\__/\___/\____/\__,_/
# /____                     matthewdavis.io, holla!
#
include .make/Makefile.inc

NS			?= default
VERSION		?= $(shell git rev-parse HEAD)
APP			?= autobots-platform-deployer
IMAGE		?= gcr.io/matthewdavis-devops/$(APP):$(VERSION)

ENV_1_NAME	?= ENV_1_NAME
ENV_1_VALUE	?= none
ENV_2_NAME	?= ENV_2_NAME
ENV_2_VALUE	?= none
ENV_3_NAME	?= ENV_3_NAME
ENV_3_VALUE	?= none
ENV_4_NAME	?= ENV_4_NAME
ENV_4_VALUE	?= none
ENV_5_NAME	?= ENV_5_NAME
ENV_5_VALUE	?= none

build:

	docker build -t $(IMAGE) .

run:

	docker run -v /var/run/docker.sock:/var/run/docker.sock $(IMAGE)

build-bot:

	docker build 	--build-arg REPO_URL=$(REPO_URL) \
					-t $(NAME) \
                    -f images/Dockerfile.NODE_11_9_0_ALPINE .
