# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 19:05:35 2017
@author: SuperKogito
"""
# Define imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.scrolledtext import *
# custom files and classes imports
from PageOne import PageOne
from ExitPage import ExitPage
from StartPage import StartPage
from ManualPage import ManualPage


class MainWindow(tk.Tk):
    """ Main window class """
    def __init__(self, title):
        super().__init__()
        xyla = [0, 0, 680, 350]
        self.ext = ''
        self.original_path = ''
        self.title(title)
        self.minsize(xyla[2], xyla[3])
        self.resizable(0, 0)
        self.configure(background='black')
        self.geometry("%dx%d+%d+%d" % (xyla[0], xyla[1], 400, 100))
        # Define colors
        myActiveTabBackgroundColor = "#0080ff"
        myActiveTabForegroundColor = "white"
        myTabBackgroundColor = "black"
        myTabForegroundColor = "white"
        myTabBarColor = "black"
        # Define style
        ttk.Style().configure("TNotebook", background=myTabBarColor)
        ttk.Style().map("TNotebook.Tab",
                        background=[("selected", myActiveTabBackgroundColor)],
                        foreground=[("selected", myActiveTabForegroundColor)])
        ttk.Style().configure("TNotebook.Tab",
                              background=myTabBackgroundColor,
                              foreground=myTabForegroundColor)
        # Define containers
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # Define frames
        self.frames = {}
        for F in (StartPage, PageOne, ExitPage, ManualPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.container.pack()
        self.show_frame("StartPage")
        # Define bind events
        self.bind("<Control-a>", self.edit_select_all)
        self.bind("<Control-s>", self.file_save)
        self.bind("<Control-S>", self.file_save_as)
        self.bind("<Control-o>", self.file_open)
        self.bind("<Escape>", self.quit_func)

        self.menu = tk.Menu(self, tearoff=False)
        # Menu item File
        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", underline=0, menu=self.filemenu)
        self.filemenu.add_command(label="Open...", underline=1,
                                  command=self.file_open,
                                  accelerator="Ctrl+o")
        self.filemenu.add_command(label="Save", underline=1,
                                  command=self.file_save,
                                  accelerator="Ctrl+s")
        self.filemenu.add_command(label="Save As...", underline=5,
                                  command=self.file_save_as,
                                  accelerator="Ctrl+shift+s")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",
                                  underline=2,
                                  command=self.quit_func,
                                  accelerator="Esc")
        # Menu item Edit
        self.editmenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", underline=0, menu=self.editmenu)
        self.editmenu.add_command(label="Cut", underline=2,
                                  command=self.edit_cut,
                                  accelerator="Ctrl+X")
        self.editmenu.add_command(label="Copy",
                                  underline=0,
                                  command=self.edit_copy,
                                  accelerator="Ctrl+c")
        self.editmenu.add_command(label="Paste", underline=0,
                                  command=self.edit_paste,
                                  accelerator="Ctrl+v")
        self.editmenu.add_command(label="Clear", underline=2,
                                  command=self.edit_clear)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select All",
                                  command=self.edit_select_all,
                                  accelerator="Ctrl+a")
        # Menu item Help
        self.helpmenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", underline=0, menu=self.helpmenu)
        self.helpmenu.add_command(label="Manual", command=self.help_manual)
        # Coloring the menu
        self.filemenu.configure(background='black', foreground='white',
                                activebackground='#0080ff',
                                activeforeground='white')
        self.editmenu.configure(background='black', foreground='white',
                                activebackground='#0080ff',
                                activeforeground='white')
        self.helpmenu.configure(background='black', foreground='white',
                                activebackground='#0080ff',
                                activeforeground='white')
        self.config(menu=self.menu)
        self.menu.configure(background='black', foreground='white',
                            activebackground='#0080ff',
                            activeforeground='white')
        self.disable_menu()
        self.file_name = ''
        self.mainloop()

    def file_open(self, event=None):
        file_type = [('Python files', '*.txt'), ('All files', '*')]
        dialog = filedialog.Open(self, filetypes = file_type)
        file_to_open = dialog.show()

        if file_to_open != '':
            text = self.read_from_file(file_to_open)
            frame = self.frames["PageOne"]
            if (frame.active_tab() == 0):
                frame.textbox.delete('1.0', tk.END)
                frame.textbox.insert('1.0', text)
            elif (frame.active_tab() == 1):
                frame.textbox2.delete('1.0', tk.END)
                frame.textbox2.insert(tk.END, text)
            elif (frame.active_tab() == 2):
                frame.textbox31.delete('1.0', tk.END)
                frame.textbox31.insert(tk.END, text)

    def read_from_file(self, file_name):
        file = open(file_name, "r")
        text = file.read()
        return text

    def dummy(self):
        print("I am a Dummy Command, I will be removed in the next step")

    def file_save(self, event=None):
        """Handle click on 'Save' menu."""
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            data = frame.aes128_encrypt_output.get()
        elif (frame.active_tab() == 1):
            data = frame.aes128_decrypt_output.get()
        elif (frame.active_tab() == 2):
            data = frame.SHA_output.get()
        if (self.file_name != ''):
            writer = open(self.file_name, 'w')
            writer.write(data)
            writer.close()
        else:
            self.file_save_as()

    def file_save_as(self, event=None):
        """Handle click on 'Save as' menu."""
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            data = frame.aes128_encrypt_output.get()
        elif (frame.active_tab() == 1):
            data = frame.aes128_decrypt_output.get()
        elif (frame.active_tab() == 2):
            data = frame.SHA_output.get()
        self.write_to_file(data)

    def write_to_file(self, data):
        self.file_name = filedialog.asksaveasfilename(parent=self,
                                                      filetypes=[('Text',
                                                                 '*.txt')],
                                                      title='Save as...')
        writer = open(self.file_name, 'w')
        writer.write(data)
        writer.close()

    # Edit menu functions
    def edit_copy(self, event=None):
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            frame.textbox.event_generate("<<Copy>>")
        elif (frame.active_tab() == 1):
            frame.textbox2.event_generate("<<Copy>>")
        elif (frame.active_tab() == 2):
            frame.textbox31.event_generate("<<Copy>>")
        return "break"

    def edit_cut(self, event=None):
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            frame.textbox.event_generate("<<Cut>>")
        elif (frame.active_tab() == 1):
            frame.textbox2.event_generate("<<Cut>>")
        elif (frame.active_tab() == 2):
            frame.textbox31.event_generate("<<Cut>>")
        return "break"

    def edit_paste(self, event=None):
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            frame.textbox.event_generate("<<Paste>>")
        elif (frame.active_tab() == 1):
            frame.textbox2.event_generate("<<Paste>>")
        elif (frame.active_tab() == 2):
            frame.textbox31.event_generate("<<Paste>>")

    def edit_clear(self, event=None):
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            frame.textbox.delete(1.0, tk.END)
        elif (frame.active_tab() == 1):
            frame.textbox2.delete(1.0, tk.END)
        elif (frame.active_tab() == 2):
            frame.textbox31.delete(1.0, tk.END)
        return 'break'

    def edit_select_all(self, event=None):
        frame = self.frames["PageOne"]
        if (frame.active_tab() == 0):
            frame.textbox.tag_add(tk.SEL, "1.0", tk.END)
            frame.textbox.mark_set(tk.INSERT, "1.0")
            frame.textbox.see(tk.INSERT)
        elif (frame.active_tab() == 1):
            frame.textbox2.tag_add(tk.SEL, "1.0", tk.END)
            frame.textbox2.mark_set(tk.INSERT, "1.0")
            frame.textbox2.see(tk.INSERT)
        elif (frame.active_tab() == 2):
            frame.textbox31.tag_add(tk.SEL, "1.0", tk.END)
            frame.textbox31.mark_set(tk.INSERT, "1.0")
            frame.textbox31.see(tk.INSERT)
        return 'break'

    def create_interface(self, tab=None):
        self.tab = tab
        self.frame = tk.Frame(self.tab)
        self.frame.pack()
        self.frame_y = tk.Frame(self.tab)
        self.frame_z = tk.Frame(self.tab)
        self.frame_z.pack()
        self.frame_y.pack(fill=tk.BOTH, expand=1)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if (page_name == "PageOne"):
            self.enable_menu()
        if (page_name == "ExitPage"):
            self.disable_menu()
        frame = self.frames[page_name]
        frame.tkraise()

    def quit_func(self, event=None):
        self.destroy()
        self.container.destroy

    def enable_menu(self):
        # Enabling file menu elements
        self.filemenu.entryconfig(0, state='normal')
        self.filemenu.entryconfig(1, state='normal')
        self.filemenu.entryconfig(2, state='normal')
        # Enabling help menu elements
        self.helpmenu.entryconfig(0, state='normal')
        self.helpmenu.entryconfig(1, state='normal')
        # Enabling edit menu elements
        self.editmenu.entryconfig(0, state='normal')
        self.editmenu.entryconfig(1, state='normal')
        self.editmenu.entryconfig(2, state='normal')
        self.editmenu.entryconfig(3, state='normal')
        self.editmenu.entryconfig(5, state='normal')

    def disable_menu(self):
        # Disabling file menu elements
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        self.filemenu.entryconfig(1, state=tk.DISABLED)
        self.filemenu.entryconfig(2, state=tk.DISABLED)
        # Disabling file menu elements
        self.editmenu.entryconfig(0, state=tk.DISABLED)
        self.editmenu.entryconfig(1, state=tk.DISABLED)
        self.editmenu.entryconfig(2, state=tk.DISABLED)
        self.editmenu.entryconfig(3, state=tk.DISABLED)
        self.editmenu.entryconfig(5, state=tk.DISABLED)

    def help_manual(self):
        self.disable_menu()
        frame = self.frames["ManualPage"]
        frame.tkraise()
