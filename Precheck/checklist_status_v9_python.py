# ------------------- importing module --------------------------
import os
import sys
from sys import *
import subprocess
import platform

# -------------------- OS name -----------------------------------
os_name = os.name

try:
# ---------------------- Log4erp and paramiko --------------------
	import log4erp

# ------------------- Variable Mapping ---------------------------
	app_sid = argv[1]
	l_user = argv[2]
	t_host = argv[3]
	t_user = argv[4]
	t_passwd = argv[5]
	t_sid = argv[6]
	solution = argv[7].lower()
#	epi = argv[8]
	l_sidadm = app_sid.lower() + 'adm'
	t_sidadm = t_sid.lower() + 'adm'

# --------------------- Check Python Existance -------------------
	command = 'echo "exit()" | python'
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
	status = command.returncode

	if status != 0:
		print 'chk:python:f: Python is not installed in the Solution manager System'
		exit()

		
# ------------------ Set the target platform ----------------------
	if os_name == 'posix':
###################################################################
# ------------------------- for Unix -----------------------------#
###################################################################
		import paramiko
	        from paramiko import *
	        import md5
	        import Crypto
           	import  hashlib

# ------------------------- check paramiko -----------------------
		client = SSHClient()
	        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	client.connect(t_host, username = t_user, password = t_passwd)
	        channel = client.invoke_shell()
		command = 'whoami'
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		output = stdout.readlines()
		output = ''.join(output)
		#print output
		if output.strip() == t_user:
			print 'chk:paramiko:p:Paramiko is already installed'
		elif stderr.readlines():
			print 'chk:paramiko:f:Paramiko is not installed correctly and it has exited with the error: ' + str(stderr.readlines())
		else:
			print 'chk:paramiko:f:Paramiko is not installed correctly'

# ---------------------- check folder existance ------------------
		
		gem_path = os.path.isdir('/home/' + app_sid.lower() + 'adm/geminyo')
		gem_path_p = '/home/' + app_sid.lower() + 'adm/geminyo'
		gem_sc_path = os.path.isdir('/home/' + app_sid.lower() + 'adm/geminyo/scripts')
		gem_sc_path_p = '/home/' + app_sid.lower() + 'adm/geminyo/scripts'
		epi_path = os.path.isdir('/home/' + app_sid.lower() + 'adm/episky')
		epi_path_p = '/home/' + app_sid.lower() + 'adm/episky'
		epi_sc_path = os.path.isdir('/home/' + app_sid.lower() + 'adm/episky/scripts')
		epi_sc_path_p = '/home/' + app_sid.lower() + 'adm/episky/scripts'
		kry_path = os.path.isdir('/home/' + app_sid.lower() + 'adm/kryptex')
		kry_path_p = '/home/' + app_sid.lower() + 'adm/kryptex'
		kry_sc_path = os.path.isdir('/home/' + app_sid.lower() + 'adm/kryptex/scripts')
		kry_sc_path_p = '/home/' + app_sid.lower() + 'adm/kryptex/scripts'
		if solution.strip() == 'geminyo':
			if gem_path == True and gem_sc_path == True and kry_path == True and kry_sc_path == True:
				print 'chk:folder_structure:p:The folder strcture is created properly for Geminyo'
###################################################################################################
# ------------------ Folder permission ---------------------------
				command = 'stat -c %a ' + gem_path_p
		        	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        			out_gem_path, err = command.communicate()
				#print out_gem_path
				command = 'stat -c %a ' + gem_sc_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_gem_sc_path, err = command.communicate()
				#print out_gem_sc_path
                                command = 'stat -c %a ' + kry_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_kry_path, err = command.communicate()
				#print out_kry_path
                                command = 'stat -c %a ' + kry_sc_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_kry_sc_path, err = command.communicate()
				#print out_kry_sc_path
				if out_gem_path.strip() != '777' or out_gem_sc_path.strip() != '777' or out_kry_path.strip() != '777' or out_kry_sc_path.strip() != '777':
					print 'chk:folder_permission:f:The permission of the script location is not 777'
				else:
					print 'chk:folder_permission:p:The permission for the script location is proper'
######################################################################################################
		elif solution.strip() == 'episky':
                        if epi_path == True and epi_sc_path == True and kry_path == True and kry_sc_path == True:
                                print 'chk:folder_structure:p:The folder strcture created properly for Episky'
