import re
import subprocess
from subprocess import *
from sys import *
import os
from log4erp import *
import paramiko
from paramiko import *
try:
# ---------------------- variable declaration ------------------------------------------
  hostname = argv[1]
  username = argv[2]
  password = argv[3]
  location = argv[4].rstrip('/') # kernel location
  drive = argv[5].rstrip('/')    # script location -> AL11 path
  license_file = argv[6].lower() # license file name
  profilepath = argv[7].rstrip('/') # profile path
  appsid = argv[8].lower()
  appuser = appsid + 'adm'
  profile_path = profilepath

  client = SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(hostname,username = username, password = password)
  channel = client.invoke_shell()

  port = 22
  transport = paramiko.Transport((hostname, port))
  transport.connect(username = username, password = password)
  sftp = paramiko.SFTPClient.from_transport(transport)

# ------------------------------- copy the license -----------------------------------------
  localpath = drive.rstrip('/') + '/' +  license_file
  remotepath = '/tmp/' + license_file
  sftp.put(localpath, remotepath)
  command = 'sudo su - ' + appuser + ' -c \'cd ' + profile_path + ';ls | grep -i "' + appsid.upper() + '_DVEBMGS" | grep -v "\."\''
  print command
  stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
  profilefile = ''.join(stdout.read()).strip()
  print profilefile

# --------------------------------- get profile name ---------------------------------------
  """
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -show | findstr -V /C:"\"Software Product Limit\"" | findstr -V /C:"\"System Number\""\"'
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  output = out
  #print output
  output = output.split('\n')
  #print output
  #hardware1=output[3].split(':')[1].strip()
  #hardware2=output[4].split(':')[1].strip()
  #hardware3=output[5].split(':')[1].strip()
  #print hardware1
  #command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -show | findstr System\"'
  #print command
  #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  #out, err = command.communicate()
  #output = out
  #print output
  #output = output.split('\n')
  #print output
  #system1=output[3].split(':')[1].strip()
  #print system1
  #system2 = output[5].split(':')[1].strip()
  #system3 = output[7].split(':')[1].strip()
  #command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -show | findstr Software\"'
  #print command
  #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  #out, err = command.communicate()
  #output = out
  #print output
  #output = output.split('\n')
  #print output
  #software1=output[3].split(':')[1].strip()
  #software2=output[5].split(':')[1].strip()
  #software3=output[7].split(':')[1].strip()
  #print software1
  keys = ''
  prods = ''
  sids = ''
  print output
  for each in output:
    print each
    if 'Hardware Key' in each:
        print '1'
    	key = each.split(':')[1].strip().split('(')[0].strip()
    	keys = keys + key + ':'
    elif 'Software Product' in each:
        print '2'
	prod = each.split(':')[1].strip()
	prods = prods + prod + ':'
    elif 'System' in each:
        print '3'
        app_sid = each.split(':')[1].strip()
        sids=sids + app_sid + ':'
  keys = keys.rstrip(':').split(':')
  prods = prods.rstrip(':').split(':')
  sids = sids.rstrip(':').split(':')
  for i in range(0,len(keys)):
  """
    
  command = 'sudo su - ' + appuser + ' -c "saplikey pf=' + profilepath + '/' + profilefile + ' -delete \'*\' \'*\' \'*\'"'
  print command
  stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
  if stdout.channel.recv_exit_status() != 0:
        print 'POST:F:The License deletion has failed'
	exit()

  command = 'sudo su - ' + appuser + ' -c \'saplikey pf=' + profilepath + '/' + profilefile + ' -install /tmp/' + license_file + '\''
  print command
  stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
  if stdout.channel.recv_exit_status() == 0:
# ----------------------------- status check ----------------------------------------------
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
