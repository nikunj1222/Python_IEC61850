#!/usr/bin/python
#from ast import If
import sys,time
from tarfile import XGLTYPE
from tkinter import S
from winreg import SetValue
import iec61850
import iecClientCtrl
from datetime import datetime
import iecGOOSEsub
import threading
import logging

x = iecGOOSEsub.gooseSub(debugmode = False)

goosesubthread = threading.Thread(target=x.GOOSESubscriber, args=())
goosesubthread.start()

while True :
        print(x.ConfRev, x._subscribehstatus, x.subcribeGooseDatasetvalue, x.stNum,
      x.sqNum, x.timeToLive, x.TestMode, x.NdsCommissioning, x.LastGooseupdatetimestamp, x.subGoosevalid)
        time.sleep(0.5)