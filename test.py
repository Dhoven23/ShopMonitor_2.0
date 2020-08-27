# importing tkinter module
from tkinter import *
import tkinter as tk
from tkinter.ttk import *


def windowe(root):
    def bar():
        for i in range(0, 1000):
            progress['value'] = 0.1 * i
            root.update_idletasks()
        root.destroy()

    progress = Progressbar(root, orient=HORIZONTAL,
                           length=100, mode='determinate')
    label = tk.Label(root, text='Success!', font='Helvetica 14 bold', fg='green').pack()
    progress.pack(pady=10)
    tk.Button(root, text='GO', font='Arial 14 bold', command=bar).pack()
# creating tkinter window
root = Tk()
windowe(root)
# Progress bar widget



# Function responsible for the updation
# of the progress bar value







mainloop()