######################################################################################################
# ------------------ Folder permission ---------------------------
                                command = 'stat -c %a ' + epi_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_epi_path, err = command.communicate()
                                command = 'stat -c %a ' + epi_sc_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_epi_sc_path, err = command.communicate()
                                command = 'stat -c %a ' + kry_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_kry_path, err = command.communicate()
                                command = 'stat -c %a ' + kry_sc_path_p
                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                out_kry_sc_path, err = command.communicate()
                                if out_epi_path.strip() != '777' or out_epi_sc_path.strip() != '777' or out_kry_path.strip() != '777' or out_kry_sc_path.strip() != '777':
                                        print 'chk:folder_permission:f:The permission of the script location is not 777'
                                else:
                                        print 'chk:folder_permission:p:The permission for the script location is proper'
########################################################################################################
		else:
			print 'chk:folder_structure:f:The folder structure has not been created properly'

# --------------------- connectivity check -----------------------
		command = 'whereis ping'
	        command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        	out, err = command.communicate()
	        pingpath = (str(out).split()[1]).strip()
		print pingpath

		command = pingpath + " -c1 " + str(t_host) + " > /dev/null 2>&1"
                response = os.system(command)
		if response == 0:
			print "chk:connectivity:p:The connectivity check for Target Server (Hostname: " + t_host + ") is Successful"
		else:
			print "chk:connectivity:f:Please check the IP address, Unable to reach the Host (Hostname: " + t_host + ")"

# ---------------- local check sudo access ------------------------
		command = "echo \"whoami\" | sudo bash"
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out
		if out.strip() == "root" :
			print 'chk:sudo_access:p:Sudo access check to for sudo user ' + l_user + ' is Successful on SOLMAN system'
		elif err:
			print 'chk:sudo_access:f:Sudo access check to for sudo user ' + l_user + ' has failed on SOLMAN system with the error: ' + str(err)
		else:
			print 'chk:sudo_access:f:Sudo access check to for sudo user ' + l_user + ' has failed on SOLMAN system'

# -------------------  check sudo access -------------------------
		command = "echo \"su - " + t_sidadm + " -c \\\" whoami \\\"\" | sudo bash"
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		output = ''.join(stdout.readlines())
                if output.strip() == t_sidadm:
			print 'chk:sudo_access:p:Sudo access check to for sudo user ' + t_user + ' is Successful on target system'
		else:
			print 'chk:sudo_access:f:Sudo access check to for sudo user ' + t_user + ' has failed on target system'

# ------------------------ Python version -------------------------
	        req_version = (2.7)
	        cur_version = sys.version

        	if str(req_version) in str(cur_version):
			print 'chk:python_version:p:The installed python is having proper  version'
		else:
			print 'chk:python_version:f:The installed python version is lesser that 2.7'

# ------------------------ Home Directory check -------------------
		command = 'sudo su - ' + t_sidadm + ' -c "getent passwd \\"' + t_sidadm + '\\""'
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = str(stdout.readlines()).split(':')
		if output:
			print 'chk:home_folder:p:The user ' + t_sidadm + ' has proper home folder'
		else:
			print 'chk:home_folder:f:The user ' + t_sidadm + ' does not have proper home folder'

# -------------------------- OS version check ----------------------
	        os_name = platform.system()
	        os_version = platform.release()
	        version = float(os_version.split('-')[0].split('.')[0] + '.' + os_version.split('-')[0].split('.')[1])
		if os_name == 'AIX' and version > 6.1:
			print 'chk:os_version:f:The check has failed as the OS version is AIX and the version is greater than 6.1'
		else:
			print 'chk:os_version:p:the OS check has been passed'


# -------------------- /usr/sap permission check ----------------------------
		folder_exist = os.path.isdir('/usr/sap')
       		if folder_exist == True:
	                command = 'stat -c "%a" /usr/sap'
               		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	                perm = stdout.readlines()[0]
               		if int(perm.strip()) <= 755:
                       		print 'chk:/usr/sap:p:The /usr/sap folder has proper permission'
	                else:
                       		print 'chk:/usr/sap:f:The /usr/sap/ folder does not have proper permission'

