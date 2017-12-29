# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 19:05:35 2017
@author: SuperKogito
"""
# Define imports
import tkinter as tk


class ExitPage(tk.Frame):
    """ Exit page class """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')
        # Define main frame
        self.main_frame = tk.Frame(self, background='black')
        self.main_frame.pack(expand=1)
        self.main_frame.pack()
        # Define upper frame
        upper_frame = tk.Frame(self.main_frame, width=300, height=50,
                               background='black')
        upper_frame.grid(column=0, row=0)
        # Define label
        exit_string = '\n\nAre you sure that you want to exit Crypotos?\n'
        exit_label = tk.Label(upper_frame, text=exit_string,
                              background='black', foreground="white")
        exit_label.pack(side="top", fill="x", pady=10)
        # Define middle frame
        middle_frame = tk.Frame(self.main_frame, background='black',
                                width=300, height=50)
        middle_frame.grid(column=0, row=1)
        # Define cancel button
        cancel_button = tk.Button(middle_frame, text="Cancel",
                                  command=lambda: controller.show_frame("PageOne"))
        cancel_button.pack(side=tk.RIGHT)
        # Define yes button
        yes_button = tk.Button(middle_frame, text="Yes",
                               command=lambda: controller.quit_func())
        yes_button.pack(side=tk.RIGHT, padx=5, pady=5)
        # Configure the buttons
        cancel_button.configure(background='black', foreground='white',
                                activebackground='#0080ff',
                                activeforeground='white')
        yes_button.configure(background='black', foreground='white',
                             activebackground='#0080ff',
                             activeforeground='white')
        # Define lower frame
        lower_frame = tk.Frame(self.main_frame, background='black',
                               width=300, height=50)
        lower_frame.grid(column=0, row=2)
        # Define label
        dev_text = (
                   "\nDeveloped by: SuperKogito\n"
                   "Gihthub repository: "
                   "https://github.com/SuperKogito/Cryptos"
                   )
        self.developper_text = tk.Label(lower_frame,
                                        text=dev_text,
                                        background='black',
                                        foreground='White')
        self.developper_text.pack(side="bottom")
