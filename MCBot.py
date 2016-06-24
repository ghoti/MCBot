import configparser
from discord.ext import commands
import mcrcon

description = '''Basic Minecraft Discord Bot'''
bot = commands.Bot(command_prefix='!', description=description)
rcon = mcrcon.MCRcon()

config = configparser.ConfigParser()
config.read('config.ini')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    rcon_connect()


def rcon_connect():
    rcon.connect(config['minecraft']['host'], int(config['minecraft']['port']))
    rcon.login(config['minecraft']['pass'])


def rcon_disco():
    rcon.disconnect()


@bot.command()
@commands.has_role(config['discord']['roleforcommand'])
async def online():
    rcon_connect()
    if rcon.socket:
        try:
            response = rcon.command('/list')
            if response:
                await bot.say(response)
        except mcrcon.MCRconException:
            await bot.say("Rcon connection failed - Check config")
    else:
        await bot.say("Rcon connection failed - check config")

    rcon_disco()


@bot.command()
@commands.has_role(config['discord']['roleforcommand'])
async def say(*message : str):
    rcon_connect()
    if rcon.socket:
        message = ' '.join(message).strip()
        try:
            response = rcon.command('/say ' + message)
            if response:
                await bot.say(response)
            await bot.say('`{}` sent to everyone.'.format(message))
        except mcrcon.MCRconException:
            await bot.say("Rcon connection failed - check config")
    else:
        await bot.say("Rcon connection failed - check config")

    rcon_disco()


@bot.command()
@commands.has_role(config['discord']['roleforcommand'])
async def whitelist():
    rcon_connect()
    if rcon.socket:
        try:
            response = rcon.command('/whitelist list')
            if response:
                await bot.say(response)
        except mcrcon.MCRconException:
            await bot.say("Rcon connection failed - check config")
    else:
        await bot.say("Rcon connection failed - check config")

    rcon_disco()


@bot.command()
@commands.has_role(config['discord']['roleforcommand'])
async def whitelistadd(*message : str):
    rcon_connect()
    if rcon.socket:
        message = ' '.join(message).strip()
        try:
            response = rcon.command('/whitelist add ' + message)
            if response:
                await bot.say(response)
        except mcrcon.MCRconException:
            await bot.say("Rcon connection failed - check config")
    else:
        await bot.say("Rcon connection failed - check config")

    rcon_disco()


@bot.command()
@commands.has_role(config['discord']['roleforcommand'])
async def whitelistremove(*message : str):
    rcon_connect()
    if rcon.socket:
        message = ' '.join(message).strip()
        try:
            response = rcon.command('/whitelist remove ' + message)
            if response:
                await bot.say(response)
        except mcrcon.MCRconException:
            await bot.say("Rcon connection failed - check config")
    else:
        await bot.say("Rcon connection failed - check config")

    rcon_disco()


bot.run(config['discord']['bottoken'])
