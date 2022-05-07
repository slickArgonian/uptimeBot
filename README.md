# UptimeBot

The goal of this project is to build a discord bot that is able to dynamically fetch data from esologs API, and provide a synthetic table of uptimes for a given report and player.

Currently, the bot focuses on uptimes provided by tank players and is limited to debuffs. It should not be too hard to cover buffs and more general roles.

To know which uptimes to compute, the bot checks the gear and the skills of the given player. Output is a table of those uptimes for each boss fight.

## Installation

### Credentials
As the bot is still a big WIP, I recommend creating your own discord bot to get your own token and use it to run the code of this repo. To create a bot, you can follow this [tutorial](https://realpython.com/how-to-make-a-discord-bot-python/). The minimal **permissions** needed are Read Messages and Send Messages. The token of the bot needs to be copied in a file named **discord_token**.

To access esologs API, you need an account on the site and a client. The client can be created at <https://www.esologs.com/api/clients/>. More information on the API is available on the **Web API** section (bottom of the page at <https://www.esologs.com/profile>). 

Once you have the client_id and the client_secret, put them in a file called **credentials**, client_id on the first line and client_secret on the second line.

### Run

Install python packages with the classic: `pip install -r requirements.txt`

The code for the discord bot is in [discord_test](src/discord_test.py). For debug purposes, you can use [main.py](src/main.py).

## Debuffs
The list of supported debuffs is present in the [debuffs file](src/Debuffs.py).

## Hosting
I am using [Okteto](https://cloud.okteto.com) to deploy a locally built docker image in a kubernetes cluster. If you want to try it out, you can put all your tokens in the [config file](./k8s/values.test.yml).

## TODOs

There are some TODOs already present in the code, they are minor modifications that can be done without too much trouble. Here is a list of bigger features to be explored:

- extend to buffs (PA, empower...)
- extend to dd and healer stuff
- bot hosting
- interactive bot. if not enough arguments given, discord bot asks for report code, gets the answer, then asks for players, answer, buffs...
- smarter parallelization