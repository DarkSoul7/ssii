# -*- coding: utf-8 -*-
import hmac
import socketserver
import intrans.auxiliary as a


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.key = bytes(a.generator(), 'utf-8')
        self.request.sendall(self.key)

        self.data = str(self.request.recv(1024), 'utf-8').strip().split('\t')
        mac = hmac.new(self.key, self.data[0].encode('utf-8'), 'sha256').digest()
        if hmac.compare_digest(mac, bytes(self.data[1], 'latin-1')):
            self.request.sendall(b'Message correctly received')
        else:
            self.request.sendall(b'There was an error during this transaction')


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Server running...')
    server.serve_forever()