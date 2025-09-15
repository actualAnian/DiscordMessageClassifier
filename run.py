import discord
from discord.ext import commands
import json
import logging
import os

from OpenAiClassifier import OpenAIClassifier
import rules as R

api_classifier = OpenAIClassifier("gpt-5-nano") # has to implement ClassifierInterface
# ---- CONFIG ----
config = None
with open("config.json", "r") as f:
    config = json.load(f)

# --- LOGGER ---
loggers = {}  # guild_id -> logger

def get_logger_for_guild(guild_id: int, log_filename : str) -> logging.Logger:
    if guild_id not in loggers:
        logger = logging.getLogger("discord_bot")
        logger.setLevel(logging.INFO)

        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        file_handler = logging.FileHandler(f"{log_filename}", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s]: %(message)s",
            "%d-%m-%Y %H:%M:%S"
        ))

        logger.addHandler(file_handler)
        loggers[guild_id] = logger

    return loggers[guild_id]

# ---- BOT ----
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message : discord.Message):
    if message.author == bot.user:
        return

    context = config["servers"][str(message.guild.id)]
    if R.only_read_specified_channels(message, context["rules"]) == False:
        return
    logger = get_logger_for_guild(message.guild.id, context["log_file"])
    image_url = None
    image_text = ""
    logger.info(f"checking message: {message.content}")
    handled_extensions = api_classifier.get_handled_image_extensions()
    if message.attachments:
        for attachment in message.attachments:
            ext = attachment.content_type.split("/")[-1]
            if ext in handled_extensions:
                image_url = attachment.url
                logger.info(f"checking image: {image_url}")

    if image_url:
        image_text = api_classifier.get_text_from_image_url(image_url)

    prompt = api_classifier.prepare_prompt(message.content, context["categories"], context["examples"], image_text)
    return_message = api_classifier.classify(prompt)

    logger.info(f"message: {message.content} got response: {return_message}")
    if return_message["category"] == 0:
        logger.info(f"message: {message.content} classified as category 0, ignoring")
        return
    response_data = next((r for r in context["response"] if r["category"] == return_message["category"]), None)
    if response_data == None:
        logger.error(f"response_data is None for category {return_message['category']}")
        return

    forward_channel = bot.get_channel(response_data["channel_id"])
    if forward_channel is None:
        logger.error(f"forward_channel is None for channel_id {response_data['channel_id']}")
        return

    forward_message = None
    try:
        forward_message = await forward_channel.fetch_message(response_data["message_id"])
    except discord.NotFound:
        logger.error(f"forward_message is None for message_id {response_data['message_id']}")
        return

    jump_link = forward_message.jump_url

    content = (
        f"This is an automated response. If you are asking about: {return_message['label']}"
        f"\n\n"
        f"[Go to FAQ message]({jump_link})"
    )

    await message.reply(content)


bot.run(config["token"])