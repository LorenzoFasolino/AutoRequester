import sys
import urllib
import json

PORTA_HTTPS = "443"
PORTA_HTTP = "80"
url = sys.argv[-1]
countHttps = 0
countHttp = 0
countHttpDue = 0
countHttpDueSettings = 0
data = None
elencoHttp = set()
i = 0

with open(url, encoding='utf-8') as file:
    data = json.load(file)
    for d in data:
        
        tcpDstport = d['_source']['layers']['tcp']['tcp.dstport']
        contenutoLayers = d['_source']['layers']

        #contro i siti http e https
        if tcpDstport == PORTA_HTTPS:
            countHttps += 1
        elif tcpDstport == PORTA_HTTP:
            countHttp += 1
        else:
            print(tcpDstport + "\n")

        # prelevo tutti i siti visitati
        if ('http2' in contenutoLayers):
            countHttpDue += 1
            # cerco  "http2.header.name": "referer",

        elif ('http' in contenutoLayers):
            # cerco  "http.host":
            elencoHttp.add(d['_source']['layers']['http']['http.host'])
        
        # pacchetti non meglio identificati
            # if len(d['_source']['layers']['http2'].keys()) > 1:
            #     print("ciaoooo"+str(d['_source']['layers']['http2'].keys()[1]))
            #     for nonLoSo in list(d['_source']['layers']['http2'].items()):
            #         # print(str(d['_source']['layers']['http2']['http2.stream'])+"\n")
            #         #print(str(nonLoSo))
            #         if 'http2.settings' in nonLoSo :
            #             #print(str(nonLoSo))
            #           #  print(str(d['_source']['layers']['http2']['http2.stream']))
            #             countHttpDueSettings += 1
            #     break




print("\n\nI pacchetti in totale sono " + str(len(data)) + "\n")
print("I pacchetti https sono " + str(countHttps) + "\n")
print("I pacchetti http2 sono " + str(countHttpDue) + "\n")
print("I pacchetti http2 Settings sono " + str(countHttpDueSettings) + "\n")
print("I pacchetti http che non usano ssl sono " +
      str(countHttp) + " (" + (str(len(data)-countHttps)) + ")\n")

# stampo i siti http
# print(str(elencoHttp) )
