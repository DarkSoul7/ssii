# -*- coding: utf-8 -*-
import tkinter
import tkinter.messagebox
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
    
    def callback():
        path = entry.get()
        res = a.new_directory(path)
        if res:
            tkinter.messagebox.showinfo('Integrity checker', 'The new directory was successfully stored')
        else:
            tkinter.messagebox.showerror('Integrity checker', 'Unable to store the new directory')
    
    label = tkinter.Label(top, text = 'Insert new directory')
    label.pack(side = tkinter.LEFT)
        
    entry = tkinter.Entry(top, width=60)
    entry.pack(side = tkinter.LEFT)
    
    button = tkinter.Button(top, text = 'Store', cursor = 'hand2', command = callback)
    button.pack(side = tkinter.LEFT)