import Service.data_service as svc

active_student: Student = None


def reload_account():
    global active_student
    if not active_student:
        return

    active_student = svc.find_student_by_studentID(active_student.StudentID)

