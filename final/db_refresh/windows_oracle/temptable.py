#!/usr/bin/sh

# source IP - $1
# database sid - $2
# target IP - $3
# database sid - $4
# source application sid - $5
import os
from sys import *
import subprocess
import log4erp
from log4erp import *

try:
#    if argv[1] == "--u":
#        print "usage: python temptable.py <Source DB Host> <Source DB sid> <Target DB Host> <Target DB sid> <Target Application sid> <Source Sudo user> <source sudo pass> <target sudo user> <target sudo pass> <Refersh ID> <Instance ID>"
#    else:
        s_host = argv[1]
        s_user = argv[6]
        s_pass = argv[7]
        t_host = argv[3]
        t_user = argv[8]
        t_pass = argv[9]
        refresh_id = argv[10] + ".log"
        location = argv[11]
        user_source_db="ora" + argv[2].lower()
        user_target_db="ora" + argv[4].lower()
        upper_source=argv[2].upper()
        upper_target=argv[4].upper()

        #print "TEMPTABLE:I: Starting SAP on target server ( Hostname - " + argv[3] + " )"
        #log4erp.write(refresh_id,"POST:I: Starting SAP on target server ( Hostname - " + argv[1] + " )")
        #command = "python sapstartapp.py " + argv[3] + " " + argv[8] + " " + argv[9] + " " + argv[5] + " " + argv[11] + " " + argv[3] + " " + argv[10]# + " > /dev/null 2>&1"
        #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        #out, err = command.communicate()
	#print out.strip()
        status = 0
        if status ==0:
            #log4erp.write(refresh_id,"POST:I: SAP started on target server ( Hostname - " + argv[3] + " )")
            #log4erp.write(refresh_id,"POST:I: SAP started on target server ( Hostname - " + argv[3] + " )")

            print "TEMPTABLE:I: Getting temporary tablespace and associated datafile details on source server ( Hostname - " + argv[1] + " )"
            log4erp.write(refresh_id,"POST:I: Getting temporary tablespace and associated datafile details on source server ( Hostname - " + argv[1] + " )")
            path='c:\python27\python.exe ' + location + '\wmiexec.py ' + s_user.strip() + ':' + s_pass.strip() + '@' + s_host + ' "echo \'select tablespace_name,file_name from DBA_TEMP_FILES;\' | sqlplus / as sysdba"'
#            print path
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            path1, err = command.communicate()
#	    print path1
            print "TEMPTABLE:I: Fetched details of temporary tablespace and associated datafiles successfully on source server ( Hostname - " + argv[1] + " )"
            log4erp.write(refresh_id,"POST:I: Fetched details of temporary tablespace and associated datafiles successfully on target server ( Hostname - " + argv[1] + " )")
            for source_path in path1:
                actual_path=source_path.strip().replace(upper_source,upper_target)
                print "TEMPTABLE:I: Adding Tempfile \'" + actual_path + "' in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + t_user.strip() + ':' + t_pass.strip() + '@' + t_host + ' "echo \"ALTER TABLESPACE PSAPTEMP ADD TEMPFILE \'' + actual_path + '\' SIZE 2000M REUSE;\" | sqlplus / as sysdba'
#		        print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                out = ''.join(out)
                if "Tablespace altered." in out:
                        print "TEMPTABLE:P: Tempfile " + actual_path + " added successfully in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
                        log4erp.write(refresh_id,"POST:P: Tempfile " + actual_path + " added successfully in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )")
                elif "already part of database" in out:
                        print "TEMPTABLE:P: Tempfile " + actual_path + " already there in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
                        log4erp.write(refresh_id,"POST:P: Tempfile " + actual_path + " already there in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )")

                else:
                        print "TEMPTABLE:F: Adding Tempfile " + actual_path + " to Temporary tablespace failed"
                        log4erp.write(refresh_id,"POST:F: Adding Tempfile " + actual_path + " to Temporary tablespace failed")
                #print "TEMPTABLE:I: Closing connection on source server ( Hostname - " + argv[1] + " )"
                #log4erp.write(refresh_id,"POST:I: Closing connection on source server ( Hostname - " + argv[1] + " )")

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "TEMPTABLE:F:GERR_2101:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2101]')
    elif str(e).strip() == "list index out of range":
    	print "TEMPTABLE:F:GERR_2102:Argument/s missing for TempTable script"
    elif str(e) == "Authentication failed.":
        print "TEMPTABLE:F:GERR_2103:Authentication failed."
    	log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 2103]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "TEMPTABLE:F:GERR_2104:Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2104]')
    elif "getaddrinfo failed" in str(e):
        print "TEMPTABLE:F:GERR_2105: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2105]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "TEMPTABLE:F:GERR_2106:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2106]')
    else:
        print "TEMPTABLE:F: " + str(e)
