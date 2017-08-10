import subprocess
from subprocess import *
from sys import *
from paramiko import *
import paramiko
import os

def export(filename, hostname, username, password, client_name, stepname, seqno, appsid,refresh_id, path):
    #print username
    print filename
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname,username = username, password = password)
    channel = client.invoke_shell()
    appuser = appsid.lower() + 'adm'
    #print appuser

    file_open = open(filename, 'wt')

    file_content = """import
client=""" + client_name + """
file='/home/""" + appuser + """/""" + filename + """.dat'
delete * from """ + filename + """
select * from """ + filename

    file_open.write(file_content)
    file_open.close()

    print path +  '/' + filename
    print '/home/' + appuser +  '/' + filename

    port = 22
    transport = paramiko.Transport((hostname, port))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put (path +  '/' + filename, '/home/' + appuser +  '/' + filename)

    command = 'sudo chmod 777 /' + path.strip('/') + '/' + filename.strip()
    print command
    stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
    final = stdout.channel.recv_exit_status()
    print final
    if final == 0 or final == 1:
        command = 'sudo su - ' + appuser + ' -c \'R3trans -w /home/' + appuser +  '/' + filename + '.log /home/' + appuser + '/' + filename + '\''
        print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        final = stdout.channel.recv_exit_status()
        if final == 0 or final == 4:
            print 'POST:P:The backup for the table ' + filename + ' has been imported'
#	    write(refresh_id,'POST:P:The backup for the table ' + filename + ' has been imported')
        else:
            print 'POST:F:The backup for the table ' + filename + ' has been failed'
#	    write(refresh_id,'POST:F:The backup for the table ' + filename + ' has been failed')
	    exit()
    else:
        print  'POST:F:The permission change has been failed for the file ' + filename
#	write(refresh_id,'POST:F:The permission change has been failed for the file ' + filename)
	exit()

    channel.close()
    client.close()
    
#    os.remove(filename)
path = argv[8]
#table_name = ['DB2CCDL_PARMS','DB2CCDS_IN','DB2CCDS_PARMS','DB2CCMO_IN1','DB2CCMO_IN2','DB2CCMO_OUTTS','DB2CCMO_PARMS','DBABD','DBABL','DBCHECKORA','DBDIFF','DBSTATC','RSNSPACE','SDBAC','SDBAC_DATA','SDBAC_TEXT','SDBAD','SDBAH','SDBAP','SDBAR','TSORA']
command = 'whoami'
command = Popen(command,shell=True,stdout=subprocess.PIPE)
out, err = command.communicate()
#command = 'python ' + path + '/win14 ' + argv[5].upper()
command = 'python ' + path + '/win14 ' + argv[5].upper()
print command
command = Popen(command,shell=True,stdout=subprocess.PIPE)
out, err = command.communicate()
table_name = (out.strip('""').strip("''").strip("'\n")).split("', '")
print table_name
seqno=int(0)
for each in table_name:
    seqno=seqno + 1
    export(each, argv[1], argv[2], argv[3], argv[4],argv[5],str(seqno),argv[6],argv[7],path)
