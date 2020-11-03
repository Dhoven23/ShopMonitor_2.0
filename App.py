####################################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#   Welcome! you are viewing the source code of the GCU Engineering Shop Activity Monitor          #
#   Clearly you are here because something isn't working, or because you want to know how it works #
#                                                                                                  #
#   I've used a functional programming style over a strictly OO method, and have used              #
#   intuitive naming instead of comments but as always,                                            #
#   If it ain't broke, feature-creep!                                                              #
#                                                                                                  #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                                                                                                  #
#   Author: Daniel Hoven (github @Dhoven23/ShopSignIn),                                            #
#   email: Daniel.Hoven@gcu.edu                                                                    #
#   Version 1.0.0                                                                                  #
#   Date edited: 8/4/2020                                                                          #
#                                                                                                  #
####################################################################################################

from datetime import datetime, timedelta
import os

import weakref
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sys
import Data.mongo_setup as mongo
from Plotting.activity import plotins
import Service.admin_svc as asv
import Service.data_service as svc
from Data.key import Key



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
    pop = Text(tab, height=7, width=55)
    pop.insert(END, text)
    pop.grid(column=1,row=2)
    button = Button(tab, text="Acknowledge", command=destroy)
    button.after(5000, button.destroy)  # destroy popup message after 5 seconds
    pop.after(15000, pop.destroy)
    button.grid(column=1,row=3)


def popup_create_student(StudentID, window, master):  # add student to mongo
    def student_create(event: object = None):
        name = prompt.get()
        for n in name:
            if n.isalnum() or (n == ' '):
                pass
            else:
                Label(pop,text='Special Characters Not allowed!',fg='red').grid(row=5,column=0)
                return
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
        def insert_capstoneID():
            value = int(get_cell_equals(str(prompt.get())))
            CapstoneID.insert(END, value)
        def capstone_student_create(event: object = None):
            name = prompt.get()
            ID = StudentID

            if isint(name) == False:
                C_Number = CapstoneID.get()
                print(str(C_Number), str(name))
                student = svc.create_capstone_student(ID, str(name), str(C_Number))
                svc.log_into_account_capstone(StudentID)
                pop.destroy()

        from Service.Reports.CapstoneProjects import get_cell_equals

        CapstoneID = Entry(pop, width=35,borderwidth=2)
        CapstoneID.grid(row=3,column=0)
        Label(pop,text="Capstone\nnumber").grid(row=3,column=1)
        insert_capstoneID()
        prompt.bind('<Tab>',insert_capstoneID)
        Bo = Button(pop,text='Create new\nCapstone Student',command=capstone_student_create)
        Bo.grid(row=4,column=0,columnspan=2)


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
            message, loggedIn = svc.log_into_account(StudentID)
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

    instruction = Label(window, text="Enter Student ID", font='Helvetica 12 bold', fg='purple4',bg='grey86')
    instruction.grid(column=1,row=0)
    entry = Entry(window, width=35, borderwidth=2, font='Helvetica 16')
    Label(window,text='             ',font='Arial 16 bold',bg='grey86').grid(column=0,row=1)
    entry.bind('<Return>', login)
    entry.bind('<ButtonPress>', delete_entry)
    entry.grid(column=1,row=1)
    #print(f'{round(time.clock(),4)}: - - - - - Login Functions Written')

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

    def delete_entry(event=None):
        DateField.delete(0, END)

    def tools_past_due(event=None):
        message = asv.PastDueTools()
        text.delete('1.0', END)
        if message:
            for mess in message:
                text.insert(END,mess)


    def get_date(event=None):

        date = DateField.get()
        messages = asv.who_was_in_the_shop(date)
        text.delete('1.0', END)
        if messages:

            for message in messages:
                mess = message.split('|')
                mess1 = str(mess[0])
                text.insert(END, mess1[0:23] + (50 - len(mess[0])) * '.' + mess1[23:(len(mess[0]) + 1)] + mess[1])
        else:
            text.insert(END,
                        f"No record exists for {date}, make sure entry \nhas format YYYY-MM-DD. ex: 2020-07-01\n")


    def plot_graphs(*args, **kwargs4):
        plotins()


    def Today():
        today=datetime.now().date()
        DateField.delete(0,END)
        DateField.insert(0,str(today))
        global date_memory
        date_memory = today
        get_date()

    def next_day():
        global date_memory
        step = timedelta(days=+1)
        date_memory = date_memory + step
        DateField.delete(0, END)
        DateField.insert(0, str(date_memory))
        get_date()


    def prev_day():
        global date_memory
        step = timedelta(days=-1)
        date_memory = date_memory + step
        DateField.delete(0, END)
        DateField.insert(0, str(date_memory))
        get_date()

    def add_capstone_id(event=None):

        def add_number():
            ID = str(E.get())
            student = svc.find_student_by_studentID(ID)

            student.capstoneID = str(E2.get())
            student.save()
            pop.destroy()
        pop = Toplevel()
        pop.minsize(300,120)
        Label(pop, text = 'Please Enter Student ID', font = 'Helvetica 14 bold', fg='Purple3').pack()
        E = Entry(pop, width=10, font = 'Helvetica 14')
        E.pack()
        Label(pop, text='Please Enter Capstone ID', font='Helvetica 14 bold', fg='Purple3').pack()
        E2 = Entry(pop, width=10, font='Helvetica 14')
        E2.pack()
        B = Button(pop, text='Submit!', font = 'helvetica 14 bold', fg='green', command=add_number).pack()



    text = Text(admin, height=15, width=50)
    DateField = Entry(admin, font='Arial 14 bold',width=10, borderwidth=3)
    button1 = Button(admin, text="Who's In the Shop?", width=25, command=whos_in_the_shop)
    button2 = Button(admin, text="Signout All", width=25, command=logout_all_users)
    button3 = Button(admin, text="Blame", width=25, command=tools_past_due)
    button4 = Button(admin, text="Edit Training", width=25, command=edit_training)
    button5 = Button(admin, text="Plot Graphs", width=25, command=plot_graphs)
    button6 = Button(admin, text="Add Capstone ID", width=25, command=add_capstone_id)
    button1.grid(column=0, row=1, columnspan=3)
    button2.grid(column=0, row=2, columnspan=3)
    button3.grid(column=0, row=3, columnspan=3)
    button4.grid(column=0, row=4, columnspan=3)
    button5.grid(column=0, row=5, columnspan=3)
    button6.grid(column=0, row=6, columnspan=3)
    Button(admin, text='<', bg='gray50',command=prev_day).grid(column=0,row=8,sticky=W+E)
    Button(admin, text='Today',command=Today).grid(column=1,row=8,sticky=W+E)
    Button(admin, text='>', bg='gray50',command=next_day).grid(column=2, row=8, sticky=W + E)
    text.grid(column=3, row=1, rowspan=10, columnspan=2)
    DateField.grid(column=1, row=7)
    DateField.bind('<Return>',get_date)
    #print(f'{round(time.clock(),4)}: - - - - - Admin functions Written')

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


