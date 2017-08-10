import re
import subprocess
from subprocess import *
import paramiko
from paramiko import *
from sys import *
import os
from log4erp import *
try:
# ---------------------- variable declaration ------------------------------------------
    hostname = argv[1]
    username = argv[2]
    password = argv[3]
 #   location = argv[4] # kernel location
    drive = argv[4].rstrip('/')    # script location -> AL11 path
    license_file = argv[5] # license file name
    profilepath = argv[6].rstrip('/') # profile path
    appsid = argv[7].lower()
    appuser = appsid + 'adm'
    logfile = argv[8]
#--------------------copying the license--------------------------------------------

    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    channel = client.invoke_shell()
    port = 22
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    localfile = drive + '/' + license_file
    remotefile = '/home/' + appuser + '/' + license_file
    sftp.put (localfile, remotefile)
    sftp.close()

# --------------------------------- get profile name ---------------------------------------
    command = 'su - ' + appuser + " -c 'cdpro; ls | grep -i --color=never \"QRP_DVEBMGS\" | grep -v \"\\.\"'"
    #print command
    stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
    #print stdout.readlines()
    filename = stdout.readlines()[0].rstrip()
    print filename
    final = stdout.channel.recv_exit_status()
    if final == 0:

#----------------------------------------------license details---------------------------------------------

        command = 'sudo su - ' + appuser + ' -c \'saplikey pf=' + profilepath + '/' + filename + ' -show | grep -v "Software Product Limit" | grep -v "System Number"\''
        #print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        file = stdout.readlines()
        #print len(file)
        keys = ''
        prods = ''
        sids = ''
        #file = file.split('\n')
        for each in file:
            #print each
            if 'Hardware Key' in each:
                #print each
                key = each.split(':')[1].strip()
                #print key
                keys = keys + key + ':'
                #print keys.rstrip(':')
            elif 'Software Product' in each:
                #print '2'
                prod = each.split(':')[1].strip()
                #print prod
                prods = prods + prod + ':'
                #print prods.rstrip(':')

            elif 'System' in each:
                #print '3'
                sid = each.split(':')[1].strip()
               # print sid
                sids = sids + sid + ':'
                #print sids.rstrip(':')
              #  for i in range(0, len(keys)):
               #     command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"' + location.rstrip('\\') + '\\saplikey pf=' + profilepath + ' -delete ' + sids[i] + ' ' + keys[i] + ' ' + prods[i] + '\"'

        keys = keys.rstrip(':').split(':')
        #print keys
        prods = prods.rstrip(':').split(':')
        #print prods
        sids = sids.rstrip(':').split(':')
        #print sids

#-------------------------------------------delete license-------------------------------------------------------
        for i in range(0, len(keys)):
            command = 'sudo su - ' + appuser + ' -c \'saplikey pf=' + profilepath + '/' + filename + ' -delete ' + sids[i] + ' ' + keys[i] + ' ' + prods[i] + '\''
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            final = stdout.channel.recv_exit_status()
            if final != 0:
                print 'POST:F:The License deletion has failed'
                exit()
#--------------------------------------------install license----------------------------------------------------

        command = 'sudo su - ' + appuser + ' -c \'saplikey pf=' + profilepath + '/' + filename + ' -install /home/' + appuser + '/' + license_file + '\''
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        final = stdout.channel.recv_exit_status()
        if final == 0:
            print 'POST:P:The License has been successfully installed'
        else:
            print 'POST:P:The License has failed to install'
            

    channel.close()
    client.close()

except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
            print "PRE:F:GERR_0201:Hostname unknown"
            write(drive.strip('\\') + '\\' +logfile,"PRE:F:GERR_0201:Hostname unknown")
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F:GERR_0201:Hostname unknown")

        elif str(e).strip() == "list index out of range":
            print "PRE:F:GERR_0202:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
            print "PRE:F:GERR_0203:Authentication failed."
            write(drive.strip('\\') + '\\' + logfile,"PRE:F:GERR_0203:Authentication failed.")
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F:GERR_0203:Authentication failed.")

        elif str(e) == "[Errno 110] Connection timed out":
            print "PRE:F:GERR_0204:Host Unreachable"
            write(drive.strip('\\') + '\\' + logfile,"PRE:F:GERR_0204:Host Unreachable")
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F:GERR_0204:Host Unreachable")

        elif "getaddrinfo failed" in str(e):
            print "PRE:F:GERR_0205: Please check the hostname that you have provide"
            write(drive.strip('\\') + '\\' + logfile,"PRE:F:GERR_0205: Please check the hostname that you have provide")
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F:GERR_0205: Please check the hostname that you have provide")

        elif "[Errno None] Unable to connect to port 22" in str(e):
            print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
            write(drive.strip('\\') + '\\' + logfile,"PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22")
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22")

        else:
            print "PRE:F: " + str(e)
            write(drive.strip('\\') + '\\' + logfile,"PRE:F: " + str(e))
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F: " + str(e))
