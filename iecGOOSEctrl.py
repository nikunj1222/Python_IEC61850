import os,sys,time
from winreg import SetValue
import iec61850
from datetime import datetime

class goosectrl:
        
        GOOSEdatasetlist = [False]
        
        def __init__(self,interfaceid='3',GOOSEappid=1000, GOOSEvlanId=0, GOOSEvlanPriority=4, GOOSEctrlblkname='simpleIOGenericIO/LLN0$GO$gcbAnalogValues', 
                        GOOSEconfRev=1, GOOSEdatasetRef='simpleIOGenericIO/LLN0$AnalogValues', TimeAllowedToLive=500):                
                self.interfaceid = interfaceid                                 
                self.gooseCommParameters =  iec61850.CommParameters()
                iec61850.CommParameters_setDstAddress(self.gooseCommParameters,0x01,0x0c,0xcd,0x01,0x00,0x01)
                self.gooseCommParameters.appId  = GOOSEappid
                self.gooseCommParameters.vlanId = GOOSEvlanId
                self.gooseCommParameters.vlanPriority = GOOSEvlanPriority
                self.GOOSEctrlblkname = GOOSEctrlblkname
                self.GOOSEconfRev = GOOSEconfRev
                self.GOOSEdatasetRef = GOOSEdatasetRef
                self.TimeAllowedToLive  = TimeAllowedToLive
                
                
        '''Create Goose dataset. Function input list of FCDA value and iec61850 dataset instance '''
        def createdatasetFCDA (self,fcdalist, datasetvalueVar):
                for l in range (len(fcdalist)):
                        iec61850.LinkedList_add(datasetvalueVar, iec61850.MmsValue_newBoolean(fcdalist[l]))

        '''Remove existing FCDA in dataset and update it with new FCDA'''                
        def publishupdatedGOOSE (self,fcdalist, datasetvalueVar, Publisher):
                datasetlength=iec61850.LinkedList_size(datasetvalueVar)
                for i in range (datasetlength):
                        h=iec61850.LinkedList_get(datasetvalueVar,0)
                        iec61850.LinkedList_remove(datasetvalueVar,h.data)
                self.createdatasetFCDA(fcdalist, datasetvalueVar)
                iec61850.GoosePublisher_publish(Publisher, datasetvalueVar)
                
        def GOOSEPublisher(self):
                print("Using interface : ", self.interfaceid)
                        
                dataSetValues = iec61850.LinkedList_create()

                self.createdatasetFCDA(self.GOOSEdatasetlist,dataSetValues)
                
                publisher = iec61850.GoosePublisher_create(self.gooseCommParameters, self.interfaceid)
                       
                if (publisher):
                        _publishstatus = True
                        iec61850.GoosePublisher_setGoCbRef(publisher, self.GOOSEctrlblkname)
                        iec61850.GoosePublisher_setConfRev(publisher, self.GOOSEconfRev)
                        iec61850.GoosePublisher_setDataSetRef(publisher, self.GOOSEdatasetRef)
                        iec61850.GoosePublisher_setTimeAllowedToLive(publisher, self.TimeAllowedToLive)
                        
                        iec61850.GoosePublisher_publish(publisher, dataSetValues)
                        _DatasetSize = iec61850.LinkedList_size(dataSetValues)
                        
                        try:
                                while True :            
                                        self.publishupdatedGOOSE(self.GOOSEdatasetlist,dataSetValues,publisher)
                                        time.sleep(self.TimeAllowedToLive/1000)
                                        
                        except KeyboardInterrupt:                                
                                iec61850.LinkedList_destroy(dataSetValues)
                                iec61850.GoosePublisher_destroy(publisher)
                                 
                else :
                        print("Failed to create GOOSE publisher. Reason can be that the Ethernet interface doesn't exist or root permission are required.\n")
                        _publishstatus = False
                        
                return _DatasetSize,_publishstatus
        