# -*- coding: utf-8 -*-
import socket
import socketserver
import threading


def client_thread(clientsocket):
    clientsocket.send("Welcome to the integrity server...\r\n")
    while True:
        data = clientsocket.recv()
        if data:
            clientsocket.send(data)
        else:
            pass


def main_server_thread():
    while 1:
        (clientsocket, address) = socketserver.accept()
        ct = threading(target=client_thread,args=((clientsocket),))
        ct.start()

        mainThread = threading(target=main_server_thread,args=())
        mainThread.start()
        while 1:
            pass


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), 80))
    serversocket.listen(5)

    while True:
        (clientsocket, address) = serversocket.accept()
        ct = client_thread(clientsocket)
        ct.start()
