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
    

def function ():
    driver.get("http://www.apple.com")





#avvio il timer
min = sys.argv[-1]

if min=='' or min==None: 
	min=1
else:
	min=int(min)

startTimer(min)  
driver = webdriver.Chrome("./chromedriver")

#avvio ciclo infinito

function()


