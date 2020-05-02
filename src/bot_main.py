#!/usr/bin/python3


from telepot import *
from ops import *

from threading import Thread
#
# token del bot
token = '***************************************'

#
# funzione che gestisce il messaggio appena ricevuto dal bot
def on_chat_message(msg):
    content_type, chat_type, chat_id = glance(msg)

    # switch sul tipo di messaggio ricevuto
    if content_type == 'text':
        name = msg["from"]["first_name"]
        text = msg['text']
        txt = text.lower()

        # switch su prima parola del messaggio
        if txt == 'ciao' or txt =='ciao bot':
            saluta(chat_id,name,bot)


        # helper
        elif txt == '/help' or txt == '/start':
            send_helper(chat_id,bot)

        elif 'imposta host' in txt:
            elenco = txt.split(' ')
            imposta_host(chat_id,bot,elenco[2])

        elif 'imposta community' in txt:
            elenco = txt.split(' ')
            imposta_community(chat_id,bot,elenco[2])

        elif 'imposta version' in txt:
            elenco = txt.split(' ')
            imposta_version(chat_id,bot,elenco[2])

        elif 'get memunused' in txt:
            get_memUsage(chat_id, bot)

        elif 'get memtotal' in txt:
            get_memTotal(chat_id, bot)

        elif 'get cpuusage' in txt:
            get_cpu(chat_id, bot)


bot = Bot(token)

class listener(Thread):
    def run(self):
        bot.message_loop(on_chat_message)




def run():
    listener().start()

run()
#
# avvio loop per gestire richieste
import time
while 1:
    time.sleep(10)