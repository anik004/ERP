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
	profile_path = argv[5]
        user = application_sid.lower() + "adm"
	logfile = "geminyo.txt"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';ls | grep -i "' + application_sid.upper() + '_DVE" | grep -v "\."\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        profilefile = ''.join(output).strip()
	print profilefile
        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile.strip() + ' | grep -iw --color=never "rdisp/wp_no_btc" | grep  --color=never "#"\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
        print output
        if not output:
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';echo "rdisp/wp_no_btc = 5" >> ' + profilefile + '\''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	    output = stdout.readlines()
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            if stdout.channel.recv_exit_status() == 0:
                print "POST:P: Parameter is changed for BDLS"
            else:
                print "POST:F: Parameter change failed for BDLS"

        elif output.__len__() == 1:
            output = ''.join(output).strip()
            output = output.replace('/','\/')
	    val = int(output[-1]) + 5
	    print val
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed "s/' + output + '/rdisp\/wp_no_btc = ' + str(val) + '/g" ' + profilefile + ' >> /tmp/star_value1.txt \''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	    print stdout.channel.recv_exit_status()
            if stdout.channel.recv_exit_status() == 0:
		command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed "s/rdisp\/wp_no_btc = 0/#rdisp\/wp_no_btc = 0/g" /tmp/star_value1.txt >> /tmp/star_value.txt \''
		print command
		#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True) 
		output = stdout.readlines()
		print output
		#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		print stdout.channel.recv_exit_status()
		if stdout.channel.recv_exit_status() == 0:
			command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';pwd \''
			print command
			#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			output = stdout.readlines()
			#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			print output
			output = output[0]
			command = 'sudo cp /tmp/star_value.txt ' + output.strip()+ '/' + profilefile
			print command
			#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			output = stdout.readlines()
			print output
			#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			if stdout.channel.recv_exit_status() == 0:
                		print "POST:P: Parameter is changed for BDLS"
				command = "sudo rm /tmp/star_value1.txt /tmp/star_value.txt"
				#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
				stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
				output = stdout.readlines()
				#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			else:
				print "POST:F: Parameter change failed for BDLS"
		else:
			 print "POST:F: Parameter change failed for BDLS"
            else:
                print "POST:F: Parameter change failed for BDLS"
        else:
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile + ' | grep -iwn "rdisp/wp_no_btc" | grep -v "#" | head -n -1 | cut -d ":" -f 1\''
	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
            numbers=""
            for number in output:
                number = number.strip() + "d"
                numbers = numbers + ";" + number
            numbers=numbers.replace(';','',1)
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed -i "' + numbers + '" ' + profilefile + '\''
	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
            if stdout.channel.recv_exit_status() == 0:
                command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed -i "s/' + output + '/rdisp\/wp_no_btc = 5/g" ' + profilefile + '\''
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                if stdout.channel.recv_exit_status() == 0:
                    print "POST:P: Parameter set to default value"
                else:
                    print "POST:F: Parameter change failed"
        channel.close()
        client.close()
except Exception as e:
    print "F: " + str(e)
