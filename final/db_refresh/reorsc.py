from sys import *
import subprocess
from log4erp import *
import timeit
start_time = timeit.default_timer()

try:
    if argv[1] == "--u":
        print "Usage: python db_refresh <Source Application host> <Source DB Host> <Source Application Sudo User> <Source Application Sudo Password> <Source Database Sudo User> <Source Database Sudo Password> <Source Application Sid> <Source Database SID> <Target Application Host> <Target Database Host> <Target Applicatio Sudo User> <Target application Sudo password> <Target database Sudo User> <Target Database Sudo password> <Target application SID> <Target database SID> <Target Instance Number> <Refresh ID> <pre/ post> <Target DB ora user Password> <pit date> <pit time> "
    else:
	pre_post = argv[19].upper()
	command = "whoami"
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
	directory = out.strip()
	directory = 'smnadm'
	print directory
        if pre_post == "PRE":
	    src_app_host = argv[1]
            print src_app_host
            src_db_host = argv[2]
            src_app_user = argv[3]
            src_app_passwd = argv[4]
            src_db_user = argv[5]
            src_db_passwd = argv[6]
            src_app_sid = argv[7]
            src_db_sid = argv[8]
            print src_db_sid

            targ_app_host = argv[9]
            targ_db_host = argv[10]
            targ_app_user = argv[11]
            targ_app_passwd = argv[12]
            targ_db_user = argv[13]
            targ_db_passwd = argv[14]
            targ_app_sid = argv[15]
            targ_db_sid = argv[16]

            targ_inst = argv[17]
            targ_ref_id = argv[18]
            print targ_ref_id
            #targ_sch_passwd = argv[16]
            #targ_sys_passwd = argv[17]
