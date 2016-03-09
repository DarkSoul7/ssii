# -*- coding: utf-8 -*-
import hmac
import socket
import tkinter
import tkinter.messagebox


def menu():

    root = tkinter.Tk('root')
    root.config(bg='white')
    root.title('Intrans')

    def callback():
        origin = entry_origin.get()
        destination = entry_destination.get()
        quantity = entry_quantity.get()
        check = True

        if not origin:
            tkinter.messagebox.showerror('Intrans', 'You must insert an origin account')
            check = False

        if not destination:
            tkinter.messagebox.showerror('Intrans', 'You must insert a destination account')
            check = False

        if not quantity:
            tkinter.messagebox.showerror('Intrans', 'You must insert a quantity')
            check = False

        if check:
            make_transfer(origin + ' ' + destination + ' ' + quantity)

    frame_transference = tkinter.Frame(root, bg='white', name='frame_transference')
    frame_transference.pack()

    frame_origin = tkinter.Frame(frame_transference, bg='white', name='frame_origin')
    frame_origin.pack(side=tkinter.TOP, anchor=tkinter.W)

    label_origin = tkinter.Label(frame_origin, bg='white', text='Origin account' + ' '*9)
    label_origin.pack(side=tkinter.LEFT)

    entry_origin = tkinter.Entry(frame_origin, width=20, bd=3)
    entry_origin.pack(side=tkinter.LEFT)

    frame_destination = tkinter.Frame(frame_transference, bg='white', name='frame_destination')
    frame_destination.pack(side=tkinter.TOP, anchor=tkinter.W)

    label_destination = tkinter.Label(frame_destination, bg='white', text='Destination account')
    label_destination.pack(side=tkinter.LEFT)

    entry_destination = tkinter.Entry(frame_destination, width=20, bd=3)
    entry_destination.pack(side=tkinter.LEFT)

    frame_quantity = tkinter.Frame(frame_transference, bg='white', name='frame_quantity')
    frame_quantity.pack(side=tkinter.TOP, anchor=tkinter.W)

    label_quantity = tkinter.Label(frame_quantity, bg='white', text='Quantity' + ' '*20)
    label_quantity.pack(side=tkinter.LEFT)

    entry_quantity = tkinter.Entry(frame_quantity, width=10, bd=3)
    entry_quantity.pack(side=tkinter.LEFT)

    button = tkinter.Button(frame_transference, text='Transfer', bg='white', cursor='hand2', command=lambda: callback())
    button.pack(side=tkinter.BOTTOM)

    root.mainloop()


def make_transfer(transfer):
    host, port = 'localhost', 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        sock.sendall(b'Starting connection\n')
        key = sock.recv(1024)
        mac = str(hmac.new(key=key, msg=transfer.encode('utf-8'), digestmod='sha256').digest(), 'latin-1')
        sock.sendall(bytes(transfer + '\t' + mac + '\n', 'utf-8'))

        received = str(sock.recv(1024), 'utf-8')
    finally:
        sock.close()

    tkinter.messagebox.showinfo('Intrans', received)


menu()
