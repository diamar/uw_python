"""
echo client, usage:

 python echo_client.py <host> <port>

Both host and port are optional, defaults: localhost 50000
host must be present if you want to provide port
"""

import socket 
import sys
import select
import time
import datetime

host = 'localhost' 
port = 50003 
size = 1024 

nargs = len(sys.argv)
if nargs > 1:
    host = sys.argv[1]
if nargs > 2:
    port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM) 
s.connect((host,port))

timeout = 10
input = [s, sys.stdin]
running = True

while running:
    
    inputready,outputready,exceptready = select.select(input,[],[],timeout)

    for soc in inputready:

        if soc == s:
            # handle the incoming message from server
            data = s.recv(size)
            print 'from (%s,%s) %s' % (host, port, data)

        elif soc == sys.stdin:
            # handle standard input
            data = sys.stdin.readline()
            if data == '\n':  #if return, then exit loop and close connection
                running = False
                s.close()
                print 'Closed connection'
                break
            s.send(data)
            print 'data was just sent'
            
