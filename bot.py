import asyncio
import discord
import requests
import threading
from discord.ext import commands
import nerimity
import nerimity.channel
import nerimity.message

NERIMITY_TOKEN = 
NERIMITY_BOT_ID = 
NERIMITY_CHANNEL_ID = 
NERIMITY_CHANNEL = nerimity.Channel()
NERIMITY_CHANNEL.id = NERIMITY_CHANNEL_ID

DISCORD_TOKEN = 
DISCORD_CHANNEL_ID = 


def send_message_to_discord(message):
    api_endpoint = f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages"

    headers = {
        "Authorization": 'Bot ' + DISCORD_TOKEN,
    }
    data = {
        "content": message,
    }

    response = requests.post(api_endpoint, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Failed to send message to Discord. Status code: {response.status_code}. Response Text: {response.text}")
        raise requests.RequestException

nerimity_bot = nerimity.Client(
    token=NERIMITY_TOKEN,
    prefix='!',
)

intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(
    command_prefix='!',
    intents=intents
)

@nerimity_bot.listen("on_message_create")
async def nerimity_on_message_create(*args):
    message = args[0]['message']
    if int(message['channelId']) != NERIMITY_CHANNEL_ID:
        return
    if int(message['createdById']) == NERIMITY_BOT_ID:
        return
    if message['type'] != 0:
        return

    out = f'<{message['createdBy']['username']}>: {message['content']}'
    send_message_to_discord(out)

@discord_bot.event
async def on_ready():
    print("Discord bot ready")

@discord_bot.event
async def on_message(message):
    out = f'<{message.author.global_name}>: {message.content}'

    NERIMITY_CHANNEL.send_message(out)
    await discord_bot.process_commands(message)

def run_discord_bot():
    asyncio.run(discord_bot.start(DISCORD_TOKEN))

def run_nerimity_bot():
    nerimity_bot.run()

if __name__ == "__main__":
    discord_thread = threading.Thread(target=run_discord_bot)
    nerimity_thread = threading.Thread(target=run_nerimity_bot)
    
    discord_thread.start()
    nerimity_thread.start()
    
    discord_thread.join()
    nerimity_thread.join()