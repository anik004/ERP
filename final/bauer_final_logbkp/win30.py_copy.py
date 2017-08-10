import re
import subprocess
from subprocess import *
from sys import *
import os
from log4erp import *
try:
# ---------------------- variable declaration ------------------------------------------
  hostname = argv[1]
  username = argv[2]
  password = argv[3]
  location = argv[4] # kernel location
  drive = argv[5]    # script location -> AL11 path
  license_file = argv[6] # license file name
  profilepath = argv[7] # profile path

# ------------------------------- copy the license -----------------------------------------
  localpath = drive.rstrip('\\') + '\\' +  license_file
  command = 'copy ' + localpath + ' \\\\' + hostname + '\\sharename /Y'
  #print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  status = command.returncode

# --------------------------------- get profile name ---------------------------------------
  command = 'c:\\python27\\python ' + drive.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + profilepath + ' /s /b | findstr DVEBMGS*"'
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  #print out
  profilepath = out.split('\n')[3].rstrip()
  #print profilepath
  
# ------------------------------- get license details --------------------------------------

  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -show | findstr Hardware\"'
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  output = out
  #print output
  output = output.split('\n')
  print output
  hardware1=output[3].split(':')[1].strip()
  hardware2=output[4].split(':')[1].strip()
  hardware3=output[5].split(':')[1].strip()
  print hardware1
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -show | findstr System\"'
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  output = out
  #print output
  output = output.split('\n')
  system1=output[3].split(':')[1].strip()
  print system1
  system2 = output[5].split(':')[1].strip()
  system3 = output[7].split(':')[1].strip()
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -show | findstr Software\"'
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  output = out
  #print output
  output = output.split('\n')
  software1=output[3].split(':')[1].strip()
  software2=output[5].split(':')[1].strip()
  software3=output[7].split(':')[1].strip()
  print software1
  
  for each in output.split('\n'):
    #print each
    if 'Hardware Key' in each:
        #print '1'
	key = each.split(':')[1].strip().split('(')[0].strip()
	#print key
    elif 'Software products' in each:
        #print '2'
	prod = each.split(':')[1].strip()
	#print prod
    elif 'System ID' in each:
        #print '3'
        app_sid = each.split(':')[1].strip()
        #print app_sid

# --------------------------------- delete license ----------------------------------------
  if key and prod:

#  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -delete \'*\' \'*\' \'*\''
#  print command
 # command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
 # out, err = command.communicate()

  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -delete ' + system3 + ' ' + hardware3 + ' ' + software3 + '\"'
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -delete ' + system1 + ' ' + hardware1 + ' ' + software1 + '\"'  
  print command
    #exit()
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()

  if 'license key(s) were deleted' not in out:
        print 'POST:F:The License deletion has failed'
	exit()

# ----------------------------------- install license --------------------------------------
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -install ' + drive[:2] + '\\erp_trans\\' + license_file + '\"'
  #print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()

# ----------------------------- status check ----------------------------------------------
  if 'SAP license key(s) successfully installed' in out:
    print 'POST:P:License has been installed successfully'
  else:
    print 'POST:F:License installation has not completed successfully'

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
