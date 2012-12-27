#!/usr/bin/python
#Author: dmatos@uolinc.com

import re
import sys
import threading
from paramiko import SSHClient, AutoAddPolicy

#_user="my_user"
#_pass="my_password"

_server_list="server.list"

if(len(sys.argv) < 3):
    print 'Uso: ', sys.argv[0], 'host/pattern ', 'comando'
    sys.exit(1)

_host=sys.argv[1]
_command=sys.argv[2]

server_list = open(_server_list,'r')
servers = []

for linha in server_list:
    if (re.match(r''.join(_host),linha)):
        servers.append(re.sub(' ','',re.sub('\n','',linha)))

#print servers
#sys.exit(1)

if(len(servers)<1):
    print 'no hosts'
    sys.exit(1)

# Worker Thread Function
def workerThread(host,user,password,cmd='uptime'):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(
        AutoAddPolicy()
    )
    try:
        ssh.connect(host, username=user, password=password,timeout=18)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        retorno = re.sub('\n',",",stdout.read())
        print host,':',retorno
        ssh.close
    except Exception, e:
        print host,': nao foi possivel executar o comando'

# Spawning Threads
for host in servers:
    t = threading.Thread(name=host,target=workerThread,args=(host,_user,_pass,_command,))
    t.start()

