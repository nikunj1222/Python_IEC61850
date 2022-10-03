#!/usr/bin/python
#from ast import If
import os,sys,time
from winreg import SetValue
import iec61850

def DPSStstr(mmsInt):
        if mmsInt == 0:
                DPSValueStr = 'Undefined'
        elif mmsInt == 1:
                DPSValueStr = 'Closed'
        elif mmsInt == 2:
                DPSValueStr = 'Open'
        elif mmsInt == 3:
                DPSValueStr = 'Intermediate'
        else:
                DPSValueStr = 'Unknown Value'
                
        return DPSValueStr

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


''' Function to capture last lastApplError.error != 0 this indicates a CommandTermination- '''
def commandTerminationHandler(ctrl):
	#test = iec61850.ControlObjectClient_create(connection)
	lastApplError = iec61850.ControlObjectClient_getLastApplError(ctrl)
	if lastApplError.addCause != 0:
		print ('Received CommandTermination- because : ' + ctrladdcausefeedbackstr(lastApplError.addCause) + ' / ' + ctrlerrorfeedbackstr(lastApplError.error)) 
		
	else:
		print ('Received CommandTermination+ because : ' + ctrladdcausefeedbackstr(lastApplError.addCause) + ' / ' + ctrlerrorfeedbackstr(lastApplError.error))


''' Function to SBO Enhanced DPC control with feedback status check '''
def SBOctrlDPCEnhanced(ctrlpath,ctrlfeedbackst,iedconnerr,iedconnection,selectValue=False,operateValue=False,cancelctrl=False,ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0,cmdtimeout=3,cmdCategory=3,cmdIdentifier='script'):
        
        if (iedconnerr == iec61850.IED_ERROR_OK):
        
                control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)
                iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
                iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)
                iec61850.ControlObjectClient_setTestMode(control, TestBit);
                slctvalue = iec61850.MmsValue_newBoolean(selectValue)
                oprvalue = iec61850.MmsValue_newBoolean(operateValue)
                iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)

                '''Send select'''
                if iec61850.ControlObjectClient_selectWithValue(control, slctvalue) :
                        if cancelctrl == True :
                                iec61850.ControlObjectClient_cancel(control)
                        else :
                                '''Send Execute'''
                                if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
                                        print("command operated successfully")
                                else :
                                        print("Commands operation failed")                                
                else :
                        print("failed to select")

                '''Get the command feedback '''        
                iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)

                iec61850.MmsValue_delete(slctvalue)
                iec61850.MmsValue_delete(oprvalue)

                '''Wait for command termination message'''
                time.sleep(cmdtimeout)

                iec61850.ControlObjectClient_destroy(control)

                ''' Check if status value has changed'''
                stVal = iec61850.IedConnection_readObject(iedconnection, ctrlfeedbackst, iec61850.IEC61850_FC_ST)
                if (iedconnerr == iec61850.IED_ERROR_OK):
                        state = iec61850.MmsValue_getBitStringAsInteger(stVal[0])
                        print("Status after command : ", DPSStstr(state))
                        iec61850.MmsValue_delete(stVal[0])
                else :
                        print("Reading Status after command failed")


''' Function to Direct Execute Enhanced DPC control with feedback status check '''
def DEctrlDPCEnhanced(ctrlpath,ctrlfeedbackst,iedconnerr,iedconnection,operateValue=False,ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0.1,cmdtimeout=3,cmdCategory=3,cmdIdentifier='script'):
        
        if (iedconnerr == iec61850.IED_ERROR_OK):
        
                control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)                
                iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
                iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)          
                oprvalue = iec61850.MmsValue_newBoolean(operateValue)                
                iec61850.ControlObjectClient_setTestMode(control, TestBit);
                iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)
                
                '''Send Execute'''
                if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
                        print("command operated successfully")
                else :
                        print("Commands operation failed")

                '''Get the command feedback '''        
                iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)

                iec61850.MmsValue_delete(oprvalue)
                                
                '''Wait for command termination message'''
                time.sleep(cmdtimeout)

                iec61850.ControlObjectClient_destroy(control)

                ''' Check if status value has changed'''
                stVal = iec61850.IedConnection_readObject(iedconnection, ctrlfeedbackst, iec61850.IEC61850_FC_ST)
                if (iedconnerr == iec61850.IED_ERROR_OK):
                        state = iec61850.MmsValue_getBitStringAsInteger(stVal[0])
                        print("Status after command : ", DPSStstr(state))
                        iec61850.MmsValue_delete(stVal[0])
                else :
                        print("Reading Status after command failed")