# ------------------------ SAP User check -----------------------------
		command = 'whoami'
		command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		output = out
		print output
		if output.strip() != l_sidadm:
			print 'chk:UserDetails:f:The tool has logged in as ' + output.strip() + ' user. Please check if all the permissions are given to the user'
		else:
			print 'chk:UserDetails:p:The tool has logged in as ' + l_sidadm + ' user successfully'

# --------------------- Geminyo Check -------------------------------
		if solution.strip() == 'geminyo':

#-------------------------- DIR_TRANS value -------------------------
			prof_path = argv[9]
			command = 'cd ' + prof_path
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			stdout = stdout.read()
			if "No such file or directory" not in stdout:
	        	        command = 'ls  ' + prof_path.strip() + ' | grep -i ' + t_sid.upper() + '_DVEBMGS| grep -v \'\.\''
	        	        #rint command
		                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
				#print stdout.readlines()
        		        profile = stdout.readlines()[0].strip()
				#print profile
                		command = "echo 'cat " + prof_path.strip() + "/"  + profile + " | grep -i DIR_TRANS' | sudo bash"
                		#print command
		                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        		        stdout = stdout.readlines()#[0].split()[8].strip()
	                	if stdout:
	                        	print 'chk:dir_trans:p:The DIR_TRANS entry is present in the instance profile'
	                	else:
	                        	print 'chk:dir_trans:f:The DIR_TRANS entry is not present in the instance profile'

#----------------------- trans local or shared -----------------------
			        command = 'ls -l ' + prof_path.strip() + ' | grep -i ' + t_sid.upper() + '_DVEBMGS'
			        #print command
	        		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		        	profile = stdout.readlines()[0].split()[8].strip()
		        	command = "echo 'cat " + prof_path.strip() + "/"  + profile + " | grep -i DIR_TRANS | grep -v \"#\"' | sudo bash"
		        	#print command
			        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	        		out = stdout.readlines()
			        file_path = str(str(str(str(out).split('=')[1])[:-2].strip()).replace('\\r\\n', ''))
	        		if '\\\\' in file_path[:2]:
	                		print 'chk:trans_dir:f:The trans directory is not local'

			        else:
	        		        print 'chk:trans_dir:p:The trans directory is local'
	        	else:
	                	print 'chk:profile:f:The profile folder does not exist on /sapmnt mountpoint'

#------------------------ TP profile --------------------------------
			trans_fol = "/usr/sap/trans/bin"

			command = "echo 'ls " + trans_fol + "' | sudo bash"
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			stdout = (stdout.read()).split()
			#print stdout

			prof = "TP_DOMAIN_" + t_sid.upper() + ".PFL"
			flag = 0

			for each in stdout:
			        if prof in each.strip():
			                command = "echo 'cat " + trans_fol + "/" + each + " | grep -i -e DIR_TRANS -e transdir | grep -v \"#\"' | sudo bash "

			                #print command
					stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			                stdout = stdout.readlines()
					#print stdout
			                flag = 1
			                if stdout:
			                        print 'chk:trans_dir:p:The TRANSDIR entry is present in the TP profile'
			                else:
	                       			print 'chk:trans_dir:f:The TRANSDIR entry is not present in the TP profile'

			if flag == 0:
			        print 'chk:trans_dir:f:STMS is not configured'


		client.close()
		channel.close()


	else:
###################################################################
# ----------------------------- for windows ----------------------#
###################################################################
# ---------------------- Script location -------------------------
#		import Crypto
#		location = raw_input("Enter the script location: ")
#		prof_drive = raw_input("Enter the profile drive: ")

		location = argv[8]
		prof_drive = argv[9]	
		loctn = location
# ----------------------- check folder existance -----------------
		gem_path = os.path.isdir(location[:2] + '\\geminyo')
		gem_sc_path = os.path.isdir(location[:2] + '\\geminyo\\scripts')
                epi_path = os.path.isdir(location[:2] + '\\episky')
                epi_sc_path = os.path.isdir(location[:2] + '\\episky\\scripts')
		kry_path = os.path.isdir(location[:2] + '\\kryptex')
                kry_sc_path = os.path.isdir(location[:2] + '\\kryptex\\scripts')
