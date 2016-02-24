# -*- coding: utf-8 -*-
import tkinter
import functions.main as m
import functions.auxiliary as a

configuracion = {'cursor': 'hand2', 'font': 'Helvetica 10 bold', 'bg': 'white'}
#Temporalidad
def menu():
    global configuracion
    
    root = tkinter.Tk('root')
    root.config(bg = 'white')
    root.title('Integrity checker')
    
    frame_menu = tkinter.Frame(root, bg = 'white', name='frame_menu')
    frame_menu.pack()
    
    button_init = tkinter.Button(frame_menu, text='Update directories', command=m.init_hashes)
    button_init.config(configuracion)
    button_init.pack(side=tkinter.LEFT)
     
    button_check = tkinter.Button(frame_menu, text='Check integrity', command=m.check_hashes)
    button_check.config(configuracion)
    button_check.pack(side=tkinter.LEFT)
    
    button_new_directory = tkinter.Button(frame_menu, text='New directory', command=lambda: create_directory())
    button_new_directory.config(configuracion)
    button_new_directory.pack(side=tkinter.LEFT)
    
    root.mainloop()
   
    
def create_directory(widget=''):
    top = tkinter.Toplevel()
    text = tkinter.Text(top)
    text.pack()