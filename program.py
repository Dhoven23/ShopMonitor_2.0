###############################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Welcome! you are viewing the source code of the GCU Engineering Shop Activity Monitor
#   Clearly you are here because something isn't working, or because you want to know how it works
#
#   I've prepared some helpful hints and comments to guide you on your journey, but as always,
#   If it ain't broke, feature-creep!
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#   Author: Daniel Hoven (github @DHoven23),
#   email: Daniel.Hoven@gcu.edu
#   Version 0.1.0
#   Date of commit: 6/30/2020
#
###############################################################################################


# import libraries and external functions. Please check the supplied requirements.txt file.
import Data.mongo_setup as mongo_setup
import login
import Service.data_service as svc
import admin

# program entry method.
def main():
    mongo_setup.global_init()
    print('Hello, welcome to the engineering shop sign in system alpha. \n')
    svc.print_day()
    # attempt to run the login code
    try:
        while True:
            case = find_user_intent()
            if case == 'admin':
                admin.run()

            elif case == 'log':
                login.run()

            else:
                print("-------------------- NOT IMPLEMENTED ----------------------")
            rule = input("\n Exit? [y/n]\n")
            if rule == 'y':
                break

    # exit if user presses CrtL+C, or something goes wrong
    except (KeyboardInterrupt, SystemError, SystemExit):
        print("\n----------------Goodbye-----------------\n")
        return 0


# add choices here, and reference corresponding function call in prior try loop
def find_user_intent():
    choice = input('\n Would you like to [log]in or perform an [admin]istrative action? \n')
    if choice == 'log':
        return 'log'
    elif choice == 'admin':
        return 'admin'



if __name__ == '__main__':
    main()
