#!/usr/bin/python
#from ast import If
import os,sys,time
from winreg import SetValue
import iec61850

def SPS_St_str(mmsInt):
	if mmsInt == 0:
		SPSValueStr = 'False'
	elif mmsInt == 1:
		SPSValueStr = 'True'
	else:
		SPSValueStr = 'Unknown Value'
		
	return SPSValueStr

def DPS_St_str(mmsInt):
	if mmsInt == 0:
		DPSValueStr = 'Intermediate'
	elif mmsInt == 1:
		DPSValueStr = 'Open'
	elif mmsInt == 2:
		DPSValueStr = 'Closed'
	elif mmsInt == 3:
		DPSValueStr = 'Undefined'
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

def Quality_state(quality):
	if quality == 0:
		Quality_st_str = 'QUALITY_VALIDITY_GOOD 0'
	elif quality == 2:
		Quality_st_str = 'QUALITY_VALIDITY_INVALID 2'
	elif quality == 1:
		Quality_st_str = 'QUALITY_VALIDITY_RESERVED 1'
	elif quality == 3:
		Quality_st_str = 'QUALITY_VALIDITY_QUESTIONABLE 3'
	elif quality == 40:
		Quality_st_str = 'QUALITY_DETAIL_OVERFLOW 4'
	elif quality == 8:
		Quality_st_str = 'QUALITY_DETAIL_OUT_OF_RANGE 8'
	elif quality == 16:
		Quality_st_str = 'QUALITY_DETAIL_BAD_REFERENCE 16'
	elif quality == 32:
		Quality_st_str = 'QUALITY_DETAIL_OSCILLATORY 32'
	elif quality == 64:
		Quality_st_str = 'QUALITY_DETAIL_FAILURE 64'
	elif quality == 128:
		Quality_st_str = 'QUALITY_DETAIL_OLD_DATA 128'
	elif quality == 256:
		Quality_st_str = 'QUALITY_DETAIL_INCONSISTENT 256'
	elif quality == 512:
		Quality_st_str = 'QUALITY_DETAIL_INACCURATE 512'
	elif quality == 1024:
		Quality_st_str = 'QUALITY_SOURCE_SUBSTITUTED 1024'
	elif quality == 2048:
		Quality_st_str = 'QUALITY_TEST 2048'
	elif quality == 4096:
		Quality_st_str = 'QUALITY_OPERATOR_BLOCKED  4096'
	elif quality == 8192:
		Quality_st_str = 'QUALITY_DERIVED 8192'
	else :
		Quality_st_str = 'Quality value not received or not captured'
	return Quality_st_str

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

''' Function to read the SPS status value'''
def ReadSPSValue(iedconnection,iedconnerr,DOpath):
	stValMMS = iec61850.IedConnection_readBooleanValue(iedconnection, (DOpath+'.stVal'), iec61850.IEC61850_FC_ST)
	qualityMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.q'), iec61850.IEC61850_FC_ST)
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
		SPSstate = stValMMS[0]
		SPSquality = iec61850.Quality_fromMmsValue(qualityMMS[0])
		print("SPS State : ", DOpath+'.stVal :' , SPS_St_str(SPSstate))
		print("SPS Quality :", DOpath+'.q :', Quality_state(SPSquality))
		#iec61850.MmsValue_delete(stValMMS[0])
		iec61850.MmsValue_delete(qualityMMS[0])
	else :
		print("Reading Status after command failed")
	return SPSstate,SPSquality

''' Function to read the DPS status value'''
def ReadDPSValue(iedconnection,iedconnerr,DOpath):
	stValMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.stVal'), iec61850.IEC61850_FC_ST)
	qualityMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.q'), iec61850.IEC61850_FC_ST)
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
		DPSstate = iec61850.Dbpos_fromMmsValue(stValMMS[0])
		DPSquality = iec61850.Quality_fromMmsValue(qualityMMS[0])
		print("DPS State : ", DOpath+'.stVal :' , DPS_St_str(DPSstate))
		print("DPS Quality :", DOpath+'.q :', Quality_state(DPSquality))
		iec61850.MmsValue_delete(stValMMS[0])
		iec61850.MmsValue_delete(qualityMMS[0])
	else :
		print("Reading Status after command failed")
	return DPSstate,DPSquality

