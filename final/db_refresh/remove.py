import paramiko 
host = "sapredhat02" 
port = 22 
transport = paramiko.Transport((host, port)) 
password = "Welcome2" 
username = "erpadm" 
transport.connect(username = username, password = password) 
sftp = paramiko.SFTPClient.from_transport(transport) 
if "aa.txt" in sftp.listdir("/tmp/") : sftp.remove("/tmp/aa.txt") 
