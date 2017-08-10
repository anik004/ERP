import subprocess
import re
import itertools
import paramiko
from paramiko import *
from sys import *

hostname=argv[1]
username=argv[2]
password=argv[3]
dbsid=argv[4]
db_user = "ora" + dbsid.lower()

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname,username = username, password = password)
channel = client.invoke_shell()

command = "whoami"
command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
out, err = command.communicate()
directory = out.strip()
print directory

for line in (open("/home/" + directory + "/geminyo/enexis/date.txt").readlines()):
	#print line
	break
		
date = "" + line.strip() + ""
#print date

date=date.split(' ')
#print date

del date[4:6]
datetime = date
#print datetime

matchdate = date[3].split(':')
#print matchdate

matchhour=matchdate[0].strip()
matchminuite=matchdate[1].strip()
lastminuite=int(matchminuite)%10
firstminuite=(int(matchminuite)-int(lastminuite))/10
matchsecond=matchdate[2].strip()

command = "sudo su - " + db_user + " -c \"echo \'select value from v\$parameter where name='\'\'background_dump_dest\'\'';' | sqlplus / as sysdba\""
print command
stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
alert_path = stdout.readlines()
print alert_path

del date[3]

matchdate1=' '.join(date)
#print matchdate1
matchdatefinal = matchdate1 + ' ' + matchdate[0] + ':'
#print "matchdatefinal"
#print matchdatefinal
command = 'grep -n --color=never "' + matchdatefinal + '[0-' + str(firstminuite) +'][0-' + str(lastminuite) + ']" /oracle/' + dbsid.upper() + '/saptrace/diag/rdbms/' + dbsid.lower() + '/' + dbsid.upper() + '/trace/alert_' + dbsid.upper() + '.log'
stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
out1 = stdout.readlines()
#print out1
out=''.join(out1)
#print len(out1)

if len(out1) > 1:
	out = out.split('\n')
	for i in reversed(out):
		if i != '':
#			print "i" + i
			i=i.split(':',1)
			x = i[1].split(' ')
			y = x[3].split(':')
#			print x
#			print y[2]
			if y[1].strip() == matchminuite:
#				print "match min"
#				print matchsecond
				if y[2].strip() < matchsecond:
#					print "matchsecond" + matchsecond
			#		print y[2]
                     			line = int(i[0])
				#	print line
				#	print "line11"
					break
				else:
					line = int(i[0])
        	                        break	
			
			elif y[1].strip() < matchminuite: 
				line = int(i[0])
				break
			else:
#				print "continue"
				continue
else:
#	print "else"
#	print matchhour
	matchhour=int(matchhour)-1
	matchhour="{0:0=2d}".format(matchhour)
	matchdatefinal = matchdate1 + ' ' + str(matchhour) + ':'
	command='grep -n "' + matchdatefinal + '*" /oracle/' + dbsid.upper() + '/saptrace/diag/rdbms/' + dbsid.lower() + '/' + dbsid.upper() + '/trace/alert_' + dbsid.upper() + '.log | tail -n 1'
#	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	out = ''.join(stdout.readlines())
	out = out.split(':',1)
#	print out
	line = int(out[0])
#	print "line"


line = int(line) + 1
#print line
command='wc -l /oracle/' + dbsid.upper() + '/saptrace/diag/rdbms/' + dbsid.lower() + '/' + dbsid.upper() + '/trace/alert_' + dbsid.upper() + '.log'
#print command
stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
count = ''.join(stdout.readlines())
count = count.split(' ')
count = int(count[0])
#print count
#print "count"

sftp_client = client.open_sftp()
for row in reversed(sftp_client.open("/oracle/" + dbsid.upper() + "/saptrace/diag/rdbms/" + dbsid.lower() + "/" + dbsid.upper() + "/trace/alert_" + dbsid.upper() + ".log").readlines()):
	if count<=line:
        	if "LGWR switch" in row.rstrip():
            		row = row.rstrip().split(' ')
            		print row[6]
           		break
	count=count-1
#command='sed -n \'' + str(count -1 ) + 'p\' /oracle/DQR/saptrace/diag/rdbms/dqr/DQR/trace/alert_DQR.log'
#command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#date, err = command.communicate()
#print date
