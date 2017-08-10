import os
from sys import *
import subprocess
import log4erp
from log4erp import *

# target Host - argv[1]
# Login User Name - argv[2]
# Login User Password - argv[3]
# database SID - argv[4]

try:
#    if argv[1] == "--u":
#        print "usage: python ctrlrun.py <Target Host> <Sudo User Name> <Sudo User Password> <database SID> <Refresh ID>"
#    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]
        refresh_id = argv[5] + ".log"
        t_location = argv[6]
        location = argv[7]

        user = "ora" + db_sid.lower()

        print "CTRLRUN:I: Running Control file to database on target server ( Hostname - " + hostname + " )"
        log4erp.write(refresh_id,"POST:I: Running Control file to database on target server ( Hostname - " + hostname + " )")
        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'@' + t_location + '\control_script_' + db_sid.upper() + '.sql\' | sqlplus / as sysdba"'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        if stdout.channel.recv_exit_status() == 0:
                print "CTRLRUN:P: The control file has been run successfully on the target server (HOSTNAME - " + hostname + ")"
                log4erp.write(refresh_id,"POST:P: The control file has been run successfully on the target server ( Hostname - " + hostname + " )")
        else:
                print "CTRLRUN:F: The control file has not been run successfully on the target server (HOSTNAME - " + hostname + ")"
                log4erp.write(refresh_id,"POST:F: The control file has not been run successfully on the target server ( Hostname - " + hostname + " )")

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "CTRLRUN:F:GERR_1801:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 1801]')
    elif str(e).strip() == "list index out of range":
        print "CTRLRUN:F:GERR_1802:Argument/s missing for ctrlrun script"
    elif str(e) == "Authentication failed.":
        print "CTRLRUN:F:GERR_1803:Authentication failed."
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 1803]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "CTRLRUN:F:GERR_1804::Host Unreachable"
	log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 1804]')
    elif "getaddrinfo failed" in str(e):
        print "CTRLRUN:F:GERR_1805: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 1805]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "CTRLRUN:F:GERR_1806:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1806]')
    else:
        print "CTRLRUN:F: " + str(e)
