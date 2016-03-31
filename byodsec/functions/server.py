# -*- coding: utf-8 -*-
import socket
import ssl
from os.path import dirname
from os.path import abspath


def server():

    dir = dirname(dirname(abspath(__file__))) + '\\files'
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssocket.bind(('localhost', 9999))
    ssocket.listen()

    sslSocket = ssl.wrap_socket(ssocket, keyfile=dir+'\\ssocket.pkey', certfile=dir+'\\ssocket.cert',
                server_side=True, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs=dir+'\\CA.cert',
                do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None)

    while True:
        print('Abriendo conexión')
        (csocket, address) = sslSocket.accept()

        msg = csocket.recv(1024)
        print('Mensaje recibido: '+msg.decode(encoding='utf-8'))

        rsp = 'Mensaje recibido correctamente'

        csocket.send(rsp.encode())
        print('Mensaje enviado: '+ rsp)

        csocket.close()
        sslSocket.close()
        print('Cerrando conexión')

        break


if __name__ == "__main__":
    server()