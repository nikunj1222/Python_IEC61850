#!/usr/bin/python
#from ast import If
import os,sys,time
from winreg import SetValue
import iec61850
import iecClientCtrl
from datetime import datetime

GOOSEctrlblkname = "simpleIOGenericIO/LLN0$GO$gcbAnalogValues"
GOOSEconfRev = 1
GOOSEdatasetRef = "simpleIOGenericIO/LLN0$AnalogValues"
goosedatasetlist = [False, False, False, False]

interface = "3"
print("Using interface : " + interface)
    
dataSetValues = iec61850.LinkedList_create()


'''
iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newIntegerFromInt32(1234));
iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newBinaryTime(False));
iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newIntegerFromInt32(5678));'''

def createdatasetFCDA (fcdalist):
    iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newBoolean(fcdalist[0]))
    iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newBoolean(fcdalist[1]))
    iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newBoolean(fcdalist[2]))
    iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newBoolean(fcdalist[3]))

createdatasetFCDA(goosedatasetlist) 

   
gooseCommParameters =  iec61850.CommParameters()
iec61850.CommParameters_setDstAddress(gooseCommParameters,0x01,0x0c,0xcd,0x01,0x00,0x01)
gooseCommParameters.appId  = 1000
gooseCommParameters.vlanId = 0
gooseCommParameters.vlanPriority = 4
    
publisher = iec61850.GoosePublisher_create(gooseCommParameters, interface)
    
if (publisher):
    iec61850.GoosePublisher_setGoCbRef(publisher, GOOSEctrlblkname)
    iec61850.GoosePublisher_setConfRev(publisher, GOOSEconfRev)
    iec61850.GoosePublisher_setDataSetRef(publisher, GOOSEdatasetRef)
    iec61850.GoosePublisher_setTimeAllowedToLive(publisher, 100)
    
    iec61850.GoosePublisher_publish(publisher, dataSetValues)
    x=iec61850.LinkedList_size(dataSetValues)
    
    
    for i in range (x):
        h=iec61850.LinkedList_get(dataSetValues,0)
        iec61850.LinkedList_remove(dataSetValues,h.data)
    
    
    #print(iec61850.LinkedList_remove(dataSetValues,h.data))
    goosedatasetlist = [True, True, True, True]
    createdatasetFCDA(goosedatasetlist) 
    iec61850.GoosePublisher_publish(publisher, dataSetValues)
    iec61850.GoosePublisher_destroy(publisher)    

else :
    print("Failed to create GOOSE publisher. Reason can be that the Ethernet interface doesn't exist or root permission are required.\n");



    
