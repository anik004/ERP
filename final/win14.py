import os
from os import *
import sys
from sys import *
from log4erp import *



lists = {

	"PRE_DB13" : ['DB2CCDL_PARMS','DB2CCDS_IN','DB2CCDS_PARMS','DB2CCMO_IN1','DB2CCMO_IN2','DB2CCMO_OUTTS','DB2CCMO_PARMS','DBABD','DBABL','DBCHECKORA','DBDIFF','DBSTATC','RSNSPACE','SDBAC','SDBAC_DATA','SDBAC_TEXT','SDBAD','SDBAH','SDBAP','SDBAR','TSORA'],

	"PRE_JOBS" : ['BTCEVTJOB','BTC_CRITERIA','BTC_CRITNODES','BTC_CRITPROFILES','BTC_CRITTYPES','BTC_TYPEFIELDS','TBTCA','TBTCB','TBTCCNTXT','TBTCCTXTT','TBTCCTXTTP','TBTCI','TBTCJSTEP','TBTCO','TBTCP','TBTCR','TBTCS', 'REORGJOBS'],

	"PRE_HTTPURLLOC" : ['HTTPURLLOC'],

	"PRE_STRUST" : ['SSF_PSE_D','SSF_PSE_H','STRUSTCAB','STRUSTCERT','STRUSTCRL','STRUSTCRP','STRUSTCRPT','STRUSTCRR','STRUSTCRRT','STRUSTCRS','STRUSTCRT','TWPSSO2ACL','USERINFO_STORAGE','USRCERTMAP','USRCERTRULE'],

	"PRE_SMTP" : ['SOOD','SOPR','SPH_SERVER','SWT_LOGCAT','SXADDRTYPE','SXADMINTAB','SXDOMAINS','SXNODES','SXROUTE','SXSERV','TSADC'],

	"PRE_SICF" : ['TSADC','ICFBUFFER','ICFDOCU','ICFHANDLER','ICFSERVICE','ICFVIRHOST','RS38T_VAR'],

	"PRE_SE61" : ['DOKENTRY', 'DOKHL', 'DOKIL', 'DOKTL'],

	"PRE_SE06_SCC4" : ['DLV_SYSTC','TRNSPACE'],

	"PRE_RZ12SMLG" : ['RZLLICLASS','RZLLITAB'],

	"PRE_RFC" : ['RFCATTRIB','RFCCHECK','RFCDES','RFCDESSECU','RFCDOC','RFCGO','RFCSYSACL','RFCTA','RFCTRUST'],

	"PRE_PRINTER" : ['TSP03','TSP03A','TSP03C','TSP03D','TSP03L','TSP03POCCNF','TSP03POCPRE','TSP03T','TSPCMDS','TSPLOMS','TSPROMS','TSPSV'],

	"PRE_PARTNER" : ['EDIPHONE','EDIPOA','EDIPOD','EDIPORT','EDMA','EDMAT','EDMMS','EDP12','EDP13','EDP21','EDPAR','EDPI1','EDPO1','EDPO3','EDPP1'],

	"PRE_OPMODE" : ['BTCOMSDL','BTCOMSET','TPFID', 'TSL1T'],

	"PRE_BTCOPTIONS" : ['BTCOPTIONS'],

	"PRE_AL11" : ['USER_DIR'],

	"PRE_RZ70" : ['SLDAGADM'],

	"PRE_SDCCN" : ['/BDL/TASKS'],

	"PRE_SE06SCC4" : ['DLV_SYSTC', 'T000', 'TRNSPACE'],

	"PRE_SMQRSMQS" : ['QIWKTAB', 'QSENDDEST'],

	"PRE_STMS" : ['TMSBUFREQ', 'TMSCSYS'],

	"PRE_TPFET" : ['TPFET', 'TPFHT'],

	"PRE_BD54" : ['TBDLS'],

	"PRE_BD64" : ['TBD00', 'TBD00T', 'TBD06'],

	"PRE_WE21" : ['EDIPHONE','EDIPOA','EDIPOD','EDIPORT','EDMA','EDMAT','EDMMS','EDP12','EDP13','EDP21','EDPAR','EDPI1','EDPO1','EDPO3','EDPP1','EDPPV'],

	"PRE_USER": ['ADCPS','ADR10S','ADR11S','ADR12S','ADR13S','ADR2S','ADR3S','ADR4S','ADR5S','ADR6S','ADR7S','ADR8S','ADR9S','ADRCOMCS','ADRCS','ADRCTS','ADRGPS','ADRGS','ADRPS','ADRTS','ADRUS','ADRVPS','ADRVS','AGR_1016','AGR_1016B','AGR_1250','AGR_1251','AGR_1252','AGR_AGRS','AGR_AGRS2','AGR_ATTS','AGR_BUFFI','AGR_BUFFI2','AGR_BUFFI3','AGR_CUSTOM','AGR_DATEU','AGR_DEFINE','AGR_FLAGS','AGR_FLAGSB','AGR_HIER','AGR_HIER2','AGR_HIER3','AGR_HIERT','AGR_HIERT2','AGR_HIERT3','AGR_HIER_BOR','AGR_HPAGE','AGR_LSD','AGR_MAPP','AGR_MINI','AGR_MINI2','AGR_MINIT','AGR_MINIT2','AGR_NUMBER','AGR_NUM_2','AGR_PROF','AGR_SELECT','AGR_TCDTXT','AGR_TCODES','AGR_TEXTS','AGR_TIME','AGR_TIMEB','AGR_TIMEC','AGR_TIMED','AGR_USERS','CUSADP','FAVO_ROLES','PRGN_CUST','SMENFAVDAT','SMENUSENEW','SMEN_BUFFC','SMEN_BUFFI','SMEN_DATEU','SSM_CUST','SSM_STAT_H','SSM_STAT_P','TPRI_DEF','TTREEF','TVARUVN','USBAPILINK','USCOMPANYS','USERS_SSM','USERS_TMP','USGRP','USGRPT','USGRP_USER','USL04','USLA04','USR01','USR02','USR04','USR05','USR06','USR06SYS','USR08','USR10','USR11','USR12','USR13','USR14','USR21S','USR22','USRACL','USRACLEXT','USRATTR','USREFUS','USREXTID','USREXTIDH','USREXTID_IDM','USRFLD','USRFLDDEF','USRFLDGRP','USRFLDSEL','USRFLDT','USRFLDVAL','USRSTAMP','USRSYSACT','USRSYSACTT','USRSYSPRF','USRSYSPRFT','USR_CUST','UST04','UST10C','UST10S','UST12','USZBVLNDRC','USZBVLNDSC','USZBVPROT','USZBVPROTC','USZBVSYS','USZBVSYSC'],

	"PRE_SM13" : ['SNAP','VBERROR','VBHDR'],

	"PRE_SM69" : ['SXPGCOSTAB','SXPGCOTABE'],

	"PRE_SMQ1SMQ2" : ['ARFCSSTATE','QRFCEVENT','TRFCQDATA','TRFCQIN','TRFCQOUT','TRFCQSTATE'],

	"PRE_TLOCK" : ['TLOCK'],

	"PRE_MONI" : ['MONI']


}
try:
	print str(lists[argv[1].upper()]).strip('[]')


