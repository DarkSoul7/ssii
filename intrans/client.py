# -*- coding: utf-8 -*-
import socket
import hmac

HOST, PORT = 'localhost', 9999
data = '123456789 987654321 200'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    sock.sendall(b'Starting connection\n')
    key = sock.recv(1024)
    mac = str(hmac.new(key=key, msg=data.encode('utf-8'), digestmod='sha256').digest(), 'latin-1')
    sock.sendall(bytes(data + '\t' + mac + '\n', 'utf-8'))

    received = str(sock.recv(1024), 'utf-8')
finally:
    sock.close()

print("Sent:     {}".format(data))
print("Received: {}".format(received))