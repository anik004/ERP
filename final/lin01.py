import subprocess
from sys import *
import log4erp
from log4erp import *

try:
	if argv[1] == "--u":
		print "usage: ip_check.py <target hostname>"
	else:
		hostname = argv[1]
		command = 'ping -c 1 ' + hostname + ' 2> /dev/null | head -n 1 | cut -d" " -f3'
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		if out:
			print "PRE:P:The Source IP is- " + (out.strip().replace("(","")).replace(")","")
		else:
			print "PRE:F:not able to resolve hostname"
except Exception as e:
	if "unknown host" in str(e):
		print "PRE:F: Unknown Host"
	elif str(e) == "list index out of range":
		print "PRE:F: Argument/s missing"
	else:
		print "PRE:F: Script has exited with the error: " + str(e)