##''' Function to read the INTEGER from ST status value'''
##def ReadSTINTValue(iedconnection,iedconnerr,DOpath):
##	stValMMS = iec61850.IedConnection_readInt32Value(iedconnection, (DOpath+'.stVal'), iec61850.IEC61850_FC_ST)
##	qualityMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.q'), iec61850.IEC61850_FC_ST)
##	
##	if (iedconnerr == iec61850.IED_ERROR_OK):
##		INTstate = stValMMS[0]
##		INTquality = iec61850.Quality_fromMmsValue(qualityMMS[0])
##		print("INT State : ", DOpath+'.stVal :' , INTstate)
##		print("INT Quality :", DOpath+'.q :', Quality_state(INTquality))
##		iec61850.MmsValue_delete(qualityMMS[0])
##	else :
##		print("Reading Status after command failed")
##	return INTstate,INTquality

''' Function to read the INTEGER from CO status value'''
def ReadCOINTValue(iedconnection,iedconnerr,DOpath):
	stValMMS = iec61850.IedConnection_readInt32Value(iedconnection, (DOpath+'.stVal'), iec61850.IEC61850_FC_CO)
	#qualityMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.q'), iec61850.IEC61850_FC_CO)
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
		INTstate = stValMMS[0]
		#INTquality = iec61850.Quality_fromMmsValue(qualityMMS[0])
		print("INT State : ", DOpath+'.stVal :' , INTstate)
		#print("INT Quality :", DOpath+'.q :', Quality_state(INTquality))
		#iec61850.MmsValue_delete(qualityMMS[0])
	else :
		print("Reading Status after command failed")
	return INTstate

''' Function to read the INTEGER value'''
def ReadINTValue(iedconnection,iedconnerr,DOpath,iecFCType=iec61850.IEC61850_FC_ST):
	stValMMS = iec61850.IedConnection_readInt32Value(iedconnection, (DOpath+'.stVal'), iecFCType)
	qualityMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.q'), iecFCType)
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
		INTstate = stValMMS[0]
		INTquality = iec61850.Quality_fromMmsValue(qualityMMS[0])
		print("INT State : ", DOpath+'.stVal :' , INTstate)
		print("INT Quality :", DOpath+'.q :', Quality_state(INTquality))
		iec61850.MmsValue_delete(qualityMMS[0])
	else :
		print("Reading Status after command failed")
	return INTstate,INTquality

''' Function to read the FLOAT status value'''
def ReadFLOATValue(iedconnection,iedconnerr,DOpath,iecFCType=iec61850.IEC61850_FC_MX):
	stValMMS = iec61850.IedConnection_readFloatValue(iedconnection, (DOpath+'.mag.f'), iecFCType)
	qualityMMS = iec61850.IedConnection_readObject(iedconnection, (DOpath+'.q'), iecFCType)
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
		FLOATValue = stValMMS[0]
		FLOATquality = iec61850.Quality_fromMmsValue(qualityMMS[0])
		print("Float Value : ", DOpath+'.mag.f :' , FLOATValue)
		print("Float Quality :", DOpath+'.q :', Quality_state(FLOATquality))
		iec61850.MmsValue_delete(qualityMMS[0])
	else :
		print("Reading Status after command failed")
	return FLOATValue,FLOATquality

