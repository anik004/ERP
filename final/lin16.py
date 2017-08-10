import paramiko
from paramiko import *
from sys import *
from log4erp import *
import re

try:
    if argv[1] == "--ani":
	print "Usage: python sapstopapp.py <Target application Host> <Target application Login User Name> <Target application User Password> <Target Application SID> <Instance ID> <Instance Host> <ref_id>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        app_sid = argv[4]

        instance = argv[5]
        logfile= argv[7] + ".log"
        host = argv[6]
	db_sid = argv[8]
	profile_path = argv[9].rstrip('/')
	dbuser = 'ora' + db_sid.lower()

        user_sap = app_sid.lower() + "adm"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user_sap + ' -c \'cd ' + profile_path + ' ; ls | grep -i ' + host + ' | grep -v "\." | grep -v "ASC" | cut -d"_" -f2\''
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.readlines()[0]

        command = 'sudo su - ' + user_sap + ' -c \'startsap -c |grep -i ' + status.strip() + ' --color=never | tail -n -1 | cut -d" " -f4\''
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.readlines()
        if status[0].strip() == "running":
            print "POST:P: The SAP service is already started on the target server (HOSTNAME - " + hostname + ")"
            log = "POST:P: The SAP service is already started on the target server (HOSTNAME - " + hostname + ")"
            write (logfile, log)
        else:
            command = "sudo su - " + user_sap + " -c 'ps -ef | grep -i " + user_sap + " | grep -i /usr/sap | grep -v # |  cut -d\" \" -f4'"
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            all_names = stdout.readlines()
            for n in range (0, (len(all_names))):
                proc = all_names[n].strip()
                command = "sudo su - " + user_sap + ' -c "kill -9 ' + proc + '"'
#		print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                if stdout.channel.recv_exit_status() == 0:
                    print "POST:I: The processes related to the SAP has been stopped in the target application server (HOSTNAME - " + hostname + ")"
                    log = "POST:I: The processes related to the SAP has been stopped in the target application server (HOSTNAME - " + hostname + ")"
                    write (logfile, log)

            command = 'sudo su - ' + user_sap + ' -c "startsap r3 '  + host + '"'
	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.channel.recv_exit_status()
            if status == 0:
                print "POST:P: The SAP service has been started on the target server (HOSTNAME - " + hostname + ")"
                log = "POST:P: The SAP service has been started on the target server (HOSTNAME - " + hostname + ")"
                write (logfile, log)
            else:
                print "POST:F: The SAP server has not been successfully started on the target server (HOSTNAME - " + hostname + ")"
                log = "POST:F: The SAP server has not been successfully started on the target server (HOSTNAME - " + hostname + ")"
                write (logfile, log)
 #           write (logfile, log)
	command = 'sudo su - ' + appuser + ' -c \'echo $dbs_ora_schema\''
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        schema = ''.join(stdout.readlines()).strip()
        #print schema
        if "does not exist" in schema:
                print "TRUNCATETABLE:F:The Target Application SID - " + app_sid + " passed by the user is incorrect"
                log4erp.write(logfile,"POST:F:The Target Application SID - " + app_sid + " passed by the user is incorrect")
        elif stdout.channel.recv_exit_status() == 0:
            cleanuptable = ['BTCEVTJOB','BTC_CRITERIA','BTC_CRITNODES','BTC_CRITPROFILES','BTC_CRITTYPES','BTC_TYPEFIELDS','REORGJOBS','TBTCA','TBTCB','TBTCCNTXT','TBTCCTXTT','TBTCCTXTTP','TBTCI','TBTCJSTEP','TBTCO','TBTCP','TBTCR','TBTCS']
            for i in cleanuptable:
                command = 'sudo su - ' + dbuser + ' -c "echo \'Truncate TABLE ' + schema + '.' + i + ';\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
                stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
                ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + "." + i + " table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(logfile,"POST:P:Truncate of " +  schema + "." + i + " table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + "." + i + " table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(logfile,"POST:F:Truncate of " + schema + "." + i + " table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + dbuser + ' -c "echo \'COMMIT;\' | sqlplus / as sysdba" | grep -i --color=never "Commit complete."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Commit complete.":
                print "TRUNCATETABLE:P:Database Commited successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(logfile,"POST:P:Database Commited successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Database Commit failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(logfile,"POST:F:Database Commit failed on target database server ( Hostname - " + dbhostname + " )")
        channel.close()
        client.close()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "POST:F:GERR_3001:Hostname unknown"
        log4erp.write(logfile,'POST:F: Hostname unknown [Error Code - 3001]')
    elif str(e).strip() == "list index out of range":
        print "POST:F:GERR_3002:Argument/s missing for sapstartapp script"
    elif str(e) == "Authentication failed.":
        print "POST:F:GERR_3003:Authentication failed."
        log4erp.write(logfile,'POST:F:Authentication failed[Error Code - 3003]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "POST:F:GERR_3004:Host Unreachable"
        write(logfile,'POST:F:Host Unreachable.[Error Code - 3004]')
    elif "getaddrinfo failed" in str(e):
        print "POST:F:GERR_3005: Please check the hostname that you have provide"
        log4erp.write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 3005]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "POST:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
        write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 3006]')
    else:
        print "POST:F: " + str(e)
	write(logfile,"POST:F: " + str(e))
