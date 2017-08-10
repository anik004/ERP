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
        t_profile_path = argv[3].rstrip('\\')

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
	
	write(ref_id,"POST:P:import triggered")
	
#	command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \'md ' + location + '\\erp_trans && net share sharename=' + argv[7] + '\\erp_trans /grant:everyone,full\''
#	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#    	out, err = command.communicate()
	command = 'c:\\python27\\python ' + loc.strip('\\') + '\\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "dir ' + t_profile_path + ' /s /b | findstr DVEBMGS* | findstr -V START"'
	write('reflogfile.log',"win36:" + command)
        print command
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
	write('reflogfile.log',out)
        profilepath = out.split('\n')[3]
        print profilepath
        command='c:\\python27\\python ' + loc.strip('\\') + '\\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "powershell.exe;\"\\"get-content ' + profilepath.strip() + ' | findstr DIR_TRANS\\"\" | findstr -V #"'
	write('reflogfile.log',"win36:" + command)
        print command
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
	write('reflogfile.log',out)
        #print out
        out=out.split('\n')
        #print out
        out=''.join(out)
        parameter = out.split('used',1)
        print parameter
        parameter = parameter[1].strip()
	print parameter
        t_path = parameter.split('=')[1].strip()
	#exit()
        
	if count1 > 3 or count1 < 3 or count2 > 3 or count2 < 3:
            print "Wrong syntax of Target/Source SID"
        else:
            for name in "cofiles", "data":
                if name == "cofiles":
                    initial = "K"
		    filename = initial + tr_part + '.' + s_sid
                else:
                    initial = "R"
	            filename = initial + tr_part + '.' + s_sid


                localpath = s_path + "\\" + name + "\\" + filename
                filepath =  t_path + "\\" + name + "\\" + filename

		write('reflogfile.log',"win36:This command copies the file from source path to the sharefolder")
		command = 'copy ' + localpath + ' \\\\' + t_hostname + '\\sharename /Y'
		write('reflogfile.log',command)
	        print command
    	        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    	        out, err = command.communicate()
		write('reflogfile.log',out)
	        status = command.returncode
		if status == 0:
		    write('reflogfile.log',"win36:This command copies the file from sharefolder to the target path")
		    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"copy ' + location[:2] + '\\erp_trans\\' + filename + ' ' + filepath + ' /Y\"'
		    write('reflogfile.log',command)
                    print command
                    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                    out, err = command.communicate()
		    write('reflogfile.log',out)
                    status = command.returncode
		    if status == 0:
                        print "POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully."
			write(ref_id,"POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully.") 
		    else:
			print 'POST:F:Agent file transfer failed'
      		        write(ref_id,'POST:F:Agent file transfer failed')
			exit()

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
		write('reflogfile.log',"win36:" + command)
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
		write('reflogfile.log',out)
	        status = get_result(out)
		print status
        	if status == '0' or '4':
		    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp modbuffer ' + tr_id + " " + t_sid  + ' mode=u+12 Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
		    write('reflogfile.log',"win36:" + command)
                    print command
		    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		    out, err = command.communicate()
		    write('reflogfile.log',out)
                    status = get_result(out)
		    print status
                    if status == '0' or '4':
			    command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp import ' + tr_id + " " +  t_sid + ' Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
			    write('reflogfile.log',"win36:" + command)
                	    print command
			    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	                    out, err = command.communicate()
			    write('reflogfile.log',out)
        	            status = get_result(out)
			    print status
                	    if status == '0' or '4':
	                        print "POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname
				write(ref_id,"POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname)
				"""
				command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"rd ' + location +  '\\erp_trans\"'
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                            	out, err = command.communicate()
				"""

	                    else:
            		        print "POST:F: TR " + tr_id + " import is failed with the error code: " + status
				write(ref_id,"POST:F: TR " + tr_id + " import is failed with the error code: " + status)
	            else:
            		    print "POST:F: The modbuffer for the TR " + tr_id + " has failed"
			    write(ref_id,"POST:F: The modbuffer for the TR " + tr_id + " has failed")
	        else:
        	    print "POST:F: TR " + tr_id + " is failed with the error code: " + status
		    write(ref_id, "POST:F: TR " + tr_id + " is failed with the error code: " + status)
		


except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "POST:F:GERR_0201:Hostname unknown"
        write(ref_id,'POST:F:GERR_0201:Hostname unknown')
	write('reflogfile.log',"POST:F:GERR_0201:Hostname unknown")
    elif str(e).strip() == "list index out of range":
        print "POST:F:GERR_0202:Argument/s missing for the script"
	write('reflogfile.log',"POST:F:GERR_0202:Argument/s missing for the script")
    elif str(e) == "Authentication failed.":
        print "POST:F:GERR_0203:Authentication failed."
        write(ref_id,'POST:F:GERR_0203:Authentication failed.')
	write('reflogfile.log',"POST:F:GERR_0203:Authentication failed.")
    elif str(e) == "[Errno 110] Connection timed out":
        print "POST:F:GERR_0204:Host Unreachable"
        write(ref_id,'POST:F:GERR_0204:Host Unreachable')
	write('reflogfile.log',"POST:F:GERR_0204:Host Unreachable")
    elif "getaddrinfo failed" in str(e):
        print "POST:F:GERR_0205: Please check the hostname that you have provide"
        write(ref_id,'POST:F:GERR_0205: Please check the hostname that you have provide')
	write('reflogfile.log',"POST:F:GERR_0205: Please check the hostname that you have provide")
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
        write(ref_id,'POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	write('reflogfile.log',"POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22")
    else:
        print "POST:F: " + str(e)
        write(ref_id,"POST:F: " + str(e))
	write('reflogfile.log',"POST:F: " + str(e))
