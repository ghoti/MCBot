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

    print('logging in...')
    rcon.connect(config['minecraft']['host'], int(config['minecraft']['port']))
    rcon.login(config['minecraft']['pass'])

@bot.command()
async def online():
    try:
        response = rcon.command('/list')
        if response:
            await bot.say(response)
    except Exception as e:
        print(e)

@bot.command()
async def say(*message : str):
    message = ' '.join(message).strip()
    try:
        response = rcon.command('/say ' + message)
        if response:
            await bot.say(response)
        await bot.say('`{}` sent to everyone.'.format(message))
    except Exception as e:
        print(e)

@bot.command()
async def whitelist():
    try:
        response = rcon.command('/whitelist list')
        if response:
            await bot.say(response)
            print(type(response))
    except Exception as e:
        print(e)



bot.run(config['discord']['bottoken'])