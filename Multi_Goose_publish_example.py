#!/usr/bin/python
#from ast import If
import sys,time
from tarfile import XGLTYPE
from tkinter import S
from winreg import SetValue
import iec61850
import iecClientCtrl
from datetime import datetime
import iecGOOSEctrl
import threading
import logging

iecGOOSEctrl.GoosepublishAction.set()

def datachange():
        while True:
                goose1.GOOSEdatasetlistupdate = [True, False, True, True, False, False, False, False, False, False]                
                time.sleep(1)
                
                goose1.GOOSEdatasetlistupdate = [False, True, False, False, False, False, False, False, False, False]
                time.sleep(1)
                
                '''
                iecGOOSEctrl.goosectrl.GOOSEdatasetlistupdate = [False, False, True, False, False] 
                time.sleep(5)
                
                iecGOOSEctrl.goosectrl.GOOSEdatasetlistupdate = [False, False, False, True, False]
                time.sleep(5)
                
                iecGOOSEctrl.goosectrl.GOOSEdatasetlistupdate = [False, False, False, False, True]
                time.sleep(5)
                '''


def datachange1():
        while True:
                goose2.GOOSEdatasetlistupdate = [True, False, True, True, False]                
                time.sleep(1)
                
                goose2.GOOSEdatasetlistupdate = [False, True, False, False, False]
                time.sleep(1)

#Create and configure logger                
logging.basicConfig(format= '[%(asctime)-4s] [%(filename)-4s] [%(levelname)-4s] %(message)s',
                    handlers=[logging.FileHandler('ScriptLog', mode='w'),logging.StreamHandler(sys.stdout)])

#Creating an LOG object
logger = logging.getLogger(__name__)

#Setting the threshold of the logger DEBUG
logger.setLevel(logging.DEBUG)

goose1 = iecGOOSEctrl.goosectrl(interfaceid='0', GOOSEappid=4, GOOSEvlanId=0, GOOSEvlanPriority=4,
                                   GOOSEctrlblkname='Goose1System/LLN0$GO$gcb01',
                                   GOOSEconfRev=10000, GOOSEdatasetRef='P139System/LLN0$SETGooseDS_1',
                                   TimeAllowedToLive=1000,vlantagstatus=False, MacAddress = [0x01,0x0c,0xcd,0x01,0x00,0x02])

goose2 = iecGOOSEctrl.goosectrl(interfaceid='0', GOOSEappid=4, GOOSEvlanId=0, GOOSEvlanPriority=4,
                                   GOOSEctrlblkname='Goose2System/LLN0$GO$gcb01',
                                   GOOSEconfRev=10000, GOOSEdatasetRef='P139System/LLN0$SETGooseDS_1',
                                   TimeAllowedToLive=1000,vlantagstatus=False)

z = threading.Thread(target=datachange, args=())
w = threading.Thread(target=datachange1, args=())
                
goosepublishthread1 = threading.Thread(target=goose1.GOOSEPublisher, args=())
goosepublishthread2 = threading.Thread(target=goose2.GOOSEPublisher, args=())

z.start()
w.start()
goosepublishthread1.start()
goosepublishthread2.start()


#time.sleep(30)
#iecGOOSEctrl.GoosepublishAction.clear()