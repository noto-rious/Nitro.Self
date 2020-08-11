from discord.ext import commands
import requests
import re
import sys, os
from os import system
from colored import fg, bg, attr
import logging
import asyncio, json, time, traceback

app_version = 'v1.1.2'

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
else:
    jfile = application_path + '/token.json'

if os.path.exists(jfile):
    jdata = json.load(open(jfile))
else:
    jdata = open(jfile, 'w')
    jdata.write('{\"token\":\"Token_Here\"}')
    jdata.close()
    json.load(open(jfile))

#system('title Nitro.Self ' + app_version + ' - Developed by: Notorious')
print(f'\33]0;Nitro.Self ' + app_version + ' - Developed by: Notorious\a', end='', flush=True)

triedC = []
codeRegex = re.compile('(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)')

color1 = fg('#4EC98F')
color2 = fg('#BA98E4')
color3 = fg('#FF0000')
color4 = fg('#FFC813')
color5 = fg('#335BFF')
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

bot = commands.Bot(command_prefix='.', self_bot=True)
ready = False

while True:
    try:
        @bot.event
        async def on_message(message):
            global ready
            if not ready:
                print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color5 + '→' + res + '] - Listening for Nitro Codes in ' + color2 + str(len(bot.guilds)) + res + ' servers...')
                ready = True
            else:
                found = 0
                r = ''
                start_time = time.time()
                if codeRegex.search(message.content):
                    codevariable = codeRegex.search(message.content).group(2)
                    print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color5 + '→' + res + '] - checking code : ' + color5 + codevariable + res)
                    if codevariable not in triedC:
                        if len(codevariable) == 16:
                            triedC.append(str(codevariable))
                            r = requests.post('https://discordapp.com/api/v6/entitlements/gift-codes/' + codevariable + '/redeem',
                                headers={'authorization': token}).text
                            r = r.json()
                        else:
                            delay = time.time() - start_time
                            print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color3 + 'x' + res + '] - fake code : ' + color3 + codevariable + res + ' - (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                    else:
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color3 + '-' + res + '] - duplicate code : ' + color3 + codevariable + res + ' - (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                        pass
                    if 'nitro' in str(r):
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color1 + '+' + res + '] - redeemed nitro : ' + color1 + codevariable + res + ' - (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                        found += 1
                        print(f'\33]0;Nitro.Self ' + app_version + ' - Developed by: Notorious - Nitro Redeemed: ' + str(found), end='', flush=True)
                    elif 'This gift has been redeemed already.' in str(r):
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color3 + '-' + res + '] - already claimed : ' + color3 + codevariable + res + ' - (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                    elif 'Unknown Gift Code' in str(r):
                        delay = time.time() - start_time
                        print('[' + color5 + time.strftime('%m/%d/%Y', time.localtime()).rstrip() + ' ' + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + res + '][' + color3 + '-' + res + '] - invalid code : ' + color3 + codevariable + res + ' - (Delay:' + color4 + ' %.3fs' % delay + res + ')')
                    elif str(r) == '':
                        pass
                    else:
                        print(r)


        bot.run(token, bot=False)
    except:
            file = open('Error-Log.txt', 'w')
            file.write(traceback.format_exc())
            file.close()
            exit(0)