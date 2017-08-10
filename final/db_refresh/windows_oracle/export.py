#from log4erp import *
import re
import subprocess
from subprocess import *
from sys import *
import os
import log4erp
from log4erp import *

def imp(filename, hostname, username, password, appsid, client_name, seqno, stepname, location, drive):
    #print username
#    client = SSHClient()
#    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    client.connect(hostname,username = username, password = password)
#    channel = client.invoke_shell()


    appuser = appsid.lower() + 'adm'
    file_open = open(filename.strip(), 'w')

    file_content = """export
client=""" + client_name + """
file='""" + location[:1] + """:\\test\\""" + filename.strip() + """.dat'
select * from """ + filename.strip()


    file_open.write(file_content)
    file_open.close()

    command = 'copy ' + filename.strip() + ' \\\\' + hostname + '\\sharename'
    print command
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    status = command.returncode
    
    if status != 0:
	    print 'File has not been created'
	

    command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"' + location.strip('\\') + '\R3trans -w ' + location[:1] + ':\\test\\' + filename + '.log ' + location[:1] + ':\\test\\' + filename + '\"'
    
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    status = command.returncode
    if status == 0 or 4:
	data_1 = out.split('\n')
	for each in data_1:
    		if 'R3trans' in each:
        		final_status = each.split('(')[1].strip(')')[:4]
			if final_status == '0000' or final_status == '0004':
			        print stepname + ':P:The backup for the table ' + filename + ' is successful'

        			command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"del ' + location[:1] + ':\\test\\' + filename + '\"'
                                #print command
        			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        			out, err = command.communicate()

        			command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"del ' + drive.strip('\\') + '\\' + filename + '\"'
                                #print command
        			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        			out, err = command.communicate()
                        """
			else:
				print stepname + ':F:The backup for the table ' + filename + ' has failed with error code:' + final_status
 			"""
    else:
        print stepname + ':F:The backup for the table ' + filename + ' has failed'
        exit()

#    os.remove(filename)

try:

  hostname = argv[1]
  username = argv[2]
  password = argv[3]
  location = argv[7]
  appsid = argv[4]
  client_name = argv[5]
  stepname = argv[6]
  drive = argv[8]

  command = 'whoami'
  command = Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  command = 'c:\python27\python ' + drive.strip('\\') + '\win14.py ' + stepname.upper()
  #print command
  command = Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  table_name = (out[:-2].strip('""').strip("''").strip("'\n")).split("', '")
  seqno=int(0)

  
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"md ' + argv[7][:2] + '\\test && net share sharename=' + argv[7][:2] + '\\test /grant:everyone,full\"'
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()

  for each in table_name:
    seqno=seqno + 1
    imp(each, argv[1], argv[2], argv[3], argv[4],argv[5],str(seqno),argv[6], argv[7], argv[8].strip('\\'))

except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
               print "PRE:F:GERR_0201:Hostname unknown"
        elif str(e).strip() == "list index out of range":
               print "PRE:F:GERR_0202:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
               print "PRE:F:GERR_0203:Authentication failed."
	elif str(e) == "[Errno 110] Connection timed out":
               print "PRE:F:GERR_0204:Host Unreachable"
        elif "getaddrinfo failed" in str(e):
               print "PRE:F:GERR_0205: Please check the hostname that you have provide"
        elif "[Errno None] Unable to connect to port 22" in str(e):
               print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
        else:
               print "PRE:F: " + str(e)
