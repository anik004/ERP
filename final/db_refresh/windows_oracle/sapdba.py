import os
from sys import *
import subprocess
import log4erp
from log4erp import *

# target IP - argv[1]
# Login User Name - argv[2]
# Login User Password - argv[3]
# Database SID - argv[4]

try:
#    if argv[1] == "--u":
#        print "python sapdba.py <Target database Host> <Target database Sudo User Name> <Target Database Sudo User Password> <Target Database SID> <Refresh ID"
#    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]
        refresh_id = argv[5] + ".log"
        schema = argv[6]
        ker_location = argv[7]
        location = argv[8]
        user = "ora" + argv[4].lower()

        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "cd ' + ker_location + '; sqlplus /nolog @sapdba_role.sql ' + schema + '"'
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        if command.returncode == 0:
                print "SAPDBA:P: The SAPDBA role updation has been successful on the target server (HOSTNAME - " + hostname + ")"
                log4erp.write(refresh_id,'POST:P: The SAPDBA role updation has been successful on the target server (HOSTNAME - ' + hostname + ')')
        else:
                print "SAPDBA:F:The SAPDBA role updation has been failed on the target server (HOSTNAME - " + hostname + ")"
                log4erp.write(refresh_id,'POST:F: The SAPDBA role updation has been failed on the target server (HOSTNAME -' + hostname + ')')

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "SAPDBA:F:GERR_2801:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2801]')
    elif str(e).strip() == "list index out of range":
        print "SAPDBA:F:GERR_2802:Argument/s missing for SAPDBA script"
    elif str(e) == "Authentication failed.":
        print "SAPDBA:F:GERR_2803:Authentication failed."
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 2803]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "SAPDBA:F:GERR_2804:Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2804]')
    elif "getaddrinfo failed" in str(e):
        print "SAPDBA:F:GERR_2805: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2805]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "SAPDBA:F:GERR_2806:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2806]')
    else:
        print "SAPDBA:F: " + str(e)
