from tkinter import *
import os


root = Tk()
root.title("User Login")
root.geometry("280x140")
instruction = Label(root, text='Please enter your database credentials',font='Helvetica').grid(row=0,column=0, columnspan=2)
user_entry = Entry(root, width = 25, borderwidth=1).grid(row=1,column=1)
user_instruction = Label(root, text='Username').grid(row=1,column=0)
password_entry = Entry(root, width = 25, borderwidth=1).grid(row=2,column=1)
password_instruction = Label(root, text='Password').grid(row=2,column=0)
root.mainloop()

user = input('Enter your Username \n->')
os.environ['USER'] = user
password = input('Enter your Password\n->')
os.environ['PASSWORD'] = password
print(os.environ.get('USER'))
print(os.environ.get('PASSWORD'))

