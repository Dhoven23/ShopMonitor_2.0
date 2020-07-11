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
#   Author: Daniel Hoven (github @DHoven23),
#   email: Daniel.Hoven@gcu.edu
#   Version 0.0.2
#   Date of commit: 7/10/2020
#
###############################################################################################

from tkinter import *
from tkinter import ttk
import Data.mongo_setup as mongo
import Service.data_service as svc
from Service.data_service import log_into_account
import Service.admin_svc as asv
import Service.Reports.generate_report as gen
import Service.Reports.send_email as send
import datetime


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
    pop = Label(tab, text=message)

    pop.pack()
    button = Button(tab, text="Acknowledge", command=destroy)
    button.after(5000, button.destroy)  # destroy popup message after 5 seconds
    pop.after(5000, pop.destroy)
    button.pack()


def popup_create_student(StudentID, window):  # add student to mongo
    def student_create(event: object = None):
        name = prompt.get()
        ID = StudentID
        pop.destroy()

        svc.create_student(ID, str(name))
        svc.log_into_account(StudentID)
        message = "Hello " + name
        popup_message(message, window)

    def delete_entry(event=None):
        prompt.delete(0, END)

    pop = Toplevel()
    pop.minsize(80, 30)
    prompt = Entry(pop, width=35, borderwidth=2)
    prompt.insert(0, "Enter your name: ")
    prompt.bind('<ButtonPress>', delete_entry)

    prompt.bind('<Return>', student_create)

    pop.wm_title("New Student")
    warning = Label(pop, text='Student not in database')
    warning.grid(row=0, column=0)
    prompt.grid(row=2, column=0)

    proceed = Button(pop, text="Acknowledge", command=pop.destroy)
    proceed.grid(row=1, column=0)


def main_login_student_operation(window):  # login/out student if in mongo
    def login(event: object = None):
        StudentID = entry.get()
        entry.delete(0, END)
        entry.insert(0, "Enter your ID: ")
        if not ((len(StudentID) == 8) and isint(StudentID)):
            return
        else:
            message, loggedIn = log_into_account(StudentID)
            if message == f"No student with ID {StudentID}":
                popup_create_student(str(StudentID), window)
            else:
                if loggedIn:
                    popup_message(message,window)
                else:
                    student = svc.find_student_by_studentID(StudentID)
                    popup_message(message + f'\n You are a level {student.training_Level} user', window)

    def delete_entry(event=None):
        entry.delete(0, END)

    instruction = Label(window, text="Enter Student ID")
    instruction.pack()
    entry = Entry(window, width=75, borderwidth=2)
    entry.insert(0, "Enter your ID: ")
    entry.bind('<Return>', login)
    entry.bind('<ButtonPress>', delete_entry)
    entry.pack()


def isadmin():
    global Master
    if Master:
        return True
    else:
        return False


