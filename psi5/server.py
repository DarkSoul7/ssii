# -*- coding: utf-8 -*-
import base64
import socketserver
from os.path import dirname
from os.path import abspath
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('Recibiendo datos...')
        self.data = self.request.recv(1024).strip().decode('utf-8')

        if self.data.split('-----', 2)[0] != '':
            data = self.data.split('\t\t')
            signature = data[1]
            data = data[0]
            with open(dirname(abspath(__file__)) + '\\publickey.txt', 'r') as publickeyfile:
                key = ''.join(publickeyfile.readlines())
            rsakey = RSA.importKey(key)
            signer = PKCS1_v1_5.new(rsakey)
            digest = SHA256.new(base64.b64decode(data))
            print(signer.verify(digest, base64.b64decode(signature)))
            self.request.sendall(bytes("Datos recibidos correctamente", encoding='utf-8'))
        else:
            try:
                with open(dirname(abspath(__file__)) + '\\publickey.txt', 'w+') as publickeyfile:
                    publickeyfile.writelines(self.data)
                self.request.sendall(bytes("Clave pública recibida correctamente", encoding='utf-8'))
            except:
                self.request.sendall(bytes("Error", encoding='utf-8'))

        print('Conexión cerrada')


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 7070

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Running server...')
    server.serve_forever()
