import paramiko
from sys import *
from paramiko import *
import re
import threading
import subprocess
import time
import log4erp
from log4erp import *

sourcehostname = argv[1]
sourceusername = argv[2]
#print sourceusername
sourcepassword = argv[3]
sourcedatabase_sid = argv[4]
user = "ora" + sourcedatabase_sid.lower()
targethostname = argv[5]
targetusername = argv[6]
targetpassword = argv[7]
targetdatabase_sid = argv[8]
#print lastarchive
path_array = []
dbuser = "ora" + targetdatabase_sid.lower()
target_db_user_pass = argv[9]
logfile = argv[10]

try:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( sourcehostname,username = sourceusername, password = sourcepassword)
        channel = client.invoke_shell()


	command = "ls /oracle/" + sourcedatabase_sid.upper() + " >&1 /dev/null"
#       print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#       print status
#       print stdout.readlines()

        if status != 0:
        	print "SCPARCHIVE:F:Provided input for the Source database SID ( " + sourcedatabase_sid + " ) is incorrect"
        	write(logfile,"POST:F:Provided input for the Source database SID ( " + sourcedatabase_sid + " ) is incorrect")
        	exit()
	    
	#command = "python readlog.py " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + sourcedatabase_sid
	#print command
	#command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	#out, err = command.communicate()
	#firstarchive = out.strip()
#	#print "firstarchive"
	#print firstarchive

	#command = "python readfile.py " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + sourcedatabase_sid
	#print command
	#command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        #out, err = command.communicate()
	#lastarchive = out.strip()
	#print "lastarchive"
	#print firstarchive
	#print lastarchive

	archlist1 = []
	print type(archlist1)
        command = 'ls -l /oracle/' + sourcedatabase_sid.upper() + "/oraarch" 
        #print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        archlist = stdout.readlines()
	#print archlist
	for arch in archlist:
		command = "echo " + arch.strip() + "| cut -d\' \' -f 9"
		#print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		out = out.split()
		archlist1 = archlist1 + out
#		print archlist1
		

################################################################ GIVING PERMISSION TO /ORAARCH DIR ############################
	command = "python permission.py " + targethostname + " " + targetusername + " " + targetpassword + " " + targetdatabase_sid + " " + logfile
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
	if "SCPARCHIVE:F:GERR" in out.strip():
		print out
		exit()

	def scpfile(sourcehostname,sourceusername,sourcepassword,sourcedatabase_sid,targethostname,dbuser,target_db_user_pass,targetdatabase_sid,each):
                #print sourceusername
                command = "expect scparch.exp " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + sourcedatabase_sid.upper() + " " + targethostname + " " + dbuser + " " + target_db_user_pass + " " + targetdatabase_sid.upper() + " " + each
                print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
          #      print out

	threads = []
	#print archlist1
	for arch in archlist1:
        	if "arch1" in arch:
			each=arch.split('_')
#			print "second"
#			print each[1]
			#if int(each[1]) >= int(firstarchive) and int(each[1]) <= int(lastarchive):
			arch='/oracle/' + sourcedatabase_sid.upper() + '/oraarch/' + arch.strip()	
#				print "arch"
			print arch
			t = threading.Thread(target=scpfile, args=(sourcehostname, sourceusername, sourcepassword, sourcedatabase_sid.upper(), targethostname, dbuser, target_db_user_pass, targetdatabase_sid.upper(), arch))
                        t.start()
                        threads.append(t)
                        time.sleep(3)
	for t in threads:
           #     print "a"
                t.join()

	command = "python arch_change.py " + targethostname + " " + targetusername + " " + targetpassword + " " + targetdatabase_sid + " " + sourcedatabase_sid
	print command
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()

	command = "python permission.py " + targethostname + " " + targetusername + " " + targetpassword + " " + targetdatabase_sid + " " + logfile
	print command
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()


	print "SCPARCHIVE:P: Archive files have been copied successfuly from Source Server " + sourcehostname + " to the Target Server " + targethostname
	write(logfile,"POST:P Archive files have been copied successfuly from Source Server " + sourcehostname + " to the Target Server " + targethostname)

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "SCPARCHIVE:F:GERR_1301:Source Hostname unknown - " + sourcehostname
                write(logfile,'POST:F: Source Hostname unknown - ' + sourcehostname + ' [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "SCPARCHIVE:F:GERR_1302:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "SCPARCHIVE:F:GERR_1303:Authentication failed to the Source Server - " + sourcehostname
                write(logfile,'POST:F:Authentication failed to the Source Server - ' + sourcehostname + ' [Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "SCPARCHIVE:F:GERR_1304:Source Host Unreachable"
                write(logfile,'POST:F:Source Host Unreachable.[Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "SCPARCHIVE:F:GERR_1305: Please check the Source hostname that you have provide" + sourcehostname
                write(logfile,'POST:F: Please check the Source hostname that you have provide ' + + sourcehostname + ' [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "SCPARCHIVE:F:GERR_1306:Source Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Source Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "SCPARCHIVE:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'Post:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "SCPARCHIVE:F: " + str(e)
                write(logfile,'Post:F: ' + str(e))
