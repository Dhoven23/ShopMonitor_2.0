from Data.Students import Student
from Service.data_service import find_day
from Service.data_service import find_student_by_studentID
import Service.data_service as svc
import datetime



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


def PastDueTools():
    out = []
    for student in Student.objects():
        if student.checked_out_tools:
            for tool in student.checked_out_tools:
                toolname = tool.split(',')
                tool_object = svc.find_tool(toolname[0], toolname[1])
                use = tool_object.usages[-1]
                date_time_str = use.ReturnDateExpect
                date_time_obj = datetime.datetime.strptime(str(date_time_str), '%Y-%m-%d')
                today = datetime.date.today()
                delta = date_time_obj.date() - today
                if int(delta.days) < 0:
                    out.append(student.name + ': -> ')
                    out.append(toolname[0] + ' ' + toolname[1] + ' ')
                    out.append('past due: ' + str(delta.days) + ' days\n')



    return out