def checkout_Machine_Key(keyNumber, root):
    arg = BooleanVar()
    arg = True
    X = root.winfo_x()
    Y = root.winfo_y()

    def check_training(*args):
        StudentID = ID.get()
        student = svc.find_student_by_studentID(StudentID)

        for number in student.keys_trained:
            if int(number) == int(keyNumber):
                alert = Toplevel()
                alert.geometry("+%d+%d" % (X+225, Y+75))
                alert.wm_title("Checkout Successful")
                confirm = Label(alert, text="You're good to go!", font='Helvetica 14 bold', fg='green')
                confirm.pack(anchor=CENTER)
                Button(alert, text='Confirm', command=alert.destroy).pack()
                checkout.destroy()
                arg = True
                return

        alert = Toplevel()
        alert.geometry("+%d+%d" % (X+225, Y+75))
        alert.wm_title("Checkout Unsuccessful")
        confirm = Label(alert, text="You are not cleared \nto use this key", font='Helvetica 14 bold', fg='red')
        confirm.pack(anchor=CENTER)
        Button(alert, text='Confirm', command=alert.destroy).pack()
        checkout.destroy()
        arg = False
        return

    checkout = Toplevel()
    checkout.geometry("+%d+%d" % (X+150, Y+75))
    checkout.minsize(320,140)
    checkout.config(bg='purple1')
    Instruction = Label(checkout, text='Please Enter your StudentID', font='Arial 12 bold', fg='white',bg='purple1').pack(side=TOP)
    ID = Entry(checkout, width=25, borderwidth=2, font = 'Helvetica 14')
    ID.bind('<Return>', check_training)
    ID.pack()
    if arg == True:
        return 'green'
    else:
        return 'red'



