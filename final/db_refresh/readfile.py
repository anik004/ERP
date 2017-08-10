import subprocess
import re
import itertools
import paramiko
from paramiko import *
from sys import *

hostname=argv[1]
username=argv[2]
password=argv[3]
s_dbsid = argv[4]

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname,username = username, password = password)
channel = client.invoke_shell()

sftp_client = client.open_sftp()
command = '/oracle/' + s_dbsid.upper() + '/saptrace/diag/rdbms/' + s_dbsid.lower() + '/' + s_dbsid.upper() + '/trace/alert_' + s_dbsid.upper() + '.log'
remote_file = sftp_client.open(command)
remote_file = list(remote_file)
#print remote_file
for line in reversed(remote_file):
	#print line
	if "LGWR switch" in line.rstrip():
		line = line.rstrip().split(' ')
		print line[6]
		exit()
#with reversed(open("/oracle/DSO/saptrace/diag/rdbms/dso/DSO/trace/alert_DSO.log")) as myFile:
#for line in reversed(open("/oracle/DSO/saptrace/diag/rdbms/dso/DSO/trace/alert_DSO.log").readlines()):
#for i, line in reversed(enumerate(fp)):
    #for num, line in enumerate(myFile, 1):
#        if "LGWR switch" in line.rstrip():
	    #print line
	    #print line.rstrip()
#            line = line.rstrip().split(' ')
#	    print line[6]
	   # print num
#	    exit()
