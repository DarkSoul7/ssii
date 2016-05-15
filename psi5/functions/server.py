# -*- coding: utf-8 -*-
import base64
import socketserver
import psi5.functions.auxiliary as a
from os.path import dirname
from os.path import abspath
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('Recibiendo datos...')
        self.data = self.request.recv(1024).strip().decode('utf-8')

        #Comprobamos que no estamos recibiendo una clave pública
        if self.data.split('-----', 2)[0] != '':
            #Obtenemos los datos enviados
            data = self.data.split('\t\t')
            device_id = data[2]
            signature = base64.b64decode(data[1])
            data = base64.b64decode(data[0])
            #Leemos el certificado del emisor
            with open(dirname(dirname(abspath(__file__))) + '\\files\\publickeys\\' + device_id + '.txt', 'r') as publickeyfile:
                key = ''.join(publickeyfile.readlines())
            #Comprobamos la firma con el certificado anterior
            rsakey = RSA.importKey(key)
            signer = PKCS1_v1_5.new(rsakey)
            digest = SHA256.new(data)
            verified = signer.verify(digest, signature)
            verified = 'Verified' if verified else 'Unverified'
            #Escribimos el pedido y la comprobación en un fichero de texto
            a.writedata(verified + ' - ' + data.decode('utf-8'))
            #Actualizar contador de verificados/no verificados
            a.writelog(verified)
            self.request.sendall(bytes("Datos recibidos correctamente", encoding='utf-8'))
        #Si es una clave pública, la almacenamos
        else:
            key = self.data.split('\t\t')
            device_id = key[1]
            key = key[0]
            try:
                with open(dirname(dirname(abspath(__file__))) + '\\files\\publickeys\\' + device_id + '.txt', 'w+') as publickeyfile:
                    publickeyfile.writelines(key)
                self.request.sendall(bytes("Clave pública recibida correctamente", encoding='utf-8'))
            except:
                self.request.sendall(bytes("Error", encoding='utf-8'))

        print('Conexión cerrada')


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 7070

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Running server...')
    server.serve_forever()
