# -*- coding: utf-8 -*-
import tkinter
from functions.main import check_hashes
from functions.main import init_hashes
from functions.auxiliary import new_directory

configuracion = {'cursor': 'hand2', 'font': 'Helvetica 10 bold', 'bg': 'white'}

def menu():
    global configuracion
    
    root = tkinter.Tk('root')
    root.config(bg = 'white')
    root.title('Integrity checker')
    
    frame_menu = tkinter.Frame(root, bg = 'white', name='frame_menu')
    frame_menu.pack()
    
    button_init = tkinter.Button(frame_menu, text='Update directories', command=init_hashes)
    button_init.config(configuracion)
    button_init.pack(side=tkinter.LEFT)
     
    button_check = tkinter.Button(frame_menu, text='Check integrity', command=check_hashes)
    button_check.config(configuracion)
    button_check.pack(side=tkinter.LEFT)
    
    button_new_directory = tkinter.Button(frame_menu, text='New directory', command=lambda: new_directory())
    button_new_directory.config(configuracion)
    button_new_directory.pack(side=tkinter.LEFT)
    
    root.mainloop()
    
menu()