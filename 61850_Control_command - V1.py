#!/usr/bin/python
from ast import If
import os,sys,time
from winreg import SetValue
import iec61850

def ctrlerrorfeedbackstr(Error):
	if Error == 0:
		ctrlerrRcv = 'Ctrl_ERROR_NO_ERROR = 0'
	elif Error == 1:
		ctrlerrRcv = 'Ctrl_ERROR_UNKNOWN = 1'
	elif Error == 2:
		ctrlerrRcv = 'Ctrl_ERROR_TIMEOUT_TEST = 2'
	elif Error == 3:
		ctrlerrRcv = 'Ctrl_ERROR_OPERATOR_TEST = 3'
	else :
		ctrlerrRcv = 'Ctrl error not received or not captured'
	return ctrlerrRcv


def ctrladdcausefeedbackstr(AddCause):

	if AddCause == 0:
		addcauseRcv = 'Addcause_UNKNOWN = 0'
	elif AddCause == 1:
		addcauseRcv = 'Addcause_NOT_SUPPORTED = 1'
	elif AddCause == 2:
		addcauseRcv = 'Addcause_BLOCKED_BY_SWITCHING_HIERARCHY = 2'
	elif AddCause == 3:
		addcauseRcv = 'Addcause_SELECT_FAILED = 3'
	elif AddCause == 4:
		addcauseRcv = 'Addcause_INVALID_POSITION = 4'
	elif AddCause == 5:
		addcauseRcv = 'Addcause_POSITION_REACHED = 5'
	elif AddCause == 6:
		addcauseRcv = 'Addcause_PARAMETER_CHANGE_IN_EXECUTION = 6'
	elif AddCause == 7:
		addcauseRcv = 'Addcause_STEP_LIMIT = 7'
	elif AddCause == 8:
		addcauseRcv = 'Addcause_BLOCKED_BY_MODE = 8'
	elif AddCause == 9:
		addcauseRcv = 'Addcause_BLOCKED_BY_PROCESS = 9'
	elif AddCause == 10:
		addcauseRcv = 'Addcause_BLOCKED_BY_INTERLOCKING = 10'
	elif AddCause == 11:
		addcauseRcv = 'Addcause_BLOCKED_BY_SYNCHROCHECK = 11'
	elif AddCause == 12:
		addcauseRcv = 'Addcause_COMMAND_ALREADY_IN_EXECUTION = 12'
	elif AddCause == 13:
		addcauseRcv = 'Addcause_BLOCKED_BY_HEALTH = 13'
	elif AddCause == 14:
		addcauseRcv = 'Addcause_1_OF_N_CONTROL = 14'
	elif AddCause == 15:
		addcauseRcv = 'Addcause_ABORTION_BY_CANCEL = 15'
	elif AddCause == 16:
		addcauseRcv = 'Addcause_TIME_LIMIT_OVER = 16'
	elif AddCause == 17:
		addcauseRcv = 'Addcause_ABORTION_BY_TRIP = 17'
	elif AddCause == 18:
		addcauseRcv = 'Addcause_OBJECT_NOT_SELECTED = 18'
	elif AddCause == 19:
		addcauseRcv = 'Addcause_OBJECT_ALREADY_SELECTED = 19'
	elif AddCause == 20:
		addcauseRcv = 'Addcause_NO_ACCESS_AUTHORITY = 20'
	elif AddCause == 21:
		addcauseRcv = 'Addcause_ENDED_WITH_OVERSHOOT = 21'
	elif AddCause == 22:
		addcauseRcv = 'Addcause_ABORTION_DUE_TO_DEVIATION = 22'
	elif AddCause == 23:
		addcauseRcv = 'Addcause_ABORTION_BY_COMMUNICATION_LOSS = 23'
	elif AddCause == 24:
		addcauseRcv = 'Addcause_ABORTION_BY_COMMAND = 24'
	elif AddCause == 25:
		addcauseRcv = 'Addcause_NONE = 25'
	elif AddCause == 26:
		addcauseRcv = 'Addcause_INCONSISTENT_PARAMETERS = 26'
	elif AddCause == 27:
		addcauseRcv = 'Addcause_LOCKED_BY_OTHER_CLIENT = 27'
	else :
		addcauseRcv = 'Addcause not received or not captured'
	return addcauseRcv

def commandTerminationHandler(ctrl):
	#test = iec61850.ControlObjectClient_create(connection)
	lastApplError = iec61850.ControlObjectClient_getLastApplError(ctrl)
	if lastApplError.addCause != 0:
		print ('Received CommandTermination- because : ' + ctrladdcausefeedbackstr(lastApplError.addCause) + ' / ' + ctrlerrorfeedbackstr(lastApplError.error)) 
		
	else:
		print ('Received CommandTermination+ because : ' + ctrladdcausefeedbackstr(lastApplError.addCause) + ' / ' + ctrlerrorfeedbackstr(lastApplError.error))

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

		
	if (error == iec61850.IED_ERROR_OK):
		print(type(iec61850.IedConnection_getLastApplError(con)))
		control = iec61850.ControlObjectClient_create(ctrlpath, con)
		ctlvalue = iec61850.MmsValue_newBoolean(True)
		iec61850.ControlObjectClient_setOrigin(control, 'script1' , 3)
		'''iec61850.ControlObjectClient_selectWithValue(control, ctlvalue)  iec61850.ControlObjectClient_selectWithValueAsync(control,iec61850.IED_ERROR_OK,True,commandTerminationHandler,None)''' 
		if iec61850.ControlObjectClient_selectWithValueAsync(control,err=error,ctlVal=ctlvalue,handler=commandTerminationHandler,parameter=None):
			iec61850.ControlObjectClient_setInterlockCheck(control,True)
			iec61850.ControlObjectClient_setSynchroCheck(control,False)
			if iec61850.ControlObjectClient_operate(control, ctlvalue, 500):
				print("command operated successfully")
			else :
				print("Commands operation failed")                                
		else :
			print("failed to select")
			
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)
		
		iec61850.MmsValue_delete(ctlvalue)
		
		time.sleep(3)
		
		iec61850.ControlObjectClient_destroy(control)
		
		stVal = iec61850.IedConnection_readObject(con, feedbackSt, iec61850.IEC61850_FC_ST)
		if (error == iec61850.IED_ERROR_OK):
			state = iec61850.MmsValue_getBitStringAsInteger(stVal[0])
			print("Status after command :", state)
			iec61850.MmsValue_delete(stVal[0])
		else :
			print("Reading Status after command failed")

		iec61850.IedConnection_destroy(con)
