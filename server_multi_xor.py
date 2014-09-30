#      _   _        __   __
#     /_\ | |__ _ _ \ \ / /_ _ _ _ __ _ ___
#    / _ \| / _` | ' \ V / _` | '_/ _` / _ \
#   /_/ \_\_\__,_|_||_\_/\__,_|_| \__, \___/
#                                 |___/

import sys
import os
import socket
import select
import thread
import threading
import string
import _winreg
import cmd
import stat
import time
import datetime
import win32api, win32con
import subprocess

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
            print '\n' + str(user) + ' >> [' + message + '] broadcast...'
            sys.stdout.write('->')
            sock.send(message)

def commands():
    while 1:
        command = str(raw_input('-> '))
        if command == 's':
            print '=> Stoping...'
            thread.interrupt_main()
            sock_serv.close()
            break

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

    sys.stdout.write('Server:\n')
    sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sys.stdout.write('  +created')
    sock_serv.bind((ip, 19999))
    sys.stdout.write('  +bind')
    ##sock_serv.bind((ip,port))
    sock_serv.listen(n_listen)
    sys.stdout.write('  +listen\n')

    SOCKET_LIST.append(sock_serv)
    NAME_LIST.append('server')
    NM_SK_DICT['server'] = sock_serv

    thread.start_new_thread(cmd.call, (commands, ))

    while 1:
        read_socks, write_socks, err_socks = select.select(SOCKET_LIST, [], [])

        for rsocket in read_socks:

            if rsocket == sock_serv:
                socket_conn, raddr = sock_serv.accept()
                username_e = socket_conn.recv(256)
                username_d = xor(username_e, my_key)

                SOCKET_LIST.append(socket_conn)
                NAME_LIST.append(username_d)
                NM_SK_DICT[username_d] = raddr

                print "\n=> " + str(raddr) + ": is connected"
                print "=> username: ", username_d
                sys.stdout.write('->')
            else:
                try:
                    data = rsocket.recv(4096)
                except:
                    mess = str("=> " + str(rsocket) + ": disconnect")
                    broadcast(rsocket, mess, rsocket)
                    print "\n=> " + str(rsocket) + ": disconnect"
                    sys.stdout.write('->')
                    rsocket.close()
                    SOCKET_LIST.remove(rsocket)
                    continue

                if data:
                    if data == 'q':
                        print "\n=> " + str(rsocket) + ": exit"
                        sys.stdout.write('->')
                        rsocket.close()
                        SOCKET_LIST.remove(rsocket)
                    else:
                        broadcast(rsocket, data, rsocket)

    sock_serv.close()






