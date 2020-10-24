import sys
import urllib
import json

url = sys.argv[-1]
countHttps = 0
countHttp = 0
countHttpDue = 0
countHttpDueSettings = 0
data = None
i = 0
with open(url, encoding='utf-8') as file:
    data = json.load(file)
    for d in data:
        tcpDstport = d['_source']['layers']['tcp']['tcp.dstport']

        if tcpDstport == "443":
            countHttps += 1
        elif tcpDstport == "80":
            countHttp += 1
        else:
            print(tcpDstport + "\n")

        if ('http2' in d['_source']['layers']):
            countHttpDue += 1
            
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

            
        ip = d['_source']['layers']['ip']['ip.dst']
        #print(str(i)+ ") " +ip)
        i += 1


print("\n\nI pacchetti in totale sono " + str(len(data)) + "\n")
print("I pacchetti https sono " + str(countHttps) + "\n")
print("I pacchetti http2 sono " + str(countHttpDue) + "\n")
print("I pacchetti http2 Settings sono " + str(countHttpDueSettings) + "\n")
print("I pacchetti http che non usano ssl sono " +
      str(countHttp) + " (" + (str(len(data)-countHttps)) + ")\n")


#              "http2.header.name": "referer",
#        "http.host":