#		gem_path = os.path.isdir('c:\\' + app_sid + 'adm\\geminyo')
#                gem_sc_path = os.path.isdir('c:\\' + app_sid + 'adm\\geminyo\\scripts')
#                epi_path = os.path.isdir('c:\\' + app_sid + 'adm\\episky')
#                epi_sc_path = os.path.isdir('c:\\' + app_sid + 'adm\\episky\\scripts')

		if solution.strip() == "geminyo":
			location = loctn[:2] + '\\geminyo\\scripts'
			if gem_path == False or gem_sc_path == False or kry_path == False or kry_sc_path == False:
	                        print 'chk:folder_structure:f:The folder strcture is not created properly'
        	        else:
                	        print 'chk:folder_structure:p:The folder structure has been created properly'

		if solution.strip() == "episky":
			location = loctn[:2] + '\\episky\\scripts'
	                if epi_path == False or epi_sc_path == False or kry_path == False or kry_sc_path == False:
        	                print 'chk:folder_structure:f:The folder strcture is not created properly'
                	else:
                        	print 'chk:folder_structure:p:The folder structure has been created properly'

# ----------------------------- connectivity check --------------
		command = "ping -n 1 " + str(t_host) #+ " > /dev/null 2>&1"
                response = os.system(command)
		if response == 0:
                        print "chk:connectivity:p:The connectivity check for Target Server (Hostname: " + t_host + ") is Successful"
                else:
                        print "chk:connectivity:f:Please check the IP address, Unable to reach the Host (Hostname: " + t_host + ")"
# ------------------------------- Impacket ----------------------
                
		command = 'c:\\python27\\python ' + location.strip('\\') + '\wmiexec.py \"' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + '\" "exit"'
		#command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  '  exit'
                #command = 'python ' + location.strip('\\') + '\wmiexec.py ts6adm:Ts64n0w1@10.0.2.174 "ipconfig"'
		#print command
		#print type(t_user)
		command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		#response = os.system (command)
		#print out
	
		if command.returncode == 0:
			print 'chk:impacket:p:The impacket installation check in the solman system is successful'
		else:
			print 'chk:impacket:f:The impacket installation check in the solman system is failed'
# ------------------------ Python version -------------------------
                req_version = (2.7)
                cur_version = sys.version

                if str(req_version) in str(cur_version):
                        print 'chk:python_version:p:The installed python is having proper  version'
                else:
                        print 'chk:python_version:f:The installed python version is lesser that 2.7'


		if solution.strip().lower() == 'geminyo':
#-------------------------- DIR_TRANS value -------------------------
			#profile_path = prof_drive + '\\sapmnt\\' + t_sid.upper() + '\\profile'
                        profile_path = prof_drive + '\\usr\\sap\\' + t_sid.upper() + '\\SYS\\profile'
			#command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" dir ' + profile_path + '\"'
			command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" dir ' + profile_path + '\"'
	                command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	                out, err = command.communicate()
			if "File Not Found" not in out:
		        	#command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" dir ' + profile_path + ' |  findstr ' + app_sid.upper() + '_DVEBMGS\"'
				command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" dir ' + profile_path + ' |  findstr ' + t_sid.upper() + '_DVEBMGS\"'
				#print  command
				command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			        out, err = command.communicate()
			        out = (out.strip()).split('\n')
			   #     print out
		        	for each in out:
		               		b = t_host.upper() + "."
		               		flag = 0
			                if b not in each:
                          #                      print each
                                                flag = 1
	               			        each = each.split(" ")
		                	        each = filter(None,each)
	               		        	if len(each) == 5:
		                               		each = each[4]
			                                each = str(each).strip()
	               			                #command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" type ' + profile_path + '\\' + each +'|  findstr " DIR_TRANS\"'
							command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" type ' + profile_path + '\\' + each +'|  findstr " DIR_TRANS\"'
                                                        #print command
		                	                command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	               		        	        out, err = command.communicate()
	                               			if out:
			                                        print 'chk:dir_trans:p:The DIR_TRANS entry is present in the instance profile'
	        	       		                else:
	                	               		        print 'chk:dir_trans:f:The DIR_TRANS entry is not present in the instance profile'
                                        #else:
                                         #       print 'chk:dir_trans:f:The DIR_TRANS entry is not present in the instance profile'
	                	if flag != 0:
                                        print 'chk:dir_trans:f:The DIR_TRANS entry is not present in the instance profile'
