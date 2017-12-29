# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 01:31:42 2017
@author: SuperKogito
"""
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

from PIL import Image
import os, sys, subprocess

class PageOne(tk.Frame):
    """ Page with main functionalities class """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')
        self.notebook = ttk.Notebook(self)
        
        # Define tabs
        self.tab1 = tk.Frame(self.notebook, background='black')
        self.tab2 = tk.Frame(self.notebook, background='black')
        self.other = tk.Frame(self.notebook, background='black')
        self.tab1.pack()
        self.tab2.pack()
        self.other.pack()
        
        # Add tabs to notebook instance
        self.notebook.add(self.tab1, text="Hide text")
        self.notebook.add(self.tab2, text="Extract text")
        self.notebook.pack(expand=1, fill="both")
        self.aes_encryption_tab()
        self.aes_decryption_tab()
        
        # Define exit button
        button = tk.Button(self, text="Exit", command=lambda: self.controller.show_frame("ExitPage"))
        button.configure(bg="black", fg='white', activebackground='#0080ff', activeforeground='white')
        button.pack(side=tk.RIGHT, padx=5, pady=5)
    # ------------------------------- tab1 ---------------------------------

    def aes_encryption_tab(self):
        self.input3 = tk.LabelFrame(self.tab1, bg="black", fg='white', text=" Image to hide text in ")
        self.input3.pack(expand=1, fill='both', padx=5, pady=5)
        
        self.target_image_path = tk.StringVar()
        self.verb_ent = tk.Entry(self.input3, width=55, textvariable=self.target_image_path)
        self.verb_ent.pack(side=tk.LEFT, expand=1, fill="both", padx=5, pady=5)
        
        button2 = tk.Button(self.input3, text="Select target image", command=lambda: self.get_path(0))
        button2.pack(side=tk.LEFT, padx=5, pady=5)
        button2.configure(bg="black", fg='white', activebackground='#0080ff', activeforeground='white')
        
        self.input = tk.LabelFrame(self.tab1, text=" Text to hide ",  background="black", foreground='white')
        self.textvar = tk.StringVar()
        self.textbox = tk.Text(self.input, height=5, width=70,  wrap='word', undo=True)
        self.textbox.pack(expand=1, fill="both", padx=5, pady=5)
        self.textbox.bind("<Key>", self.update)

        self.counter = tk.StringVar()
        self.counter.set('Charcters count: ' +'0'+ ' | Max allowed characters = 255')
        self.char_count = tk.Label(self.input, textvariable=self.counter, bg="Black", fg= '#0080ff')
        self.char_count.pack(side=tk.LEFT, expand=1, fill="both", padx=5, pady=5)
        
        button21 = tk.Button(self.input, text="Hide text", command=lambda: self.hide())
        button21.pack(side=tk.RIGHT, padx=5, pady=5)
        button21.configure(bg="black", fg='white', activebackground='#0080ff', activeforeground='white')
        
        self.input.pack(expand=1, fill="both", padx=5, pady=5)

        self.input1 = tk.LabelFrame(self.tab1, bg="black", fg='white', text=" Hide text status ")
        self.status_message = tk.StringVar()
        self.status_message.set('\n No text is hidden yet\n')
        
        textwidget = tk.Label(self.input1, textvariable=self.status_message, bg='black', fg="white", wraplength=590)
        textwidget.configure(relief='flat', state="normal")
        textwidget.pack(expand=1, fill="both", padx=5, pady=5)
        
        self.input1.pack(expand=1, fill="both", padx=5, pady=5)
    # ------------------------------- tab2 ---------------------------------

    def aes_decryption_tab(self):
        self.input22 = tk.LabelFrame(self.tab2, bg="black", fg='white', text=" Image with hidden text ")
        self.source_image_path = tk.StringVar()
        self.input22.pack(expand=1, padx=5, pady=5)
        
        self.verb_ent2 = tk.Entry(self.input22, width=55, textvariable=self.source_image_path)
        self.verb_ent2.pack(side=tk.LEFT, expand=1, fill="both", padx=5, pady=5)
        
        button22 = tk.Button(self.input22, text="Select source image", command=lambda: self.get_path(1))
        button22.pack(side=tk.LEFT, expand=1, fill="both", padx=5, pady=5)
        button22.configure(background="black", foreground='white', activebackground='#0080ff', activeforeground='white')
        
        self.input31 = tk.LabelFrame(self.tab2, background="black", foreground='white', text=" Image to hide text in ")
        self.input31.pack(expand=1, padx=5, pady=5)

        self.input23 = tk.LabelFrame(self.tab2, bg="black", fg='white', text=" Extracted text ")
        self.input23.pack(expand=1, fill="both", padx=5, pady=5)
        
        self.extracted_message = tk.StringVar()
        self.extracted_message.set('\nExtracted text\n')
        
        textwidget3 = tk.Label(self.input23, textvariable=self.extracted_message, background='black', foreground="white")
        textwidget3.pack(expand=1, fill="both", padx=5, pady=5)
        
        button12 = tk.Button(self.input23, text="Extract text", command=lambda: self.extract())
        button12.pack(side=tk.RIGHT, padx=5, pady=5)
        button12.configure(bg="black", fg='white', activebackground='#0080ff', activeforeground='white')
    # ------------------------------- logic --------------------------------
    def dummy(self):
        pass
  
    def get_path(self, hide_or_extract):
        # Browse button to search for files
        filename = filedialog.askopenfilename(filetypes=(("Template files", "*.png"), ("All files", "*.*") ))
        if hide_or_extract == 0:
            self.target_image_path.set(filename)
        else:
            self.source_image_path.set(filename)


    def active_tab(self):
        return self.notebook.index(self.notebook.select())


    def encode_image(self, img, msg):
        """
        use the red portion of an image (r, g, b) tuple to
        hide the msg string characters as ASCII values
        red value of the first pixel is used for length of string
        """
        length = len(msg)
        # limit length of message to 255
        if length > 255:
            self.status_update("ERROR: text too long! (don't exeed 255 characters)")
            return False
        if img.mode != 'RGB':
            self.status_update("ERROR: image mode needs to be RGB")
            return False
        # use a copy of image to hide the text in
        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index -1]
                    asc = ord(c)
                else:
                    asc = r
                encoded.putpixel((col, row), (asc, g , b))
                index += 1
        return encoded
    
    def decode_image(self, img):
        """
        check the red portion of an image (r, g, b) tuple for
        hidden message characters (ASCII values)
        """
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                try:
                    r, g, b = img.getpixel((col, row))
                except ValueError:
                    # need to add transparency a for some .png files
                    r, g, b, a = img.getpixel((col, row))		
                # first pixel r value is length of message
                if row == 0 and col == 0:
                    length = r
                elif index <= length:
                    msg += chr(r)
                index += 1
        return msg
    
    
    def update(self, event):
        retrieved_text = self.textbox.get("1.0", tk.END)
        self.counter.set('Charcters count: ' + str(len(retrieved_text)) + ' | Max allowed characters = 255')
            
    def hide(self):
        # pick a .png or .bmp file you have in the working directory
        # or give full path name
        original_image_file = self.target_image_path.get()
        img = Image.open(original_image_file)
        # image mode needs to be 'RGB'
        #self.status_update(img, img.mode)
        
        # create a new filename for the modified/encoded image
        # don't exceed 255 characters in the message
        import ntpath
        encoded_image_file = ntpath.split(original_image_file)[0] + "/enc_" + ntpath.basename(original_image_file)
        secret_msg = self.textbox.get("1.0", tk.END)        
        img_encoded = self.encode_image(img, secret_msg)
        
        if img_encoded:
            # save the image with the hidden text
            img_encoded.save(encoded_image_file)
            self.status_update("{} saved!".format(encoded_image_file))
        
            # view the saved file, works with Windows only behaves like double-clicking on the saved file
            #os.startfile(encoded_image_file)
            if sys.platform == "win32":
                os.startfile(encoded_image_file)
            else:
                opener ="open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, encoded_image_file])

    def extract(self):
        # Extract the hidden text back ...
        encoded_image_file = self.source_image_path.get()
        img = Image.open(encoded_image_file)
        hidden_text = self.decode_image(img)
        self.extracted_message.set(hidden_text)
        print("Hidden text:\n{}".format(hidden_text))
    
    def status_update(self, status):
        self.status_message.set(status)
