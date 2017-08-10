from paramiko import *
import paramiko
from sys import *
import log4erp
from log4erp import *
import timeit
start_time = timeit.default_timer()
try:
    if argv[1] == "--u":
        print "usage: python truncatetable.py <Target Application Hostname> <Target sudo User Name> <Target sudo user password> <Target Application SID> <Target Database Hostname> <Target Database User Name> <Target Database sudo user password> <Target Database SID> <Refresh ID>"
    else:
        dbhostname = argv[1]
        dbusername = argv[2]
        dbpassword = argv[3]
        database_sid = argv[4]
        orauser = "ora" + database_sid.lower()
        refreshid = argv[5] + ".log"
	try:
        	client = SSHClient()
	        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	        client.connect( dbhostname,username = dbusername, password = dbpassword)
	        channel = client.invoke_shell()
	except Exception as e:
		if str(e) == "[Errno -2] Name or service not known":
	        	print "TRUNCATETABLE:F:GERR_2301:Target Application Hostname unknown"
	        	log4erp.write(refreshid,'POST:F: Target Application Hostname unknown [Error Code - 2301]')
		elif str(e) == "Authentication failed.":
        		print "TRUNCATETABLE:F:GERR_2303:Authentication failed to the Target Application Host"
	        	log4erp.write(refreshid,'POST:F:Authentication failed to the Target Application Host [Error Code - 2303]')
		elif str(e) == "[Errno 110] Connection timed out":
        		print "TRUNCATETABLE:F:GERR_2304:Target Application Host Unreachable"
	        	write(refreshid,'POST:F:Target Application Host Unreachable.[Error Code - 2304]')
		elif "getaddrinfo failed" in str(e):
        		print "TRUNCATETABLE:F:GERR_2305: Please check the Application hostname that you have provide"
	        	log4erp.write(refreshid,'POST:F: Please check the Application hostname that you have provide [Error Code - 2305]')
		elif "[Errno None] Unable to connect to port 22 on" in str(e):
        		print "TRUNCATETABLE:F:GERR_2306:Target Application Host Unreachable or Unable to connect to port 22"
	        	write(refreshid,'POST:F: Target Application Host Unreachable or Unable to connect to port 22 [Error Code - 2306]')
		else:
			print "TRUNCATETABLE:F:" + str(e)
			write(refreshid,'POST:F: ' + str(e))

        client1 = SSHClient()
        client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client1.connect( dbhostname,username = dbusername, password = dbpassword)
        channel1 = client1.invoke_shell()

        command = 'sudo su - ' + orauser + ' -c \'echo $dbs_ora_schema\''
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        schema = ''.join(stdout.readlines()).strip()
	#print schema
	if "does not exist" in schema:
		print "TRUNCATETABLE:F:The Target Application SID - " + app_sid + " passed by the user is incorrect"
		log4erp.write(refreshid,"POST:F:The Target Application SID - " + app_sid + " passed by the user is incorrect")
        elif stdout.channel.recv_exit_status() == 0:
	    jobtables = ['BTCEVTJOB','BTC_CRITERIA','BTC_CRITNODES','BTC_CRITPROFILES','BTC_CRITTYPES','BTC_TYPEFIELDS','REORGJOBS','TBTCA','TBTCB','TBTCCNTXT','TBTCCTXTT','TBTCCTXTTP','TBTCI','TBTCJSTEP','TBTCO','TBTCP','TBTCR','TBTCS']
	    for i in jobtables:
            	command = 'sudo su - ' + orauser + ' -c "echo \'Truncate TABLE ' + schema + '.' + i + ';\' | sqlplus / as sysdba" | grep -i --color=never "Table truncated."'
            	stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
            	ouuput = ''.join(stdout.readlines()).strip()
            	if ouuput == "Table truncated.":
                	print "TRUNCATETABLE:P:Truncate of " +  schema + "." + i + " table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                	log4erp.write(refreshid,"POST:P:Truncate of " +  schema + "." + i + " table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            	else:
                	print "TRUNCATETABLE:F:Truncate of " + schema + "." + i + " table has failed on target database server ( Hostname - " + dbhostname + " )"
                	log4erp.write(refreshid,"POST:F:Truncate of " + schema + "." + i + " table has failed on target database server ( Hostname - " + dbhostname + " )")
            
        client.close()
        
        channel1.close()
        client1.close()
        elapsed = timeit.default_timer() - start_time
	#print elapsed


except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "TRUNCATETABLE:F:GERR_2301:Target Database Hostname unknown"
        log4erp.write(refreshid,'POST:F: Target Database Hostname unknown [Error Code - 2301]')
    elif str(e).strip() == "list index out of range":
        print "TRUNCATETABLE:F:GERR_2302:Argument/s missing for TRUNCATETABLE script"
    elif str(e) == "Authentication failed.":
        print "TRUNCATETABLE:F:GERR_2303:Authentication failed to the Target Database Host"
        log4erp.write(refreshid,'POST:F:Authentication failed to the Target Database Host [Error Code - 2303]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "TRUNCATETABLE:F:GERR_2304:Target Database Host Unreachable"
	write(refreshid,'POST:F:Target Database Host Unreachable.[Error Code - 2304]')
    elif "getaddrinfo failed" in str(e):
        print "TRUNCATETABLE:F:GERR_2305: Please check the hostname that you have provide"
        log4erp.write(refreshid,'POST:F: Please check the hostname that you have provide [Error Code - 2305]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "TRUNCATETABLE:F:GERR_2306:Target Database Host Unreachable or Unable to connect to port 22"
        write(refreshid,'POST:F: Target Database Host Unreachable or Unable to connect to port 22 [Error Code - 2306]')
    else:
        print "TRUNCATETABLE:F: " + str(e)
	write(refreshid,'POST:F: ' + str(e))
