#!/usr/bin/env bash

docker build --rm=true -t rallybot .

#add /bin/bash to the end of this command if you need to debug
docker run --rm -it -e SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN} --name rally-bot rallybot
