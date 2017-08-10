import os
from sys import *
import subprocess
import log4erp
from log4erp import *
try:
#    if argv[1] == "--u":
#        print "usage: python truncatetable.py <Target Application Hostname> <Target sudo User Name> <Target sudo user password> <Target Application SID> <Target Database Hostname> <Target Database User Name> <Target Database sudo user password> <Target Database SID> <Refresh ID>"
#    else:
            dbhostname = argv[1]
            dbusername = argv[2]
            dbpassword = argv[3]
            database_sid = argv[4]
            orauser = "ora" + database_sid.lower()
            refreshid = argv[5] + ".log"
            schema = argv[6]
            location = argv[7]

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.DBSTATHORA;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTATHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTATHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTATHORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTATHORA table has failed on target database server ( Hostname - " + dbhostname + " )")
            
            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.DBSTAIHORA;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTAIHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTAIHORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTAIHORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTAIHORA table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.DBSTATIORA;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTATIORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTATIORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTATIORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTATIORA table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.DBSTATTORA;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSTATTORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSTATTORA table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSTATTORA table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSTATTORA table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.ALCONSEG;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".ALCONSEG table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".ALCONSEG table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".ALCONSEG table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".ALCONSEG table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.ALSYSTEMS;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".ALSYSTEMS table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".ALSYSTEMS table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".ALSYSTEMS table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".ALSYSTEMS table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.DBSNP;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DBSNP table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DBSNP table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DBSNP table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DBSNP table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.MONI;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".MONI table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".MONI table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".MONI table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".MONI table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.OSMON;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".OSMON table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".OSMON table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".OSMON table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".OSMON table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.PAHI;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".PAHI table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".PAHI table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".PAHI table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".PAHI table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.SDBAD;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAD table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAD table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAD table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAD table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.SDBAH;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAH table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAH table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAH table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAH table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.SDBAP;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAP table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAP table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAP table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAP table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.SDBAR;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".SDBAR table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".SDBAR table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".SDBAR table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".SDBAR table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.DDLOG;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".DDLOG table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".DDLOG table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".DDLOG table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".DDLOG table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.TPFET;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".TPFET table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".TPFET table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".TPFET table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".TPFET table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.TPFHT;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".TPFHT table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".TPFHT table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".TPFHT table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".TPFHT table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'Truncate TABLE ' + schema + '.TLOCK;\' | sqlplus / as sysdba"'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
            if "Table truncated." in out:
                print "TRUNCATETABLE:P:Truncate of " +  schema + ".TLOCK table has completed successfully on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:P:Truncate of " +  schema + ".TLOCK table has completed successfully on target database server ( Hostname - " + dbhostname + " )")
            else:
                print "TRUNCATETABLE:F:Truncate of " + schema + ".TLOCK table has failed on target database server ( Hostname - " + dbhostname + " )"
                log4erp.write(refreshid,"POST:F:Truncate of " + schema + ".TLOCK table has failed on target database server ( Hostname - " + dbhostname + " )")

            command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + dbusername.strip() + ':' + dbpassword.strip() + '@' + dbhostname + ' "echo \'COMMIT;\' | sqlplus / as sysdba" | grep -i --color=never "Commit complete."'
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            out = ''.join(out)
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
