# -*- coding: utf-8 -*-
import socket
import ssl
from os.path import dirname
from os.path import abspath


def client():
    print('Abriendo conexión')

    dir = dirname(dirname(abspath(__file__))) + '\\files'
    csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sslSocket = ssl.wrap_socket(csocket, keyfile=dir+'\\csocket.pkey', certfile=dir+'\\csocket.cert',
                server_side=False, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2,
                ca_certs=dir+'\\CA.cert', do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None)

    sslSocket.connect(('localhost', 9999))

    msg = input('Introduzca mensaje: ')

    sslSocket.send(msg.encode())
    print('Mensaje enviado: '+ msg)

    rsp = sslSocket.recv(1024)
    print('Mensaje recibido: '+ rsp.decode(encoding='utf-8'))

    sslSocket.close()
    print('Cerrando conexión')


if __name__ == "__main__":
    client()