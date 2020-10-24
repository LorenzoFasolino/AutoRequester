import sys
import urllib
import json

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

        # contro i siti http e https
        if tcpDstport == PORTA_HTTPS:
            countHttps += 1
        elif tcpDstport == PORTA_HTTP:
            countHttp += 1
        else:
            print(tcpDstport + "\n")

        # prelevo tutti i siti visitati
        if ('http2' in contenutoLayers):
            countHttp2 += 1
            if 'http2.stream' in contenutoLayers['http2']:
                if 'http2.header' in contenutoLayers['http2']['http2.stream']:
                    for elem in contenutoLayers['http2']['http2.stream']['http2.header']:
                        if elem['http2.header.name'] == "referer":
                            elencoHttp2.add(elem['http2.header.value'])

        elif ('http' in contenutoLayers):
            # cerco  "http.host":
            elencoHttp.add(contenutoLayers['http']['http.host'])


print("\n\nI pacchetti in totale sono " + str(len(data)) + "\n")
print("I pacchetti https sono " + str(countHttps) + "\n")
print("I pacchetti http2 sono " + str(countHttp2) + "\n")
print("I pacchetti http2 Settings sono " + str(countHttp2Settings) + "\n")
print("I pacchetti http che non usano ssl sono " +
      str(countHttp) + " (" + (str(len(data)-countHttps)) + ")\n")


# TODO forse non serve più salvare i siti nel json
# Ho trovato una soluzione con gli insiemi

# elenco siti visitati dopo il test
# json_data = []
# for item in elencoHttp:
#     json_data.append(item)
# for item in elencoHttp2:
#     json_data.append(item)
# salvo i siti chiamati in un file json
# with open("elencoSitiChiamati.json","w") as out:
#     out.write(json.dumps(json_data))


# stampo i siti http
#print(str(elencoHttp) )
#print(str(elencoHttp2) )


# primi 50 siti più visitati al mondo
elencoSitiIniziali = set()
# elenco completo siti chiamati
insieme = elencoHttp.union(elencoHttp2)



print("***Siti invocati***")
i = 0
with open('Top 50 Alexa sites/top-1m.csv') as f:
    for line in f.read().splitlines():
        elencoSitiIniziali.add(line)
        print(str(i)+") "+str(line))
        i += 1

print("\n\n\n")

# siti di terze parti
print("***Siti di terze parti***")
i = 0
for item in insieme.difference(elencoSitiIniziali):
    print(str(i)+") "+str(item))
    i += 1
