import time
import discord
import requests
import json
import re
import sys, os
from os import system
import colorama
from colorama import Fore, Back, Style, init
import logging
import asyncio

init()
app_version = 'v1.0.13'

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

if os == 'Windows':
    system('cls')
    jfile = application_path + '\\token.json'
else:
    system('clear')
    print(chr(27) + '[2J')
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

print(Fore.GREEN + " ███╗   ██╗██╗████████╗██████╗  ██████╗    ███████╗███████╗██╗     ███████╗")
print(" ████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗   ██╔════╝██╔════╝██║     ██╔════╝")
print(" ██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║   ███████╗█████╗  ██║     █████╗  ")
print(" ██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║   ╚════██║██╔══╝  ██║     ██╔══╝  ")
print(" ██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝██╗███████║███████╗███████╗██║     ")
print(" ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝╚══════╝╚══════╝╚═╝ " + app_version + "\n" + Fore.RESET)

vlink = 'https://noto.cf/ns_ver.txt'
f = requests.get(vlink)
if f.text != app_version and str(f.text[0]) == 'v':
    print(Fore.LIGHTRED_EX + 'Looks like you may not be running the most current version. Check https://noto.cf/ for an update.\n' + Fore.RESET)

jdata = json.load(open(jfile))
os.environ["rg"] = str(jdata['token'])
token = str(jdata['token'])

if token == "Token_Here":
        print ("You haven't properly configured the \'token.json\' file. Please put your Discord token in token.json using the correct JSON syntax and then run the program again.")
        time.sleep(8)
        sys.exit()

print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.LIGHTBLUE_EX + '→' + Fore.RESET + '] - Listening for Nitro Codes...')

client = discord.Client()

@client.event
async def on_message(message):
    found = 0
    r = ''
    start_time = time.time()
    if codeRegex.search(message.content):
       codevariable = codeRegex.search(message.content).group(2)
       print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.LIGHTBLUE_EX + '→' + Fore.RESET + '] - checking code : ' + Fore.LIGHTBLUE_EX + codevariable + Fore.RESET)
       if codevariable not in triedC:
           if len(codevariable) == 16:
                triedC.append(str(codevariable))
                r = requests.post('https://discordapp.com/api/v6/entitlements/gift-codes/' + codevariable + '/redeem',
                                    headers={'authorization': token})
                r = r.json()
           else:
                delay = time.time() - start_time
                print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.LIGHTRED_EX + 'x' + Fore.RESET + '] - fake code : ' + Fore.LIGHTRED_EX + codevariable + Fore.RESET + ' - (Delay:' + Fore.YELLOW + ' %.3fs' % delay + Fore.RESET + ')')
       else:
           delay = time.time() - start_time
           print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.LIGHTRED_EX + '-' + Fore.RESET + '] - duplicate code : ' + Fore.LIGHTRED_EX + codevariable + Fore.RESET + ' - (Delay:' + Fore.YELLOW + ' %.3fs' % delay + Fore.RESET + ')')
           pass
       if 'nitro' in str(r):

           delay = time.time() - start_time
           print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.GREEN + '+' + Fore.RESET + '] - redeemed nitro : ' + Fore.GREEN + codevariable + Fore.RESET + ' - (Delay:' + Fore.YELLOW + ' %.3fs' % delay + Fore.RESET + ')')
           found += 1
           print(f'\33]0;Nitro.Self ' + app_version + ' - Developed by: Notorious - Nitro Redeemed: ' + str(found), end='', flush=True)
       elif 'This gift has been redeemed already.' in str(r):
           delay = time.time() - start_time
           print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.LIGHTRED_EX + '-' + Fore.RESET + '] - already claimed : ' + Fore.LIGHTRED_EX + codevariable + Fore.RESET + ' - (Delay:' + Fore.YELLOW + ' %.3fs' % delay + Fore.RESET + ')')
       elif 'Unknown Gift Code' in str(r):
           delay = time.time() - start_time
           print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',time.localtime()).rstrip() + Fore.RESET + '][' + Fore.LIGHTRED_EX + '-' + Fore.RESET + '] - invalid code : ' + Fore.LIGHTRED_EX + codevariable + Fore.RESET + ' - (Delay:' + Fore.YELLOW + ' %.3fs' % delay + Fore.RESET + ')')
       elif str(r) == '':
           pass
       else:
           print(r)

client.run(token, bot=False)