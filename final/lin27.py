import paramiko
from log4erp import *
from paramiko import *
import os.path
from sys import *
import subprocess

try:
    if argv[1] == "--u":
        print "python transport.py <path in Source> <Transport id> <Path in target> <target IP> <target Application SID> <Domain name> <Target Sudo Login User Name> <Target Sudo User Password> <Source Application SID>"

    else:
        s_path = argv[1]

        tr_id = argv[2]
        t_path = argv[3]

        t_hostname = argv[4]
        t_sid = argv[5].lower()
        domain = argv[6].upper()
        t_username = argv[7]
        t_password = argv[8]

        tr_part = tr_id[4:]
        sid = t_sid.upper()
        s_sid = argv[9].upper()
	logfile = argv[10]
	client = argv[11]
	t_user = t_sid.lower() + "adm"

        count1 = len(t_sid)
        count2 = len(s_sid)
	
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(t_hostname,username = t_username, password = t_password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + t_user + ' -c \'cdpro;ls | grep -i "' + t_sid.upper() + '_DVE" | grep -v "\."\''

        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	profilefile = stdout.readlines()[0].strip()
	print profilefile
	command = 'sudo su - ' + t_user + ' -c \'cdpro;cat ' + profilefile + ' | grep -iw "DIR_TRANS" | grep -v "#"\''
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        t_path = stdout.readlines()[0].strip()
	t_path = t_path.split('=')[1].strip()
	print t_path
	if count1 > 3 or count1 < 3 or count2 > 3 or count2 < 3:
            print "Wrong syntax of Target/Source SID"
        else:
            for name in "cofiles", "data":
                if name == "cofiles":
                    initial = "K"
                else:
                    initial = "R"

		"""
                command = 'ls ' + s_path + '/' + name + ' | grep -i "' + initial + tr_part + '"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                filename = out

        #    command = 'scp ' + s_path + "/" + name + "/" + initial + tr_part + "." + s_sid + " " + t_username.lower() + '@' + t_hostname + ':' + t_path + "/" + name
                port = 22
                transport1 = paramiko.Transport((t_hostname, port))
                transport1.connect(username = t_username, password = t_password)
                sftp1 = paramiko.SFTPClient.from_transport(transport1)
                localpath = s_path + "/" + name + "/" + initial + tr_part + "." + s_sid
                #print localpath
                filepath =  t_path + "/" + name + "/" + initial + tr_part + "." + s_sid
                #print filepath
            	sftp1.put(localpath, filepath)

                print "POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully."
		write(logfile,"POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully.")
                command = 'sudo chown ' + t_sid.lower() + 'adm:sapsys ' + t_path + '/' + name + '/' + initial + tr_part + '.' + s_sid + '; sudo chmod 777 ' + t_path + '/' + name + '/' + initial + tr_part + '.' + s_sid
# target IP - $1

# database sid - $2
# application sid - $3
# schema passwd - $4
            	if stdout.channel.recv_exit_status() != 0:
                   print "POST:F: The permission changing is not possible because of network issue"
		   write(logfile,"POST:F: The permission changing is not possible because of network issue")
               # else:
               #    print "tansport.py:I: The permission is changed successfully"
		"""

        command = 'sudo su - ' + t_sid.lower() + "adm" + ' -c "tp addtobuffer ' + tr_id + " " + t_sid  + ' Client=' + client + ' pf=' + t_path + '/bin/TP_' + domain + '.PFL "| grep -i \'tp finished with return code:\' | tail -n 1 | cut -d ":" -f2'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.readline().rstrip().strip()

        if status == "0" or status == "4":
            command = 'sudo su - ' + t_sid.lower() + 'adm -c "tp modbuffer ' + tr_id + " " + t_sid + ' mode=u+12 Client=' + client + ' pf=' + t_path + '/bin/TP_' + domain + '.PFL" |grep -i \'tp finished with return code:\' | tail -n 1 |cut -d ":" -f2'
            print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.readline().rstrip().strip()

            if status == "0" or status == "4":
                command = 'sudo su - ' + t_sid.lower() + 'adm -c "tp import ' + tr_id + " " +  t_sid + ' Client=' + client + ' pf=' + t_path + '/bin/TP_' + domain + '.PFL U123689"|grep -i \'tp finished with return code:\' |tail -n 1 | cut -d ":" -f2'
                print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                status = stdout.readline().rstrip().strip()

                if status == "0" or status == "4":
                    print "POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname
		    write(logfile,"POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname)
                else:
                    print "POST:F: TR " + tr_id + " import is failed with the error code: " + status
		    write(logfile,"POST:F: TR " + tr_id + " import is failed with the error code: " + status)
            else:
                print "POST:F: The modbuffer for the TR " + tr_id + " has failed"
		write(logfile,"POST:F: The modbuffer for the TR " + tr_id + " has failed")
        else:
            print "POST:F: TR " + tr_id + " is failed with the error code: " + status
	    write(logfile,"POST:F: TR " + tr_id + " is failed with the error code: " + status)

            channel.close()
            client.close()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "POST:F:GERR_0301:Hostname unknown"
	write(logfile,"POST:F:GERR_0301:Hostname unknown")
    elif str(e) == "list index out of range":
        print "POST:F:GERR_0302:Argument/s missing for authorisation script"
    elif str(e) == "Authentication failed.":
        print "POST:F:GERR_0303:Authentication failed."
	write(logfile,"POST:F:GERR_0303:Authentication failed.")
    elif str(e) == "[Errno 110] Connection timed out":
        print "POST:F:GERR_0304:Host Unreachable"
	write(logfile,"POST:F:GERR_0304:Host Unreachable")
    else:
        print "POST:F: " + str(e)
	write(logfile,"POST:F: " + str(e))

