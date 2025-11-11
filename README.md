# CLASSIFICATOR BOT FOR DISCORD

This bot reads messages in discord channel and tries to classify them. If able to do so, it will respond to the message with a link to a specified message

## installation
pip install -r requirements.txt

run the bot with:
py.\run.py

## adding your own api caller
the caller should implement ClassifierInterface, it can be added in:
line 10 of run.py

## OpenAi caller
expects you to export the OPENAI_API_KEY first

## the bot requires a config file to use
```json
{
    "token" : "tokenId",
    "servers":
    {
        "[serverId]":
        {
            "debug_mode" : false,
            "server_name" : "just for visual clarity",
            "log_file" : "path to log file",
            "cha" :
            {
                "type": "is_in_specified_channels",
                "channels": [1, 2, 3]
            },
            "for" :
            {
                "type": "is_in_specified_forums",
                "forums": [1, 2]
            },
            "cat" :
            {
                "type": "is_in_specified_categories",
                "categories": [1]
            },
            "roles" :
            {
                "type": "has_specified_role",
                "roles": [1, 2]
            },
            "rule_expression" : "not cha or (for and cat)", // supports not, and, or, ()
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