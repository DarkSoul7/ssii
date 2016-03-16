# -*- coding: utf-8 -*-
import hmac
import socket
import tkinter
import tkinter.messagebox

configuration = {'cursor': 'hand2', 'font': 'Helvetica 10 bold', 'bg': 'white'}


def menu():
    global configuration

    root = tkinter.Tk('root')
    root.config(bg='white')
    root.title('Intrans')

    button_transference = tkinter.Button(root, text='Make a transference', command=lambda: menu_transfer())
    button_transference.config(configuration)
    button_transference.pack(side=tkinter.LEFT)

    button_man_in_the_middle = tkinter.Button(root, text='Simulate a man in the middle attack',
                                              command=lambda: menu_transfer(mitm=True))
    button_man_in_the_middle.config(configuration)
    button_man_in_the_middle.pack(side=tkinter.LEFT)

    button_replay = tkinter.Button(root, text='Simulate a replay attack', command=lambda: menu_transfer(replay=True))
    button_replay.config(configuration)
    button_replay.pack(side=tkinter.LEFT)

    root.mainloop()


def menu_transfer(mitm=False, replay=False):

    top = tkinter.Toplevel()

    def callback():
        origin = entry_origin.get()
        destination = entry_destination.get()
        quantity = entry_quantity.get()
        algorithm = var_algorithm.get()
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
            make_transfer(origin + ' ' + destination + ' ' + quantity, algorithm, mitm, replay)

    frame_transference = tkinter.Frame(top, bg='white', name='frame_transference')
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

    frame_algorithm = tkinter.Frame(frame_transference, bg='white', name='frame_algorithm')
    frame_algorithm.pack(side=tkinter.TOP, anchor=tkinter.W)

    label_algorithm = tkinter.Label(frame_algorithm, bg='white', text='Available algorithms')
    label_algorithm.pack(side=tkinter.TOP, anchor=tkinter.W)

    label_algorithm2 = tkinter.Label(frame_algorithm, bg='white', text='sha1 and md5 are already deprecated')
    label_algorithm2.pack(side=tkinter.TOP)

    var_algorithm = tkinter.StringVar()

    radio_sha512 = tkinter.Radiobutton(frame_algorithm, text='sha512', variable=var_algorithm, value='sha512', bg='white')
    radio_sha512.pack(anchor=tkinter.W)

    radio_sha384 = tkinter.Radiobutton(frame_algorithm, text='sha384', variable=var_algorithm, value='sha384', bg='white')
    radio_sha384.pack(anchor=tkinter.W)

    radio_sha256 = tkinter.Radiobutton(frame_algorithm, text='sha256', variable=var_algorithm, value='sha256', bg='white')
    radio_sha256.pack(anchor=tkinter.W)

    radio_sha224 = tkinter.Radiobutton(frame_algorithm, text='sha224', variable=var_algorithm, value='sha224', bg='white')
    radio_sha224.pack(anchor=tkinter.W)

    radio_sha1 = tkinter.Radiobutton(frame_algorithm, text='sha1', variable=var_algorithm, value='sha1', bg='white')
    radio_sha1.pack(anchor=tkinter.W)

    radio_md5 = tkinter.Radiobutton(frame_algorithm, text='md5', variable=var_algorithm, value='md5', bg='white')
    radio_md5.pack(anchor=tkinter.W)

    radio_sha512.select()

    button = tkinter.Button(frame_transference, text='Transfer', bg='white', cursor='hand2', command=lambda: callback())
    button.pack(side=tkinter.BOTTOM)


def make_transfer(transfer, algorithm, mitm, replay):
    host, port = 'localhost', 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        sock.sendall(b'Starting connection\n')
        key = sock.recv(1024)
        mac = str(hmac.new(key=key, msg=transfer.encode('utf-8'), digestmod=algorithm).digest(), 'latin-1')
        if mitm:
            message = 'Simulating a mitm attack\t\t' + mac + '\t\t' + algorithm + '\n'
        else:
            message = transfer + '\t\t' + mac + '\t\t' + algorithm + '\n'
        sock.sendall(bytes(message, encoding='utf-8'))

        received = str(sock.recv(1024), 'utf-8')

        if replay:
            sock.sendall(bytes(message, encoding='utf-8'))
            received2 = str(sock.recv(1024), 'utf-8')
    finally:
        sock.close()

    if replay:
        tkinter.messagebox.showinfo('Intrans', 'First attemp: ' + received)
        tkinter.messagebox.showinfo('Intrans', 'Second attemp: ' + (received2 if received2 else 'No response received'))
    else:
        tkinter.messagebox.showinfo('Intrans', received)


menu()
