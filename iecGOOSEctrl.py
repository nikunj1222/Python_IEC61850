import os,sys,time
from winreg import SetValue
from xmlrpc.client import boolean
from pyautogui import FAILSAFE
import iec61850
#from datetime import datetime

def Quality_intvalue(quality):
        if quality == 'QUALITY_VALIDITY_GOOD':
                Quality_int = 0
        elif quality == 'QUALITY_VALIDITY_INVALID':
                Quality_int = 2
        elif quality == 'QUALITY_VALIDITY_RESERVED':
                Quality_int = 1
        elif quality == 'QUALITY_VALIDITY_QUESTIONABLE':
                Quality_int = 3
        elif quality == 'QUALITY_DETAIL_OVERFLOW':
                Quality_int = 4
        elif quality == 'QUALITY_DETAIL_OUT_OF_RANGE':
                Quality_int = 8
        elif quality == 'QUALITY_DETAIL_BAD_REFERENCE':
                Quality_int = 16
        elif quality == 'QUALITY_DETAIL_OSCILLATORY':
                Quality_int = 32
        elif quality == 'QUALITY_DETAIL_FAILURE':
                Quality_int = 64
        elif quality == 'QUALITY_DETAIL_OLD_DATA':
                Quality_int = 128
        elif quality == 'QUALITY_DETAIL_INCONSISTENT':
                Quality_int = 256
        elif quality == 'QUALITY_DETAIL_INACCURATE':
                Quality_int = 512
        elif quality == 'QUALITY_SOURCE_SUBSTITUTED':
                Quality_int = 1024
        elif quality == 'QUALITY_TEST':
                Quality_int = 2048
        elif quality == 'QUALITY_OPERATOR_BLOCKED':
                Quality_int = 4096
        elif quality == 'QUALITY_DERIVED':
                Quality_int = 8192
        else :
                Quality_int = 0  
        return Quality_int