#            pre_post = argv[19].upper()
            logfile = targ_ref_id + ".log"
            print logfile
	    directory =  'smnadm'

	    write(logfile,'PRE:P:START OF PRE RECOVERY DB CONFIGURATIONS')
            command = "python /home/" + directory + "/geminyo/scripts/mountpoint " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " source " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " target " + targ_ref_id
            print command
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            print out
            status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
            if status == "P":
                command = "python /home/" + directory + "/geminyo/scripts/sapstopapp " + targ_app_host + " " + targ_app_user + " " + targ_app_passwd + " " + targ_app_sid + " " + targ_inst + " " + targ_app_host + " " + targ_ref_id
                print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                print out
                status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                if status == "P":
                    command = "python /home/" + directory + "/geminyo/scripts/dbstop "  + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ref_id
                    print command
                    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                    out, err = command.communicate()
                    print out
                    status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                    if status == "P":
                        command = "python /home/" + directory + "/geminyo/scripts/cleanup " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ref_id
                        print command
                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        out, err = command.communicate()
                        print out
                        status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                        if status == "P":
                            print "pre db refresh activities completed successfully."
			    write(logfile,'PRE:P:END OF PRE RECOVERY DB CONFIGURATIONS')
        elif pre_post == "POST":
            src_app_host = argv[1]
            print src_app_host
            src_db_host = argv[2]
            src_app_user = argv[3]
            src_app_passwd = argv[4]
            src_db_user = argv[5]
            src_db_passwd = argv[6]
            src_app_sid = argv[7]
            src_db_sid = argv[8]
            print src_db_sid

            targ_app_host = argv[9]
            targ_db_host = argv[10]
            targ_app_user = argv[11]
            targ_app_passwd = argv[12]
            targ_db_user = argv[13]
            targ_db_passwd = argv[14]
            targ_app_sid = argv[15]
            targ_db_sid = argv[16]

            targ_inst = argv[17]
            targ_ref_id = argv[18]
            print targ_ref_id
            #targ_sch_passwd = argv[16]
            #targ_sys_passwd = argv[17]
            logfile = targ_ref_id + ".log"
            print logfile
	    targ_ora_user_pass = argv[20]


	    write(logfile,'POST:P:START OF POST RECOVERY DB CONFIGURATIONS')
            command = "python /home/" + directory + "/geminyo/scripts/db_begin_mode " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_ref_id
            print command
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            print out
            status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
	    print status
            if status == "P":
		command = "python /home/" + directory + "/geminyo/scripts/scpfile " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ora_user_pass + " " + targ_ref_id
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                print out
                status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
		#status = "P"
                if status == "P":
			command = "python /home/" + directory + "/geminyo/scripts/db_end_mode " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_ref_id
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			print command
	                out, err = command.communicate()
        	        print out
			#status = "P"
                	status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
	                if status == "P":
				command = "python /home/" + directory + "/geminyo/scripts/scp_control " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ora_user_pass + " " + targ_ref_id
				print command
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		                out, err = command.communicate()
                		print out
		                status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                		if status == "P":
					command = "python /home/" + directory + "/geminyo/scripts/control " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + src_db_sid + " " + targ_db_sid + " " + targ_ref_id
	 		                print command
			                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			                out, err = command.communicate()
			                print out
			                status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                    			if status == "P":
			                        command = "python /home/" + directory + "/geminyo/scripts/ctrlrun " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ref_id
                        			print command
			                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                        			out, err = command.communicate()
			                        print out
                        			status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
			                        if status == "P":
							command = "python /home/" + directory + "/geminyo/scripts/updating_archive " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_ref_id
							print command
	                                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        	                                        out, err = command.communicate()
                	                                print out
                        	                        status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
							if status == "P":
								command = "python /home/" + directory + "/geminyo/scripts/scparchive " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ora_user_pass + " " + targ_ref_id
								print command
	                                                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        	                                                out, err = command.communicate()
                	                                        print out
                        	                                status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                                	                        if status == "P":
									print "files has been archived sucessfully" 
									write(logfile,'POST:P:files has been archived sucessfully')
	elif pre_post == "RECOVER":
        	src_app_host = argv[1]
	        print src_app_host
        	src_db_host = argv[2]
	        src_app_user = argv[3]
        	src_app_passwd = argv[4]
	        src_db_user = argv[5]
        	src_db_passwd = argv[6]
	        src_app_sid = argv[7]
        	src_db_sid = argv[8]
	        print src_db_sid

                targ_app_host = argv[9]
                targ_db_host = argv[10]
                targ_app_user = argv[11]
                targ_app_passwd = argv[12]
                targ_db_user = argv[13]
                targ_db_passwd = argv[14]
                targ_app_sid = argv[15]
                targ_db_sid = argv[16]

                targ_inst = argv[17]
                targ_ref_id = argv[18]
                print targ_ref_id
                #targ_sch_passwd = argv[16]
                #targ_sys_passwd = argv[17]
		pit_date = argv[21]
	        pit_time = argv[22]
        	logfile = targ_ref_id + ".log"
	        print logfile


		command = "python /home/" + directory + "/geminyo/scripts/recover_db " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + pit_date + " " + pit_time + " " + targ_ref_id
		print command
	        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                print out
                status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                if status == "P":
           		command = "python /home/" + directory + "/geminyo/scripts/resetlog " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ref_id
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out
			status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
			if status == "P":
				command = "python /home/" + directory + "/geminyo/scripts/sapdba " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + src_app_sid + " " + src_db_sid + " " + targ_ref_id
				print command
	                        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        	                out, err = command.communicate()
                	        print out
                        	status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                                if status == "P":
					command = "python /home/" + directory + "/geminyo/scripts/ops " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_app_sid + " " + src_app_sid + " " + src_db_sid + " " + targ_ref_id
					print command
	                                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        	                        out, err = command.communicate()
                	                print out
                        	        status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
                                	if status == "P":
						command = "python /home/" + directory + "/geminyo/scripts/lsnr_start " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ref_id
						print command
						command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
						out, err = command.communicate()
						print out
						status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
						if status == "P":
							command = "python /home/" + directory + "/geminyo/scripts/r3trans " + targ_app_host + " " + targ_app_user + " " + targ_app_passwd + " " + targ_app_sid + " " + targ_ref_id
					                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                        		out, err = command.communicate()
					                print out
                                        		status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
					                if status == "P":
								command = "python /home/" + directory + "/geminyo/scripts/truncatetable " + targ_app_host + " " + targ_app_user + " " + targ_app_passwd + " " + targ_app_sid + " " + targ_db_host + " " + targ_db_user + " " + targ_db_passwd + " " + targ_db_sid + " " + targ_ref_id
								command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
								out, err = command.communicate()
								print out
								status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
								if status == "P":
									command = "python /home/" + directory + "/geminyo/scripts/temptable " + src_db_host + " " + src_db_user + " " + src_db_passwd + " " + src_db_sid + " " + targ_db_host + " " +  targ_db_user + " " + targ_db_passwd + " " + targ_app_sid + " " + targ_db_sid + " " + targ_ref_id
									print command
									command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
									out, err = command.communicate()
									print out
									status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
									if status == "P":
										command = "python /home/" + directory + "/geminyo/scripts/sapstartapp " + targ_app_host + " " + targ_app_user + " " + targ_app_passwd + " " + targ_app_sid + " " + targ_inst + " " + targ_app_host + " " + targ_ref_id
										print command
										command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                                                        			out, err = command.communicate()
							                        print out
                                                        			status = (out.split('\n')[len(out.split('\n')) - 2]).split(':')[1]
										if status == "P":
											write(logfile,'POST:P:END OF POST RECOVERY DB CONFIGURATIONS')
											elapsed = timeit.default_timer() - start_time
											print elapsed
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "DB_REFRESH:F:GERR_1001:Hostname unknown"
        write(logfile,'DB:F: Hostname unknown [Error Code - 1001]')
    elif str(e).strip() == "list index out of range":
        print "DB_REFRESH:F:GERR_1002:Argument/s missing for DB_REFRESH script"
    elif str(e) == "Authentication failed.":
        print "DB_REFRESH:F:GERR_1003:Authentication failed."
        write(logfile,'DB:F:Authentication failed[Error Code - 1003]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "DB_REFRESH:F:GERR_1004:Host Unreachable"
	write(logfile,'DB:F:Host Unreachable[Error Code - 1004]')
    elif "getaddrinfo failed" in str(e):
        print "DB_REFRESH:F:GERR_1005: Please check the hostname that you have provide"
        write(logfile,'DB:F: Please check the hostname that you have provide [Error Code - 1005]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "DB_REFRESH:F:GERR_1006:Host Unreachable or Unable to connect to port 22"
	write(logfile,'DB:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1006]')
    else:
        print "DB_REFRESH:F: " + str(e)
	write(logfile,'DB:F: ' + str(e))
