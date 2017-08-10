import os
from sys import *
import subprocess
import log4erp
from log4erp import *

try:
#    if argv[1] == "--u":
#        print "Usage: python sapstart.py <Target database host> <Target database root> <Target database root passwd> <Target Database SID> <Refresh ID>"
#    else:
     if len(argv) < 5:
        print "F:DBSTOP: Argument/s missing for the script [Error Code - 1302]"
     else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]

        logfile= argv[5] + ".log"

        user_db = "ora" + db_sid.lower()

        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'shutdown immediate\' | sqlplus / as sysdba"'
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        if command.returncode == 0:
            print 'DBSTOP:P: The Database has been stopped on the target server (HOSTNAME - ' + hostname + ')'
            log = 'PRE:P: The Database has been stopped on the target server (HOSTNAME - ' + hostname + ')'
            write (logfile, log)
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "lsnrctl stop"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print 'DBSTOP:P: The listener has been stopped on the target server (HOSTNAME - ' + hostname +')'
                log = 'PRE:P: The listener has been stopped on the target server (HOSTNAME - ' + hostname +')'
                write(logfile, log)
            else:
                print 'DBSTOP:F: The Database is not successfully stopped successfully on the target server (HOSTNAME - ' + hostname + ')'
                log = 'PRE:F: The Database is not successfully stopped successfully on the target server (HOSTNAME - ' + hostname + ')'
                write (logfile, log)
except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "DBSTOP:F:GERR_1301:Hostname unknown"
                write(logfile,'PRE:F: Hostname unknown [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "DBSTOP:F:GERR_1302:Argument/s missing for the script"
                write(logfile,'PRE:F: Argument/s missing for the script [Error Code - 1302]')
     elif str(e) == "Authentication failed.":
                print "DBSTOP:F:GERR_1303:Authentication failed."
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "DBSTOP:F:GERR_1304:Host Unreachable"
                write(logfile,'PRE:F:Host Unreachable.[Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "DBSTOP:F:GERR_1305: Please check the hostname that you have provide"
                write(logfile,'PRE:F: Please check the hostname that you have provide [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "DBSTOP:F:GERR_1306:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "DBSTOP:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'PRE:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "DBSTOP:F: " + str(e)
