__author__ = 'AlanVargo'

import socket

sock_serv=socket.socket()
sock_serv.bind(('127.0.0.1' , 7070))
sock_serv.listen(5)

print 'Server is ready'

while 1:
    sock_conn, addr = sock_serv.accept()
    print 'Connection: ' , addr
    while 1:
        data = sock_conn.recv(2048)
        if data == "-stop-":
            print "Stop from client"
            break
        print '<< '+data
        send = raw_input(">> ")
        sock_conn.send(send)
        if send == "-stop-":
            print "Stop from server"
            print ''
            break
    sock_conn.close()