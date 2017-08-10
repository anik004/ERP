from paramiko import *
import paramiko
from sys import *
import log4erp
from log4erp import *
from time import gmtime, strftime


try:
    if argv[1] == "--u":
        print "usage: python ddic_setone.py <Application Hostname> <Root User Name> <Root user password> <Application SID> <Target/Source>"
    else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        application_sid = argv[4]
	logfile = "geminyo.txt"
	profile_path = argv[5]
        user = application_sid.lower() + "adm"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path  + ' ;ls | grep -i "' + application_sid.upper() + '_DVE" | grep -v "\."\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        profilefile = ''.join(output).strip()
	
        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile + ' | grep -iw "login/no_automatic_user_sapstar" | grep -v "#"\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	print output
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        if not output:
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';echo "login/no_automatic_user_sapstar = 1" >> ' + profilefile + '\''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	    output = stdout.readlines()
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            if stdout.channel.recv_exit_status() == 0:
                print "POST:P: SAP* Parameter set to one"
		#write(logfile, "POST:P: SAP* Parameter set to one" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "POST:F: Failed to set SAP* Parameter to one"
		#write(logfile, "POST:F: Failed to set SAP* Parameter to one" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

        elif output.__len__() == 1:
            output = ''.join(output).strip()
            output = output.replace('/','\/')
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed "s/' + output + '/login\/no_automatic_user_sapstar = 1/g" ' + profilefile + ' >> /tmp/star_one.txt \''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    print output
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            if stdout.channel.recv_exit_status() == 0:
		command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';pwd \''
		print command
                #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = stdout.readlines()
                #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
                output = output[0]
                command = 'sudo mv /tmp/star_one.txt ' + output.strip()+ '/' + profilefile
                print command
                #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = stdout.readlines()
                #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		if stdout.channel.recv_exit_status() == 0:
	                print "POST:P: SAP* Parameter set to one"
			#write(logfile, "POST:P: SAP* Parameter set to one" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		else:
			print "POST:F: Failed to set SAP* Parameter to one"
			#write(logfile, "POST:F: Failed to set SAP* Parameter to one" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "POST:F: Failed to set SAP* Parameter to one"
		#write(logfile, "POST:F: Failed to set SAP* Parameter to one" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        else:
            print "POST:F: SAP* Parameter change failed"
	    #write(logfile, "POST:F: Failed to set SAP* Parameter to one" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

        channel.close()
        client.close()
except Exception as e:
    print "F: " + str(e)
