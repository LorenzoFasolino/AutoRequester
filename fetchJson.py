import sys
import urllib, json

url = sys.argv[-1]
countHttps = 0
countHttp = 0
data=None
i=0
with open(url, encoding='utf-8') as file:
    data = json.load(file)
    for d in data:
        tcpDstport = d['_source']['layers']['tcp']['tcp.dstport']
        
        if tcpDstport == "443":
            countHttps+=1
        elif tcpDstport == "80": 
            countHttp+=1
        else:
            print(tcpDstport + "\n")
        
        ip=d['_source']['layers']['ip']['ip.dst']
        print(str(i)+ ") " +ip)
        i+=1          
            


print("\n\nI pacchetti in totale sono " + str(len(data)) + "\n")
print("I pacchetti https sono " + str(countHttps) + "\n")
print("I pacchetti http sono " + str(countHttp) + " ("+ (str(len(data)-countHttps) )+ ")\n")
