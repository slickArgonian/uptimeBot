
import discord

with open("./discord_token", "r") as tk:
    TOKEN = tk.readlines()[0].strip()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!uptime" in message.content:
        args = message.content.split()
        report = args[1]
        start = report.find("reports/")
        report_code = report[start+len("reports/"):]
        await message.channel.send("here are the uptimes for "+report_code)
client.run(TOKEN)