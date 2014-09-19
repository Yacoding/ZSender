__author__ = 'AlanVargo'

import socket
import thread
import sys

my_key = 'P@s$w0rD'

# XOR
def xor(string, key):
    data = ''
    for char in string:
        for ch in key:
            char = ch(ord(char) ^ ord(ch))
        data += char
    return data

def recv_data():
    while 1:
        try:
            recv_data = sock_client.recv(4096)
        except:
            print 'Server closed connection'
            thread.interrupt_main()
            break
        if not recv_data:
            print 'Server closed connection'
            thread.interrupt_main()
            break
        else:
            print '\nNon decrypt: [ ' + recv_data + ' ]'
            recv_data = xor(recv_data, my_key)
            print '\nDecrypt: [ ', recv_data, ' ]'

def send_data():
    while 1:
        send_data = str(raw_input('>> '))
        if send_data == 'q':
            sock_client.send(send_data)
            thread.interrupt_main()
            break
        else:
            send_data = xor(send_data, my_key)
            sock_client.send(send_data)

if __name__ == "__main__":

    print '=== TCP CLIENT ==='
    ip = str(raw_input('\nIP to connection: '))
    user = str(raw_input('Username: '))

    print '\nClient: '
    sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print '\t===Created'
    sock_client.connect((ip, 19999))
    print '\t===Connected\n'

    print 'Connected to', ip, ':19999 [ ', sock_client.getsockname(), ' ]'

    thread.start_new_thread(recv_data(), ())
    thread.start_new_thread(send_data(), ())

    try:
        while 1:
            continue
    except:
        print 'Exit from client'
        sock_client.close()

