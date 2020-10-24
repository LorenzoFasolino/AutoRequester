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
                d[k] = [d[k],v]
        else:
           d[k] = v
    return d

with open(url, encoding='utf-8') as file:
    f = file.read()
    data = json.loads(f, object_pairs_hook=dict_raise_on_duplicates )

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
            if 'http2.stream' in contenutoLayers['http2']:
                if 'http2.header' in contenutoLayers['http2']['http2.stream']:
                    for elem in contenutoLayers['http2']['http2.stream']['http2.header']:
                        if elem['http2.header.name'] == "referer":
                            elencoHttp2.add(elem['http2.header.value'])


        elif ('http' in contenutoLayers):
            # cerco  "http.host":
            elencoHttp.add(contenutoLayers['http']['http.host'])
        
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

#stampo i siti http
#print(str(elencoHttp) )
#print(str(elencoHttp2) )



json_data = []

for item in elencoHttp:
    json_data.append(item)
for item in elencoHttp2:
    json_data.append(item)

with open("elencoSiti.json","w") as out:
    out.write(json.dumps(json_data))

