from paramiko import *
import paramiko
from sys import *
import log4erp
from log4erp import *
from time import gmtime, strftime


def remove_files(application_sid):
        command = "sudo rm -rf /tmp/re_assign_value1.txt /tmp/re_assign_value2.txt /tmp/re_assign_value.txt /tmp/assign_value.txt /tmp/assign_value1.txt"
        print command
        #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
        print output
        #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')


def assign_zero(user,profilefile,application_sid):
	command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile + ' | grep -iw --color=never "#rdisp/wp_no_btc = 0" \''
        print command
        #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	print output
        if output:
        	command = "sudo su - " + user + ' -c \'cd ' + profile_path + ';sed "s/#rdisp\/wp_no_btc = 0/rdisp\/wp_no_btc = 0/ " /tmp/assign_value1.txt >> /tmp/assign_value.txt \''
                print command
                #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = stdout.readlines()
                if stdout.channel.recv_exit_status() == 0:
                        print "PRE:P: rdisp/wp_no_btc = 0 has been added to temporary file successfully"
                        #write(logfile,"PRE:P: rdisp/wp_no_btc = 0 has been added to temporary file successfully " + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			file_name = "assign_value.txt"
                else:
                        print "PRE:F: Failed to add rdisp/wp_no_btc = 0 in the temporary file"
                        #write(logfile,"PRE:F: Failed to add rdisp/wp_no_btc = 0 in the temporary file " + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			remove_files(application_sid)
			exit()
	else:
        	command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';echo "rdisp/wp_no_btc = 0" >> /tmp/assign_value1.txt \''
            	print command
            	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            	output = stdout.readlines()
            	print output
            	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            	if stdout.channel.recv_exit_status() == 0:
			print "PRE:P: rdisp/wp_no_btc = 0 has been added to temporary file successfully"
                        #write(logfile,"PRE:P: rdisp/wp_no_btc = 0 has been added to temporary file successfully " + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			file_name = "assign_value1.txt"
		else:
			print "PRE:F: Failed to add rdisp/wp_no_btc = 0 in the temporary file"
                        #write(logfile,"PRE:F: Failed to add rdisp/wp_no_btc = 0 in the temporary file " + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			remove_files(application_sid)
                        exit()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';pwd \''
        print command
        #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
        print output
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        output = output[0]

	command = "sudo su - " + user + ' -c \'cd ' + profile_path + ';cp /tmp/'+ file_name + ' ' + output.strip() + '/' + profilefile + ' \''
	print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	print output
        #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        if stdout.channel.recv_exit_status() == 0:
              	print "PRE:P: Parameter set to 0"
	        #write(logfile, "PRE:P: Parameter set to 0" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		remove_files(application_sid)
        else:
        	print "PRE:F: Parameter change failed"
                #write(logfile, "PRE:F: Parameter change failed" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		remove_files(application_sid)
	        exit()


try:
    if argv[1] == "--u":
        print "usage: python ddic_setzero.py <Application Hostname> <Root User Name> <Root user password> <Application SID> <Target/Source>"
    else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
	logfile = "geminyo.log"
        application_sid = argv[4].lower()
	profile_path = argv[5]

        user = application_sid.lower() + "adm"
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()
        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';ls | grep -i "' + application_sid.upper() + '_DVEBMGS" | grep -v "\."\''
        print command
	##write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        profilefile = ''.join(stdout.readlines()).strip()
	print profilefile
	#write(logfile, str(profilefile) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

	command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';ls ' + profilefile + '\''
	print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	file_exist = stdout.readlines()
	print file_exist[0]
	#write(logfile, str(file_exist) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

	if file_exist[0].strip() == profilefile:
		command = "sudo su - " + user + " -c \'cd ' + profile_path + ';cp " + profilefile + " " + "profilefile_autom_bkp \'"
		print command
		#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		a = stdout.readlines()
		#write(logfile, str(a) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		if not a:
			print "PRE:P: Backup file of Instance profile " + profilefile + " has been created successfully"
			#write(logfile,"PRE:P: Backup file of Instance profile " + profilefile + " has been created successfully")
		else:
			print "PRE:F: Failed to take the backup of the instance profile " + profilefile
			#write(logfile,"PRE:F: Failed to take the backup of the instance profile " + profilefile + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			exit()
			
	else:
		print "PRE:F: Couldn't find the instance profile " + profilefile
		#write(logfile,"PRE:F: Couldn't find the instance profile " + profilefile)
		exit()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile + ' | grep -iw "rdisp/wp_no_btc" | grep -v "#"\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	print output
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

        if not output:
	    assign_zero(user,profilefile,application_sid)

        elif output.__len__() == 1:
            output = ''.join(output).strip()
            output = output.replace('/','\/')

	    command = "sudo su - " + user + ' -c \'cd ' + profile_path + ';sed "s/' + output + '/# ' + output + '/g" ' + profilefile + ' >> /tmp/assign_value1.txt \''
	    print command
            #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    print output
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	    if stdout.channel.recv_exit_status() == 0:
                print "PRE:P: Commented the original value"
		#write(logfile, "PRE:P: Commented the original value" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "PRE:F: Failed to comment the original value"
		#write(logfile, "PRE:F: Failed to comment the original value" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		remove_files(application_sid)
		exit()

	    assign_zero(user,profilefile,application_sid)

        else:
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile + '.bkp | grep -iwn "rdisp/wp_no_btc" | grep -v "#" | head -n -1 | cut -d ":" -f 1\''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    print output
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            numbers=""

            for number in output:
                number = number.strip() + "d"
                numbers = numbers + ";" + number

            numbers=numbers.replace(';','',1)
	    print numbers
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed -i "' + numbers + '" ' + profilefile + '\''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    print output
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

            if stdout.channel.recv_exit_status() == 0:
                command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed -i "s/' + output + '/rdisp\/wp_no_btc = 0/g" ' + profilefile + '\''
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                if stdout.channel.recv_exit_status() == 0:
                    print "PRE:P: Parameter set to 0"
                else:
                    print "PRE:P: Parameter change failed"
        channel.close()
        client.close()
except Exception as e:
    print "F: " + str(e)
