import Service.data_service as svc


# grab studentID from user, this is the pivot of all lookups
def login():
    while True:
        studentID = input('What is your Student ID?    ([q] to exit): \n').strip().lower()
        studentID = str(studentID)
        if studentID == 'q':
            break
        # Check that the entered ID is 8 digits long. Not foolproof, but better than nothing
        if len(studentID) == 8:
            svc.log_into_account(studentID)
        else:
            print(f"\n oops, {studentID} is not a valid Student ID, please check spelling and try again")


# Function handle for main method. Add functions here as capability is added
def run():

    login()

