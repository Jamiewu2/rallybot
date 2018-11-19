import os
import sys
from slackclient import SlackClient
from rally import rallyClient
from slack import slackClient
import json

config_filename = "config.json"

if not os.path.isfile(config_filename):
    print("Config file, please create a config file named: `config.json`. See config.json.template")
    sys.exit(1)

with open("config.json") as f:
    config_vals = json.load(f)
    slack_bot_token = config_vals["SLACK_BOT_TOKEN"]
    rally_api_token = config_vals["RALLY_API_TOKEN"]
    rally_workspace = config_vals["RALLY_WORKSPACE"]
    rally_project = config_vals["RALLY_PROJECT"]

if None in (slack_bot_token, rally_api_token, rally_workspace, rally_project):
    print("Configuration values not defined, please set your values in a config.json")
    sys.exit(1)

# instantiate clients
slack_client = SlackClient(slack_bot_token)
rally_client = rallyClient.RallyClient(rally_api_token, rally_workspace, rally_project)

rally_bot_client = slackClient.RallyBotClient(slack_client, rally_client)
rally_bot_client.run()
