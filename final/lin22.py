from paramiko import *
from time import gmtime, strftime
import paramiko
from sys import *
import log4erp
from log4erp import *


try:
    if argv[1] == "--u":
        print "usage: python ddic_setone.py <Application Hostname> <Root User Name> <Root user password> <Application SID> <Target/Source>"
    else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        application_sid = argv[4]
        user = application_sid.lower() + "adm"
	profile_path = argv[5].rstrip('/')
	print profile_path
	logfile = "geminyo.txt"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path +';ls | grep -i "' + application_sid.upper() + '_DVE" | grep -v "\."\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	print output
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        profilefile = ''.join(output).strip()
	print profilefile
        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile.strip() + ' | grep -iw --color=never "rdisp/wp_no_btc" | grep  --color=never -v "#"\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
        print output
        if output.__len__() == 1:
            output = ''.join(output).strip()
            output = output.replace('/','\/')
	    val = int(output[-1]) - 5
	    print val
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed "s/' + output + '/rdisp\/wp_no_btc = ' + str(val) + '/g" ' + profilefile + ' >> /tmp/star_value1.txt \''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	    print stdout.channel.recv_exit_status()
            if stdout.channel.recv_exit_status() == 0:
			command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ' ;pwd \''
			print command
			#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			output = stdout.readlines()
			#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			print output
			output = output[0]
			command = 'sudo mv /tmp/star_value1.txt ' + output.strip()+ '/' + profilefile
			print command
			#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			output = stdout.readlines()
			print output
			#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			if stdout.channel.recv_exit_status() == 0:
                		print "POST:P: Parameter is set to original value"
				command = "sudo rm /tmp/value1.txt"
				#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
				stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
				output = stdout.readlines()
				#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			else:
				print "POST:F: Failed to set parameter to original value"
				#write(logfile, "POST:F: Failed to set parameter to original value" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "POST:F: Failed to set parameter to original value"
		#write(logfile, "POST:F: Failed to set parameter to original value" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

        channel.close()
        client.close()
except Exception as e:
    print "F: " + str(e)
