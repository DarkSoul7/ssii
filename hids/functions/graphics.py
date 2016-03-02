# -*- CODING: UTF-8 -*-
import tkinter.messagebox
import hids.functions.main as m
import hids.functions.auxiliary as a

configuracion = {'cursor': 'hand2', 'font': 'Helvetica 10 bold', 'bg': 'white'}


def menu():
    global configuracion

    root = tkinter.Tk('root')
    root.config(bg = 'white')
    root.title('integrity checker')

    frame_menu = tkinter.Frame(root, bg = 'white', name='frame_menu')
    frame_menu.pack()

    button_init = tkinter.Button(frame_menu, text='Update all directories', command=lambda:m.update_all_directories())
    button_init.config(configuracion)
    button_init.pack(side=tkinter.LEFT)

    button_check = tkinter.Button(frame_menu, text='Check integrity', command=lambda:m.check_hashes())
    button_check.config(configuracion)
    button_check.pack(side=tkinter.LEFT)

    button_new_directory = tkinter.Button(frame_menu, text='New directory', command=lambda: create_directory())
    button_new_directory.config(configuracion)
    button_new_directory.pack(side=tkinter.LEFT)

    button_update_time = tkinter.Button(frame_menu, text='Update timer', command=lambda: change_time())
    button_update_time.config(configuracion)
    button_update_time.pack(side=tkinter.LEFT)

    button_update_time = tkinter.Button(frame_menu, text='Update number of logs', command=lambda: change_nlogs())
    button_update_time.config(configuracion)
    button_update_time.pack(side=tkinter.LEFT)

    button_update_threshold = tkinter.Button(frame_menu, text='Update threshold', command=lambda: change_threshold())
    button_update_threshold.config(configuracion)
    button_update_threshold.pack(side=tkinter.LEFT)

    button_get_directories = tkinter.Button(frame_menu, text='Stored directories', command=lambda: get_directories())
    button_get_directories.config(configuracion)
    button_get_directories.pack(side=tkinter.LEFT)

    button_get_config = tkinter.Button(frame_menu, text='Configuration file', command=lambda: view_config_file())
    button_get_config.config(configuracion)
    button_get_config.pack(side=tkinter.LEFT)
    
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
    
    button = tkinter.Button(top, text = 'Store', cursor = 'hand2', command = lambda:callback())
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
    
    label = tkinter.Label(top, text = 'Insert new time in minutes')
    label.pack(side = tkinter.LEFT)
        
    entry = tkinter.Entry(top, width=60)
    entry.pack(side = tkinter.LEFT)
    
    button = tkinter.Button(top, text = 'Update', cursor = 'hand2', command = lambda:callback())
    button.pack(side = tkinter.LEFT)
    
    
def change_nlogs():
    top = tkinter.Toplevel(bg = 'white')
    
    def callback():
        nlogs = entry.get()
        res = a.update_nlogs(nlogs)
        if res:
            tkinter.messagebox.showinfo('Integrity checker', 'Successfully updated')
        else:
            tkinter.messagebox.showerror('Integrity checker', 'Unable to update')
    
    label = tkinter.Label(top, text = 'Insert new number of logs')
    label.pack(side = tkinter.LEFT)
        
    entry = tkinter.Entry(top, width=60)
    entry.pack(side = tkinter.LEFT)
    
    button = tkinter.Button(top, text = 'Update', cursor = 'hand2', command = lambda:callback())
    button.pack(side = tkinter.LEFT)
    
    
def change_threshold():
    top = tkinter.Toplevel(bg = 'white')
    
    def callback():
        threshold = int(entry.get())
        if threshold < 0 or threshold > 100:
            tkinter.messagebox.showerror('Integrity checker', 'The threshold cannot be less than zero or greater than 100')
        else:
            res = a.update_threshold(threshold)
            if res:
                tkinter.messagebox.showinfo('Integrity checker', 'Threshold successfully updated')
            else:
                tkinter.messagebox.showerror('Integrity checker', 'Unable to update the threshold')
    
    label = tkinter.Label(top, text = 'Insert new threshold')
    label.pack(side = tkinter.LEFT)
        
    entry = tkinter.Entry(top, width=60)
    entry.pack(side = tkinter.LEFT)
    
    button = tkinter.Button(top, text = 'Update', cursor = 'hand2', command = lambda:callback())
    button.pack(side = tkinter.LEFT)
    

def get_directories():
    global configuracion
    top = tkinter.Toplevel(bg = 'white')
    
    directories = a.get_directories()
    
    if not directories:
        label = tkinter.Label(top, text='There is no stored directories to show', bg='white')
        label.pack(side=tkinter.LEFT, anchor=tkinter.W)
    else:
        for d in directories:
            frame = tkinter.Frame(top, bg='white')
            frame.pack(side=tkinter.TOP, anchor=tkinter.W)
            
            label = tkinter.Label(frame, text=d[0] + ': ' + d[1], bg='white')
            label.pack(side=tkinter.LEFT, anchor=tkinter.W)
            
            button_update = tkinter.Button(frame, text='Update hashes', command=lambda d=d[0] : m.update_directory(d))
            button_update.config(configuracion)
            button_update.pack(side=tkinter.LEFT)
            
            button_delete = tkinter.Button(frame, text='Delete directory', command=lambda d=d[0] : delete_directory(d, top))
            button_delete.config(configuracion)
            button_delete.pack(side=tkinter.LEFT)
            
            button_files = tkinter.Button(frame, text='View stored files', command=lambda d=d : view_files(d))
            button_files.config(configuracion)
            button_files.pack(side=tkinter.LEFT)
            
            button_excluded = tkinter.Button(frame, text='View excluded files', command=lambda d=d : view_excluded(d))
            button_excluded.config(configuracion)
            button_excluded.pack(side=tkinter.LEFT)
            
            button_manage = tkinter.Button(frame, text='Manage excluded files', command=lambda d=d[0] : m.manage_excluded(d))
            button_manage.config(configuracion)
            button_manage.pack(side=tkinter.LEFT)
        
        
def delete_directory(d, top):
    m.delete_directory(d)
    
    top.destroy()
    get_directories()
    

def view_excluded(d):
    excluded_files = m.view_excluded(d[0])
    
    top = tkinter.Toplevel(bg = 'white')
    
    text = tkinter.Text(top, width=120)
    text.insert('end', 'Excluded files for directory: ' + d[1] + '\n\n')
    
    if not excluded_files:
        text.insert('end', 'None')
    else:
        for file in excluded_files:
            text.insert('end', file + '\n')
    
    text.config(state='disabled')
    text.pack()
    
    
def view_files(d):
    stored_files = m.view_files(d[0])
    
    top = tkinter.Toplevel(bg = 'white')
    
    text = tkinter.Text(top, width=120)
    text.insert('end', 'Stored files for directory: ' + d[1] + '\n\n')
    
    for file in stored_files:
        text.insert('end', str(file) + '\n')
    
    text.config(state='disabled')
    text.pack()
        

def view_config_file():
    config_file = m.view_config_file()
    
    top = tkinter.Toplevel(bg = 'white')
    
    text = tkinter.Text(top, width=120)
    text.insert('end', 'Configuration file' + '\n\n')
    
    for config in config_file:
        line = config.split(',')
        text.insert('end', line[0].strip() + ': ' + line[1].strip() + '\n')
    
    text.config(state='disabled')
    text.pack()
        
menu()