''' Function to read the STRING status value'''
def ReadSTRINGValue(iedconnection,iedconnerr,DOpath,iecFCType=iec61850.IEC61850_FC_CO):
	STRINGValMMS = iec61850.IedConnection_readObject(iedconnection, DOpath , iecFCType)
	if (iedconnerr == iec61850.IED_ERROR_OK):
		OCTETmaxsize = iec61850.MmsValue_getOctetStringMaxSize(STRINGValMMS[0])
		stringbyteValue = []
		for i in range(OCTETmaxsize):
			octetValue = iec61850.MmsValue_getOctetStringOctet(STRINGValMMS[0],i)
			stringbyteValue.append(octetValue)
			stringValue = ''.join(map(chr, stringbyteValue))
		print("Float Value : ", DOpath, ' :' , stringValue)
	else :
		print("Reading Status after command failed")
	return stringValue

''' Function to capture last lastApplError.error != 0 this indicates a CommandTermination- '''
def commandTerminationHandler(ctrl):
	lastApplError = iec61850.ControlObjectClient_getLastApplError(ctrl)
	if lastApplError.addCause != 0:
		print ('Received CommandTermination- because : ' + ctrladdcausefeedbackstr(lastApplError.addCause) + ' / ' + ctrlerrorfeedbackstr(lastApplError.error)) 
		ctrlAddcause = lastApplError.addCause
		ctrlError = lastApplError.error
	else:
		print ('Received CommandTermination+ because : ' + ctrladdcausefeedbackstr(lastApplError.addCause) + ' / ' + ctrlerrorfeedbackstr(lastApplError.error))
		ctrlAddcause = lastApplError.addCause
		ctrlError = lastApplError.error


''' Function for SBO Enhanced DPC control with feedback status check '''
def SBOctrlDPCEnhanced(ctrlpath,iedconnerr,iedconnection,selectValue=False,operateValue=False,cancelctrl=False,
		       ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0,cmdtimeout=3,cmdCategory=3,
		       cmdIdentifier='script', selectctlNum=1,operatectlNum=1):
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
	
		control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)
		iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
		iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)
		iec61850.ControlObjectClient_setTestMode(control, TestBit)
		iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)
		iec61850.ControlObjectClient_setCtlNum(control, selectctlNum)
		
		slctvalue = iec61850.MmsValue_newBoolean(selectValue)
		oprvalue = iec61850.MmsValue_newBoolean(operateValue)
		
		'''Send select'''
		if iec61850.ControlObjectClient_selectWithValue(control, slctvalue) :
			if cancelctrl == True :
				iec61850.ControlObjectClient_cancel(control)
			else :
				'''Send Execute'''
				iec61850.ControlObjectClient_setCtlNum(control, operatectlNum)
				if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
					print("command operated successfully")
				else :
					print("Commands operation failed")                                
		else :
			print("failed to select")

		'''Get the command feedback '''
		feedback=iec61850.ControlObjectClient_getLastApplError(control)
		CmdAddCause = feedback.addCause
		CmdError = feedback.error
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)             

		iec61850.MmsValue_delete(slctvalue)
		iec61850.MmsValue_delete(oprvalue)

		'''Wait for command termination message'''
		time.sleep(cmdtimeout)

		iec61850.ControlObjectClient_destroy(control)

	return CmdAddCause,CmdError

''' Function for Direct Execute Enhanced DPC control with feedback status check '''
def DEctrlDPCEnhanced(ctrlpath,iedconnerr,iedconnecControlObjectClient_setCommandTerminationHandlertion,operateValue=False,
		      ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0.1,cmdtimeout=3,cmdCategory=3,cmdIdentifier='script'):
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
	
		control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)                
		iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
		iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)        
		iec61850.ControlObjectClient_setTestMode(control, TestBit)
		iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)
		
		oprvalue = iec61850.MmsValue_newBoolean(operateValue)
		
		'''Send Execute'''
		if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
			print("command operated successfully")
		else :
			print("Commands operation failed")

		'''Get the command feedback '''
		feedback=iec61850.ControlObjectClient_getLastApplError(control)
		CmdAddCause = feedback.addCause
		CmdError = feedback.error
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)

		iec61850.MmsValue_delete(oprvalue)
				
		'''Wait for command termination message'''
		time.sleep(cmdtimeout)

		iec61850.ControlObjectClient_destroy(control)

	return CmdAddCause,CmdError

