import paramiko
from sys import *
import ntpath
from paramiko import *
import log4erp
from log4erp import *
import re
import threading 
import subprocess


def check(hostname,username,passwd,database_sid,user,dest,logfile):
	try:
		path_array = []
		client = SSHClient()
        	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	        client.connect( hostname,username = username, password = passwd)
	        channel = client.invoke_shell()


		if dest == "source":
		        command = "ls /home/" + user + "/control_script_" + database_sid.upper() + ".sql >&1 /dev/null"
		        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		        status = stdout.channel.recv_exit_status()
		        if status == 0:
				command = "mv -f /home/" + user + "/control_script_" + database_sid.upper() + ".sql /home/" + user + "/control_script_" + database_sid.upper() + ".bkp.sql"
				stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
				status = stdout.channel.recv_exit_status()

			        command = 'sudo su - ' + user + ' -c "echo \'alter database backup controlfile to trace as \'\\\'/home/' + user + '/control_script_' + database_sid.upper() + '.sql\\\'\';\' > /home/' + user + '/sql.sql;chmod 777 /home/' + user + '/sql.sql"'
        			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			        status = stdout.channel.recv_exit_status()

			        command = 'sudo su - ' + user + ' -c "echo @/home/' + user + '/sql.sql | sqlplus system/Welcome2" | grep -i "ERROR:"'
			        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			        if stdout.readlines():
		        	        print "SCPFILE:F: The database is not available in the Source host ( " + hostname + ")"
			                write(logfile,"POST:F: The database is not available in the Source host ( " + hostname + ")")
			                exit()
        				status = stdout.channel.recv_exit_status()


	        sftp_client = client.open_sftp()
        	command = '/home/' + user + '/control_script_' + database_sid.upper() + '.sql' # | grep -i "sapdata*"' # variable IN
	        remote_file = sftp_client.open(command)
        	remote_file = list(set(remote_file))
		for line in remote_file:
        	        paths = ""
                	if "ALTER" not in line:
                        	if re.search("sapdata", line):
                                	directory = line.split("/")
	                                for dire in directory:
        	                                if "sapdata" in dire:
                	                                paths = str(paths) + "/" + str(dire)
                        	                        break
                                	        else:
                                        	        paths = str(paths) + "/" + str(dire)
	                                path_array.append(paths[4:])

	        path_array = list(set(path_array))
		if path_array is not None:
			for folder in path_array:
				command = "chmod -R 777 " + folder
		#		print command
				stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		#		print stdout.channel.recv_exit_status() 
			return (path_array)
		else:
			print "POST:F:GERR_0506:Failed to fetch the mount points of server" + hostname
			write(logfile,"POST:F:GERR_0506:Failed to fetch the mount points of server" + hostname)

		channel.close()
		client.close()
	
	except Exception as e:
		if str(e) == "[Errno -2] Name or service not known":
	                print "POST:F:GERR_1101:" + dest + " Hostname unknown - " + hostname
        	        write(logfile,'POST:F:' + dest + ' Hostname unknown - ' + hostname + ' [Error Code - 1101]')
			exit()
	        elif str(e) == "list index out of range":
        	        print "POST:F:GERR_1102:Argument/s missing for the script"
	        elif str(e) == "Authentication failed.":
        	        print "POST:F:GERR_1103:Authentication failed to the " + dest + " Server - " + hostname
                	write(logfile,'POST:F:Authentication failed to the ' + dest + ' Server - ' + hostname + ' [Error Code - 1103]')
			exit()
	        elif str(e) == "[Errno 110] Connection timed out":
        	        print "POST:F:GERR_0504:" + dest + " Host Unreachable - " + hostname
                	write(logfile,'POST:F:GERR_0504:' + dest + ' Host Unreachable - ' + hostname)
			exit()
	        elif "getaddrinfo failed" in str(e):
        	        print "POST:F:GERR_0505: Please check the " + dest + " hostname that you have provide"
                	write(logfile,'POST:F:GERR_0505: Please check the ' + dest + ' hostname that you have provide')
			exit()
	        elif "[Errno None] Unable to connect to port 22 on" in str(e):
        	        print "POST:F:GERR_0506:" + dest + " Host Unreachable or Unable to connect to port 22"
                	write(logfile,'POST:F:GERR_0506:' + dest + ' Host Unreachable or Unable to connect to port 22')
			exit()
	        elif "invalid decimal" in str(e):
        	        print "POST:F:GERR_0507:Unknown Error:" + str(e)
                	write(logfile,'POST:F:GERR_0507:Unknown Error:' + str(e))
			exit()
	        else:
        	        print "POST:F:" + str(e)
			write(logfile,'POST:F: ' + str(e) + ' - ' + hostname)
			exit()

