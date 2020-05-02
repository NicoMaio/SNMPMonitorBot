#!/usr/bin/python3


from telepot import *
from ops import *

from threading import *
#
# token del bot

token = '1245778549:AAE19xidp5-Vy-iAGW7V5X748pjzC4hQJNc'


class waiterCpu(Thread):

    def __init__(self, *args, **kwargs):
        super(waiterCpu, self).__init__(*args, **kwargs)
        self._stop_event = Event()
        self.fine = False

    def run(self):
        start_rrd_cpu(self)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

waitCpu = waiterCpu()

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

        elif 'start record cpu' in txt:
            waitCpu.start()
            bot.sendMessage(chat_id,"Starting record cpu data...")

        elif 'send cpu image' in txt:
            if not waitCpu.stopped():
                send_image(chat_id,bot)
            else: bot.sendMessage(chat_id,'Il waiter thread è stato stoppato')

        elif 'stop record cpu' in txt:
            waitCpu.stop()
            bot.sendMessage(chat_id,"Ending record cpu data")


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