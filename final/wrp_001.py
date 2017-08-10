from os import *
from sys import *
from subprocess import *
import subprocess
from log4erp import *


try:
	hostname = argv[1]
	username = argv[2]
	password = argv[3]
	app_sid = argv[4]
	db_sid = argv[5]
	app_db = argv[6]
	os_name = argv[7]
	db_name = argv[8]
	#db_username = argv[9]
	#db_password = argv[10]
	string = 'target'
	location = argv[11]


	#################### WINDOWS #################
	if os_name.lower() == 'windows on ia64' or os_name.lower() == 'windows on x64':
	##############################################

		write('reflogfile.log',"wrp_001:This command calls the lin03 script")
		command = 'c:\python27\python ' + location.strip('\\') + '\lin03 ' + hostname + ' ' + string
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()
		
		#################### FOR APP ##################
		if app_db.lower() == 'ai' or app_db.lower() == 'ci':
		###############################################

			write('reflogfile.log',"wrp_001:This command calls the win03 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win03 ' + hostname + ' ' + username + ' ' + password
			write('reflogfile.log',command)
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

		################ FOR ORA ##################
                elif app_db.lower() == 'db' and db_name.lower() == 'ora':
                ###########################################

			write('reflogfile.log',"wrp_001:This command calls the win03 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win03 ' + hostname + ' ' + username + ' ' + password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the win04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR DB2 ##################
                elif app_db.lower() == 'db' and db_name.lower() == 'db6':
                ###########################################

			write('reflogfile.log',"wrp_001:This command calls the win03 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win03 ' + hostname + ' ' + username + ' ' + password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the win05 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win05 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR MAXDB ################
                elif app_db.lower() == 'db' and db_name.lower() == 'ada':
                ###########################################

			write('reflogfile.log',"wrp_001:This command calls the win06 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win06 ' + hostname + ' ' + username + ' ' + password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the win04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR SYBASE ###############
                elif app_db.lower() == 'db' and db_name.lower() == 'syb':
                ###########################################

			write('reflogfile.log',"wrp_001:This command calls the win07 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win07 ' + hostname + ' ' + username + ' ' + password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the win04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR MSSQL ################
                elif app_db.lower() == 'db' and db_name.lower() == 'mss':
                ###########################################

			write('reflogfile.log',"wrp_001:This command calls the win08 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win08 ' + hostname + ' ' + username + ' ' + password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the win04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


	################## LINUX ####################
	else:
	#############################################

		write('reflogfile.log',"wrp_001:This command calls the lin03 script")
		command = 'c:\python27\python ' + location.strip('\\') + '\lin03 ' + hostname + ' ' + string
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()

		################# FOR APP #################
		if app_db.lower() == 'ai' or app_db.lower() == 'ci':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + app_sid + ' ' + 'app'
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

		################ FOR ORA ##################
		if app_db.lower() == 'db' and db_name.lower() == 'ora':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the lin10 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin10 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


		################ FOR MAXDB ################
		if app_db.lower() == 'db' and db_name.lower() == 'ada':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the lin11 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin11 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


		################ FOR DB2 ##################
		if app_db.lower() == 'db' and db_name.lower() == 'db6':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the lin12 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin12 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


		################ FOR MSSQL ################
		if app_db.lower() == 'db' and db_name.lower() == 'mss':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the lin13 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin13 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


		################ FOR SYBASE ###############
		if app_db.lower() == 'db' and db_name.lower() == 'syb':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the lin14 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin14 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


		################ FOR HANA #################
		if app_db.lower() == 'db' and db_name.lower() == 'hdb':
		###########################################

			write('reflogfile.log',"wrp_001:This command calls the lin04 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_001:This command calls the lin15 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\lin15 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + argv[9] + ' ' + argv[10]
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


################# ERROR ##################
except Exception as e:
##########################################
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_0201:Hostname unknown"
	write('reflogfile.log',"PRE:F:GERR_0201:Hostname unknown")
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_0202:Argument/s missing for the script"
	write('reflogfile.log',"PRE:F:GERR_0202:Argument/s missing for the script")
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_0203:Authentication failed."
	write('reflogfile.log',"PRE:F:GERR_0203:Authentication failed.")
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_0204:Host Unreachable"
	write('reflogfile.log',"PRE:F:GERR_0204:Host Unreachable")
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0205: Please check the hostname that you have provide"
	write('reflogfile.log',"PRE:F:GERR_0205: Please check the hostname that you have provide")
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
	write('reflogfile.log',"PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22")
    else:
        print "PRE:F: " + str(e)
	write('reflogfile.log',"PRE:F: " + str(e))
