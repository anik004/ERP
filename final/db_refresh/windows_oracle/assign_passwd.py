import os
from sys import *
import subprocess
import log4erp
from log4erp import *
try:
#    if argv[1] == '--u':
#        print 'usage: python assign_passwd.py <Target DB Hostname> <Target DB Sudo User> <Target DB Sudo User passwd> <Target SYSTEM user password> <System user new password> <schema user new password> <Refresh ID>'
#    else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        sys_pass = argv[4]
        new_sys_pass = argv[5]
        new_sch_pass = argv[6]
        refresh_id = argv[7] + '.log'
        app_user = argv[8].lower() + 'adm'
        print app_user
        db_user = 'ora' + argv[9].lower()
        schema = argv[10]
        location = argv[11].strip('\\')

        command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "brconnect -u system/' + sys_pass + ' -c -f chpass -o SYSTEM -p ' + new_sys_pass + '"'
        print command
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        #print out
        if command.returncode == 0:
            print 'ASSIGN:P: The password for the system user has been changed successfully in the target database server (hostname - ' + hostname + ')'
            log4erp.write(refresh_id,'POST:P:The password for the system user has been changed in the target server (Hostname -' + hostname + ')')
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "brconnect -u system/' + sys_pass + ' -c -f chpass -o ' + schema + ' -p ' + new_sys_pass + '"'
            print command
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
        #print out
            if command.returncode == 0:
                print 'ASSIGN:P: The password for the ' + schema[0].strip() + ' user has been changed successfully in the target database server (hostname - ' + hostname + ')'
                log4erp.write(refresh_id,'POST:P:The password for the ' + schema[0].strip() + ' user has been changed in the Target Server (Hostname -' + hostname + ')')
            else:
                print 'ASSIGN:F: The password for the ' + schema[0].strip() + ' user has not been changed successfully in the target database server (hostname - ' + hostname + ')'
                log4erp.write(refresh_id,'POST:F::The password for the ' + schema[0].strip() + ' user has not changed in the Target Server (Hostname -' + hostname + ')')
        else:
            print 'ASSIGN:F: The password for the system user has not been changed successfully in the target database server (hostname - ' + hostname + ')'
            log4erp.write(refresh_id,'POST:F:The password for the system user has not changed in the target server (Hostname -' + hostname + ')')

except Exception as e:
    if str(e) == '[Errno -2] Name or service not known':
        print 'ASSIGN:F:GERR_2401:Hostname unknown'
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2401]')
    elif str(e).strip() == 'list index out of range':
        print 'ASSIGN:F:GERR_2402:Argument/s missing for Control script'
    elif str(e) == 'Authentication failed.':
        print 'ASSIGN:F:GERR_2403:Authentication failed.'
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code -2403]')
    elif str(e) == '[Errno 110] Connection timed out':
        print 'ASSIGN:F:GERR_2404:Host Unreachable'
        write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2404]')
    elif 'getaddrinfo failed' in str(e):
        print 'ASSIGN:F:GERR_2405: Please check the hostname that you have provide'
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2405]')
    elif '[Errno None] Unable to connect to port 22 on' in str(e):
        print 'ASSIGN:F:GERR_2406:Host Unreachable or Unable to connect to port 22'
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2406]')
    else:
        print 'ASSIGN:F: ' + str(e)

