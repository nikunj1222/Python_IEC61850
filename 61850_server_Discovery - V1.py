#!/usr/bin/python
from ast import If
import os,sys,time
from winreg import SetValue
import iec61850
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



##      if (error == iec61850.IED_ERROR_OK):
##              [deviceList, error] = iec61850.IedConnection_getLogicalDeviceList(con)
##              device = iec61850.LinkedList_getNext(deviceList)
##              while device:
##                      LD_name=iec61850.toCharP(device.data)
##                      print("LD: %s" % LD_name)
##                      time.sleep(0.001)
##                      [logicalNodes, error] = iec61850.IedConnection_getLogicalDeviceDirectory(con, LD_name)
##                      logicalNode = iec61850.LinkedList_getNext(logicalNodes)
##                      while logicalNode:
##                              LN_name=iec61850.toCharP(logicalNode.data)
##                              print(" LN: %s" % LN_name)
##                              [LNobjects, error] = iec61850.IedConnection_getLogicalNodeVariables(con, LD_name+"/"+LN_name)
##                              LNobject = iec61850.LinkedList_getNext(LNobjects)
##                              while LNobject:
##                                      print("  DO: %s" % iec61850.toCharP(LNobject.data))
##                                      LNobject = iec61850.LinkedList_getNext(LNobject)
##                              iec61850.LinkedList_destroy(LNobjects)
##                              logicalNode = iec61850.LinkedList_getNext(logicalNode)
##                              #print(iec61850.IedConnection_getFileDirectory())
##                      iec61850.LinkedList_destroy(logicalNodes)
##                      device = iec61850.LinkedList_getNext(device)
##              iec61850.LinkedList_destroy(deviceList)
##              iec61850.IedConnection_close(con)
##      else:
##              print("Failed to connect to %s:%i\n"%(hostname, tcpPort))
##      #iec61850.IedConnection_destroy(con)
	
	def commandTerminationHandler(ctrl):
		#test = iec61850.ControlObjectClient_create(connection)
		lastApplError = iec61850.ControlObjectClient_getLastApplError(ctrl)
		if lastApplError.addCause != 0:
			print ('Received CommandTermination-')
			print ('Control Error Number : ', lastApplError.error)
			print ('Control addCause Number :', lastApplError.addCause)
		else:
			print ('Received CommandTermination+')
			print ('Control Error Number : ', lastApplError.error)
			print ('Control addCause Number :', lastApplError.addCause)
			
	#con = iec61850.ControlObjectClient_create()
	#lastApplError = iec61850.ControlObjectClient_getLastApplError(con)

	#test = iec61850.CommandTermHandler()
	
	if (error == iec61850.IED_ERROR_OK):
		
		control = iec61850.ControlObjectClient_create(ctrlpath, con)
		ctlvalue = iec61850.MmsValue_newBoolean(True)
		iec61850.ControlObjectClient_setOrigin(control, 'script1' , 4)

		if iec61850.ControlObjectClient_selectWithValue(control, ctlvalue) :
			print(iec61850.ControlObjectClient_getLastError(control))
			iec61850.ControlObjectClient_setInterlockCheck(control,True)
			iec61850.ControlObjectClient_setSynchroCheck(control,True)
			cmdselectSt=iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)
			if iec61850.ControlObjectClient_operate(control, ctlvalue, 0):
				print("command operated successfully")
			else :
				print("Commands operation failed")                                
		else :
			print("failed to select")
			
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)
		iec61850.MmsValue_delete(ctlvalue)
		time.sleep(1)
		iec61850.ControlObjectClient_destroy(control)
		
		stVal = iec61850.IedConnection_readObject(con, feedbackSt, iec61850.IEC61850_FC_ST)
		if (error == iec61850.IED_ERROR_OK):
			state = iec61850.MmsValue_getBoolean(stVal[0])
			print("New status after command :", state)
			iec61850.MmsValue_delete(stVal[0])
		else :
			print("Reading Status after command failed")

		iec61850.IedConnection_destroy(con)
