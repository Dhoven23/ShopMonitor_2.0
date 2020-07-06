import datetime
from datetime import date

from Data.tool import Tool
from Data.Students import Student
from Data.signins import Signin
from Data.day import Day





def create_student(studentID: str, name: str):
    student = Student()
    student.name = name
    student.studentID = studentID

    student.save()

    return student.name

def CreateTool(keyNumber: int, name: str, TrainingLevel: int):
    tool = Tool()
    tool.name = name
    tool.keyNumber = keyNumber
    tool.TrainingLevel = TrainingLevel
    tool.save()
    return tool.keyNumber





def log_into_account(studentID: str):
        studentID = str(studentID)
        student = find_student_by_studentID(studentID)

        if not student:
            message = f"No student with ID {studentID}"
            return message

        SignedIn = student.Is_signedIn
        if SignedIn == False:
            message = f"Hello {student.name}"
            day_login(studentID)
            student.event()
            return message



        if SignedIn == True:
            message = f" Goodbye {student.name} "
            day_logout(studentID)
            student.event()
            return message


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