class KeyButton:

    def __init__(self, master, x, y, number, root, name, color):
        def Onclick():

            if self.button["bg"] == color:
                self.button["bg"] = "grey86"
                key = Key.objects(keyNumber=number).first()
                result = checkout_Machine_Key(key.keyNumber, root)

            else:
                self.button["bg"] = color
                pop = Toplevel()
                pop.geometry("300x140")
                pop.minsize(320,140)
                Label(pop, text='Key Successfully Returned\n'
                                'Please Ensure Machine is Clean', font='Arial 14 bold', fg='MediumPurple3').pack()
                Button(pop, text='Accept', font='Helvetica 16 bold', fg='green',command=pop.destroy).pack()



        if svc.key_exists(number):
            self.button = Button(master, text=str(number) + '\n' + name, bg=color,width=15, height=2, command=Onclick)
            self.button.grid(column=x, row=y)


def build_keys_tab(tabStructure, root):

    keys = ttk.Frame(tabStructure)
    Key_Buttons_list_function(keys,root)

    tabStructure.add(keys, text="Keys")


def Key_Buttons_list_function(keys, root):
    from Data.KeysList import RM131_keys, RM130_keys, RM132_keys

    keys.grid()
    key1 = KeyButton(keys,1,1,1,root,RM130_keys[1], 'MediumPurple1')
    key2 = KeyButton(keys,2,1,2,root,RM130_keys[2], 'MediumPurple1')
    key3 = KeyButton(keys,3,1,3,root,RM130_keys[3], 'MediumPurple1')
    key4 = KeyButton(keys,4,1,4,root,RM130_keys[4], 'MediumPurple1')
    key5 = KeyButton(keys,5,1,5,root,RM130_keys[5], 'MediumPurple1')
    key6 = KeyButton(keys,1,2,6,root,RM130_keys[6], 'MediumPurple1')
    key7 = KeyButton(keys,2,2,7,root,RM130_keys[7], 'MediumPurple1')
    key8 = KeyButton(keys,3,2,8,root,RM130_keys[8], 'MediumPurple1')
    key9 = KeyButton(keys,4,2,9,root,RM130_keys[9], 'MediumPurple1')
    key10 =KeyButton(keys,5,2,10,root,RM130_keys[10],'MediumPurple1')
    key11 =KeyButton(keys,1,3,11,root,RM130_keys[11],'MediumPurple1')
    key11 = KeyButton(keys, 2, 3, 12, root, RM130_keys[12], 'MediumPurple1')

    key13 = KeyButton(keys,3,3,13,root,RM132_keys[13],'orange red')
    key14 = KeyButton(keys,4,3,14,root,RM132_keys[14],'orange red')
    key15 = KeyButton(keys, 5, 3, 15, root, RM132_keys[15], 'orange red')
    key16 = KeyButton(keys, 1, 4, 16, root, RM132_keys[16], 'orange red')
    key17 = KeyButton(keys, 2, 4, 17, root, RM132_keys[17], 'orange red')
    key18 = KeyButton(keys, 3, 4, 18, root, RM132_keys[18], 'orange red')
    key19 = KeyButton(keys, 4, 4, 19, root, RM132_keys[19], 'orange red')
    key20 = KeyButton(keys, 5, 4, 20, root, RM132_keys[20], 'orange red')
    key21 = KeyButton(keys, 1, 5, 21, root, RM132_keys[21], 'orange red')

    key22 = KeyButton(keys, 2, 5, 22, root, RM131_keys[22], 'bisque')
    key23 = KeyButton(keys, 3, 5, 23, root, RM131_keys[23], 'bisque')
    key24 = KeyButton(keys, 4, 5, 24, root, RM131_keys[24], 'bisque')
    key25 = KeyButton(keys, 5, 5, 25, root, RM131_keys[25], 'bisque')
    key26 = KeyButton(keys, 1, 6, 26, root, RM131_keys[26], 'bisque')



