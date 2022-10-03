#!/usr/bin/python
from ast import If
import os,sys,time
from winreg import SetValue
import iec61850
import iecClientCtrl

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

	if error == iec61850.IED_ERROR_OK :
		iecClientCtrl.SBOctrlDPCEnhanced(ctrlpath,feedbackSt,error,con,False,False,False,True,False,False,1)
	else :
		print('IED connection failed')
		
	iec61850.IedConnection_destroy(con)