def admin_duties(admin):  # admin operation
    def whos_in_the_shop(event=None):
        messages = asv.whos_in_the_shop()
        text.delete('1.0', END)

        if messages:
            for message in messages:
                text.insert(END, f"-> {message}\n")

        return None

    def logout_all_users(event: object = None):
        Are_you_sure()

    def edit_training(event=None):

        def training(event=None):
            Student = asv.edit_training_level(prompt.get(),train.get())
            if Student:
                pop.destroy()

        def delete_name_entry(event=None):
            prompt.delete(0, END)
        def delete_train_entry(event=None):

            train.delete(0,END)


        pop = Toplevel()
        pop.minsize(80, 30)
        prompt = Entry(pop, width=35, borderwidth=2)
        prompt.insert(0, "Enter Student name: ")
        prompt.bind('<ButtonPress>', delete_name_entry)

        train = Entry(pop, width=35, borderwidth=2)
        train.insert(0,"Enter training level: ")
        train.bind('<ButtonPress>', delete_train_entry)

        train.bind('<Return>', training)

        pop.wm_title("Training")

        prompt.grid(row=2, column=0)
        train.grid(row=3,column=0)
        proceed = Button(pop, text="Cancel", fg='red' ,command=pop.destroy)
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
                    text.insert(END, message[0:24] + (50 - len(message)) * '.' + message[25:(len(message) + 1)])
            else:
                text.insert(END,
                            f"No record exists for {date}, make sure entry \nhas format YYYY-MM-DD. ex: 2020-07-01\n")

        DateField.insert(0, 'YYYY-MM-DD')
        DateField.bind('<ButtonPress>', delete_entry)
        prompt = Label(admin, text="Please enter the day")
        DateField.bind('<Return>', get_date)
        prompt.pack(side=BOTTOM)

    text = Text(admin, height=6, width=50)
    DateField = Entry(admin, width=50, borderwidth=3)
    button1 = Button(admin, text="Who's In the Shop?", width=35, command=whos_in_the_shop)
    button2 = Button(admin, text="Signout All", width=35, command=logout_all_users)
    button3 = Button(admin, text="Blame", width=35, command=who_was_in_the_shop)
    button4 = Button(admin, text="Edit Training", width=35, command=edit_training)
    button1.pack()
    button2.pack()
    button3.pack()
    button4.pack()
    text.pack()
    DateField.pack(side=BOTTOM)


def build_login_tab(tabStructure):
    login = ttk.Frame(tabStructure)

    tabStructure.add(login, text="login")

    main_login_student_operation(login)


def Are_you_sure():  # simple yes/no for logout-all
    def do_yes():
        asv.logout_all_users()
        question.destroy()

    def do_no():
        question.destroy()

    question = Toplevel()
    question.wm_title("Confirm")

    prompt = Label(question, text='Are You Sure?')
    yes = Button(question, text='YES', width=30, fg='green',command=do_yes)
    no = Button(question, text='NO', width=30, fg='red',command=do_no)
    prompt.pack()
    yes.pack()
    no.pack()
    question.geometry('210x75')


def build_admin_tab(tabStructure):
    admin = ttk.Frame(tabStructure)

    tabStructure.add(admin, text="admin")

    admin_duties(admin)


def build_tools_tab(tabStructure):
    def tool_key(number, event=None):
        print(number)
        pass

    d = {}
    tools = ttk.Frame(tabStructure)
    for x in range(1, 6):
        for y in range(1, 6):
            d["button{0}".format(x * y)] = Button(tools, text=str(x * y), command=lambda: tool_key(x * y),
                                                  width=13, height=2).grid(row=x, column=y)

    tabStructure.add(tools, text="Tools")


def build_all_the_tabs_admin(master):
    tabStructure = ttk.Notebook(master)

    build_login_tab(tabStructure)
    build_admin_tab(tabStructure)
    build_tools_tab(tabStructure)

    tabStructure.pack(expand=1, fill='both')


def build_all_the_tabs(master):
    tabStructure = ttk.Notebook(master)

    build_login_tab(tabStructure)

    build_tools_tab(tabStructure)

    tabStructure.pack(expand=1, fill='both')


class app:  # constructor for GUI
    def __init__(self, master):
        self.master = master
        global Master
        Master = False

        def onExit():
            master.quit()

        def generate():
            gen.generate()

        def send_weekly_report():
            send.send_weekly_report()

        def LoginAsAdmin():
            global Master
            Master = True
            build_all_the_tabs(master)

        master.title("Shop Activity Monitor")
        master.geometry("500x320")
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


def main():  # run the app

    date = 'Today is: ' + svc.print_day() + ", time: %s:%s" % (
        datetime.datetime.now().hour, datetime.datetime.now().minute)
    root = Tk()
    root.iconbitmap('app.ico')
    app(root)

    root.mainloop()


if __name__ == '__main__':
    mongo.global_init()  # always include this function call to connect to mongoDB
    main()
