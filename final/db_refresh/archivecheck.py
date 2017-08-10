from paramiko import *
import paramiko
from sys import *


try:
    if argv[1] == "--u":
        print "usage: python archivecheck.py <DB Hostname> <Sudo User Name> <Sudo user password> <DB SID> <Target/Source>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        database_sid = argv[4]
        user = "ora" + database_sid.lower()

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()
        command = 'sudo su - ' + user + ' -c "echo \'select log_mode from "v\$database";\' | sqlplus / as sysdba" | tail -n 3 | head -n 1'
#        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output=''.join(stdout.readlines()).strip()
#	print output
        if stdout.channel.recv_exit_status() == 0:
            if output=="ARCHIVELOG":
                print "ARCHIVECHECK:W:Archive is enabled in the target database server ( Hostname - " + hostname + " )"
            else:
                print "ARCHIVECHECK:P:Archive is disabled in target database server ( Hostname - " + hostname + " )"
        channel.close()
        client.close()
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "ARCHIVECHECK:F:GERR_0901:Hostname unknown"
    elif str(e) == "list index out of range":
        print "ARCHIVECHECK:F:GERR_0902:Argument/s missing for the script"
    elif str(e) == "Authentication failed.":
        print "ARCHIVECHECK:F:GERR_0903:Authentication failed."
    elif str(e) == "[Errno 110] Connection timed out":
        print "ARCHIVECHECK:F:GERR_0904:Host Unreachable"
    elif "getaddrinfo failed" in str(e):
        print "MOUNTPOINT:F:GERR_0905: Please check the hostname that you have provide"
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "MOUNTPOINT:F:GERR_0906:Host Unreachable or Unable to connect to port 22"
    elif "invalid decimal" in str(e):
        print "MOUNTPOINT:F:GERR_0907:Unknown Error:" + str(e)
    else:
        print "ARCHIVECHECK:F: " + str(e)