#----------------------- trans local or shared -----------------------
			        #command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" dir ' + profile_path + ' |  findstr ' + app_sid.upper() + '_DVEBMGS\"'
				command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host +  ' \" dir ' + profile_path + ' |  findstr ' + t_sid.upper() + '_DVEBMGS\"'
			 #       print  command
	        		command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			        out, err = command.communicate()
	        		out = (out.strip()).split('\n')
	        	#	print out
	        		
		        	for each in out:
                                
	        	        	b = t_host.upper() + "."
	        	        
		                	if b not in each:
                          #                      print each
	        	                	each = each.split(" ")
		        	                each = filter(None,each)
		        	        
	        	        	        if len(each) == 5:
                                                
	                	        	        each = each[4]
	                        	        	each = str(each).strip()
		                                	#command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + ' \" type ' + profile_path + '\\' + each +'|  findstr " DIR_TRANS " | findstr -V "#\"'
							command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + ' \" type ' + profile_path + '\\' + each +'|  findstr " DIR_TRANS " | findstr -V "#\"'
			#				print command
			                                command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	        		                        out, err = command.communicate()
	                #		                print out
	                                		file_path = out.split("=")[1].strip()
		                                	#print out
		        #	                        #file_path = str(str(str(str(out).split('=')[1])[:-2].strip()).replace('\\r\\n', ''))
	        	 #       	                print file_path
	                	        	        if '\\\\' in file_path[:2]:
	                        	        	        print 'chk:trans:p:The TRANS is shared'
		                        	        else:
	        	                        	        print 'chk:trans:p:The TRANS is local'
			else:
        	                print 'chk:profile_folder:f:The profile folder does not exist on /sapmnt mountpoint'

#------------------------ TP profile --------------------------------
			trans_fol = prof_drive + "\\usr\\sap\\trans\\bin"

			#command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + '\"dir ' + prof_drive + '\"'
			command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + ' \"dir ' + trans_fol + '\"'
			command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			out, err = command.communicate()
			out = (out.strip()).split("\n")
			#print out

			prof = "TP_DOMAIN_" + t_sid + ".PFL"
			flag = 0

			for each in out:
			        if prof in each:
#	                		print each
			                each = (each.strip()).split()
	                		each = each[4]
			                #command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + '\"type ' + trans_fol + '/' + each + ' | findstr "TRANSDIR DIR_TRANS" | findstr /v "#" \"'
					command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + ' \"type ' + trans_fol + '/' + each + ' | findstr "TRANSDIR DIR_TRANS" | findstr /v "#" \"'
					
	                		command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			                out, err = command.communicate()
	                		flag = 1

			                if out:
	                		        print 'chk:trans_dir:p:The TRANSDIR entry is present in the TP profile'
			                else:
	                		        print 'chk:trans_dir:f:The TRANSDIR entry is not present in the TP profile'

			if flag == 0:
			        print 'chk:stms:f:STMS is not configured'

#------------------------------- Powershell ---------------------------
			#command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + '\"powershell.exe ; exit\"'
			command = 'python ' + location.strip('\\') + '\\wmiexec.py ' + t_user.strip() + ':' + t_passwd.strip() + '@' + t_host + ' \"powershell.exe ; exit\"'
			command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        #print out
			if "'powershell.exe' is not recognized as an internal or external command" in str(out):
				print "chk:powershell:f:Powershell is not recognized as an internal or external command"
			else:
				print "chk:powershell:p:Powershell is configured"



# ------------------------------- Exceptions --------------------
except Exception as e:
	exc_type, exc_obj, tb = sys.exc_info()
	lineno = str(tb.tb_lineno)
	if str(e) == 'No module named log4erp':
		print 'chk:log4erp:f:The module "log4erp" does not exist in the solam system'
	if str(e) == 'No module named hashlib':
                print 'chk:hashlib:f:The module "hashlib" does not exist in the solam system'
	if str(e) == 'No module named md5':
                print 'chk:md5:f:The module "md5" does not exist in the solam system'
	if str(e) == 'No module named crypto':
                try:
                        import cryptography
                except Exception as e:
                        print 'chk:crypto:f:The module "crypto or cryptography" does not exist in the solam system'
	if str(e) == 'No module named paramiko':
                print 'chk:paramiko:f:The module "paramiko" does not exist in the solam system'
	if str(e) == 'Name or service not known':
		print 'chk:connectivity:f:The hostname or IP is not rechable'
	else:
		print 'chk:exeception:f:' + str(e) + ':' + lineno
