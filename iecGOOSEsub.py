from asyncio.windows_events import NULL
from datetime import datetime
from operator import sub
import os,sys,time
import signal
from winreg import SetValue
from xmlrpc.client import boolean
import iec61850

class gooseSub:
    
    GooseSubRunning = 1
    _subscribehstatus = False
    subcribeGooseDatasetvalue = {}
    stNum = 0
    sqNum = 0
    timeToLive = 0
    ConfRev = 0
    TestMode = False
    NdsCommissioning = False
    LastGooseupdatetimestamp = 0
    subGoosevalid = False
    
    '''
    def signal_handler(signum, frame):  
        print("Signal ID:", signum, " Frame: ", frame) 

    def sigint_handler(signalId):
        GooseSubRunning = 0
    '''    
    def __init__(self,interfaceid='3',GOOSEappid=0x0002, GOOSEID='TESTP30System/LLN0$GO$gcb01', 
                 GOOSEctrlblkname='TESTP30System/LLN0$GO$gcb01',
                 MacAddress = [0x01,0x0c,0xcd,0x01,0x00,0x00], debugmode = False):
        self.interfaceid = interfaceid
        self.GOOSEappid  = GOOSEappid
        self.GOOSEID = GOOSEID
        self.GOOSEctrlblkname = GOOSEctrlblkname
        self.MacAddress = MacAddress
        self.debugmode = debugmode
                            
                            
    def gooseListner(self, subscriber) :
        print("GOOSE event:\n")
        print('stNum: ', iec61850.GooseSubscriber_getStNum(subscriber))
        print('sqNum: ', iec61850.GooseSubscriber_getSqNum(subscriber))
        print("timeToLive: ", iec61850.GooseSubscriber_getTimeAllowedToLive(subscriber))    
        print("ConfRev: ", iec61850.GooseSubscriber_getConfRev(subscriber))      
        print("Test Mode: ", iec61850.GooseSubscriber_isTest(subscriber))         
        print("Needs Commissioning: ", iec61850.GooseSubscriber_needsCommission(subscriber))     
        print("Publish Goose Dataset Ref: ", iec61850.GooseSubscriber_getDataSet(subscriber))         
        print("Publish Goose GOiD: ", iec61850.GooseSubscriber_getGoId(subscriber))

        RcvgooseTimestamp = iec61850.GooseSubscriber_getTimestamp(subscriber)

        print("Last goose Change timestamp: ", datetime.fromtimestamp(RcvgooseTimestamp/1e3))
        print("Goose message is valid: ", iec61850.GooseSubscriber_isValid(subscriber))

        values = iec61850.GooseSubscriber_getDataSetValues(subscriber)

        buffer=iec61850.MmsValue_printToBuffer(values,1024)

        #print("AllData:\n", buffer[0])
    
    def GOOSESubscriber(self):
        print("Goose Subscribed Using interface : ", self.interfaceid)
        
        receiver = iec61850.GooseReceiver_create()

        iec61850.GooseReceiver_setInterfaceId(receiver, self.interfaceid)

        subscriber = iec61850.GooseSubscriber_create(self.GOOSEctrlblkname, None)

        iec61850.GooseReceiver_addSubscriber(receiver, subscriber)
        iec61850.GooseReceiver_start(receiver)
        

        iec61850.GooseSubscriber_setDstMac(subscriber, self.MacAddress[0],self.MacAddress[1],self.MacAddress[2],self.MacAddress[3],self.MacAddress[4],self.MacAddress[5])
        iec61850.GooseSubscriber_setAppId(subscriber, self.GOOSEappid)

        iec61850.GooseSubscriber_setListener(subscriber, self.gooseListner(subscriber),None)

        if iec61850.GooseReceiver_isRunning(receiver):
            self._subscribehstatus = True
            #signal.signal(signal.SIGINT, signal_handler)
            while self.GooseSubRunning :
                if self.debugmode == True:
                    iec61850.GooseSubscriber_setListener(subscriber, self.gooseListner(subscriber),None)
                self.stNum = iec61850.GooseSubscriber_getStNum(subscriber)
                self.sqNum = iec61850.GooseSubscriber_getSqNum(subscriber)
                self.timeToLive = iec61850.GooseSubscriber_getTimeAllowedToLive(subscriber)
                self.ConfRev = iec61850.GooseSubscriber_getConfRev(subscriber)
                self.TestMode = iec61850.GooseSubscriber_isTest(subscriber)
                self.NdsCommissioning = iec61850.GooseSubscriber_needsCommission(subscriber)
                self.LastGooseupdatetimestamp = iec61850.GooseSubscriber_getTimestamp(subscriber)
                self.subGoosevalid = iec61850.GooseSubscriber_isValid(subscriber)        
                MMSsubGoosedataset = iec61850.GooseSubscriber_getDataSetValues(subscriber)
                buffer=iec61850.MmsValue_printToBuffer(MMSsubGoosedataset,1024)
                self.subcribeGooseDatasetvalue = buffer[0]
                time.sleep(1)
        else :
            print("Failed to start GOOSE subscriber. Reason can be that the Ethernet interface doesn't exist or root permission are required.\n")
            self._subscribehstatus = False
        iec61850.GooseReceiver_stop(receiver)
        iec61850.GooseReceiver_destroy(receiver)
    
    
        