# -*- coding: utf-8 -*-
import socketserver
from intrans.functions import server as server
from server import MyTCPHandler

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Running server...')
    server.serve_forever()