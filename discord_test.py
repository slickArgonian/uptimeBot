import discord
from uptimes import uptimes

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

        if len(args) != 3:
            await message.channel.send(
                "```You must specify an esologs report code or url and the user_id (case insensitive) of the player you want to gather uptimes for."
                "\nExamples: !uptime https://www.esologs.com/reports/NHtJPYjwfZn1Wqp2 arkaell  \n"
                "          !uptime NHtJPYjwfZn1Wqp2 ArkAeLl```")

        else:
            report = args[1]
            if "reports/" not in report:
                report_code = report
            else:
                start = report.find("reports/")
                report_code = report[start + len("reports/"):]
            user = args[2]
            await message.channel.send("Computing uptimes for " + report_code + " and user " + user)
            res = uptimes(report_code, user)
            await message.channel.send(f"```If a number is in parenthesis next to another number, it means the player "
                                       f"was not the only one to provide the debuff. The parenthesis is the total uptime,"
                                       f" coming from all players"
                                       f"\n\n{res}```")
        # need to draw the different tables and format big dic
        # sea adder a boss? compare fight name to bosses name to separate boss and others?


if __name__ == '__main__':
    client.run(TOKEN)
