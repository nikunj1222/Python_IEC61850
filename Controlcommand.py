#!/usr/bin/python
#from ast import If
import os,sys,time
from tarfile import XGLTYPE
from winreg import SetValue
import iec61850
import iecClientCtrl
from datetime import datetime
import iecGOOSEctrl
import threading

def datachange():
        while True:
                iecGOOSEctrl.goosectrl.GOOSEdatasetlist = [True, False, False, False, False] 
                
                time.sleep(1)
                
                iecGOOSEctrl.goosectrl.GOOSEdatasetlist = [False, True, False, False, False]
                time.sleep(1)
                
                iecGOOSEctrl.goosectrl.GOOSEdatasetlist = [False, False, True, False, False] 
                time.sleep(1)
                
                iecGOOSEctrl.goosectrl.GOOSEdatasetlist = [False, False, False, True, False]
                time.sleep(1)
                
                iecGOOSEctrl.goosectrl.GOOSEdatasetlist = [False, False, False, False, True]
                time.sleep(1)
        
        
        
if __name__=="__main__":
        hostname = "192.20.30.1";
        tcpPort = 102
        if len(sys.argv)>1:
                hostname = sys.argv[1]
        if len(sys.argv)>2:
                port = sys.argv[2]

        con = iec61850.IedConnection_create()
        error = iec61850.IedConnection_connect(con, hostname, tcpPort)
        ctrlpath = 'TESTP30Control/CSWI1.Pos'
        feedbackSt = 'TESTP30Control/CSWI1.Pos.stVal'
        
        x=iecGOOSEctrl.goosectrl(interfaceid='3',GOOSEappid=2, GOOSEvlanId=0, GOOSEvlanPriority=4, GOOSEctrlblkname='DUMMYSystem/LLN0$GO$gcb01', 
                        GOOSEconfRev=1, GOOSEdatasetRef='DUMMYSystem/LLN0$Dataset1', TimeAllowedToLive=500)
   
        '''MMS connection'''
        if error == iec61850.IED_ERROR_OK :
                
                controlCmd = iecClientCtrl.SBOctrlDPCEnhanced(ctrlpath=ctrlpath,iedconnerr=error,iedconnection=con,
                                                 selectValue=False,operateValue=False,cancelctrl=False,ILKBit=True,SYNCBit=False,TestBit=False,operctrltimeafterselect=1,
                                                 cmdtimeout=1,cmdCategory=3,cmdIdentifier='script',selectctlNum=24,operatectlNum=24)
                '''controlCmd = iecClientCtrl.SBOctrlDPCNormal(ctrlpath=ctrlpath,iedconnerr=error,iedconnection=con
                                                 ,operateValue=True,cancelctrl=False,operctrltimeafterselect=1,
                                                 cmdtimeout=1,cmdCategory=3,cmdIdentifier='script123yoyo',selectctlNum=24,operatectlNum=24)'''
                print('AddCause : ',controlCmd[0],'Error : ',controlCmd[1])

                DPS = iecClientCtrl.ReadDPSValue(con,error,ctrlpath)
                print(DPS[0],DPS[1],DPS[2])

                SPS = iecClientCtrl.ReadSPSValue(con,error,'TESTP30Control/CILO1.EnaOpn')
                print(SPS[0],SPS[1],SPS[2])

                INTST = iecClientCtrl.ReadINTValue(con,error,'TESTP30Control/CSWI1.Mod')
                print(INTST[0],INTST[1],INTST[2])

                FLOATST = iecClientCtrl.ReadFLOATValue(con,error,'TESTP30Measurements/MmuPriMMXU1.TotW')
                print(FLOATST[0],FLOATST[1],FLOATST[2])

                STRST = iecClientCtrl.ReadSTRINGValue(con,error,'TESTP30Control/CSWI1.Pos.SBOw.origin.orIdent')
                print(STRST)

                value = iec61850.MmsValue_newInteger(2)
                iec61850.IedConnection_writeObject(con,'TESTP30System/LLN0.Mod.ctlModel',iec61850.IEC61850_FC_CF,value)

                '''IedConnection_writeInt32Value(IedConnection self, IedClientError* error, const char* objectReference,
                FunctionalConstraint fc, int32_t value)
                IedConnection_writeObject(IedConnection self, IedClientError* error, const char* dataAttributeReference, FunctionalConstraint fc,
                MmsValue* value)
                '''       
        else :
                print('IED connection failed')
                
        iec61850.IedConnection_destroy(con)
        
        z = threading.Thread(target=datachange, args=())
        y = threading.Thread(target=x.GOOSEPublisher, args=())

        z.start()
        y.start()
      
       


