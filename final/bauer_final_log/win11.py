import re
import subprocess
from subprocess import *
from sys import *
import os
from log4erp import *

def imp(filename, hostname, username, password, appsid, client_name, seqno, stepname, location, drive):

    if '/' in filename:
        print 'yes'
        file = filename
        filename = filename.split('/')[1]
    else:
        file = filename
    #print filename

    #appuser = appsid.lower() + 'adm'
    file_open = open(filename.strip(), 'w')

    file_content = """import
client=""" + client_name + """
file='""" + location[:1] + """:\\erp_trans\\""" + filename.strip() + client_name + """.dat'
select * from '""" + filename.strip() + '\''


    file_open.write(file_content)
    file_open.close()

    # ---------------------- For Binding Error-----------------------------------
    """
    command = 'ping -n 1 ' + hostname
    #print command
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    hostname = str(out.split('\r\n')[2].split(" ")[2][:-1])
	"""
# ------------------- End of binding error --------------------------------------
# ------------------- Copy File -------------------------------------------------
    write('reflogfile.log','win11: This command is used to copy files to sharefolder')
    command = 'copy ' + filename.strip() + ' \\\\' + hostname + '\\sharename'
    #print command
    write('reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    write('reflogfile.log',out)
    status = command.returncode
    
    if status != 0:
	    print 'POST:F:The database script has not been created'
	# -------------------------------------- IMPORT -----------------------------
    command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"' + location.strip('\\') + '\R3trans -w ' + location[:1] + ':\\erp_trans\\' + filename + '.log ' + location[:1] + ':\\erp_trans\\' + filename + '\"'
    print command
    write('reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    write('reflogfile.log',out)
    status = command.returncode
    if status == 0 or 4:
        data_1 = out.split('\n')
        for each in data_1:
            if 'R3trans finished' in each:
                final_status = each.split('(')[1].strip(')')[:4]
                #print final_status
                if final_status == '0000' or final_status == '0004':
                    print 'POST:P:The import for the table ' + filename + ' is successful'
                else:
                    print 'POST:F:The import for the table ' + filename + ' is failed'

                command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"del ' + location[:1] + ':\\erp_trans\\' + filename + '\"'
                #print command
		write('reflogfile.log',command)
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
		write('reflogfile.log',out)

                command = "del " + drive.strip('\\') + '\\' + filename + '\"'
                #print command
		write('reflogfile.log',command)
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
		write('reflogfile.log',out)
    else:
        print 'POST:F:The restoration for the table ' + filename + ' has failed'
try:

  hostname = argv[1]
  username = argv[2]
  password = argv[3]
  appsid = argv[4].upper()
  client_name = argv[5]
  stepname = argv[6]
  location = argv[7]
  drive = argv[8] # script location

  command = 'whoami'
  write('reflogfile.log',command)
  command = Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  write('reflogfile.log',out)
  command = 'c:\python27\python ' + drive.strip('\\') + '\win14 ' + stepname.upper()
  #print command
  write('reflogfile.log',command)
  command = Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  write('reflogfile.log',out)
  table_name = (out[:-2].strip('""').strip("''").strip("'\n")).split("', '")
  seqno=int(0)
# ----------------------------- Get The Hostname of the system ----------------------------------
  """
  command = 'ping -n 1 ' + hostname
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  hostname = str(out.split('\r\n')[2].split(" ")[2][:-1])
  """
# ------------------------------- Check Backup Folder Existance -----------------------------------
  """
  command = 'c:\\python27\\python ' + drive.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + argv[7][:2] + ' /s /b | findstr erp_trans"'
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  profilepath = out
  if 'erp_trans' not in profilepath:
      print 'POST:F:The data backup files are not present'
  else:
      print 'skip'
  """
# ------------------------- End of Check the Backup folder Existance ----------------------------
  for each in table_name:
    seqno=seqno + 1
    imp(each, argv[1], argv[2], argv[3], argv[4],argv[5],str(seqno),argv[6], argv[7], argv[8].strip('\\'))

except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
               print "PRE:F:GERR_0201:Hostname unknown"
	       write('reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
        elif str(e).strip() == "list index out of range":
               print "PRE:F:GERR_0202:Argument/s missing for the script"
	       write('reflogfile.log','PRE:F:GERR_0202:Argument/s missing for the script')
        elif str(e) == "Authentication failed.":
               print "PRE:F:GERR_0203:Authentication failed."
	       write('reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
	elif str(e) == "[Errno 110] Connection timed out":
               print "PRE:F:GERR_0204:Host Unreachable"
	       write('reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
        elif "getaddrinfo failed" in str(e):
               print "PRE:F:GERR_0205: Please check the hostname that you have provide"
	       write('reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
        elif "[Errno None] Unable to connect to port 22" in str(e):
               print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
	       write('reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
        else:
               print "PRE:F: " + str(e)
	       write('reflogfile.log','PRE:F: ' + str(e))
