from log4erp import *
import re
import subprocess
from subprocess import *
from sys import *
import os

def imp(filename, hostname, username, password, appsid, client_name, seqno, stepname, location, drive):

    if '/' in filename:
        print 'yes'
        file = filename
        filename = filename.split('/')[1]
    else:
        file = filename
    file_open = open(filename.strip(), 'w')

    file_content = """export
client=""" + client_name + """
file='""" + location[:1] + """:\\erp_trans\\""" + filename.strip() + client_name + """.dat'
select * from '""" + file.strip() + '\''


    file_open.write(file_content)
    file_open.close()
    
    # ----------------------- For Binding Error ---------------------------
    """
	command = 'ping -n 1 ' + hostname
    print command
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    hostname = str(out.split('\r\n')[2].split(" ")[2][:-1])
    #print hostname
    """
    # ------------------------- For binding Error -----------------------
    write(drive.strip('\\') + '\\reflogfile.log','win12 : this command is used to copy files to share folder')
    command = 'copy ' + filename.strip() + ' \\\\' + hostname + '\\sharename'
    #print command
    write(drive.strip('\\') + '\\reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    write(drive.strip('\\') + '\\reflogfile.log',out)
    status = command.returncode

    if "1" not in out:
        print 'File has not been created'
        #write(drive.strip('\\') + logfile,'File has not been created')
	# -------------------------------- EXPORT ---------------------------------------
    command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"' + location.strip('\\') + '\R3trans -w ' + location[:1] + ':\\erp_trans\\' + filename + '.log ' + location[:1] + ':\\erp_trans\\' + filename + '\"'
    #print command
    write(drive.strip('\\') + '\\reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    write(drive.strip('\\') + '\\reflogfile.log',out)
    status = command.returncode
    if status == 0 or status == 4:
        data_1 = out.split('\n')
        for each in data_1:
            if 'R3trans finished' in each:
                final_status = each.split('(')[1].strip(')')[:4]
                #print final_status
                if final_status == '0000' or final_status == '0004':
                    print stepname + ':P:The backup for the table ' + filename + ' is successful'
                    #write(drive.strip('\\') + logfile,stepname + ':P:The backup for the table ' + filename + ' is successful')
                else:
                    print stepname + ':F:The backup for the table ' + filename + ' is failed'
                    #write(drive.strip('\\') + logfile,stepname + ':P:The backup for the table ' + filename + ' is successful')
                write(drive.strip('\\') + '\\reflogfile.log','win12 : this command is used to del the share folder')
                command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"del ' + location[:1] + ':\\erp_trans\\' + filename + '\"'
                #print command
                write(drive.strip('\\') + '\\reflogfile.log',command)
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                write(drive.strip('\\') + '\\reflogfile.log',out)

                command = "del " + drive.strip('\\') + '\\' + filename + '\"'
                #print command
                write(drive.strip('\\') + '\\reflogfile.log',command)
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                write(drive.strip('\\') + '\\reflogfile.log',out)
    else:
        print stepname + ':F:The backup for the table ' + filename + ' has failed'
        #write(drive.strip('\\') + logfile,stepname + ':F:The backup for the table ' + filename + ' has failed')

try:
 # print 'start'
  hostname = argv[1]
  username = argv[2]
  password = argv[3]
  location = argv[7]
  appsid = argv[4]
  client_name = argv[5]
  stepname = argv[6]
  drive = argv[8]

  command = 'whoami'
  write(drive.strip('\\') + '\\reflogfile.log',command)
  command = Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  write(drive.strip('\\') + '\\reflogfile.log',out)
  command = 'c:\python27\python ' + drive.strip('\\') + '\win14 ' + stepname.upper()
  #print command
  write(drive.strip('\\') + '\\reflogfile.log',command)
  command = Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  write(drive.strip('\\') + '\\reflogfile.log',out)
  table_name = (out[:-2].strip('""').strip("''").strip("'\n")).split("', '")
  seqno=int(0)
  # --------------------- For Binding Error -----------------------------------
  """
  command = 'ping -n 1 ' + hostname
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  hostname = str(out.split('\r\n')[2].split(" ")[2][:-1])
  print hostname
  """
  # -------------------------- Fro binding Error -----------------------------
  command = 'c:\\python27\\python ' + drive.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + argv[7][:2] + ' /s /b | findstr erp_trans"'
  #print command
  write(drive.strip('\\') + '\\reflogfile.log',command)
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  write(drive.strip('\\') + '\\reflogfile.log',out)
  profilepath = out
  #print 'Prof: ' + profilepath
  if 'erp_trans' not in profilepath:
      write(drive.strip('\\') + '\\reflogfile.log','win12 : this command is used to create share folder and grant full permission')
      command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + hostname + ' \"md ' + argv[7][:2] + '\\erp_trans && net share sharename=' + argv[7][:2] + '\\erp_trans /grant:everyone,full\"'
      #print command
      write(drive.strip('\\') + '\\reflogfile.log',command)
      command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
      out, err = command.communicate()
      write(drive.strip('\\') + '\\reflogfile.log',out)
     # print out

  for each in table_name:
    seqno=seqno + 1
    imp(each, argv[1], argv[2], argv[3], argv[4],argv[5],str(seqno),argv[6], argv[7], argv[8].strip('\\'))
    #print "test"

except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
            print "PRE:F:GERR_0201:Hostname unknown"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
            #write(drive.strip('\\') + logfile,'PRE:F:GERR_0201:Hostname unknown')
        elif str(e).strip() == "list index out of range":
            print "PREFGERR_0202:Argument/s missing for the script"
            write(drive.strip('\\') + '\\reflogfile.log','PREFGERR_0202:Argument/s missing for the script')
            #write(drive.strip('\\') + logfile,'PREFGERR_0202:Argument/s missing for the script')
        elif str(e) == "Authentication failed.":
            print "PRE:F:GERR_0203:Authentication failed."
    	    write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
            #write(drive.strip('\\') + logfile,"PRE:F:GERR_0203:Authentication failed.")
    	elif str(e) == "[Errno 110] Connection timed out":
            print "PRE:F:GERR_0204:Host Unreachable"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
            #write(drive.strip('\\') + logfile,"PRE:F:GERR_0204:Host Unreachable")
        elif "getaddrinfo failed" in str(e):
            print "PRE:F:GERR_0205: Please check the hostname that you have provide"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
            #write(drive.strip('\\') + logfile,"PRE:F:GERR_0205: Please check the hostname that you have provide")
        elif "[Errno None] Unable to connect to port 22" in str(e):
            print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
            #write(drive.strip('\\') + logfile,'PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
        else:
            print "PRE:F: " + str(e)
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F: ' + str(e))
            #write(drive.strip('\\') + logfile,'PRE:F: ' + str(e))
