from telepot import *
from easysnmp import Session
from easysnmp import exceptions as exce

host = "localhost"
community = "public"
version = 1

def saluta(chat_id,name,bot):
    bot.sendMessage(chat_id, 'ciao %s, sono un bot in fase primordiale' % name)

def send_helper(chat_id,bot):
    bot.sendMessage(chat_id,
                    'scrivi: <imposta host> <host> per impostare host a cui fare richieste snmp')
    bot.sendMessage(chat_id,
                    'scrivi: <imposta community> <public or private or ...> per impostare la community di host richiesto')
    bot.sendMessage(chat_id,

                    'scrivi: <imposta version> <version> per impostare versione per le richieste snmp')
    bot.sendMessage(chat_id,
                    'scrivi: <get memUnused> per ricevere il quantitativo di byte della ram liberi su host')
    bot.sendMessage(chat_id,'scrivi: <get memTotal> per ricevere la dimensione totale della ram dell''host'
                    )

    bot.sendMessage(chat_id,
                    'scrivi: <get cpuUsage> per ricevere percentuale della CPU in uso su host selezionato'
                    )

def imposta_host(chat_id,bot,txt):
    host = txt
    bot.sendMessage(chat_id,'ho impostato host: '+host)

def imposta_community(chat_id,bot,txt):
    community = txt
    bot.sendMessage(chat_id, 'ho impostato community: ' + community)

def imposta_version(chat_id,bot,txt):
    version = int(txt)
    bot.sendMessage(chat_id, 'ho impostato versione: ' + version)

def get_cpu(chat_id,bot):
    try:
        session = Session(hostname=host,community=community,version=version)

        cpuUsage = session.get("ssCpuIdle.0")
        cpu = int(cpuUsage.value)

        bot.sendMessage(chat_id,'Percentuale CPU in uso su '+host+' = '+str(cpu)+"%")

    except exce.EasySNMPError as error:
        bot.sendMessage(chat_id, 'Durante interrogazione ho riscontrato errore su host: ' + host)
        print(error)

def get_memUsage(chat_id,bot):
    try:
        session = Session(hostname=host,community=community,version=version)

        memUsage = session.get("memAvailReal.0")
        mem = int(memUsage.value)

        bot.sendMessage(chat_id,'Memoria della ram utilizzabile su '+host+' = '+str(mem)+" kB")

    except exce.EasySNMPError as error:
        bot.sendMessage(chat_id, 'Durante interrogazione ho riscontrato errore su host: ' + host)
        print(error)


def get_memTotal(chat_id, bot):
    try:
        session = Session(hostname=host, community=community, version=version)

        memTotal = session.get("memTotalReal.0")
        mem = int(memTotal.value)

        bot.sendMessage(chat_id, 'Memoria della ram totale su ' + host + ' = ' + str(mem) + " kB")
    except exce.EasySNMPError as error:
        bot.sendMessage(chat_id, 'Durante interrogazione ho riscontrato errore su host: ' + host)
        print(error)
