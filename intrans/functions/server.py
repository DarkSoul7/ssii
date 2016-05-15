# -*- coding: utf-8 -*-
import datetime
import hmac
import socketserver
import auxiliary as a
from os.path import dirname
from os.path import abspath


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.key = bytes(a.generator(), 'utf-8')
        self.request.sendall(self.key)

        self.data = str(self.request.recv(1024), 'utf-8').strip().split('\t\t')
        mac = hmac.new(self.key, self.data[0].encode('utf-8'), self.data[2]).digest()
        # Quitar un dirname al generar el ejecutable
        log_dir = dirname(dirname(abspath(__file__))) + '\\files\\logs\\' + \
          str(datetime.datetime.today()).split(' ')[0] + '.txt'

        if hmac.compare_digest(mac, bytes(self.data[1], 'latin-1')):
            message = 'Message correctly received'
            self.request.sendall(bytes(message, encoding='utf-8'))
            a.writelog(log_dir, self.data[0] + '\t\t' + message)
        else:
            message = 'There was an error during this transaction'
            self.request.sendall(bytes(message, encoding='utf-8'))
            a.writelog(log_dir, self.data[0] + '\t\t' + message, True)

        extra_data = str(self.request.recv(1024), 'utf-8').strip().split('\t\t')
        if extra_data[0].strip():
            message = 'Replay attack detected'
            self.request.sendall(bytes(message, encoding='utf-8'))
            a.writelog(log_dir, self.data[0] + '\t\t' + message, True)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Running server...')
    server.serve_forever()
