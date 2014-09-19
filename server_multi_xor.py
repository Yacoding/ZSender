__author__ = 'AlanVargo'
import sys
import socket
import select
import threading
import string

my_key = 'P@s$w0rD'

# XOR
def xor(string, key):
    data = ''
    for char in string:
        for ch in key:
            char = chr(ord(char)^ ord(ch))
        data += char
    return data

#broadcast for all sockets in SOCKET_LIST
def broadcast(recv_socket , message , user):
    for sock in SOCKET_LIST:
        if sock != recv_socket:
            print '[' + user + '] >> ' + message
            print 'broadcast...\n'
            sock.send(message)


if __name__ == "__main__":

    SOCKET_LIST = []

    print '=== TCP SERVER ===\n'
    ip = str(raw_input('IP to bind: '))
    ##port = str(raw_input('Port to bind: '))
    n_listen = int(raw_input('Number of clients: '))

    print '\nServer:'
    sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print '\t===created'
    sock_serv.bind((ip, 9999))
    print '\t===bind'
    ##sock_serv.bind((ip,port))
    sock_serv.listen(n_listen)
    print '\t===listen\n'

    SOCKET_LIST.append(sock_serv)

    while 1:
        read_socks, write_socks, err_socks = select.select(SOCKET_LIST, [], [])

        for rsocket in read_socks:
            if rsocket == sock_serv:
                socket_conn, raddr = sock_serv.accept()
                SOCKET_LIST.append(socket_conn)
                print "== %s is offline ==" % socket.gethostname()
            else:
                try:
                    data = rsocket.recv(4096)
                except:
                    broadcast(socket, "== %s is offline ==" % rsocket.gethostname(), rsocket.gethostname())
                    print "== %s is offline ==" % rsocket.gethostname()
                    rsocket.close()
                    SOCKET_LIST.remove(rsocket)
                    continue

                if data:
                    if data == 'q':
                        print "== %s is offline ==" % socket.gethostname()
                        rsocket.close()
                        SOCKET_LIST.remove(rsocket)
                    else:
                        broadcast(rsocket, data, rsocket.gethostname())

    sock_serv.close()






