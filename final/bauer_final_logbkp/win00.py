import subprocess
from sys import *
from log4erp import *

try:
#	logfile = argv[2]
	if argv[1] == "--u":
		print "usage: ip_check.py <target hostname> <Target/Source>"
	
	else:		
		hostname = argv[1]
		print hostname
#		'reflogfile.log' = argv[2]
		command = ''
#		ref_id = argv[2]
		write('reflogfile.log',"This command is used to ping the Host")
		command = 'ping -n 1 ' + hostname
		print command
		write('reflogfile.log',command)
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out
		write('reflogfile.log',out)
		if out:
			print "PRE:P:The IP of the target is- " + str(out.split('\r\n')[2].split(" ")[2][:-1])
			#print "success"
		else:
			print "PRE:F:The hostname is not able to resolve"

except Exception as e:
	if "unknown host" in str(e):
		print "PRE:F: Unknown Host"
	elif str(e) == "list index out of range":
		print "PRE:F: Argument/s missing"
	else:
		print "PRE:F: Script has exited with the error: " + str(e)
