__author__ = 'AlanVargo'

import socket
import thread
import sys

my_key = 'ASD'

def xor(string, key):
    data = ''
    for char in string:
        for ch in key:
            char = chr(ord(char) ^ ord(ch))
        data += char
    return data

def recv_data():
    while 1:
        try:
            recv_data = sock_client.recv(4096)
        except:
            print '\nServer closed connection'
            thread.interrupt_main()
            break
        if not recv_data:
            print '\nServer closed connection'
            thread.interrupt_main()
            break
        else:
            print '\nN << ', recv_data
            recv_data = xor(recv_data, my_key)
            print 'D << ', recv_data
            sys.stdout.write('>> ')

def send_data():
    while 1:
        send_data = str(raw_input('>> '))
        if send_data == '->':
            command()
        else:
            send_data = xor(send_data, my_key)
            sock_client.send(send_data)

def sended_data(send_data, do_crypt):
    if do_crypt == False or not do_crypt:
        sock_client.send(send_data)
    elif do_crypt == True:
        send_data = xor(send_data, my_key)
        sock_client.send(send_data)

def command():
    command = str(raw_input('-> '))
    if command == "q":
        thread.interrupt_main()
        sock_client.close()

def command(comm):
    if comm == "q":
        thread.interrupt_main()
        sock_client.close()

if __name__ == "__main__":

    print '=== TCP CLIENT ==='

    ip = '127.0.0.1'
    ##ip = str(raw_input('\nIP to connection: '))
    user = str(raw_input('Username: '))
    print '\nClient: '
    sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sys.stdout.write('  +Created')
    sock_client.connect((ip, 19999))
    sys.stdout.write('  +Connected\n')

    print 'Connected to', ip, ':19999 [ ', sock_client.getsockname(), ' ]'
    sended_data(user, True)

    thread.start_new_thread(recv_data, ())
    thread.start_new_thread(send_data, ())

    try:
        while 1:
            continue
    except:
        print 'Exit from client'
        sock_client.close()

