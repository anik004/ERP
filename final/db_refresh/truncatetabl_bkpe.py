from paramiko import *
import paramiko
from sys import *
import log4erp
import timeit
start_time = timeit.default_timer()
try:
    if argv[1] == "--u":
        print "usage: python truncatetable.py <Target Application Hostname> <Target sudo User Name> <Target sudo user password> <Target Application SID> <Target Database Hostname> <Target Database User Name> <Target Database sudo user password> <Target Database SID> <Refresh ID>"
    else:
        apphostname = argv[1]
        appusername = argv[2]
        apppassword = argv[3]
        app_sid = argv[4]
        appuser = app_sid.lower() + "adm"
        dbhostname = argv[5]
        dbusername = argv[6]
        dbpassword = argv[7]
        database_sid = argv[8]
        orauser = "ora" + database_sid.lower()
        refreshid = argv[9] + ".log"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( apphostname,username = appusername, password = apppassword)
        channel = client.invoke_shell()

        client1 = SSHClient()
        client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client1.connect( dbhostname,username = dbusername, password = dbpassword)
        channel1 = client1.invoke_shell()

        command = 'sudo su - ' + appuser + ' -c \'echo $dbs_ora_schema\''
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        schema = ''.join(stdout.readlines()).strip()
        if stdout.channel.recv_exit_status() == 0:
            
            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.DBSTATHORA;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTATHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTATHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTATHORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTATHORA table has failed on target database server ( Hostname - " + dbhostname + " )")
            
            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.DBSTAIHORA;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTAIHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTAIHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTAIHORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTAIHORA table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.DBSTATIORA;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTATIORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTATIORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTATIORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTATIORA table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.DBSTATTORA;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTATTORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTATTORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTATTORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTATTORA table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.DBSNP;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSNP table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSNP table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSNP table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSNP table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.MONI;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".MONI table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".MONI table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".MONI table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".MONI table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.OSMON;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".OSMON table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".OSMON table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".OSMON table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".OSMON table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.PAHI;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".PAHI table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".PAHI table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".PAHI table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".PAHI table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.SDBAD;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAD table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAD table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAD table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAD table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.SDBAH;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAH table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAH table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAH table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAH table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.SDBAP;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAP table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAP table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAP table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAP table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.SDBAR;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAR table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAR table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAR table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAR table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.DDLOG;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DDLOG table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DDLOG table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DDLOG table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DDLOG table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.TPFET;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".TPFET table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".TPFET table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".TPFET table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".TPFET table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.TPFHT;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".TPFHT table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".TPFHT table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".TPFHT table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".TPFHT table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.TLOCK;\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Table truncated.":
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".TLOCK table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".TLOCK table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".TLOCK table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".TLOCK table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'sudo su - ' + orauser + ' -c "echo \'COMMIT;\' | sqlplus / as sysdba" | grep -i --color=never "Commit complete."'
            stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            ouuput = ''.join(stdout.readlines()).strip()
            if ouuput == "Commit complete.":
                print "TRUNCATETABLE:P:Database Commited successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Database Commited successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Database Commit failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Database Commit failed on target database server ( Hostname - " + dbhostname + " )")

        channel.close()
        client.close()
        
        channel1.close()
        client1.close()
        elapsed = timeit.default_timer() - start_time
	#print elapsed


except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "TRUNCATETABLE:F:GERR_2301:Hostname unknown"
        log4erp.write(refreshid,'POST:F: Hostname unknown [Error Code - 2301]')
    elif str(e).strip() == "list index out of range":
        print "TRUNCATETABLE:F:GERR_2302:Argument/s missing for TRUNCATETABLE script"
    elif str(e) == "Authentication failed.":
        print "TRUNCATETABLE:F:GERR_2303:Authentication failed."
        log4erp.write(refreshid,'POST:F:Authentication failed[Error Code - 2303]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "TRUNCATETABLE:F:GERR_2304:Host Unreachable"
	write(refreshid,'POST:F:Host Unreachable.[Error Code - 2304]')
    elif "getaddrinfo failed" in str(e):
        print "TRUNCATETABLE:F:GERR_2305: Please check the hostname that you have provide"
        log4erp.write(refreshid,'POST:F: Please check the hostname that you have provide [Error Code - 2305]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "TRUNCATETABLE:F:GERR_2306:Host Unreachable or Unable to connect to port 22"
        write(refreshid,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2306]')
    else:
        print "TRUNCATETABLE:F: " + str(e)
