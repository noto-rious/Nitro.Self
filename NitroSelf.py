from discord.ext import commands
import requests
import re
import sys, os
from os import system
from colored import fg, bg, attr
import logging
import asyncio, json, time, traceback
from random import randint

app_version = 'v1.2.0'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

os.system('cls' if os.name == 'nt' else 'clear')

if os == 'Windows':
    jfile = application_path + '\\token.json'
    bfile = application_path + '\\svr_blacklist.txt'
else:
    jfile = application_path + '/token.json'
    bfile = application_path + '/svr_blacklist.txt'

if os.path.exists(jfile):
    jdata = json.load(open(jfile))
else:
    jdata = open(jfile, 'w')
    jdata.write('{\"token\":\"Token_Here\"}')
    jdata.close()
    json.load(open(jfile))

if os.path.exists(bfile):
    blines = open(bfile).read().split('\n')
else:
    blines = open(bfile, 'w')
    blines.write('')
    blines.close()
    blines = open(bfile).read().split('\n')

print(f'\33]0;Nitro.Self ' + app_version + ' - Developed by: Notorious\a', end='', flush=True)

triedC = []
codeRegex = re.compile('(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)')

color1 = fg('#4EC98F')
color2 = fg('#BA98E4')
color3 = fg('#FF0000')
color4 = fg('#FFC813')
color5 = fg('#335BFF')
color6 = fg('#E0FFFF')
res = attr('reset')

print(color1 + " ███╗   ██╗██╗████████╗██████╗  ██████╗    ███████╗███████╗██╗     ███████╗")
print(" ████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗   ██╔════╝██╔════╝██║     ██╔════╝")
print(" ██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║   ███████╗█████╗  ██║     █████╗  ")
print(" ██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║   ╚════██║██╔══╝  ██║     ██╔══╝  ")
print(" ██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝██╗███████║███████╗███████╗██║     ")
print(" ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝╚══════╝╚══════╝╚═╝ " + app_version + "\n" + res)

vlink = 'https://noto.cf/ns_ver.txt'
f = requests.get(vlink)
if f.text != app_version:
    print(color3 + 'Looks like you may not be running the most current version. Check https://noto.cf/ for an update.\n' + res)

jdata = json.load(open(jfile))
os.environ["rg"] = str(jdata['token'])
token = str(jdata['token'])

if token == "Token_Here":
        print ("You haven't properly configured the \'token.json\' file. Please put your Discord token in token.json using the correct JSON syntax and then run the program again.")
        time.sleep(8)
        sys.exit()

blength = len(blines)-1
print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][🔫] • Black-List Servers Loaded: [' + color2 + str(f"{blength:,d}") + res + ']')

bot = commands.Bot(command_prefix='.', self_bot=True)
ready = False

while True:
    try:
        @bot.event
        async def on_message(message):
            global ready
            if not ready:
                print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][🔫] • Listening for Nitro Codes in [' + color2 + str(len(bot.guilds)) + res + '] servers...')
                ready = True
            else:
                found = 0
                r = ''
                start_time = time.time()
                if codeRegex.search(message.content):
                    codevariable = codeRegex.search(message.content).group(2)
                    print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][🔫] • Checking code: ' + color5 + codevariable + res + ' • [' + color2 +  message.author.name + '#' + message.author.discriminator + res + ']')
                    if codevariable not in triedC:
                        if len(codevariable) == 16:
                            triedC.append(str(codevariable))
                            r = requests.post('https://discordapp.com/api/v6/entitlements/gift-codes/' + codevariable + '/redeem',
                                json={"channel_id": str(message.channel.id)}, headers={'authorization': token}).text
                        else:
                            delay = time.time() - start_time
                            print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][📛] • Fake code: ' + color3 + codevariable + res + ' • [' + color2 +  message.author.name + '#' + message.author.discriminator.replace(' ', '')  + res + '] • (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                    else:
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][❗] • Duplicate code: ' + color3 + codevariable + res + ' • [' + color2 +  message.author.name + '#' + message.author.discriminator.replace(' ', '')  + res + '] • (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                        pass
                    if 'nitro' in str(r):
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][🎉] • Nitro Redeemed: ' + color1 + codevariable + res + ' • [' + color2 +  message.author.name + '#' + message.author.discriminator.replace(' ', '')  + res + ']')
                        found += 1
                        print(f'\33]0;Nitro.Self ' + app_version + ' - Developed by: Notorious - Nitro Redeemed: ' + str(found), end='', flush=True)
                    elif 'This gift has been redeemed already.' in str(r):
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][❗] • Code already claimed: ' + color3 + codevariable + res + ' • [' + color2 +  message.author.name + '#' + message.author.discriminator.replace(' ', '') + res + '] • (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                    elif 'Unknown Gift Code' in str(r):
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][⛔] • Invalid code: ' + color3 + codevariable + res + ' • [' + color2 +  message.author.name + '#' + message.author.discriminator.replace(' ', '')  + res + '] • (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                    elif str(r) == '':
                        pass
                    else:
                        print(r)
                elif (('**giveaway**' in str(message.content).lower() or ('react with' in str(message.content).lower() and 'giveaway' in str(message.content).lower()))) and str(message.guild.id)  not in blines:
                    try:
                        await asyncio.sleep(randint(100, 200))
                        await message.add_reaction("🎉")
                        print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][✅] • Entered Giveaway • [' + color2 +  message.guild.name + ' > ' + message.channel.name + res + ']')
                    except:
                        print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][⛔] • Failed to enter Giveaway • [' + color2 +  message.guild.name + ' > ' + message.channel.name + res + ']')
                elif '<@' + str(bot.user.id) + '>' in message.content and ('giveaway' in str(message.content).lower() or 'won' in str(message.content).lower() or 'winner' in str(message.content).lower()):
                    print(color5 + time.strftime("%H:%M:%S ", time.localtime()) + res, end='')
                    try:
                        won = re.search("You won the \*\*(.*)\*\*", message.content).group(1)
                    except:
                        won = "UNKNOWN"
                    print('[' + color5 + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][🎉] • Congratulations! You won Giveaway: ' + color6 + won + res + ' • [' + color2 +  message.guild.name + ' > ' + message.channel.name + res + ']')

        bot.run(token, bot=False)
    except:
            file = open('Error_Log.txt', 'w')
            file.write(traceback.format_exc())
            file.close()
            exit(0)