''' Function for Direct Execute Enhanced SPC control '''
def DEctrlSPCEnhanced(ctrlpath,iedconnerr,iedconnecControlObjectClient_setCommandTerminationHandlertion,operateValue=False,
		      ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0.1,cmdtimeout=3,cmdCategory=3,cmdIdentifier='script'):
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
	
		control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)                
		iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
		iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)        
		iec61850.ControlObjectClient_setTestMode(control, TestBit)
		iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)
		
		oprvalue = iec61850.MmsValue_newBoolean(operateValue)
		
		'''Send Execute'''
		if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
			print("command operated successfully")
		else :
			print("Commands operation failed")

		'''Get the command feedback '''
		feedback=iec61850.ControlObjectClient_getLastApplError(control)
		CmdAddCause = feedback.addCause
		CmdError = feedback.error
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)

		iec61850.MmsValue_delete(oprvalue)
				
		'''Wait for command termination message'''
		time.sleep(cmdtimeout)

		iec61850.ControlObjectClient_destroy(control)

	return CmdAddCause,CmdError

''' Function for Direct Execute Enhanced APC (Setpoint Integer) control '''
def DEctrlSPINTEnhanced(ctrlpath,iedconnerr,iedconnecControlObjectClient_setCommandTerminationHandlertion,operateValue=0,
		      ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0.1,cmdtimeout=3,cmdCategory=3,cmdIdentifier='script'):
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
	
		control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)                
		iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
		iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)        
		iec61850.ControlObjectClient_setTestMode(control, TestBit)
		iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)
		
		oprvalue = iec61850.MmsValue_newInteger(operateValue)
		
		'''Send Execute'''
		if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
			print("command operated successfully")
		else :
			print("Commands operation failed")

		'''Get the command feedback '''
		feedback=iec61850.ControlObjectClient_getLastApplError(control)
		CmdAddCause = feedback.addCause
		CmdError = feedback.error
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)

		iec61850.MmsValue_delete(oprvalue)
				
		'''Wait for command termination message'''
		time.sleep(cmdtimeout)

		iec61850.ControlObjectClient_destroy(control)

	return CmdAddCause,CmdError

''' Function for Direct Execute Enhanced APC (Setpoint Float) control '''
def DEctrlSPFLOATEnhanced(ctrlpath,iedconnerr,iedconnecControlObjectClient_setCommandTerminationHandlertion,operateValue=0.0,
		      ILKBit=False,SYNCBit=False,TestBit=False,operctrltimeafterselect=0.1,cmdtimeout=3,cmdCategory=3,cmdIdentifier='script'):
	
	if (iedconnerr == iec61850.IED_ERROR_OK):
	
		control = iec61850.ControlObjectClient_create(ctrlpath, iedconnection)                
		iec61850.ControlObjectClient_setInterlockCheck(control,ILKBit)
		iec61850.ControlObjectClient_setSynchroCheck(control,SYNCBit)        
		iec61850.ControlObjectClient_setTestMode(control, TestBit)
		iec61850.ControlObjectClient_setOrigin(control, cmdIdentifier , cmdCategory)
		
		oprvalue = iec61850.MmsValue_newFloat(operateValue)
		
		'''Send Execute'''
		if iec61850.ControlObjectClient_operate(control, oprvalue, operctrltimeafterselect):
			print("command operated successfully")
		else :
			print("Commands operation failed")

		'''Get the command feedback '''
		feedback=iec61850.ControlObjectClient_getLastApplError(control)
		CmdAddCause = feedback.addCause
		CmdError = feedback.error
		iec61850.ControlObjectClient_setCommandTerminationHandler(control,commandTerminationHandler(control), None)

		iec61850.MmsValue_delete(oprvalue)
				
		'''Wait for command termination message'''
		time.sleep(cmdtimeout)

		iec61850.ControlObjectClient_destroy(control)

	return CmdAddCause,CmdError
