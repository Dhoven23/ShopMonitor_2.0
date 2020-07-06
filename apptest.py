
from tkinter import *
import Data.mongo_setup as mongo
from Service.data_service import log_into_account
import Service.data_service as svc
import admin as admin



mongo.global_init()

root = Tk()
root.minsize(230, 170)
root.title("Shop Activity Monitor")
root.iconbitmap('C:/Users/Tesla/Desktop/app.ico')

e = Entry(root, width=75, borderwidth=2)






def popup_hello(message: str):
    pop = Toplevel()
    pop.minsize(70, 30)
    pop.wm_title("Login/Logout")
    l = Label(pop, text=message)
    l.grid(row=0, column=0)

    b = Button(pop, text="Acknowledge", command=pop.destroy)
    b.grid(row=1, column=0)


def popup_create_student(StudentID: str):
    def student_create(event=None):
        name = prompt.get()
        ID = StudentID
        pop.destroy()
        popup_hello('Hello ' + name)
        svc.create_student(ID, str(name))
        svc.log_into_account(StudentID)


    pop = Toplevel()
    pop.minsize(80, 30)
    prompt = Entry(pop, width = 35, borderwidth=2)
    prompt.insert(0, "Enter your name: ")

    prompt.bind('<Return>', student_create)

    pop.wm_title("New Student")
    l = Label(pop, text='test')
    l.grid(row=0, column=0)
    prompt.grid(row=2,column=0)

    b = Button(pop, text="Acknowledge", command=pop.destroy)
    b.grid(row=1, column=0)



def login(event=None):
    StudentID = e.get()
    if not len(StudentID) == 8:
        return
    else:
        message = log_into_account(StudentID)
        if message == f"No student with ID {StudentID}":
            popup_create_student(str(StudentID))


        else:
            popup_hello(message)
    e.delete(0, END)


e.pack()
e.insert(0, "Enter your ID: ")
e.bind('<Return>', login)

myButton = Button(root, text="Enter Your Student ID", command=login)
myButton.pack()
AdminButton = Button(root, text="Run as Admin", command=admin.run)
AdminButton.pack()

if __name__ == '__main__':
    svc.print_day()
    root.mainloop()
