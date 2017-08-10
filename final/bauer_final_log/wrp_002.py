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
	path = argv[7].strip('\\') + '\\'
	os_name = argv[8]
	db_name = argv[9]

	if app_db.lower() == 'db' and db_name.lower() != 'mss':
		db_username = argv[10]
		db_password = argv[11]
#		s_hostname = argv[12]
#		s_username = argv[13]
#		s_password = argv[14]
#		s_db_sid = argv[15]

	string = 'target'
	

	#################### WINDOWS #################
	if os_name.lower() == 'windows':
	##############################################

		write('reflogfile.log',"wrp_002:This command calls the win00 script")
		command = 'c:\python27\python.exe ' + path + 'win00 ' + hostname
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()

#		write('reflogfile.log',"wrp_002:This command calls the win01 script")
#		command = 'c:\python27\python.exe ' + path + 'win01 ' + hostname + ' ' + username + ' ' + password + ' ' + app_sid + ' ' + s_hostname + ' ' + s_username + ' ' + s_password + ' ' + s_db_sid
#		write('reflogfile.log',command)
#		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#		out, err = command.communicate()
#		print out.strip()

		write('reflogfile.log',"wrp_002:This command calls the lin03 script")
		command = 'c:\python27\python.exe ' + path + 'lin03 ' + hostname + ' ' + string
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()

		write('reflogfile.log',"wrp_002:This command calls the win03 script")
		command = 'c:\python27\python.exe ' + path + 'win03 ' + hostname + ' ' + username + ' ' + password + ' ' + path
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()

		##################### CONNECT FOR DB ###############
		if app_db.lower() == 'db':
		####################################################

			command = path ############ dummy for indentation
#			command = 'c:\python27\python.exe ' + path + 'lin03 ' + s_hostname + ' ' + string
#			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#			out, err = command.communicate()
#			print out.strip()

		################ FOR APP ##################
                elif app_db.lower() == 'ai' or app_db.lower() == 'ci':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the win03 script")
			command = 'c:\python27\python.exe ' + path + 'win03 ' + hostname + ' ' + username + ' ' + password + ' ' + path
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

		################ FOR ORA ##################
                elif app_db.lower() == 'db' and db_name.lower() == 'ora':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the win03 script")
			command = 'c:\python27\python.exe ' + path + 'win03 ' + hostname + ' ' + username + ' ' + password + ' ' + path
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

			write('reflogfile.log',"wrp_002:This command calls the win04 script")
			command = 'c:\python27\python.exe ' + path + 'win04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + db_username + ' ' + db_password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR DB2 ##################
                elif app_db.lower() == 'db' and db_name.lower() == 'db6':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the win05 script")
			command = 'c:\python27\python.exe ' + path + 'win05 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR MAXDB ################
                elif app_db.lower() == 'db' and db_name.lower() == 'ada':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the win06 script")
			command = 'c:\python27\python.exe ' + path + 'win06 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR SYBASE ###############
                elif app_db.lower() == 'db' and db_name.lower() == 'syb':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the win07 script")
			command = 'c:\python27\python.exe ' + path + 'win07 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


		################ FOR MSSQL ################
                elif app_db.lower() == 'db' and db_name.lower() == 'mss':
                ###########################################

			print 'mss'
			command = 'dummy'
#			command = 'c:\python27\python.exe ' + path + 'win08 '
#                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#                        out, err = command.communicate()
#                        print out.strip()


	################## LINUX ####################
	else:
	#############################################

		write('reflogfile.log',"wrp_002:This command calls the lin01 script")
		command = 'python ' + path + '/lin01 ' + hostname
		write('reflogfiel.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()

		################### AIX ##############
		if os_name == 'aix':
		######################################
			
			command = 'dummy' ############# dummy for indentation
#			command = 'python ' + path + '\\ax02 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + s_hostname + ' ' + s_username + ' ' + s_password + ' ' + s_db_sid
#			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#			out, err = command.communicate()
#			print out.strip()

		################# LINUX #############
		else:
		#####################################

			command = 'dummy' ############ dummy for indentation
#			command = 'python ' + path + '\\lin02 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + s_hostname + ' ' + s_username + ' ' + s_password + ' ' + s_db_sid
#			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#			out, err = command.communicate()
#			print out.strip()

		write('reflogfile.log',"wrp_002:This command calls the lin03 script")
		command = 'python ' + path + '/lin03 ' + hostname + ' ' + 'target'
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out.strip()

#		command = 'python ' + path + '\\lin03 ' + s_hostname + ' ' + 'source'
#		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#		out, err = command.communicate()
#		print out.strip()
		
		################# FOR APP #################
		if app_db.lower() == 'ai' or app_db.lower() == 'ci':
		###########################################

			write('reflogfile.log',"wrp_002:This command calls the lin04 script")
			command = 'python ' + path + '/lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + app_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_002:This command calls the lin09 script")
			command = 'python ' + path + '/lin09 ' + hostname + ' ' + username + ' ' + password + ' ' + app_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

		################ FOR ORA ##################
		elif app_db.lower() == 'db' and db_name.lower() == 'ora':
		###########################################

			write('reflogfile.log',"wrp_002:This command calls the lin04 script")
			command = 'python ' + path + '/lin04 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_002:This command calls the lin10 script")
			command = 'python ' + path + '/lin10 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + db_username + ' ' + db_password
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()
			
			write('reflogfile.log',"wrp_002:This command calls the lin05 script")
			command = 'python ' + path + '/lin05 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()

			write('reflogfile.log',"wrp_002:This command calls the lin09 script")
			command = 'python ' + path + '/lin09 ' + hostname + ' ' + username + ' ' + password + ' ' + db_sid + ' ' + app_db
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out.strip()


                ################ FOR MAXDB ################
                elif app_db.lower() == 'db' and db_name.lower() == 'ada':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the lin11 script")
                        command = 'python ' + path + '/lin11 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


                ################ FOR DB2 ##################
                elif app_db.lower() == 'db' and db_name.lower() == 'db6':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the lin12 script")
                        command = 'python ' + path + '/lin12 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()


                ################ FOR SYBASE ###############
                elif app_db.lower() == 'db' and db_name.lower() == 'syb':
                ###########################################

			write('reflogfile.log',"wrp_002:This command calls the lin14 script")
                        command = 'python ' + path + '/lin14 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

		############## SUSE ######################
		elif app_db.lower() == 'db' and os_name.lower() == 'suse linux' and db_name.lower() == 'hdb':
		##########################################

			write('reflogfile.log',"wrp_002:This command calls the lin15 script")
                        command = 'python ' + path + '/lin15 '
			write('reflogfile.log',command)
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out.strip()

		############## SUSE ######################
		else:
		##########################################
			
			print "PRE:F:The OS and Database combination " + os_name.lower() + ' and ' + db_name.lower() + " is wrongly entered"
		write('reflogfile.log',"wrp_002:This command calls the lin08 script")
		command = 'python ' + path + '/lin08 ' + hostname + ' ' + username + ' ' + password
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
	write('reflogfile.log', "PRE:F: " + str(e))
