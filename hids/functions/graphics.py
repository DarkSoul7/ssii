# -*- coding: utf-8 -*-
import tkinter.messagebox
import functions.main as m
import functions.auxiliary as a

configuracion = {'cursor': 'hand2', 'font': 'Helvetica 10 bold', 'bg': 'white'}


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
    
    button_update_time = tkinter.Button(frame_menu, text='Update timer', command=lambda: change_time())
    button_update_time.config(configuracion)
    button_update_time.pack(side=tkinter.LEFT)
    
    button_get_directories = tkinter.Button(frame_menu, text='Stored directories', command=lambda: get_directories())
    button_get_directories.config(configuracion)
    button_get_directories.pack(side=tkinter.LEFT)
    
    root.mainloop()
   
    
def create_directory(widget=''):
    top = tkinter.Toplevel(bg = 'white')
    
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
    

def change_time():
    top = tkinter.Toplevel(bg = 'white')
    
    def callback():
        time = entry.get()
        res = a.update_time(time)
        if res:
            tkinter.messagebox.showinfo('Integrity checker', 'Timer was successfully updated')
        else:
            tkinter.messagebox.showerror('Integrity checker', 'Unable to update the timer')
    
    label = tkinter.Label(top, text = 'Insert new time')
    label.pack(side = tkinter.LEFT)
        
    entry = tkinter.Entry(top, width=60)
    entry.pack(side = tkinter.LEFT)
    
    button = tkinter.Button(top, text = 'Update', cursor = 'hand2', command = callback)
    button.pack(side = tkinter.LEFT)
    
    
def get_directories():
    top = tkinter.Toplevel(bg = 'white')
    
    scrollbar = tkinter.Scrollbar(top)
    scrollbar.pack(side = tkinter.RIGHT, fill=tkinter.Y)
    
    text = tkinter.Text(top, height = 30, width = 120,  yscrollcommand = scrollbar.set)
    text.pack(side = tkinter.LEFT)
    
    directories = a.get_directories()
    
    for d in directories:
        text.insert(tkinter.END, 'Name: ' + d[0])
        text.insert(tkinter.END, '\n')
        text.insert(tkinter.END, 'Path: ' + d[1])
        text.insert(tkinter.END, '\n\n')

        
menu()