try:
	
	sourcehostname = argv[1]
	sourceusername = argv[2]
	sourcepassword = argv[3]
	sourcedatabase_sid = argv[4]
	user = "ora" + sourcedatabase_sid.lower()
	source = "source"
	targethostname = argv[5]
	targetusername = argv[6]
	targetpassword = argv[7]
	targetdatabase_sid = argv[8]
	user1 = "ora" + targetdatabase_sid.lower()
	target = "target"
	path_array = []
	logfile = argv[9]

	target_arr = check(targethostname,targetusername,targetpassword,targetdatabase_sid,user1,target,logfile)
	print target_arr
	source_arr = check(sourcehostname,sourceusername,sourcepassword,sourcedatabase_sid,user,source,logfile)
	print source_arr

	client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( targethostname,username = targetusername, password = targetpassword)
        channel = client.invoke_shell()

	for folder in target_arr:
		command = "chmod 777 " + folder
		print command
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                status = stdout.channel.recv_exit_status()

	def scpfile(sourcehostname,sourceusername,sourcepassword,sourcedatabase_sid,targethostname,targetusername,targetpassword,targetdatabase_sid,each):
               #	print sourceusername 
		#command = "expect scp.exp " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + sourcedatabase_sid.upper() + " " + targethostname + " " + targetusername + " " + targetpassword + " " + targetdatabase_sid.upper() + " " + each
                #print command
		#command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
     		#out, err = command.communicate()
	#threads = []
	#threadcount=threading.activeCount()
	#print len(threads)
	#count = 1
	#for each in source_arr:
	#	print "each"
        #       	print each
        #       	t = threading.Thread(target=scpfile, args=(sourcehostname, sourceusername, sourcepassword, sourcedatabase_sid.upper(), targethostname, targetusername, targetpassword, targetdatabase_sid.upper(), each.strip()))
		#print t
       	#	t.start()
         #      	threads.append(t)
	#for t in threads:
		#print "a"
	#	t.join()
	#print "POST:P:Database Files has been copied successfully from the source server - " + sourcehostname  + " to the target server - " + targethostname
	#write(logfile,"POST:P:Database Files has been copied successfully from the source server - " + sourcehostname  + " to the target server - " + targethostname)

	#for folder in target_arr:
         #       command = "chmod -R 777 " + folder
	#	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
         #       status = stdout.channel.recv_exit_status()
	

	a = sorted(source_arr)
	i = 0
	counter = 1
	for arry in sorted(target_arr):
		if ntpath.basename(a[i]) != ntpath.basename(arry):
	                command = "mv /home" + a[i] + " /home" + arry
			print command
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			print stdout.readlines()
	                status = stdout.channel.recv_exit_status()
			if status != 0:
				counter = counter + 1
		if counter != 1 and (ntpath.basename(a[i]) != ntpath.basename(arry)):
			print "POST:F:Failed to rename the Target Server - " + targethostname + " mountpoints name"
			write(logfile,"POST:F:Failed to rename the Target Server - " + targethostname + " mountpoints name")
		elif counter == 1 and ntpath.basename(a[i]) != ntpath.basename(arry):
			print "POST:P:Target Server - " + targethostname + " mountpoints names has been renamed Successfully"
			write(logfile,"POST:P:Target Server - " + targethostname + " mountpoints names has been renamed Successfully")
		
		i = i+1
		
	channel.close()
	client.close()


except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
	        print "POST:F:GERR_1101:Target Hostname unknown - " + targethostname
                write(logfile,'POST:F:Target Hostname unknown - ' + targethostname + ' [Error Code - 1101]')
        elif str(e) == "list index out of range":
                print "POST:F:GERR_1102:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "POST:F:GERR_1103:Authentication failed to the Target Server - " + targethostname
                write(logfile,'POST:F:Authentication failed to the Target Server - ' + targethostname + ' [Error Code - 1103]')
        elif str(e) == "[Errno 110] Connection timed out":
                print "POST:F:GERR_0504:Target Host Unreachable - " + targethostname
                write(logfile,'POST:F:GERR_0504:Target Host Unreachable - ' + targethostname)
        elif "getaddrinfo failed" in str(e):
                print "POST:F:GERR_0505: Please check the Target hostname that you have provide"
                write(logfile,'POST:F:GERR_0505: Please check the Target hostname that you have provide')
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "POST:F:GERR_0506:Target Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F:GERR_0506:Target Host Unreachable or Unable to connect to port 22')
        elif "invalid decimal" in str(e):
                print "POST:F:GERR_0507:Unknown Error:" + str(e)
                write(logfile,'POST:F:GERR_0507:Unknown Error:' + str(e))
        else:
                print "POST:F:" + str(e)
                write(logfile,'POST:F: ' + str(e) + ' - ' + targethostname)
