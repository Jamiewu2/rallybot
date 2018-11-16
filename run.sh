#!/usr/bin/env bash

docker build --rm=true -t rallybot .

#add /bin/bash to the end of this command if you need to debug
docker run --rm -it -e SLACK_BOT_TOKEN=xoxb-10686179668-481830263475-CouYnaiS0J4JZU09t3MnqVJ5 --name rally-bot rallybot