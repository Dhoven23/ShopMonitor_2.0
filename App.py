###############################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Welcome! you are viewing the source code of the GCU Engineering Shop Activity Monitor
#   Clearly you are here because something isn't working, or because you want to know how it works
#
#   I've used a functional programming style over a strictly OO method, and have used
#   intuitive naming instead of comments but as always,
#   If it ain't broke, feature-creep!
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#   Author: Daniel Hoven (github @Dhoven23/ShopSignIn),
#   email: Daniel.Hoven@gcu.edu
#   Version 1.0.0
#   Date edited: 8/4/2020
#
###############################################################################################

import datetime
import os
import time
from tkinter import *
from tkinter import ttk
import sys
import Data.mongo_setup as mongo
import Service.Reports.generate_report as gen
import Service.Reports.send_email as send
import Service.admin_svc as asv
import Service.data_service as svc
from Data.key import Key
from Service.data_service import log_into_account


def isint(s):  # universal check for integer
    try:
        int(s)
        return True
    except ValueError:
        return False


def popup_message(text, tab):  # universally callable message-display
    def destroy():
        pop.destroy()
        button.destroy()

    message = text
    pop = Text(tab, height=7, width=70)
    pop.insert(END, text)
    pop.pack()
    button = Button(tab, text="Acknowledge", command=destroy)
    button.after(15000, button.destroy)  # destroy popup message after 5 seconds
    pop.after(15000, pop.destroy)
    button.pack()


def popup_create_student(StudentID, window, master):  # add student to mongo
    def student_create(event: object = None):
        name = prompt.get()
        ID = StudentID

        if isint(name) == False:
            student = svc.create_student(ID, str(name))
            svc.log_into_account(StudentID)
            message = "Hello " + name
            popup_message(message, window)
            pop.destroy()

    def delete_entry(event=None):
        prompt.delete(0, END)

    def Capstone():
        pass
        # CapstoneID = Entry(pop, width=35,borderwidth=2).grid(row=3,column=0)
        # Label(pop,text="Capstone\nnumber").grid(row=3,column=1)
        # CapstoneID.bind('<Return>',delete_entry)

    pop = Toplevel()
    x = master.winfo_x()
    y = master.winfo_y()
    v = IntVar()
    pop.geometry("+%d+%d" % (x + 130, y + 70))
    pop.minsize(80, 30)
    prompt = Entry(pop, width=35, borderwidth=2)
    capstone = Button(pop, text='Capstone', command=Capstone).grid(row=2, column=1)
    prompt.insert(0, "Enter your name: ")
    prompt.bind('<ButtonPress>', delete_entry)

    prompt.bind('<Return>', student_create)

    pop.wm_title("New Student")
    warning = Label(pop, text='Student not in database')
    warning.grid(row=0, column=0)
    prompt.grid(row=2, column=0)


def main_login_student_operation(window, master):
    def login(*args, **kwargs):
        StudentID = entry.get()
        entry.delete(0, END)

        if not (((len(StudentID) == 8) | (len(StudentID) == 6)) and isint(StudentID)):
            return
        else:
            message, loggedIn = log_into_account(StudentID)
            if message == f"No student with ID {StudentID}":
                popup_create_student(str(StudentID), window, master)
            else:
                if loggedIn:
                    popup_message(message, window)
                else:
                    student = svc.find_student_by_studentID(StudentID)
                    popup_message(message, window)

    def delete_entry(*args):
        entry.delete(0, END)

    instruction = Label(window, text="Enter Student ID")
    instruction.pack()
    entry = Entry(window, width=55, borderwidth=2)

    entry.bind('<Return>', login)
    entry.bind('<ButtonPress>', delete_entry)
    entry.pack()


