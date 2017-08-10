from sys import argv
import subprocess
import os
from log4erp import *

try:
	if argv[1] == '--ani':
		print "usage"
	else:
		#----------------------- variable declaration --------------------
		hostname = argv[1]
		username = argv[2]
		password = argv[3]
		sid = argv[4]
		al11 = argv[5]
		location = al11.strip('\\')
		final_table = []
		logfile = argv[6]
		db_name = argv[7]
		# ---------------------------- Create File --------------------------
		file_open = open(al11.strip() + "\\" + logfile + "_bdls.txt", 'w')
		file_sql = open(al11.strip() + "\\" + logfile + "_sql.sql", 'w')
		file_sql.write ('use ' + sid.upper() + '\n')
		"""
		# ------------------------ get hostname ----------------------------
		command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname.strip() + ' "hostname"'
        command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out, err = command.communicate()
		domain_name = out.split('\n')[2]
		"""
		domain_name = hostname.strip()
		# ---------------------- get schema name ----------------------------
		write(location + '\\reflogfile.log', "win25 : this command is used to get the schema name")
		command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + db_name.upper() + '; select  TOP 1 TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES\\""'
		print command
		write(location + '\\reflogfile.log',command)
		command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		#print out
		write(location + '\\reflogfile.log',out)
		schema = out.split('\n')[5].strip()

		#print schema
        if schema:
	# ----------------------- get table names ---------------------------
			write(location + '\\reflogfile.log', "win25 : this command is used to get the table names")
			command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + db_name.upper() + '; select b.TABNAME, FIELDNAME from ' + schema + '.DD03L as a INNER JOIN ' + schema + '.DD02L as b on a.TABNAME = b.TABNAME where a.DOMNAME = \'LOGSYS\' and b.TABCLASS = \'TRANSP\'\\"\"'
			print command
			write(location + '\\reflogfile.log',command)
			command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			out, err = command.communicate()
			write(location + '\\reflogfile.log',out)
			#print out
			if command.returncode == 0 or command.returncode.returncode == 4:
				table_list = out.split('\n')[6:]
				#print table_list
                # ------------------------- Unique names -----------------------------
				for each in table_list:
					if each.strip() and '(' not in each:
						#print each
						table=each.split()[0]
						file_open.write(table + '\n')
				file_open.close()
			# ---------------------------- each table ----------------------------
                        #print table_list
				for each in table_list:
					#print each
					if len(each.split()) != 0 and 'rows affected' not in each:
						table_name = each.split()[0]
						field_name = each.split()[1]
						if '/' not in table_name and '/' not in field_name:
							file_sql.write ('create index ' + table_name + '_' + field_name + ' on ' + schema + '.' + table_name + '(' + field_name + ')\n')
#                           command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname.strip() + ' "sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + sid.upper() + '; create index ' + table_name + '_' + field_name + ' on ' + schema + '.' + table_name + '(' + field_name + ')"'
				file_sql.write ('go')
				file_sql.close()
				write(location + '\\reflogfile.log',"win25 : this command is used to copy files to share folder")
				command = 'copy ' + logfile + '_sql.sql' + ' \\\\' + hostname + '\\sharename'
				#print command
				write(location + '\\reflogfile.log',command)
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
				out, err = command.communicate()
				write(location + '\\reflogfile.log',out)
				write(location + '\\reflogfile.log','win25 : this command is used to execute the SQL query')
				command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname.strip() + ' "sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -i ' + location.strip()[:2] + "\\erp_trans\\" + logfile + "_sql.sql\""
				print command
				write(location + '\\reflogfile.log',command)
				command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
				out, err = command.communicate()
				write(location + '\\reflogfile.log',out)
				status = command.returncode
				if status == 0 or status == 4:
					print "POST:P:The indexes has been created successfully for the tables"
					write (location + '\\' + logfile, "POST:P:The indexes has been created successfully for the table " + table_name)
				else:
					print "POST:F:The index creation has been failed for the tables"
					write (location + '\\' + logfile, "POST:P:The indexes has failed for the table " + table_name)
			
			else:
				print "POST:F:The table list has not been fetched successfully"
				write (location + '\\' + logfile,  "POST:F:The table list has not been fetched successfully")
# ---------------------------- Exceptions ------------------------------------
except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
		print "POST:F:GERR_0201:Hostname unknown"
		write(location + '\\' + logfile, 'POST:F:GERR_0201:Hostname unknown')
		write(location + '\\reflogfile.log','POST:F:GERR_0201:Hostname unknown')
	elif str(e).strip() == "list index out of range":
		print "POST:F:GERR_0202:Argument/s missing for the script"
		write(location + '\\reflogfile.log','POST:F:GERR_0202:Argument/s missing for the script')
	elif str(e) == "Authentication failed.":
		print "POST:F:GERR_0203:Authentication failed."
		write(location + '\\' + logfile, 'POST:F:GERR_0203:Authentication failed.')
		write(location + '\\reflogfile.log','POST:F:GERR_0203:Authentication failed.')
	elif str(e) == "[Errno 110] Connection timed out":
		print "POST:F:GERR_0204:Host Unreachable"
		write(location + '\\' + logfile, 'POST:F:GERR_0204:Host Unreachable')
		write(location + '\\reflogfile.log','POST:F:GERR_0204:Host Unreachable')
	elif "getaddrinfo failed" in str(e):
		print "POST:F:GERR_0205: Please check the hostname that you have provide"
		write(location + '\\' + logfile, 'POST:F:GERR_0205: Please check the hostname that you have provide')
	elif "[Errno None] Unable to connect to port 22 on" in str(e):
		print "POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
		write(location + '\\' + logfile, 'POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
		write(location + '\\reflogfile.log','POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	else:
		print "POST:F: " + str(e)
		write(location + '\\reflogfile.log',"POST:F: " + str(e))
		write(location + '\\' + logfile,  "POST:F: " + str(e))
