 #!/usr/bin/sh

# target IP - $1
# target database sid - $2
import os
from sys import *
import subprocess
import log4erp
from log4erp import *

try:
#    if argv[1] == "--u":
#        print "usage: sh startlsnr.sh <Target Database IP> <Target database sid> <Target Sudo User> <Target Sudo User Password> <Refresh ID>"
#    else:
        hostname = argv[1]
        username = argv[3]
        password = argv[4]
        user="ora" + argv[2].lower()
        refresh_id = argv[5] + ".log"
        location = argv[6]

        print "STARTLSNR:I: Starting Listner on target server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on target server ( Hostname - " + argv[1] + " )")
		
        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "lsnrctl start"'
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        out = ''.join(out)
        if "already been started" in out:
                print "STARTLSNR:P: Listner service was already running on the target server ( HOSTNAME - " + argv[1] + " )"
                log4erp.write(refresh_id,"POST:I: Listner service was already running on the target server ( HOSTNAME - " + argv[1] + " )")
        elif "The command completed successfully" in out:
                print "STARTLSNR:P: Listner has been started on the target server ( HOSTNAME - " + argv[1] + " )"
                log4erp.write(refresh_id,"POST:I: Listner has been started on the target server ( HOSTNAME - " + argv[1] + " )")
        else:
                print "STARTLSNR:F: The listener has not been started on the target server HOSTNAME - " + argv[1] + " )"
                log4erp.write(refresh_id,"POST: F: The listener has not been started on the target server HOSTNAME - " + argv[1] + " )")

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
