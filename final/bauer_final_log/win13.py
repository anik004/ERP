import paramiko
import re
import log4erp
from log4erp import *
from paramiko import *
import os.path
from sys import *
import subprocess

try:
    if argv[1] == "--u":
        print "c:\python27\python ' + loc.strip('\\') + '\transport.py <path in Source> <Transport id> <Path in target> <target IP> <target Application SID> <Domain name> <Target Sudo Login User Name> <Target Sudo User Password> <Source Application SID> <Location> <Ref_id>"

    else:
	def get_result(out):
	    for each in out.split('\n'):
		if 'tp finished with return code' in each:
			return each.split(':')[1]

        s_path = argv[1].rstrip('\\')

        tr_id = str(argv[2]).strip()
        t_path = argv[3].rstrip('\\')

        t_hostname = argv[4]
        t_sid = argv[5].lower()
        domain = argv[6].upper()
        t_username = argv[7]
        t_password = argv[8]

        tr_part = tr_id[4:]
        sid = t_sid.upper()
        s_sid = argv[9].upper()
	s_sid = tr_id[:3].upper()

	ref_id = argv[11]
	location = argv[10].strip('\\') # kernel path
	loc = argv[12]			# script location
        count1 = len(t_sid)
        count2 = len(s_sid)
	
#	command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \'md ' + location + '\\erp_trans && net share sharename=' + argv[7] + '\\erp_trans /grant:everyone,full\''
#	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#    	out, err = command.communicate()
        
	if count1 > 3 or count1 < 3 or count2 > 3 or count2 < 3:
            print "Wrong syntax of Target/Source SID"
        else:
	    f = open(loc + "\\" + ref_id + "\\transport.bat","w+")
            for name in "cofiles", "data":
                if name == "cofiles":
                    initial = "K"
		    filename = initial + tr_part + '.' + s_sid
                else:
                    initial = "R"
	            filename = initial + tr_part + '.' + s_sid


                localpath = s_path + "\\" + name + "\\" + filename
                filepath =  t_path + "\\" + name + "\\" + filename

		command = 'copy ' + localpath + ' \\\\' + t_hostname + '\\sharename /Y'
	        print command
		write('reflogfile.log',command)
    	        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    	        out, err = command.communicate()
                write('reflogfile.log',out)
		print out
	        status = command.returncode
		if status == 0:
		    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"copy ' + location[:2] + '\\erp_trans\\' + filename + ' ' + filepath + ' /Y\"'
		    f.write(command)
                    print command
                    write('reflogfile.log',command)
                    #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                    #out, err = command.communicate()
		    #print out
                    #status = command.returncode
		    #if status == 0:
                    #    print "POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully."
			#write(ref_id,"POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully.") 
		    #else:
		    #	print 'POST:F:Agent file transfer failed'
      		        #write(ref_id,'POST:F:Agent file transfer failed')
		    #	exit()

		"""		
		command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \'where /r ' + location + ': tp.exe\''
	        #print command
	        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	        out, err = command.communicate()
	        out = out.split('\n')
	        for line in out:
	            if re.search('DRL',line):
	                if re.search('SYS',line):
            	            if 'BKP' not in line:
#		            	print line
                		path = line.split('\\')
                  		del path[-1]
                	        path = '\\'.join(path)
		"""
	    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp addtobuffer ' + tr_id + " " + t_sid  + ' Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
	    f.write(command)
	    print command
	    write('reflogfile.log',command)
		#command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                #out, err = command.communicate()
	        #status = get_result(out)
		#print status
        	#if status == '0' or '4':
	    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp modbuffer ' + tr_id + " " + t_sid  + ' mode=u+12 Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
	    f.write(command)
            print command
            write('reflogfile.log',command)
		#    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		#    out, err = command.communicate()
                #    status = get_result(out)
		#    print status
                #    if status == '0' or '4':
	    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp import ' + tr_id + " " +  t_sid + ' Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
	    f.write(command)
            print command
            write('reflogfile.log',command)
	    f.close()
	    command = 'copy ' + loc + '\\' + ref_id + 'transport.bat' + ' \\\\' + t_hostname + '\\sharename /Y'
	    write('reflogfile.log',command)
	    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
	    write('reflogfile.log',out)
	    if command.returncode == 0:
		command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + 'schtasks.exe /create /TN \'test\' /SC ONCE /TR ' + E:\erp_trans\test.bat /ST 05:41:00
                write('reflogfile.log',command)
            #status = get_result(out)
		#	    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	        #            out, err = command.communicate()
        	#            status = get_result(out)
		#	    print status
                #	    if status == '0' or '4':
	        #                print "POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname
		#		#write(ref_id,"POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname)
				"""
				command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"rd ' + location +  '\\erp_trans\"'
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                            	out, err = command.communicate()
				"""

	                    else:
            		        print "POST:F: TR " + tr_id + " import is failed with the error code: " + status
				#write(ref_id,"POST:F: TR " + tr_id + " import is failed with the error code: " + status)
	            else:
            		    print "POST:F: The modbuffer for the TR " + tr_id + " has failed"
			    #write(ref_<F5><F5>id,"POST:F: The modbuffer for the TR " + tr_id + " has failed")
	        else:
        	    print "POST:F: TR " + tr_id + " is failed with the error code: " + status
		    #write(ref_id, "POST:F: TR " + tr_id + " is failed with the error code: " + status)
		


except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "POST:F:GERR_0201:Hostname unknown"
        #write(ref_id,'POST:F:GERR_0201:Hostname unknown')
	write('reflogfile.log','POST:F:GERR_0201:Hostname unknown')
    elif str(e).strip() == "list index out of range":
        print "POST:F:GERR_0202:Argument/s missing for the script"
	write('reflogfile.log','POST:F:GERR_0202:Argument/s missing for the script')
    elif str(e) == "Authentication failed.":
        print "POST:F:GERR_0203:Authentication failed."
        #write(ref_id,'POST:F:GERR_0203:Authentication failed.')
	write('reflogfile.log','POST:F:GERR_0203:Authentication failed.')
    elif str(e) == "[Errno 110] Connection timed out":
        print "POST:F:GERR_0204:Host Unreachable"
        #write(ref_id,'POST:F:GERR_0204:Host Unreachable')
	write('reflogfile.log','POST:F:GERR_0204:Host Unreachable')
    elif "getaddrinfo failed" in str(e):
        print "POST:F:GERR_0205: Please check the hostname that you have provide"
        #write(ref_id,'POST:F:GERR_0205: Please check the hostname that you have provide')
	write('reflogfile.log','POST:F:GERR_0205: Please check the hostname that you have provide')
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
        #write(ref_id,'POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	write('reflogfile.log','POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
    else:
        print "POST:F: " + str(e)
        #write(ref_id,"POST:F: " + str(e))
	write('reflogfile.log',"POST:F: " + str(e))

