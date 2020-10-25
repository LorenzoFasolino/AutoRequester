import sys
import urllib
import json
import time

PORTA_HTTPS = "443"
PORTA_HTTP = "80"
url = sys.argv[-1]
countHttps = 0
countHttp = 0
countHttp2 = 0
countHttp2Settings = 0
data = None
elencoHttp = set()
elencoHttp2 = set()
i = 0


# prendo il tempo di inizio script
avvio = time.perf_counter()

# metodo utile per leggerere il json che ha chiavi uguali 
def dict_raise_on_duplicates(ordered_pairs):
    """Convert duplicate keys to JSON array."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            if type(d[k]) is list:
                d[k].append(v)
            else:
                d[k] = [d[k], v]
        else:
            d[k] = v
    return d


with open(url, encoding='utf-8') as file:
    f = file.read()
    data = json.loads(f, object_pairs_hook=dict_raise_on_duplicates)

    for d in data:
        tcpDstport = d['_source']['layers']['tcp']['tcp.dstport']
        contenutoLayers = d['_source']['layers']

        # controllo i siti http e https
        if tcpDstport == PORTA_HTTPS:
            countHttps += 1
        elif tcpDstport == PORTA_HTTP:
            countHttp += 1
        else:
            print(tcpDstport + "")

        # prelevo tutti i siti visitati
        if ('http2' in contenutoLayers):
            countHttp2 += 1
            if 'http2.stream' in contenutoLayers['http2']:
                if 'http2.header' in contenutoLayers['http2']['http2.stream']:
                    for elem in contenutoLayers['http2']['http2.stream']['http2.header']:
                        if elem['http2.header.name'] == "referer":
                            urlRichiesta2 = ""
                            http2HeaderValue = elem['http2.header.value']
                            if (str(http2HeaderValue).startswith('https://')):
                                urlRichiesta2 = str(http2HeaderValue).split(
                                    'https://')[1].split('/')[0]
                            elif (str(http2HeaderValue).startswith('http://')):
                                urlRichiesta2 = str(http2HeaderValue).split(
                                    'http://')[1].split('/')[0]
                            else:
                                urlRichiesta2 = str(http2HeaderValue)
                            if urlRichiesta2.strip() != "":
                                if not urlRichiesta2.startswith('www.'):
                                    urlRichiesta2 = "www."+urlRichiesta2
                                elencoHttp2.add(urlRichiesta2)

        elif ('http' in contenutoLayers):
            # cerco  "http.host":
            urlRichiesta = ""
            httpHost = contenutoLayers['http']['http.host']
            if (httpHost.startswith('https://')):
                urlRichiesta = httpHost.split(
                    'https://')[1].split('/')[0]
            elif (httpHost.startswith('http://')):
                urlRichiesta = httpHost.split(
                    'http://')[1].split('/')[0]
            else:
                urlRichiesta = httpHost
            if urlRichiesta.strip() != "":
                if not urlRichiesta.startswith('www.'):
                    urlRichiesta = "www."+urlRichiesta
                elencoHttp.add(urlRichiesta)


# primi 50 siti più visitati al mondo
elencoSitiIniziali = set()
# elenco completo siti chiamati
sitiVisitati = elencoHttp.union(elencoHttp2)

# leggo i 50 siti chiamati da selenium e li memorizzo in un insieme
with open('Top 50 Alexa sites/top-1m.csv') as f:
    for line in f.read().splitlines():
        elencoSitiIniziali.add(line)

# salvo i siti chiamati da script
# i = 1
# with open("result/"+url.split('.')[0].split('/')[1]+"_elencoSitiChiamati.txt", "w+") as out:
#     for item in elencoSitiIniziali:
#         out.write(str(i)+") "+str(item)+"\n")
#         i += 1

# salvo in un insieme i siti di terze parti
i = 1
with open("result/"+url.split('.')[0].split('/')[1]+"_elencoSitiTerziChiamati.txt", "w+") as out:
    for item in sitiVisitati.difference(elencoSitiIniziali):
        out.write(str(i)+") "+str(item)+"\n")
        i += 1

# prendo il tempo di fine script
fine = time.perf_counter()

with open("result/"+url.split('.')[0].split('/')[1]+"_esito.txt", "w+") as f:
    f.write("I pacchetti in totale sono " + str(len(data)) + "\n")
    f.write("I pacchetti https sono " + str(countHttps) + "\n")
    f.write("I pacchetti http2 sono " + str(countHttp2) + "\n")
    f.write("I pacchetti http che non usano ssl sono " +
            str(countHttp) + " (" + (str(len(data)-countHttps)) + ")\n")
    f.write("I siti di interesse visitati sono " +
            str(len(elencoSitiIniziali)) + "\n")
    f.write("I siti di terze parti visitati sono " +
            str(len(sitiVisitati.difference(elencoSitiIniziali))) + "\n")
    f.write("Lo script ha impiegato " +
            str(fine-avvio) + " secondi per essere eseguito\n")
