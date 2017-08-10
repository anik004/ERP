import paramiko
import log4erp
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
        print "Usage: python lsnr_start.py <Source database host> <Source sudo user> <Source sudo user passwd> <Source Database SID> <Refresh ID>"
    else:
        host = argv[1]
        sudo_user = argv[2]
        passwd = argv[3]
        db_user = "ora" + argv[4]
        logfile = argv[5] + ".log"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,username = sudo_user, password = passwd)
        channel = client.invoke_shell()


################################### STARTING LISTENER ########################################################

        command = 'sudo su - ' + db_user + ' -c "lsnrctl start LISTENER"'
#        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#       print status
        if status != 0 and status != 1:
            print "LSNR_START:F: The listener has not been started on the target Server (HOSTNAME - " + host + ")"
            log4erp.write(POST,":F: The listener has not been started on the target Server (HOSTNAME - " + host + ")")
            exit()
        else:
            print 'LSNR_START:P: The listener has been started on the target Server (HOSTNAME - ' + host + ')'
            log4erp.write(POST,":P: The listener has been started on the target Server (HOSTNAME - " + host + ')')
	channel.close()
	client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "LSNR_START:F:GERR_1301:Hostname unknown - " + host
                write(logfile,'POST:F: Hostname unknown - ' + host + ' [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "LSNR_START:F:GERR_1302:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "LSNR_START:F:GERR_1303:Authentication failed to the Source server - " + host
                write(logfile,'POST:F:Authentication failed to the Source server - ' + host + ' [Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "LSNR_START:F:GERR_1304:Source Host Unreachable - " + host
                write(logfile,'POST:F:Source Host Unreachable - ' + host + ' [Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "LSNR_START:F:GERR_1305: Please check the hostname that you have provide"
                write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "LSNR_START:F:GERR_1306:Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "LSNR_START:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'Post:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "LSNR_START:F: " + str(e)
                write(logfile,'Post:F: ' + str(e))


