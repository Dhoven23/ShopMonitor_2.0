
import Service.admin_svc as asv

def admin():
    while True:
        password = input('\n Enter password ([q] to exit): (password = admin)\n')
        if password == 'admin':
            choice = choices()
            action(choice)
            break
        else:
            print("Nope")
            pass


def choices():
    choice = input("Select action:\n"
                   "[1] -> View who's in the shop\n"
                   "[2] -> View who was in the shop\n"
                   "[3] -> View student details\n"
                   "[4] -> Logout all users \n"
                   "[5] -> Edit student training\n"
                   "[6] -> Return to login\n")
    check = int(choice)
    if 0 < check <= 6:
        return choice
    else:
        print("\n---------------------------NOT IMPLEMENTED---------------------------- \n")



def action(act):
    if act == '1':
        asv.whos_in_the_shop()
    if act == '2':
        asv.who_was_in_the_shop()
    if act == '4':
        asv.logout_all_users()


def run():
    admin()