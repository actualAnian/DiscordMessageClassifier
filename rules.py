def only_read_specified_channels(message, rules):
    if "only_read_specified_channels" in rules and rules["only_read_specified_channels"]:
        if message.channel.id not in rules["only_read_specified_channels"]["channels"]:
            return False
    return True

def only_read_specified_forums(message, rules):
    if "thread" not in message.channel.type.name:
        return True
    if "only_read_specified_forums" in rules and rules["only_read_specified_forums"]:
        if message.channel.parent_id not in rules["only_read_specified_forums"]["forums"]:
            return False
    return True