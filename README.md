# CLASSIFICATOR BOT FOR DISCORD

This bot reads messages in discord channel and tries to classify them. If able to do so, it will respond to the message with a link to a specified message

## installation
pip install -r requirements.txt

run the bot with:
py.\run.py

## adding your own api caller
the caller should implement ClassifierInterface, it can be added in:
line 10 of run.py


## the bot requires a config file to use
```json
{
    "token" : "tokenId",
    "servers":
    {
        "[serverId]":
        {
            "server_name" : "just for visual clarity",
            "log_file" : "path to log file",
            "rules" : // currently available rules, check in rules.py
            {
                "only_read_specified_channels" :
                {
                    "channels": [123, 123]
                },
                "only_read_specified_forums" :
                {
                    "channels": [123, 123]
                }
            },
            "categories": [
            {
                "id": 0, // mandatory
                "label": "Other",
                "description": "anything that does not fit into the other categories"
            },
            {
                "id": 1,
                "label": "Talking about cheese",
                "description": "all cheese related comments"
            }],
            "examples" : [
            {
                "text": "Is gouda good?",
                "output": {"category": 1, "label": "Talking about cheese"}
            }],
            "response": [
            {
                "category": 1,
                "channel_id": 123,
                "message_id": 123
            }]
        }
    }
}
```