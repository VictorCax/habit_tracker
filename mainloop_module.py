import class_module as cm
import database_module as dm
import os.path
import json as js
import sqlite3 as sql
import datetime





def create_habit(habit_name, habit_desc, habit_period):
    #This function is used to create habits meaning new instances of the habit class and save them into the sql database file

    global habits_database
    new_habit = cm.habit(habit_name, habit_desc, habit_period, habit_date = datetime.date.today(), habit_lastup = datetime.date.today(), habit_streak = 0,
                 habit_record = 0)


    dm.database_cursor.execute('''INSERT INTO habits (habit_name, habit_desc, habit_period, habit_date, habit_lastup, 
        habit_streak, habit_record) VALUES (?,?,?,?,?,?,?)''',(new_habit.habit_name,new_habit.habit_desc,new_habit.habit_period,
                                                               new_habit.habit_date,new_habit.habit_lastup,
                                                               new_habit.habit_streak,new_habit.habit_record))
    dm.database_connection.commit()
    print()
    print("__________________________________________________".center(50))
    print()
    print("The habit {} was created successfuly".format(new_habit.habit_name).center(50))
    print()

    main_menu()



def greeting():
    # A simple greeting to introduce the user to the program. Its sparated from the main menu because it should eb only shown
    # at the beginning
    today_date = datetime.date.today()

    print("__________________________________________________".center(50))
    print("....Welcome to Cax´s habit tracker....".center(50))
    print("Today´s date is: {}".format(today_date).center(50))
    print()



def main_menu():
    # This is the main menu function which will be called at the beginning and everytime a task is completed. Here the user
    # has the possibility to navigate to all the options

    print("__________________________________________________".center(50))
    print("-Main Menu-".center(50))
    print()
    print("1    Add new habit")
    print("2    Manage habits (check/delete)")
    print("3    Analyze habits")
    print("4    End program")
    print()
    main_menu_input = input("Enter option number: ")


    if main_menu_input not in ['1','2','3','4']:
        # This checks if the user is entering any value that is not predetermined so the program is not stopping
        print()
        print("wrong input".center(50))
        print("....returning to main menu....".center(50))
        return main_menu()

    #Opens add habit dialog
    elif main_menu_input == '1':
        # This statement is activated if the user input in the main menu is 1 and opens the add habit dialog
        # which calls the create habit method with the values provided by the user

        habit_name = input("Enter habit name: ")
        habit_description = input("Enter habit description: ")
        habit_period = input("Enter habit period (daily or weekly): ")

        while habit_period != "daily" and habit_period != "weekly":
            #This makes sure the user is providing the right input instead of stopping the program upon fail entry
            print()
            print("...You entered a wrong value for the period...".center(50))
            print("Please enter the period properly".center(50))
            print()
            habit_period = input("Enter habit period (daily or weekly): ")

        create_habit(habit_name,habit_description,habit_period)

    #Opens mananage habit dialog
    elif main_menu_input == '2':
        # This statement opens the check and delete habit functions

        print()
        print("Which operation do you whish do perform? (check or delete): ")
        print()
        del_or_mod = input("Enter check or delete: ")
        while del_or_mod != "check" and del_or_mod != "delete":
            print()
            print("...You entered a wrong selection value...".center(50))
            print("Please enter the selection value properly".center(50))
            print()
            del_or_mod = input("Enter check or delete: ")


        if del_or_mod == "check":
            # If the user is entering check the check function will be called
            print()
            print("__________________________________________________".center(50))
            print("Which habit you whish to check?".center(50))
            print()
            print("....List of all habits....".center(50))
            dm.get_all("names_period_lastup-streak")
            print()

            habit_to_check = input("Enter the name of the habit you whish to check: ")
            print("__________________________________________________".center(50))
            print()

            # Seletcs all habits in the database that match with the user input:
            dm.database_cursor.execute('''SELECT * FROM habits where habit_name =? ''', (habit_to_check,))
            selection = dm.database_cursor.fetchone()

            if selection is not None:
                # If the row is not None it means the habit exists in the database so we can delete it
                h = cm.habit(*selection)
                h.check_habit(h.habit_name)
                print()
                print("....Returnung to main menu....".center(50))

            else:
                print("__________________________________________________".center(50))
                print()
                print("Habit not found in the database.".center(50))
                print()

            main_menu()




        elif del_or_mod == "delete":
            # If the user is entering delete this line of code will first display the name,description and period of all
            # habits in the database and then after the user enters the specific name of the habit he wants to have deleted
            # the delete_habit method of that instance is called

            print()
            print("__________________________________________________".center(50))
            print("Which habit you whish to delete?".center(50))
            print()
            print("....List of all habits....".center(50))
            dm.get_all("names_description_period")
            print()

            habit_to_delete = input("Enter the name of the habit you whish to delete: ")
            print()

            #Seletcs all habits in the database that match with the user input:
            dm.database_cursor.execute('''SELECT * FROM habits where habit_name =? ''',(habit_to_delete,))
            selection = dm.database_cursor.fetchone()


            if selection is not None:
                # If the row is not None it means the habit exists in the database so we can delete it
                h = cm.habit(*selection)
                h.delete_habit(h.habit_name)
                print("__________________________________________________".center(50))
                print()
                print("Habit deleted successfully!".center(50))
                print()
            else:
                print("__________________________________________________".center(50))
                print()
                print("Habit not found in the database.".center(50))
                print()

            main_menu()

    #Opens analyze habit dialog
    elif main_menu_input == '3':

        print()
        print("__________________________________________________".center(50))
        print()
        print("Analyze habits".center(50))
        print()
        print("Select the type of analysis you would like to perform: ".center(50))
        print()
        print("1    See all habits in detail")
        print("2    Show all daily or weekly habits")
        print("3    Show the longest habit streak")
        print("4    Show the highest streak record of all habits")
        print()

        analyze_input = input("Enter option number: ")
        print()
        print("__________________________________________________".center(50))
        dm.analyze_habits(analyze_input)



        #This lines leave the analyze menu and go back to the main menu no matter what the user input is
        print()
        whish_back = input("Press enter to go back to the main menu")

        if whish_back == False:
            main_menu()
        else:
            main_menu()





    elif main_menu_input == '4':

        print("__________________________________________________".center(50))
        print()
        print("....Program ended....".center(50))
        print()
        print("All data saved".center(50))
        print("Auf Wiedersehen | Goodbye | Adiós".center(50))



greeting()
main_menu()
dm.database_connection.close()


