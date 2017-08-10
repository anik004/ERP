import os
import sys
import subprocess

command = 'ls'
command = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
out, err = command.communicate()

for each in out.split('\n'):
	if each != 'wmiexec.py' and each != 'log4erp.pyc' and each != '' and each != 'encr.py':
		command = 'cxfreeze --no-copy-deps  --target-name=' + each.split('.')[0] + ' ' + each
		print command
		command = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
