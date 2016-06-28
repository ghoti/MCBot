import configparser
import logging
from discord.ext import commands
import mcrcon

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

description = '''Basic Minecraft Discord Bot'''
bot = commands.Bot(command_prefix='!', description=description)
rcon = mcrcon.MCRcon()

config = configparser.ConfigParser()
config.read('config.ini')

admin = config['discord']['adminrole']
mod = config['discord']['modrole']
user = config['discord']['userrole']


@bot.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(bot.user.name)
    logging.info(bot.user.id)


async def rcon_connect():
    logging.info('Starting RCON connection at {}:{} with pass starting with {}'.
                  format(config['minecraft']['host'], config['minecraft']['port'], config['minecraft']['pass'][:2]))
    try:
        rcon.connect(config['minecraft']['host'], int(config['minecraft']['port']))
        rcon.login(config['minecraft']['pass'])
    except ConnectionRefusedError:
        await bot.say('RCON refused our connection, is it up?')
    except ConnectionError:
        await bot.say('General Network Error, check that bot server can reach RCON server')
    except Exception as e:
        await bot.say('PANIC: {} - This happened'.format(e))


def rcon_disco():
    logging.debug('Disconnecting from RCON')
    if not rcon.socket:
        logging.debug('No server to disconnect from, aborting')
        return
    rcon.disconnect()


async def send_receive_rcon(command):
    logging.info('Sending command {} to rcon and listening for response'.format(command))
    await rcon_connect()
    if rcon.socket:
        try:
            response = rcon.command(command)
            if response:
                await bot.say(response)
        except mcrcon.MCRconException:
            await bot.say('RCON Connection Error - Check config for proper credentials to RCON')

    rcon_disco()


@bot.command()
@commands.has_any_role(admin, mod, user)
async def online():
    '''
    List the users online on the server (maybe)
    '''
    logging.debug('list command called')
    await send_receive_rcon('/list')


@bot.command()
@commands.has_any_role(admin, mod)
async def say(*message: str):
    '''
    Announce to the server as console
    '''
    logging.debug('server announce called')
    message = ' '.join(message).strip()
    await send_receive_rcon('/say ' + message)


@bot.command()
@commands.has_any_role(admin, mod, user)
async def whitelist():
    '''
    Show the whitelist
    '''
    logging.debug('whitelist list called')
    await send_receive_rcon('/whitelist list')


@bot.command()
@commands.has_any_role(admin)
async def whitelistadd(*message : str):
    '''
    Add a user to the whitelist
    '''
    logging.debug('whitelist add called')
    message = ' '.join(message).strip()
    await send_receive_rcon('/whitelist add ' + message)


@bot.command()
@commands.has_any_role(admin)
async def whitelistremove(*message: str):
    '''
    Remove a user from the whitelist
    '''
    logging.debug('whitelist remove called')
    message = ' '.join(message).strip()
    await send_receive_rcon('/whitelist remove ' + message)


@bot.command()
@commands.has_any_role(admin, mod, user)
async def status():
    '''
    Show the status.. of .. some thing!
    '''
    logging.debug('status called')
    await send_receive_rcon('/cofh tps')
	
	
@bot.command()
@commands.has_any_role(admin)
async def forgecraft():
    '''
    Emulates the weather on forgecraft!
    '''
    logging.debug('Forgecraft weather enabled')
    await send_receive_rcon('/weather thunder')


@bot.command()
@commands.has_any_role(admin, mod)
async def kick(*message: str):
    '''
    Kick a fool
    '''
    logging.debug('user kicked called')
    message = ' '.join(message)
    await send_receive_rcon('/kick ' + message)
	

@bot.command()
@commands.has_any_role(admin)
async def ban(*message: str):
    '''
    Ban a fool
    '''
    logging.debug('user banned called')
    message = ' '.join(message)
    await send_receive_rcon('/ban ' + message)

	
@bot.command()
@commands.has_any_role(admin)
async def pardon(*message: str):
    '''
    Pardon a fool you banned
    '''
    logging.debug('user unbanned called')
    message = ' '.join(message)
    await send_receive_rcon('/pardon ' + message)
	
	
bot.run(config['discord']['bottoken'])
