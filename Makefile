#                                 __                 __
#    __  ______  ____ ___  ____ _/ /____  ____  ____/ /
#   / / / / __ \/ __ `__ \/ __ `/ __/ _ \/ __ \/ __  /
#  / /_/ / /_/ / / / / / / /_/ / /_/  __/ /_/ / /_/ /
#  \__, /\____/_/ /_/ /_/\__,_/\__/\___/\____/\__,_/
# /____                     matthewdavis.io, holla!
#
include .make/Makefile.inc

NS			?= default
NAME		?= bot
REPO_URL 	?= https://github.com/mateothegreat/discord-bot-javascript-evaluator

build:

	docker build 	--build-arg REPO_URL=$(REPO_URL) \
					-t $(NAME) \
                    -f images/Dockerfile.NODE_11_9_0_ALPINE .

run:

	docker run 	-v /var/run/docker.sock:/var/run/docker.sock \
				$(NAME)
