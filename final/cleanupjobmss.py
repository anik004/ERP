#print 'PRE:W:The database type "Sybase" is not supported'
# -*- coding: utf-8 -*- 
from paramiko import *
import paramiko
from sys import *
import re
import subprocess

#from log4erp import *
try:
	hostname = argv[1]
        username = argv[2]
        password = argv[3]
        sid = argv[4]
        al11 = argv[5]
        location = al11.strip('\\')
        logfile = argv[6]
        db_name = argv[7]
	domain_name = hostname.strip()
	
	######## Fetching schema details ########

	command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + db_name.upper() + '; select  TOP 1 TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES\\""'
       	print command
        write(location + '\\reflogfile.log',command)
        command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out, err = command.communicate()
                #print out
        write(location + '\\reflogfile.log',out)
        schema = out.split('\n')[5].strip()

	####### list of tables related to JOB ########

	jobtables = ['BTCEVTJOB','BTC_CRITERIA','BTC_CRITNODES','BTC_CRITPROFILES','BTC_CRITTYPES','BTC_TYPEFIELDS','REORGJOBS','TBTCA','TBTCB','TBTCCNTXT','TBTCCTXTT','TBTCCTXTTP','TBTCI','TBTCJSTEP','TBTCO','TBTCP','TBTCR','TBTCS']
	file=open("truncatetable.sql","w+")
	for i in jobtables:
		file.write('Truncate TABLE ' + i + ';')
	file.write("go");
	file.close()
	
	command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname.strip() + ' "sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -i ' + location.strip()[:2] + "\\erp_trans\\truncatetable.sql\""
	if out:
		print "PRE:P:Truncate table is successful on  server " + hostname
	else:
		print "PRE:F:Truncate table  is failed on  server " + hostname
#p = []
#out = str(out).replace(" ","")
#p = ' \n'.join(out.split()) 
#out= (out.strip()).split('\n')
#print type(p)
#for each in out:
#	print each.split(' ')
except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
                print "PRE:F:GERR_0201:Hostname unknown"
        elif str(e).strip() == "list index out of range":
                print "PRE:F:GERR_0202:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "PRE:F:GERR_0203:Authentication failed for the " + string + " system " + hostname + " for user " + sudo_user
        elif str(e) == "[Errno 110] Connection timed out":
                print "PRE:F:GERR_0204:Host Unreachable"
        elif "getaddrinfo failed" in str(e):
                print "PRE:F:GERR_0205: Please check the hostname that you have provide"
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
        else:
                print "PRE:F: " + str(e)