def admin_duties(admin, tabStructure, master):  # admin operation
    def whos_in_the_shop(*args):
        messages = asv.whos_in_the_shop()
        text.delete('1.0', END)

        if messages:
            for message in messages:
                text.insert(END, f"-> {message}\n")

        return None

    def logout_all_users(event: object = None):
        Are_you_sure()

    def edit_training(*args2):

        def training(*args0):
            Student = asv.edit_training_level(prompt.get(), train.get())
            if Student:
                pop.destroy()

        def delete_name_entry(*args1):
            prompt.delete(0, END)

        def delete_train_entry(*args):
            train.delete(0, END)

        pop = Toplevel()
        x = master.winfo_x()
        y = master.winfo_y()

        pop.geometry("+%d+%d" % (x + 200, y + 100))
        pop.minsize(80, 30)
        prompt = Entry(pop, width=35, borderwidth=2)
        prompt.insert(0, "Enter Student name: ")
        prompt.bind('<ButtonPress>', delete_name_entry)

        train = Entry(pop, width=35, borderwidth=2)
        train.insert(0, "Enter Key Number: ")
        train.bind('<ButtonPress>', delete_train_entry)

        train.bind('<Return>', training)

        pop.wm_title("Training")

        prompt.grid(row=2, column=0)
        train.grid(row=3, column=0)
        proceed = Button(pop, text="Cancel", fg='red', command=pop.destroy)
        proceed.grid(row=1, column=0)

    def who_was_in_the_shop():
        def delete_entry(event=None):
            DateField.delete(0, END)

        def get_date(event=None):
            prompt.destroy()
            date = DateField.get()
            messages = asv.who_was_in_the_shop(date)
            text.delete('1.0', END)
            if messages:
                for message in messages:
                    text.insert(END, message[0:23] + (50 - len(message)) * '.' + message[23:(len(message) + 1)])
            else:
                text.insert(END,
                            f"No record exists for {date}, make sure entry \nhas format YYYY-MM-DD. ex: 2020-07-01\n")

        DateField.insert(0, 'YYYY-MM-DD')
        DateField.bind('<ButtonPress>', delete_entry)
        prompt = Label(admin, text="Please enter the day")
        DateField.bind('<Return>', get_date)
        prompt.grid(column=0, row=6)

    def add_tool(*args, **kwargs4):

        def adding_tool(*args2, **kwargs3):
            svc.CreateTool(number.get(), name.get())
            pop.destroy()

            build_keys_tab(tabStructure)

        def delete_name_entry(*args3, **kwargs2):
            name.delete(0, END)

        def delete_number_entry(*args4, **kwargs1):
            number.delete(0, END)

        pop = Toplevel()
        x = master.winfo_x()
        y = master.winfo_y()

        pop.geometry("+%d+%d" % (x + 200, y + 100))
        pop.minsize(80, 30)
        name = Entry(pop, width=35, borderwidth=2)
        name.insert(0, "Enter Machine Name: ")
        name.bind('<ButtonPress>', delete_name_entry)

        number = Entry(pop, width=35, borderwidth=2)
        number.insert(0, "Enter Key Number: ")
        number.bind('<ButtonPress>', delete_number_entry)

        number.bind('<Return>', adding_tool)

        pop.wm_title("Tools")

        name.grid(row=2, column=0)
        number.grid(row=3, column=0)
        proceed = Button(pop, text="Cancel", fg='red', command=pop.destroy)
        proceed.grid(row=1, column=0)

    text = Text(admin, height=15, width=50)
    DateField = Entry(admin, width=25, borderwidth=3)
    button1 = Button(admin, text="Who's In the Shop?", width=25, command=whos_in_the_shop)
    button2 = Button(admin, text="Signout All", width=25, command=logout_all_users)
    button3 = Button(admin, text="Blame", width=25, command=who_was_in_the_shop)
    button4 = Button(admin, text="Edit Training", width=25, command=edit_training)
    button5 = Button(admin, text="Add Key", width=25, command=add_tool)
    button1.grid(column=0, row=1)
    button2.grid(column=0, row=2)
    button3.grid(column=0, row=3)
    button4.grid(column=0, row=4)
    button5.grid(column=0, row=5)
    text.grid(column=1, row=1, rowspan=10, columnspan=2)
    DateField.grid(column=0, row=7)


def build_login_tab(tabStructure, master):
    login = ttk.Frame(tabStructure)

    tabStructure.add(login, text="login")

    main_login_student_operation(login, master)


def Are_you_sure():  # simple yes/no for logout-all
    def do_yes():
        asv.logout_all_users()
        question.destroy()

    def do_no():
        question.destroy()

    question = Toplevel()
    question.wm_title("Confirm")

    prompt = Label(question, text='Are You Sure?')
    yes = Button(question, text='YES', width=30, fg='green', command=do_yes)
    no = Button(question, text='NO', width=30, fg='red', command=do_no)
    prompt.pack()
    yes.pack()
    no.pack()
    question.geometry('210x75')


def build_admin_tab(tabStructure, master):
    admin = ttk.Frame(tabStructure)

    tabStructure.add(admin, text="admin")

    admin_duties(admin, tabStructure, master)


def checkout_tool(keyNumber):
    def check_training(*args):
        StudentID = ID.get()
        student = svc.find_student_by_studentID(StudentID)

        for number in student.keys_trained:
            if int(number) == int(keyNumber):
                alert = Toplevel()
                alert.geometry("230x80")
                alert.wm_title("Checkout Successful")
                confirm = Label(alert, text="You're good to go!", font='Helvetica 14 bold', fg='green')
                confirm.pack(anchor=CENTER)
                Button(alert, text='Confirm', command=alert.destroy).pack()
                checkout.destroy()
                return

        alert = Toplevel()
        alert.geometry("230x80")
        alert.wm_title("Checkout Unsuccessful")
        confirm = Label(alert, text="You are not cleared \nto use this key", font='Helvetica 14 bold', fg='red')
        confirm.pack(anchor=CENTER)
        Button(alert, text='Confirm', command=alert.destroy).pack()
        checkout.destroy()
        return

    checkout = Toplevel()
    Instruction = Label(checkout, text='Please Enter your StudentID').pack(side=TOP)
    ID = Entry(checkout, width=35, borderwidth=2)
    ID.bind('<Return>', check_training)
    ID.pack()