except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
		print "DB:F:GERR_0201:Hostname unknown"
		write('reflogfile.log','DB:F:GERR_0201:Hostname unknown')
		write(loc.strip() + '\\' + ref_id,'DB:F:GERR_0201:Hostname unknown')
	elif str(e).strip() == "list index out of range":
		print "DB:F:GERR_0202:Argument/s missing for the script"
		write('reflogfile.log','DB:F:GERR_0202:Argument/s missing for the script')
		write(loc.strip() + '\\' + ref_id,'DB:F:GERR_0202:Argument/s missing for the script')
	elif str(e) == "Authentication failed.":
		print "DB:F:GERR_0203:Authentication failed."
		write('reflogfile.log','DB:F:GERR_0203:Authentication failed.')
		write(loc.strip() + '\\' + ref_id,'DB:F:GERR_0203:Authentication failed.')
	elif str(e) == "[Errno 110] Connection timed out":
		print "DB:F:GERR_0204:Host Unreachable"
		write('reflogfile.log','DB:F:GERR_0204:Host Unreachable')
		write(loc.strip() + '\\' + ref_id,'DB:F:GERR_0204:Host Unreachable')
	elif "getaddrinfo failed" in str(e):
		print "DB:F:GERR_0205: Please check the hostname that you have provide"
		write('reflogfile.log','DB:F:GERR_0205: Please check the hostname that you have provide')
		write(loc.strip() + '\\' + ref_id,'DB:F:GERR_0205: Please check the hostname that you have provide')
	elif "[Errno None] Unable to connect to port 22" in str(e):
		print "DB:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
		write('reflogfile.log','DB:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
		write(loc.strip() + '\\' + ref_id,'DB:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	else:
		print "DB:W: " + str(e)
		write('reflogfile.log','DB:W: ' + str(e))
		write(loc.strip() + '\\' + ref_id,'DB:W: ' + str(e))
