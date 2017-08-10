from subprocess import *
import subprocess
from sys import *
import os
#surabhi ka ghatia addition
#anik k changes
#jesna learn hindi 

def write(filename, string):
# ------------------------- file existance check --------------------
    if os.path.isfile(filename) != 'True':
# ------------------------- create file -----------------------------
	f = open(filename, 'a')
# -------------------- Count ---------------------------
    with open(filename) as f:
	count = sum(1 for _ in f)
    if int(count) > 0:
        with open(filename) as f:
            count = f.readlines()[len(f.readlines()) - 1].split(':')[-1][0]
    else:
        count = 2
    count = int(count) + 1
    f = open(filename, 'a')
    f.write(string + ':' + str(count) + '\r\n')
    f.close()

#write(argv[1], argv[2])
