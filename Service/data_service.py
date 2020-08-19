import datetime
from datetime import date
import re
from Data.key import Key
from Data.Students import Student
from Data.signins import Signin
from Data.tool import Tool
from Data.usages import Usage
from Data.day import Day





def create_student(studentID: str, name: str) -> Student:
    student = Student()
    student.name = name
    student.studentID = studentID
    student.save()

    return student

def CreateTool(keyNumber: int, name: str):
    tool = Key()
    tool.name = name
    tool.keyNumber = keyNumber
    tool.save()
    return tool.keyNumber





def log_into_account(studentID: str):
        studentID = str(studentID)
        student = find_student_by_studentID(studentID)

        if not student:
            message = f"No student with ID {studentID}"
            return message, False

        SignedIn = student.Is_signedIn
        if SignedIn == False:
            message = f"Hello {student.name}, you are cleared to use:\n"
            for number in student.keys_trained:
                tool = Key.objects(keyNumber=number).first()
                addition = tool.name
                message = message + '-> ' + addition + '\n'

            day_login(studentID)
            student.event()
            return message, False



        if SignedIn == True:
            message = f" Goodbye {student.name} "
            day_logout(studentID)
            student.event()
            return message, True


def find_student_by_studentID(studentID: str) -> Student:
    student = Student.objects(studentID=studentID).first()
    return student


def create_day() -> Day:
    day = Day()
    day.Begin = datetime.datetime.now().hour
    day.date = str(date.today())
    print(f"Welcome, today is {date.today().strftime('%A')}, {date.today()}")
    day.save()
    return day

def find_day(date: str) -> Day:
    day0 = Day.objects(date=date).first()

    return day0

def print_day():
    day0 = Day.objects(date=str(date.today())).first()
    if not day0:
        day0 = create_day()

    return day0.date


def day_login(studentID: str):
    signin = Signin()
    signin.StudentID = studentID
    signin.Login = str(datetime.datetime.now())

    day = find_day(str(date.today()))
    day.increment()
    day.hourly_entry_add()
    for sign in day.signins:
        if sign.StudentID == studentID:
            return
    day.signins.append(signin)

    day.save()


def day_logout(studentID: str):

    model = find_day(str(date.today()))
    for signin in model.signins:
        if signin.StudentID == studentID:
            signin.Logout = str(datetime.datetime.now())

    model.hourly_entry_rmv()
    model.save()


def key_exists(number):
    if Key.objects(keyNumber=number):
        return True
    else:
        return False
def Create_Tool(name, size) -> Tool:
    tool = Tool()
    tool.name = name.lower()
    tool.size = size
    tool.save()
    return tool

def find_tool(name, size):
    tools = Tool.objects(name=name.lower)
    for tool in tools:
        if tool.size == size:
            return tool
        else:
            return False



def Checkout_tool(toole, ID):
    new_usage = Usage()
    new_usage.checkout_ID = ID
    new_usage.checkout_time = str(datetime.datetime.now())
    toole.usages.append(new_usage)
    toole.save()

def lookup_tool(text):
    message = []
    name = re.compile(f'.*{text}.*', re.IGNORECASE)
    tools = Tool.objects(name=name)
    for tool in tools:
        message.append(tool.name + ' ' + tool.size)

    return message


def Return(toole, ID):
    for use in toole.usages:
        if use.checkout_ID == ID:
            use.return_time = str(datetime.datetime.now())
    toole.save()
