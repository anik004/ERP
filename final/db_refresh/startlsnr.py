 #!/usr/bin/sh

# target IP - $1
# target database sid - $2
import paramiko
from sys import *
from paramiko import *
import log4erp

try:
#    if argv[1] == "--u":
#        print "usage: sh startlsnr.sh <Target Database IP> <Target database sid> <Target Sudo User> <Target Sudo User Password> <Refresh ID>"
#    else:
        user="ora" + argv[2].lower()
        refresh_id = argv[5] + ".log"

        print "STARTLSNR:I: Establishing Connection on target server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on target server ( Hostname - " + argv[1] + " )")
		
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( argv[1],username = argv[3], password = argv[4])
        channel = client.invoke_shell()
		
        print "STARTLSNR:I: Connection established successfully on target server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Connection established successfully on target server ( Hostname - " + argv[1] + " )")

        print "STARTLSNR:I: Starting Listner on target server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on target server ( Hostname - " + argv[1] + " )")
		
        command="sudo su - " + user + " -c \'lsnrctl start\'"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        #print stdout.readlines()
        #print stdout.channel.recv_exit_status()
        if stdout.channel.recv_exit_status() == 0:
            print "STARTLSNR:P: The listener has been started on the target server ( HOSTNAME - " + argv[1] + " )"
            log4erp.write(refresh_id,"POST:P: The listener has been started on the target server ( HOSTNAME - " + argv[1] + " )")
        else:
            command="sudo su - " + user + " -c \'lsnrctl start\' | grep -i \'already been started\'"
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status=stdout.readlines()
            #print status
            if "already been started" in status[0]:
                print "STARTLSNR:P: Listner service was already running on the target server ( HOSTNAME - " + argv[1] + " )"
                log4erp.write(refresh_id,"POST:I: Listner service was already running on the target server ( HOSTNAME - " + argv[1] + " )")
            else:
                lsnr_status="sudo su - " + user + " -c \'lsnrctl start LISTENER | grep -i \"Linux error: 111\" | cut -d\":\" -f3\'"
                stdin, stdout, stderr = client.exec_command(lsnr_status, timeout=1000, get_pty=True)
                lsnr_status=stdout.readlines()
            #print lsnr_status
                if not lsnr_status:
                    print "STARTLSNR:F: There is an issue.. Kindly start the listener manually on the target server ( HOSTNAME - " + argv[1] + " )"
                    log4erp.write(refresh_id,"POST: F: There is an issue.. Kindly start the listener manually on the target server ( HOSTNAME - " + argv[1] + " )")
                else:
                    print "STARTLSNR:F: The listener has not been started on the target server HOSTNAME - " + argv[1] + " )"
                    log4erp.write(refresh_id,"POST: F: The listener has not been started on the target server HOSTNAME - " + argv[1] + " )")

        print "STARTLSNR:I: Closing connection on target server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Closing connection on target server ( Hostname - " + argv[1] + " )")
		
        channel.close()
        client.close()
		
        print "STARTLSNR:P: Connection closed successfully on target server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Connection closed successfully on target server ( Hostname - " + argv[1] + " )")

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "STARTLSNR:F:GERR_2001:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2001]')
    elif str(e).strip() == "list index out of range":
        print "STARTLSNR:F:GERR_2002:Argument/s missing for STARTLSNR script"
    elif str(e) == "Authentication failed.":
        print "STARTLSNR:F:GERR_2003:Authentication failed."
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 2003]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "STARTLSNR:F:GERR_2004:Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2004]')
    elif "getaddrinfo failed" in str(e):
        print "STARTLSNR:F:GERR_2005: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2005]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "STARTLSNR:F:GERR_2006:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2006]')
    else:
        print "STARTLSNR:F: " + str(e)
