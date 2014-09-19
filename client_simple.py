__author__ = 'AlanVargo'

import socket

sock_client = socket.socket()
sock_client.connect(('127.0.0.1' , 7070))
sock_client.send(socket.gethostname())

print "Connected to" , sock_client.getpeername()

while 1:
    data = sock_client.recv(2048)
    if data == "-stop-":
        break
    else:
        print "<< "+data
        send = raw_input(">> ")
        if send == "-stop-":
            sock_client.send(send)
            break
        sock_client.send(send)
sock_client.close()
