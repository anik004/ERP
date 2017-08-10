import subprocess
import itertools
import paramiko
from paramiko import *
command='date'
command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
date, err = command.communicate()
date = 'Thu Sep 22 12:31:10 2016'
date = 'Thu Sep 22 08:00:41 2016'
date=date.split(' ')
print date
del date[4:6]
datetime = date
print datetime
#date=' '.join(date)
matchdate = date[3].split(':')
print matchdate
matchhour=matchdate[0].strip()
matchminuite=matchdate[1].strip()
lastminuite=int(matchminuite)%10
firstminuite=(int(matchminuite)-int(lastminuite))/10
matchsecond=matchdate[2].strip()

del date[3]
matchdate1=' '.join(date)
print matchdate1
matchdatefinal = matchdate1 + ' ' + matchdate[0] + ':'
print matchdatefinal
command = 'grep -n "' + matchdatefinal + '[0-' + str(firstminuite) +'][0-' + str(lastminuite) + ']" Alertlog.txt'
print command
#command='cat Alertlog.txt | grep -n \'' + matchdate + '*\''
command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
out, err = command.communicate()
print out
if out:
#	print out
	out = out.split('\n')
	for i in reversed(out):
		if i != '':
			i=i.split(':',1)
			x = i[1].split(' ')
			y = x[3].split(':')
			#print i[1]
			if y[1].strip() == matchminuite:
				if y[2].strip() < matchsecond:
			#		print "matchsecond" + matchsecond
			#		print y[2]
                     			line = int(i[0])
					break
				else:
					continue
			elif y[1].strip() < matchminuite: 
			#	print "matchminuite" + matchminuite
			#	print y[1]
				line = int(i[0])
				break
			else:
				continue
else:
#	print "else"
#	print matchhour
	matchhour=int(matchhour)-1
	matchhour="{0:0=2d}".format(matchhour)
	matchdatefinal = matchdate1 + ' ' + str(matchhour) + ':'
	command='grep -n "' + matchdatefinal + '*" Alertlog.txt | tail -n 1'
	print command 
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	out, err = command.communicate()
	print out
	print type(out)
	out = out.split(':',1)
	print out
	line = int(out[0])
	print line
	print "line"

line = line + 1
#print line
command='wc -l Alertlog.txt'
print command
command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
count, err = command.communicate()
count = count.split(' ')
count = int(count[0])
print count
print "count" 
hostname="sapredhat01"
username="qrpadm"
password="Welcome2"
client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect( hostname,username = username, password = password)
channel = client.invoke_shell()
sftp_client = client.open_sftp()
for row in reversed(sftp_client.open("Alertlog.txt").readlines()):
#for i, line in reversed(enumerate(fp)):
    #for num, line in enumerate(myFile, 1):
	if count<=line:
        	if "LGWR switch" in row.rstrip():
            		row = row.rstrip().split(' ')
            		print row[6]
            		#print num
           		break
	count=count-1
#command='sed -n \'' + str(count -1 ) + 'p\' Alertlog.txt'
#command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#date, err = command.communicate()
#print date
