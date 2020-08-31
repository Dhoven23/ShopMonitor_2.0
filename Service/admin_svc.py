from Data.Students import Student
from Service.data_service import find_day
from Service.data_service import find_student_by_studentID
import Service.data_service as svc




def whos_in_the_shop():
    candidates = Student.objects
    message = []
    if candidates:
        for student in candidates:
            if student.Is_signedIn == True:
                message.append(student.name)

    return message


def who_was_in_the_shop(date):
    day = None
    IDs = []
    message = []

    day = find_day(date)

    if day:
        for signin in day.signins:
            IDs.append(signin.StudentID)

    else:
        pass
    i = 0
    if day and IDs:
        for id in IDs:
            found = find_student_by_studentID(id)
            tools = '\n'
            for tool in found.checked_out_tools:
                tools = tools + f"  * {tool}\n"
            message.append('-> ' + found.name + f'............ {day.signins[i].Login[11:16]} to {day.signins[i].Logout[11:16]}|' + tools)
            i += 1
    return message


def logout_all_users():
    students = Student.objects
    for student in students:
        if student.Is_signedIn == True:
            student.Is_signedIn = False
            svc.day_logout(student.studentID)
            student.save()
    return True

def edit_training_level(name,value):
    student = None
    student = Student.objects(name=name).first()

    if student:
        student.train(value)
        return True
    else:
        return False


