from selenium import webdriver
from threading import Timer
import sys

timerHasGone = False;

def stopTimer():
    timerHasGone = True;
    driver.close()
    print("stopped")

def startTimer(min):
    print("starting")
    timerHasGone = False;
    t = Timer((min * 60.0), stopTimer)
    t.start()         
    print("started")    
    

driver = webdriver.Chrome("./chromedriver")
def function ():
    with open("Top 50 Alexa sites/top-1m.csv") as reader:

        line = reader.readline()
        while line != '' and (not timerHasGone):
            driver.get("http://"+line)
            # headlines = driver.find_elements_by_class_name("story-heading")
            # for headline in headlines:
            #     print(headline.text.strip())
            line = reader.readline()

#avvio il timer
min = sys.argv[-1]

if min=='' or min==None: 
	min=1
else:
	min=int(min)

startTimer(min)  

#avvio ciclo infinito
while True and (not timerHasGone):
    function()


