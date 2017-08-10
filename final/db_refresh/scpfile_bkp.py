import paramiko
from sys import *
from paramiko import *
import re
import threading 
import subprocess

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
path_array = []
	

try:
	client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( sourcehostname,username = sourceusername, password = sourcepassword)
        channel = client.invoke_shell()

        command = "sudo ls /oracle/" + sourcedatabase_sid.upper() + " >&1 /dev/null"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()

        if status != 0:
            print "SAPFILE:F: Provided input for the database SID ( " + sourcedatabase_sid + " ) in " + sourcehostname + " host is incorrect"

            exit()

        command = "sudo ls /home/" + user + "/control_script_" + sourcedatabase_sid.upper() + ".sql >&1 /dev/null"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
        if status == 0:
            command = "sudo mv /home/" + user + "/control_script_" + sourcedatabase_sid.upper() + ".sql /home/" + user + "/control_script_" + sourcedatabase_sid.upper() + ".bkp.sql"
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.channel.recv_exit_status()

        command = 'sudo su - ' + user + ' -c "echo \'alter database backup controlfile to trace as \'\\\'/home/' + user + '/control_script_' + sourcedatabase_sid.upper() + '.sql\\\'\';\' > /home/' + user + '/sql.sql;chmod 777 /home/' + user + '/sql.sql"'
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()

        command = 'sudo su - ' + user + ' -c "echo @/home/' + user + '/sql.sql | sqlplus system/Welcome2" | grep -i "ERROR:"'
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        if stdout.readlines():
                print "SAPFILE:F: The database is not available in the " + system_name + " host ( " + sourcehostname + ")"
                #write(logfile,"DB:F: The database is not available in the " + system_name + " host ( " + sourcehostname + ")")
                exit()
        status = stdout.channel.recv_exit_status()


        sftp_client = client.open_sftp()
        command = '/home/' + user + '/control_script_' + sourcedatabase_sid.upper() + '.sql' # | grep -i "sapdata*"' # variable IN
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
        #print path_array

	def scpfile(sourcehostname,sourceusername,sourcepassword,sourcedatabase_sid,targethostname,targetusername,targetpassword,targetdatabase_sid,each):
                #print sourceusername
		command = "expect scp.exp " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + sourcedatabase_sid.upper() + " " + targethostname + " " + targetusername + " " + targetpassword + " " + targetdatabase_sid.upper() + " " + each
                print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            	out, err = command.communicate()

        threads = []
	threadcount=threading.activeCount()
	#print len(threads)
	#count = 1
        for each in path_array:
                print each
                t = threading.Thread(target=scpfile, args=(sourcehostname, sourceusername, sourcepassword, sourcedatabase_sid.upper(), targethostname, targetusername, targetpassword, targetdatabase_sid.upper(), each.strip()))
		print t
        	t.start()
                threads.append(t)
	#print len(threads)
	#print threading.activeCount()
	#t.join()
	#print threading.enumerate()
	for t in threads:
		#print "a"
		t.join()
	print "finished"
	#while ( threading.activeCount() != threadcount ):
	#	print threading.activeCount()
	#	continue
	#print threading.activeCount()


        #return float(total)

except Exception as e:
    print "F: " + str(e)
