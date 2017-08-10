import paramiko
from paramiko import *
from sys import *
import log4erp
from log4erp import *


# target IP - argv[1]
# Login User Name - argv[2]
# Login User Password - argv[3]
# Database SID - argv[4]

try:
    if argv[1] == "--u":
        print "python r3trans.py <Target Application Host> <Target Application Sudo User Name> <Target Application Sudo User Password> <Target Application SID> <Refresh ID>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]

        user = argv[4].lower() + "adm"
        refresh_id = argv[5] + ".log"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user  + ' -c "R3trans -d | tail -n 1" | awk \'{print $NF}\''
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        out = stdout.readlines()
#	print out[0]
	if "does not exist" in out[0].strip():
	    print "R3TRANS:F: The Target App SID - " + db_sid + " passed by the user is incorrect."
	    write(refresh_id,"POST:F: The Target App SID - " + db_sid + " passed by the user is incorrect.")
        elif out[0].strip() == "(0000).":
            print "R3TRANS:P: The Database Refresh process has been completed successfully"
            log = "POST:P: The Database Refresh process has been completed successfully"
            write(refresh_id,log)
        else:
            print "R3TRANS:F: The database Refresh process has been failed"
            log = "POST:P: The Database Refresh process has been failed"
            write(refresh_id,log)

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "R3TRANS:F:GERR_2901:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2901]')
    elif str(e).strip() == "list index out of range":
        print "R3TRANS:F:GERR_2902:Argument/s missing for r3trans script"
    elif str(e) == "Authentication failed.":
        print "R3TRANS:F:GERR_2903:Authentication failed."
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 2903]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "R3TRANS:F:GERR_2904:Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2904]')
    elif "getaddrinfo failed" in str(e):
        print "R3TRANS:F:GERR_2905: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2905]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "R3TRANS:F:GERR_2906:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2906]')
    else:
        print "R3TRANS:F: " + str(e)