def Checkout_tool(x, y, toolname):

    def checkout():
        ID = e.get()
        ReturnDate = date.get()
        svc.Checkout_tool(toolname, ID, ReturnDate)
        pop.destroy()

    pop = Toplevel()
    pop.geometry("+%d+%d" % (x+280, y+75))
    pop.minsize(350,240)
    pop.title(f'Checkout {toolname.name} {toolname.size}')
    i = Label(pop, text='Enter Student ID', font = 'Arial 14 bold')
    e = Entry(pop, font='Helvetica 12', width=25)
    space = Label(pop, text ='', font = 'Arial 10')
    i.pack()
    e.pack()
    space.pack()
    date_instruction = Label(pop, text='Return Date', font='Arial 14 bold')
    date_instruction.pack()
    date = Entry(pop, font='Helvetica 12', width=25)
    date.pack()
    Label(pop, text=' ', font='Arial 10').pack()
    Button(pop,text='OK', width=20,font='Helvetica 12 bold',fg='green',command =checkout).pack()
    Button(pop, text='Cancel', width=20, font='Helvetica 12 bold', fg='red', command = lambda: pop.destroy()).pack()


def Return_Tool(x, y, toolname):
    def retern():
        ID = E.get()
        if isint(ID) and (len(ID)==8):
            print(toolname.name + toolname.size)
            svc.Return(toolname, ID)
        pop.destroy()

    pop = Toplevel()
    pop.geometry("+%d+%d" % (x + 280, y + 75))
    pop.minsize(220,140)
    I = Label(pop, text='Confirm Student ID', font='Helvetica 14 bold')
    I.pack()
    E = Entry(pop, width=35, borderwidth=2, font='Helvetica 12')
    E.pack()
    Label(pop, text='  ', font='Arial 14').pack()
    B = Button(pop, width=20, text='Return Tool', font='Arial 14 bold', fg = 'green', command=retern).pack()

class ToolLabel:

    _instances = set()
    def __init__(self, master, message, n, root, col, returner):

        message = message.split(',')


        def Onclick1(*args):
            x = root.winfo_x()
            y = root.winfo_y()

            tool = svc.find_tool(message[0], message[1])
            self.button.destroy()
            Checkout_tool(x, y, tool)

        def Onclick2(*args):
            x = root.winfo_x()
            y = root.winfo_y()
            self.button.destroy()
            tool = svc.find_tool(message[0], message[1])
            Return_Tool(x, y, tool)



        if returner==False:
            self.button = ttk.Button(master, text=f"{message[0]}\n{message[1]}", command=Onclick1, style='flat.TButton')
        else:
            self.button = ttk.Button(master, text=f"{message[0]}\n{message[1]}", command=Onclick2, style='flat.TButton')


        self.button.grid(row=n, column=col,sticky=W + E)
        self._instances.add(weakref.ref(self))

    def clear(self,event=None):
        self.button.destroy()

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead



def tools_tab_functions(tools, root, tabStructure):
    def ActiveToolSearch(event=None):
        text = toolName.get()
        toolname = text.split(',')
        temp = toolname[0].split(' ')
        print('Toolname : ',toolname)
        print('temp : ', temp)
        text = ''
        for t in temp:
            if text:
                text = text + '-' + t
            else:
                text = t
        name = text
        size = ''
        if len(toolname) > 1:
            size = toolname[1].strip()


        messages = svc.lookup_tool(name, size)
        n = IntVar()
        n = 2
        destroy()
        toolName.bind('<Tab>')
        col = 0
        for message in messages:
            if n > 9:
                col = col + 1
                n = 2
            if col == 3:
                return
            toolLabel = ToolLabel(tools, message, n, root, col, False)
            n += 1

    def ActiveToolReturn(event=None):
        StudentID = return_ID.get()

        message = svc.FindCheckedOutTools(StudentID)
        n=2
        destroy()
        if message:
            for mess in message:
                toolLabel = ToolLabel(tools, mess, n, root, 4, True)
                n+=1



    def destroy():
        for model in ToolLabel.getinstances():
            model.clear()


    instruction = Label(tools, text='Name of Tool\n(For tool checkout)', font='Helvetica 14 bold', bg='MediumPurple1',fg='white').grid(row=0,columnspan=3, sticky=N+S+W+E)

    toolName = Entry(tools, width=30, borderwidth=2, font='Arial 12')
    toolName.bind('<Key>', ActiveToolSearch)

    toolName.grid(row=1, columnspan=3,sticky=W + E)
    return_instruction = Label(tools, text='Student_ID\n(For tool return)', font='Helvetica 14 bold', bg='MediumPurple1', fg='white')
    return_ID = Entry(tools, width=30, borderwidth=2, font='Arial 12')
    return_ID.bind('<Return>', ActiveToolReturn)
    return_instruction.grid(row=0,column=4, sticky=W+E)
    color=root.cget('bg')
    Label(tools, text='-------', font='Cambrian 13',fg=color,bg='seashell2').grid(row=1,column=3)
    return_ID.grid(row=1,column=4)
    #print(f'{round(time.clock(),4)}: - - - - - Tools tab functions built')