class KeyButton:

    def __init__(self, master, x, y, number):
        def Onclick():
            tool = Key.objects(keyNumber=number).first()
            checkout_tool(tool.keyNumber)

        if svc.key_exists(number):
            self.button = Button(master, text=str(number), bg='green', width=10, height=2, command=Onclick)
            self.button.grid(column=x, row=y)


def build_keys_tab(tabStructure):
    keys = ttk.Frame(tabStructure)
    Key_Buttons_list_function(keys)

    tabStructure.add(keys, text="Keys")


def Key_Buttons_list_function(tools):
    number = 1
    for y in range(1, 7):
        for x in range(1, 7):
            # noinspection PyTypeChecker
            KeyButton.__init__(KeyButton, tools, x, y, number)
            number += 1


class ToolLabel:
    def __init__(self, master, message):
        out = message.split(' ')

        def checkout(event=None):

            tool = svc.find_tool(out[0], out[1])
            if tool:
                print(tool.name)

        def green_text(event=None):
            self.label.config(fg='green')

        def black_text(event=None):
            self.label.config(fg='black')

        def cleer(event=None):
            self.label.destroy()

        self.label = Label(master, text=message)
        self.label.pack()
        self.label.bind("<Button-1>", checkout)
        self.label.bind("<Enter>", green_text)
        self.label.bind("<Leave>", black_text)


def tools_tab_functions(tools, tabStructure, master):
    def printing(event=None):
        text = toolName.get()
        messages = svc.lookup_tool(text)

        for message in messages:
            ToolLabel.__init__(ToolLabel,tools, message)

    instruction = Label(tools, text='Name of Tool').pack()
    toolName = Entry(tools, width=50, borderwidth=2)
    toolName.bind('<Return>', printing)
    toolName.pack()


def buils_tools_tab(tabStructure, master):
    tools = ttk.Frame(tabStructure)
    tabStructure.add(tools, text="Tools")
    tools_tab_functions(tools, tabStructure, master)
    pass


def build_all_the_tabs_admin(master):
    tabStructure = ttk.Notebook(master)

    build_login_tab(tabStructure, master)
    build_admin_tab(tabStructure, master)
    build_keys_tab(tabStructure)
    buils_tools_tab(tabStructure, master)

    tabStructure.pack(expand=1, fill='both')


class app:  # constructor for GUI
    def __init__(self, master):
        self.master = master

        def onExit():
            master.quit()

        def generate():
            gen.generate()

        def send_weekly_report():
            send.send_weekly_report()

        master.title("Shop Activity Monitor")
        master.geometry("640x320")
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        fileMenu.add_command(label="Create Report", command=generate)
        fileMenu.add_command(label="Send last Report", command=send_weekly_report)

        self.statusbar = Label(master, text="", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)
        build_all_the_tabs_admin(master)
        self.update()

    def update(self):
        date = 'Today is: ' + svc.print_day() + f", time: " \
                                                f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute} "

        self.statusbar.config(text=str(date))
        self.statusbar.after(1000, self.update)


def login():
    def check(*args):
        os.environ['USER'] = user_entry.get()
        os.environ['PASSWORD'] = password_entry.get()
        mongo.global_init(os.environ.get('USER'), os.environ.get('PASSWORD'))
        log.destroy()

    log = Tk()
    log.title("User Login")
    log.geometry("280x140")
    instruction = Label(log, text='Please enter your database credentials', font='Helvetica').grid(row=0, column=0,
                                                                                                   columnspan=2)
    user_entry = Entry(log, width=25, borderwidth=1)
    user_entry.grid(row=1, column=1)
    user_instruction = Label(log, text='Username')
    user_instruction.grid(row=1, column=0)
    password_entry = Entry(log, width=25, borderwidth=1)
    password_entry.grid(row=2, column=1)
    password_instruction = Label(log, text='Password')
    password_instruction.grid(row=2, column=0)
    attempt = Button(log, text='GO', font='Helvetica', width=15, command=check)
    attempt.grid(row=3, column=0, columnspan=2)
    log.mainloop()


def login_error():
    def ok():
        error.destroy()
        login()

    def cancel():
        error.quit()
        sys.exit()

    error = Tk()
    error.geometry("260x100")
    Label(error, text='Invalid Login\n Please try again', font='Helvetica', fg='red').pack()
    Button(error, text='Ok', width=15, command=ok, fg='green').pack()
    Button(error, text='Cancel', width=15, command=cancel, fg='red').pack()
    error.mainloop()


def main():  # run the app

    login()

    while True:
        try:
            svc.print_day()
        except:
            mongo.global_disconnect()
            login_error()

        else:
            break

    root = Tk()
    app(root)
    root.mainloop()