class goosectrl:
        
        GOOSEdatasetlistupdate =  [True, False, True, False, True]
        GOOSEdatasetlistdefault = [True, False, False, False, False, False, False, False, False, False, 'INTERMEDIATE', True, 'QUALITY_TEST'] 
        stNum = 1

        def __init__(self,interfaceid='2',GOOSEappid=1000, GOOSEvlanId=1, GOOSEvlanPriority=7, GOOSEctrlblkname='simpleIOGenericIO/LLN0$GO$gcbAnalogValues',
                        GOOSEconfRev=1, GOOSEdatasetRef='simpleIOGenericIO/LLN0$AnalogValues', TimeAllowedToLive=500, mintime=10, maxtime=1000, timeincreament=10, vlantagstatus=False):                
                self.interfaceid = interfaceid                                 
                self.gooseCommParameters =  iec61850.CommParameters()
                iec61850.CommParameters_setDstAddress(self.gooseCommParameters,0x01,0x0c,0xcd,0x01,0x00,0x01)
                self.gooseCommParameters.appId  = GOOSEappid
                self.gooseCommParameters.vlanId = GOOSEvlanId
                self.gooseCommParameters.vlanPriority = GOOSEvlanPriority
                self.vlantagstatus = vlantagstatus
                self.GOOSEctrlblkname = GOOSEctrlblkname
                self.GOOSEconfRev = GOOSEconfRev
                self.GOOSEdatasetRef = GOOSEdatasetRef
                self.TimeAllowedToLive  = TimeAllowedToLive
                #self.mintime = mintime
                #self.maxtime = maxtime
                #self.timeincreament = timeincreament
                #self.GOOSEtranstime = timeincreament               
                
        '''Create Goose dataset. Function input list of FCDA value and iec61850 dataset instance '''
        def createdatasetFCDA (self,fcdalist, datasetvalueVar):
                for l in range (len(fcdalist)):
                        if fcdalist[l] == False:
                                iec61850.LinkedList_add(datasetvalueVar, iec61850.MmsValue_newBoolean(fcdalist[l]))
                        elif fcdalist[l] == True:
                                iec61850.LinkedList_add(datasetvalueVar, iec61850.MmsValue_newBoolean(fcdalist[l]))
                        elif fcdalist[l] == 'INTERMEDIATE':
                                valueof_l = 0
                                iec61850.LinkedList_add(datasetvalueVar, iec61850.Dbpos_toMmsValue(None, valueof_l))
                        elif fcdalist[l] == 'OPEN':
                                valueof_l = 1
                                iec61850.LinkedList_add(datasetvalueVar, iec61850.Dbpos_toMmsValue(None, valueof_l))
                        elif fcdalist[l] == 'CLOSE':
                                valueof_l = 2
                                iec61850.LinkedList_add(datasetvalueVar, iec61850.Dbpos_toMmsValue(None, valueof_l))
                        elif fcdalist[l] == 'UNDEFINED':
                                valueof_l = 3
                                iec61850.LinkedList_add(datasetvalueVar, iec61850.Dbpos_toMmsValue(None, valueof_l))
                        elif 'QUALITY' in fcdalist[l] :
                                mmsval = iec61850.MmsValue_newBitString(13)
                                iec61850.MmsValue_setBitStringFromIntegerBigEndian(mmsval,Quality_intvalue(fcdalist[l]))
                                iec61850.LinkedList_add(datasetvalueVar, mmsval)

        '''Remove existing FCDA in dataset and update it with new FCDA'''                
        def publishupdatedGOOSE (self,fcdalist, datasetvalueVar, Publisher):
                datasetlength=iec61850.LinkedList_size(datasetvalueVar)
                for i in range (datasetlength):
                        h=iec61850.LinkedList_get(datasetvalueVar,0)
                        iec61850.LinkedList_remove(datasetvalueVar,h.data)
                self.createdatasetFCDA(fcdalist, datasetvalueVar)
                if(self.GOOSEdatasetlistdefault != fcdalist):
                        iec61850.GoosePublisher_setSqNum(Publisher,0)
                        iec61850.GoosePublisher_increaseStNum(Publisher)
                        self.GOOSEdatasetlistdefault = fcdalist
                iec61850.GoosePublisher_publish(Publisher, datasetvalueVar)
                
        def GOOSEPublisher(self):
                print("Using interface : ", self.interfaceid)
                        
                dataSetValues = iec61850.LinkedList_create()

                self.createdatasetFCDA(self.GOOSEdatasetlistupdate,dataSetValues)
                
                publisher = iec61850.GoosePublisher_createEx(self.gooseCommParameters, self.interfaceid, self.vlantagstatus)
                       
                if (publisher):
                        _publishstatus = True
                        iec61850.GoosePublisher_setGoCbRef(publisher, self.GOOSEctrlblkname)
                        iec61850.GoosePublisher_setConfRev(publisher, self.GOOSEconfRev)
                        iec61850.GoosePublisher_setDataSetRef(publisher, self.GOOSEdatasetRef)
                        iec61850.GoosePublisher_setTimeAllowedToLive(publisher, self.TimeAllowedToLive)
                        iec61850.GoosePublisher_publish(publisher, dataSetValues)
                        self.GOOSEdatasetlistdefault = self.GOOSEdatasetlistupdate
                        _DatasetSize = iec61850.LinkedList_size(dataSetValues)
                        
                        try:
                                while True :       
                                        self.publishupdatedGOOSE(self.GOOSEdatasetlistupdate,dataSetValues,publisher)
                                        time.sleep(1)
                                        
                        except KeyboardInterrupt:
                                iec61850.LinkedList_destroy(dataSetValues)
                                iec61850.GoosePublisher_destroy(publisher)
                                 
                else :
                        print("Failed to create GOOSE publisher. Reason can be that the Ethernet interface doesn't exist or root permission are required.\n")
                        _publishstatus = False
                        
                return _DatasetSize,_publishstatus
        