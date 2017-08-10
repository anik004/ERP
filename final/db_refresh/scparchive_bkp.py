import paramiko
from sys import *
from paramiko import *
import re
import threading
import subprocess
import time

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
firstarchive = argv[9]
#print firstarchive
lastarchive = argv[10]
#print lastarchive
path_array = []

try:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( sourcehostname,username = sourceusername, password = sourcepassword)
        channel = client.invoke_shell()


        command = 'ls -l /oracle/' + sourcedatabase_sid.upper() + '/oraarch | cut -d\' \' -f 9'
        print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        archlist = stdout.readlines()
	print archlist
	print "archlist"
#        print len(archlist)
#	print "first"
	print type(archlist)

	def scpfile(sourcehostname,sourceusername,sourcepassword,sourcedatabase_sid,targethostname,targetusername,targetpassword,targetdatabase_sid,each):
                #print sourceusername
                command = "expect scparch.exp " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + sourcedatabase_sid.upper() + " " + targethostname + " " + targetusername + " " + targetpassword + " " + targetdatabase_sid.upper() + " " + each
                print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
          #      print out

	threads = []

	for arch in archlist:
		print "arch"
		print arch
        	if "arch1" in arch:
			each=arch.split('_')
#			print "second"
			print each[1]
			if int(each[1]) >= int(firstarchive) and int(each[1]) <= int(lastarchive):
				arch='/oracle/' + sourcedatabase_sid.upper() + '/oraarch/' + arch.strip()	
#				print "arch"
				print arch
				t = threading.Thread(target=scpfile, args=(sourcehostname, sourceusername, sourcepassword, sourcedatabase_sid.upper(), targethostname, targetusername, targetpassword, targetdatabase_sid.upper(), arch))
                                t.start()
                                threads.append(t)
                                time.sleep(1)
	for t in threads:
           #     print "a"
                t.join()
        print "finished"

######################################################## CHANGING ARCHIVE FILENAME ######################################################

#	command = "sudo mv /oracle/" + targetdatabase_sid + "/ /home/" + t_user + "/control_script_" + t_db_sid.upper() + ".sql"
		

except Exception as e:
    print "F: " + str(e)