def buils_tools_tab(tabStructure, master):


    tools = ttk.Frame(tabStructure)

    tabStructure.add(tools, text="Tools")
    tools_tab_functions(tools, master, tabStructure)



def build_all_the_tabs_admin(master):
    s = ttk.Style()
    s.configure('base.TNotebook', background='white')
    tabStructure = ttk.Notebook(master, style='base.TNotebook')


    build_login_tab(tabStructure, master)
    #print(f'{round(time.clock(),4)}: - - - - - Login Tab built')
    build_admin_tab(tabStructure, master)
    #print(f'{round(time.clock(),4)}: - - - - - Admin Tab built')
    build_keys_tab(tabStructure, master)
    #print(f'{round(time.clock(),4)}: - - - - - keys Tab built')
    buils_tools_tab(tabStructure, master)
    #print(f'{round(time.clock(),4)}: - - - - - Tools Tab built')

    tabStructure.pack(expand=1, fill='both')
    #print(f'{round(time.clock(),4)}: - - - - - Tabstructure built')


class app:  # constructor for GUI
    def __init__(self, master):
        self.master = master

        def onExit():
            master.quit()


        master.title("Shop Activity Monitor")
        master.geometry("600x300")
        styles = ttk.Style(master)
        styles.theme_use('clam')
        styles.configure('flat.TButton', borderwidth=0,font='Helvetica 8')
        styles.configure('green.TButton', foreground='green', borderwidth=0)
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        #fileMenu.add_command(label="Create Report", command=generate)
        #fileMenu.add_command(label="Send last Report", command=send_weekly_report)

        self.statusbar = Label(master, text="", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)
        build_all_the_tabs_admin(master)
        self.update()

    def update(self):
        date = 'Today is: ' + svc.print_day() + f", time: " \
                                                f"{datetime.now().hour}:{datetime.now().minute} "

        self.statusbar.config(text=str(date))
        self.statusbar.after(1000, self.update)


def login():
    def check(*args):
        os.environ['USER'] = user_entry.get()
        os.environ['PASSWORD'] = password_entry.get()
        mongo.global_init(os.environ.get('USER'), os.environ.get('PASSWORD'))
        #print(f'{round(time.clock(),4)}: - - - - - Connected to Cloud')
        log.destroy()

    log = Tk()
    log.title("User Login")
    log.geometry("280x140")
    instruction = Label(log, text='Please enter your database credentials', font='Helvetica').grid(row=0, column=0,
                                                                                                   columnspan=2)
    user_entry = Entry(log, width=25, borderwidth=1)
    user_entry.grid(row=1, column=1)
    user_entry.insert(0,'DHoven')
    user_instruction = Label(log, text='Username')
    user_instruction.grid(row=1, column=0)
    password_entry = Entry(log, width=25, borderwidth=1)
    password_entry.grid(row=2, column=1)
    password_entry.insert(0, '12345')
    password_instruction = Label(log, text='Password')
    password_instruction.grid(row=2, column=0)
    attempt = Button(log, text='GO', font='Helvetica', width=15, command=check)
    attempt.grid(row=3, column=0, columnspan=2)
    #print(f'{round(time.clock(),4)}: - - - - - Network Login launched')
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

    #print(f'{round(time.clock(),4)}: - - - - - Program execution Begin')
    login()
    #print(f'{round(time.clock(),4)}: - - - - - Cloud Login')

    while True:
        try:
            svc.print_day()
        except:
            mongo.global_disconnect()
            login_error()

        else:
            break

    root = tk.Tk()
    #print(f'{round(time.clock(),4)}: - - - - - App window launch')
    root.config(bg='purple1')
    app(root)
    root.mainloop()
