__author__ = 'AlanVargo'
import sys
import socket
import select
import threading
import string

my_key = 'ASD'

def xor(string, key):
    data = ''
    for char in string:
        for ch in key:
            char = chr(ord(char) ^ ord(ch))
        data += char
    return data

def broadcast(recv_socket , message , user):
    for sock in SOCKET_LIST:
        if sock != recv_socket and sock != sock_serv:
            print str(user) + ' >> [' + message + '] broadcast...\n'
            sock.send(message)

# main
if __name__ == "__main__":

    SOCKET_LIST = []
    NAME_LIST = []
    NM_SK_DICT = {}

    print '=== TCP SERVER ===\n'
    ip = '127.0.0.1'
    n_listen = 5
    ##ip = str(raw_input('IP to bind: '))
    ##port = str(raw_input('Port to bind: '))
    ##n_listen = int(raw_input('Number of clients: '))

    print '\nServer:'
    sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print '\t===created'
    sock_serv.bind((ip, 19999))
    print '\t===bind'
    ##sock_serv.bind((ip,port))
    sock_serv.listen(n_listen)
    print '\t===listen\n'

    SOCKET_LIST.append(sock_serv)
    NAME_LIST.append('server')
    NM_SK_DICT['server']=sock_serv

    while 1:
        read_socks, write_socks, err_socks = select.select(SOCKET_LIST, [], [])

        for rsocket in read_socks:

            if rsocket == sock_serv:
                socket_conn, raddr = sock_serv.accept()
                username_e = socket_conn.recv(256)
                username_d = xor(username_e, my_key)

                SOCKET_LIST.append(socket_conn)
                NAME_LIST.append(username_d)
                NM_SK_DICT[username_d]=socket_conn

                print "== (%s, %s): is connected ==" % raddr
                print "username: ", str(NM_SK_DICT)
            else:
                try:
                    data = rsocket.recv(4096)
                except:
                    mess = str("== (%s, %s) disconnect ==" % raddr)
                    broadcast(rsocket, mess, raddr)
                    print "== (%s, %s) disconnect ==" % raddr
                    rsocket.close()
                    SOCKET_LIST.remove(rsocket)
                    continue

                if data:
                    if data == 'q':
                        print "== (%s, %s) exit ==" % raddr
                        rsocket.close()
                        SOCKET_LIST.remove(rsocket)
                    else:
                        broadcast(rsocket, data, raddr)

    sock_serv.close()






