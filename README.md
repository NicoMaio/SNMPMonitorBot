# SNMPMonitorBot

DESCRIPTION:
- It's a simple telegram bot that interrogate localhost with snmp query.

INSTALLATION:
- You need to install these packages before running the bot_main.py script:
  - sudo apt-get install libsnmp-dev snmp-mibs-downloader gcc python-dev
  - pip3 install easysnmp
  - pip3 install telepot
  
USAGE: 
- ./bot_main.py

FROM TELEGRAM:
- After create your telegram bot with BotFather, take the token and insert it in bot_main.py on constant: token. And then interrogate the bot from telegram. Write /help to see the commands.
