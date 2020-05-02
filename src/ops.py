from telepot import *
from easysnmp import Session
from easysnmp import exceptions as exce
import rrdtool
import time


class host_info:

    host = "localhost"
    community = "public"
    version = 1

    def get_host(self):
        return self.host

    def get_community(self):
        return self.community

    def get_version(self):
        return self.version

    def set_host(self,new_host):
        self.host = new_host


host_details = host_info()

def saluta(chat_id,name,bot):
    if name == "Nicolò":
        bot.sendPhoto(chat_id,open('cpuGraph.png','rb'))
    else:
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

    bot.sendMessage(chat_id,
                    'scrivi: <start record cpu> per cominciare a registrare i valori della cpu in un rrd database'
                    )

    bot.sendMessage(chat_id,
                    'scrivi: <send cpu image> per ricevere grafico utilizzo cpu'
                    )

    bot.sendMessage(chat_id,
                    'scrivi: <stop record cpu> per stoppare la registrazione di percentuale della CPU in un rrd database'+
                    ' ATTENZIONE: sconsigliato, perché una volta lanciato sarà impossibile ricominciare la registrazione dei dati'
                    )

def imposta_host(chat_id,bot,txt):
    host_details.set_host(txt)
    bot.sendMessage(chat_id,'ho impostato host: '+host_details.get_host())


def imposta_community(chat_id,bot,txt):
    community = txt
    bot.sendMessage(chat_id, 'ho impostato community: ' + community)


def imposta_version(chat_id,bot,txt):
    version = int(txt)
    bot.sendMessage(chat_id, 'ho impostato versione: ' + version)


def get_cpu(chat_id,bot):
    try:
        session = Session(hostname=host_details.get_host(),community=host_details.get_community(),version=host_details.get_version())

        cpuUsage = ""

        if host_details.get_host() == 'localhost':
            cpuUsage = session.get("ssCpuIdle.0")
        else:
            cpuUsage = session.get(".1.3.6.1.4.1.2021.11.11.0")
        cpu = int(cpuUsage.value)

        bot.sendMessage(chat_id,'Percentuale CPU in uso su '+host_details.get_host()+' = '+str(cpu)+"%")

    except exce.EasySNMPError as error:
        bot.sendMessage(chat_id, 'Durante interrogazione ho riscontrato errore su host: ' + host_details.get_host())
        print(error)

def get_memUsage(chat_id,bot):
    try:
        session = Session(hostname=host_details.get_host(),community=host_details.get_community(),version=host_details.get_version())

        memUsage = ""
        if host_details.get_host() == 'localhost':
            memUsage = session.get("memAvailReal.0")
        else:
            memUsage = session.get(".1.3.6.1.4.1.2021.4.6.0")
        mem = int(memUsage.value)

        bot.sendMessage(chat_id,'Memoria della ram utilizzabile su '+host_details.get_host()+' = '+str(mem)+" kB")

    except exce.EasySNMPError as error:
        bot.sendMessage(chat_id, 'Durante interrogazione ho riscontrato errore su host: ' + host_details.get_host())
        print(error)


def get_memTotal(chat_id, bot):
    try:
        session = Session(hostname=host_details.get_host(),community=host_details.get_community(),version=host_details.get_version())

        memTotal = ""
        if host_details.get_host() == 'localhost':
            memTotal = session.get("memTotalReal.0")
        else:
            memTotal = session.get(".1.3.6.1.4.1.2021.4.5.0")
        mem = int(memTotal.value)

        bot.sendMessage(chat_id, 'Memoria della ram totale su ' + host_details.get_host() + ' = ' + str(mem) + " kB")
    except exce.EasySNMPError as error:
        bot.sendMessage(chat_id, 'Durante interrogazione ho riscontrato errore su host: ' + host)
        print(error)

def thread_function(self):
    try :
        session = Session(hostname=host_details.get_host(),community=host_details.get_community(),version=host_details.get_version())
        while not self.stopped():
            perc = session.get('ssCpuIdle.0')
            rrdtool.update('cpu.rrd', 'N:' + str(perc.value))


            time.sleep(5)

    except exce.EasySNMPError as error:
        print(error)

def start_rrd_cpu(waitCpu):
    rrdtool.create('cpu.rrd', '--step', '5', 'DS:cpu:GAUGE:6:0:100', 'RRA:AVERAGE:0.5:1:720')
    thread_function(waitCpu)

def send_image(chat_id,bot):
    rrdtool.graph("cpuGraph.png", "--start", "now-5min", "--end", "now", "DEF:in=cpu.rrd:cpu:AVERAGE",
                  "AREA:in#ff1203:CPUusedReal")
    bot.sendPhoto(chat_id, open('cpuGraph.png', 'rb'))