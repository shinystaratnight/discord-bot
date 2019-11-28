# pip -r install requirements.txt 실행

import asyncio
import discord
from discord.ext import commands

from connector import Connector

TOKEN = "xxxxxxxxx"
client = discord.Client()
mysql_config = {
    'user': '',
    'password': '',
    'host': '',
    'database': '',
    'raise_on_warnings': True
}
cnx = None

@client.event
async def on_ready():
    print('Bot online.')

@client.event
async def on_member_join(member):
    await cnx.register_user(member.id)

@client.event
async def on_message(message):
    await cnx.register_user(message.author.id)
    await cnx.update_user(message)

def exit_gracefully(cnx):
    if cnx is not None:
        del cnx

if __name__ == '__main__':
    try:
        cnx = Connector(mysql_config)
        client.run(TOKEN)
    except Exception:
        print("Error occurred")
    finally:
        exit_gracefully(cnx)