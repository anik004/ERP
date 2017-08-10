import os
from sys import *
import subprocess
import log4erp
from log4erp import *

try:
#    if argv[1] == "--u":
#        print "usage: python globalname.py <Target Database IP> <Target Database sid> <Target Database Sudo Username> <Target Database Sudo Password> <Refresh ID>"
#    else:
        hostname = argv[1]
        username = argv[3]
        password = argv[4]
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( argv[1],username = argv[3], password = argv[4])
        channel = client.invoke_shell()

        user="ora" + argv[2].lower()
        logfile = argv[5] + ".log"
        location = argv[6]

        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'alter database rename global_name to ' + argv[2] + ';\' | sqlplus / as sysdba"'
        print command
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        if command.returncode == 0:
            print "GLOBALNAME:P: The global name change has been successful on the target database server (HOSTNAME - " + argv[1] + ")"
            log = "POST:P: the global name has been changed on the target database server (HOSTNAME - " + argv[1] + ")"
            write(logfile, log)
        else:
            print "GLOBALNAME:F: the global name has not  been changed on the target database server (HOSTNAME - " + argv[1] + ")"
            log = "POST:F: the global name has not been changed on the target database server (HOSTNAME - " + argv[1] + ")"
            write(logfile, log)

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "GLOBALNAME:F:GERR_2701:Hostname unknown"
        log4erp.write(logfile,'POST:F: Hostname unknown [Error Code - 2701]')
    elif str(e).strip() == "list index out of range":
        print "GLOBALNAME:F:GERR_2702:Argument/s missing for GLOBALNAME script"
    elif str(e) == "Authentication failed.":
        print "GLOBALNAME:F:GERR_2703:Authentication failed."
        log4erp.write(logfile,'POST:F:Authentication failed[Error Code - 2703]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "GLOBALNAME:F:GERR_2704:Host Unreachable"
	write(logfile,'POST:F:Host Unreachable.[Error Code - 2704]')
    elif "getaddrinfo failed" in str(e):
        print "GLOBALNAME:F:GERR_2705: Please check the hostname that you have provide"
        log4erp.write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 2705]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "GLOBALNAME:F:GERR_2706:Host Unreachable or Unable to connect to port 22"
        write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2706]')
    else:
        print "GLOBALNAME:F: " + str(e)
