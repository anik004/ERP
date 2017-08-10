import os
from sys import *
import subprocess
import log4erp
from log4erp import *

# target Host - argv[1]
# Database SID - argv[2]

try:
    #if argv[1] == "--u":
     #       print "python changeid.py <target database Host> <Target Login User Name> <Target Login User Name Password> <Target database sid> <Target Refresh ID>"
#    else:
            hostname = argv[1]
            username = argv[2]
            password = argv[3]
            db_sid = argv[4]

            user = "ora" + argv[4].lower()
            refresh_id = argv[5] + '.log'
            location = argv[6]

#            print "CHANGEID:I: Establishing Connection on target server ( Hostname - " + hostname + " )"

            print "CHANGEID:I: Shutting down database on target server ( Hostname - " + hostname + " )"
            log4erp.write(refresh_id,"POST:I: Shutting down database on target server ( Hostname - " + hostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'shutdown immediate\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print "CHANGEID:P: Database Shutdown completed successfully on target server ( Hostname - " + hostname + " )"
                log4erp.write(refresh_id,"POST:P: Database Shutdown completed successfully on target server ( Hostname - " + hostname + " )")

            print "CHANGEID:I: Mounting database on target server ( Hostname - " + hostname + " )"
            log4erp.write(refresh_id,"POST:I: Mounting database on target server ( Hostname - " + hostname + " )")
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'startup mount\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print "CHANGEID:P: Mounting database completed successfully on target server ( Hostname - " + hostname + " )"
                log4erp.write(refresh_id,"POST:P: Mounting database completed successfully on target server ( Hostname - " + hostname + " )")

            print "CHANGEID:I: Setting new ID for database on target server ( Hostname - " + hostname + " )"
            log4erp.write(refresh_id,"POST:I: Setting new ID for database on target server ( Hostname - " + hostname + " )")
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "yes | nid TARGET=/"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print "CHANGEID:P: Setting new database ID completed successfully on target server ( Hostname - " + hostname + " )"
                log4erp.write(refresh_id,"POST:P: Setting new database ID completed successfully on target server ( Hostname - " + hostname + " )")

            print "CHANGEID:I: Shutting down database on target server ( Hostname - " + hostname + " )"
            log4erp.write(refresh_id,"POST:I: Shutting down database on target server ( Hostname - " + hostname + " )")
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'shutdown immediate\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print "CHANGEID:P: Database Shutdown completed successfully on target server ( Hostname - " + hostname + " )"
                log4erp.write(refresh_id,"POST:P: Database Shutdown completed successfully on target server ( Hostname - " + hostname + " )")

            print "CHANGEID:I: Mounting database on target server ( Hostname - " + hostname + " )"
            log4erp.write(refresh_id,"POST:I: Mounting database on target server ( Hostname - " + hostname + " )")
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'startup mount\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print "CHANGEID:P: Mounting database completed successfully on target server ( Hostname - " + hostname + " )"
                log4erp.write(refresh_id,"POST:P: Mounting database completed successfully on target server ( Hostname - " + hostname + " )")

            print "CHANGEID:I: Altering resetlogs in database on target server ( Hostname - " + hostname + " )"
            log4erp.write(refresh_id,"POST:I: Altering resetlogs in database on target server ( Hostname - " + hostname + " )")
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'ALTER DATABASE OPEN RESETLOGS;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            if command.returncode == 0:
                print "CHANGEID: P: The reset database has been altered on the target server (HOSTNAME - " + argv[1] + ")"
                log4erp.write(refresh_id,"POST: P: The reset database has been altered on the target server (HOSTNAME - " + argv[1] + ")")

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "CHANGEID:F:GERR_2601:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2601]')
    elif str(e).strip() == "list index out of range":
        print "CHANGEID:F:GERR_2602:Argument/s missing for ChangeId script"
    elif str(e) == "Authentication failed.":
        print "CHANGEID:F:GERR_2603:Authentication failed."
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 2603]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "CHANGEID:F:GERR_2604:Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2604]')
    elif "getaddrinfo failed" in str(e):
        print "CHANGEID:F:GERR_2605: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2605]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "CHANGEID:F:GERR_2606:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2606]')
    else:
        print "CHANGEOI:F: " + str(e)

