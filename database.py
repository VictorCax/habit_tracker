import sqlite3 as sql
import os.path
from classes import *


# This module contains the database setup and management

def inizialize_database():
    #Here the database is set up. i checks if the path of the database is already existing. If no, it is creating a new database file
    #at the defined location. If it is it is connecting to the database.In both cases a connection and cursor variable for access
    #is created

    print("....Setting up database....".center(50))
    database_path = "/Users/victor_cax/Library/Mobile Documents/com~apple~CloudDocs/Knowledge/Coding/Python/Habit Tracker/habits_database.db"
    if os.path.isfile(database_path):
        #Database already exists
        database_connection = sql.connect("habits_database.db")
        database_cursor = database_connection.cursor()

        print("Found existing database: habits_database.db".center(50))
        print()

    else:
        #Creates new database and connection and cursor variables
        database_connection = sql.connect("habits_database.db")
        database_cursor = database_connection.cursor()

        # Create new Table in that database

        habit_table = database_cursor.execute('''CREATE TABLE IF NOT EXISTS habits (habit_name, habit_desc, habit_period, habit_date, habit_lastup, habit_streak,
                         habit_record)''')

        print("Created new database: habits_database.db".center(50))
        print()

    return (database_cursor, database_connection)

database_cursor, database_connection = inizialize_database()


def get_all(what):

    #This method returns certain values of all the items in the database

    database_cursor.execute('''SELECT * FROM habits ''')
    selection = database_cursor.fetchall()
    results = []

    if what == "names_description_period":
        #Here the habit Name, description and the period is retuned when called
        for row in selection:


            habit_name = "Habit name: {}".format(row[0])
            habit_description = "Habit description {}".format(row[1])
            habit_period = "Habit period: {}".format(row[2])
            results.append(f"\n{habit_name}\n{habit_description}\n{habit_period}\n")


    if what == "names_period_lastup-streak":
        #Here the habit name,streak,period,lastupdate is returned when called
        for row in selection:


            habit_name = "Habit name: {}".format(row[0])
            habit_streak = "Habit streak: {}".format(row[5])
            habit_period = "Habit period: {}".format(row[2])
            habit_lastup = "Last time updated/checked: {}".format(row[4])
            results.append(f"\n{habit_name}\n{habit_streak}\n{habit_period}\n{habit_lastup}\n ")

    return "".join(results)



def analyze_habits(what):
#This function is for analyzing the habits. It searches and lists habits depending on different properties. The function
#is called with a number to determine which anazlying action should be taken

    results = []

    if what == "1":
        #This is the analyzing action to list all habits in the database

        database_cursor.execute('''SELECT * FROM habits ''')
        selection = database_cursor.fetchall()
        num_selection = len(selection)
        print()
        print(("\033[31m" + "You have {} total habits".format(num_selection)+ '\033[0m').center(50))
        for row in selection:


            habit_name = "\033[31m" + "Habit name: {}".format(row[0])+ '\033[0m'
            habit_description = "Habit description: {}".format(row[1])
            habit_period = "Habit period: {}".format(row[2])
            habit_date = "Habit creation date: {}".format(row[3])
            habit_lastup = "Last time updated/checked: {}".format(row[4])
            habit_streak = "Habit streak: {}".format(row[5])
            habit_record = "Habit streak record: {}".format(row[6])
            spacer = "__________________________________________________".center(50)

            results.append(f"\n{habit_name}\n{habit_description}\n{habit_period}\n{habit_date}\n{habit_lastup}\n{habit_streak}\n{habit_record}\n{spacer}\n")

    if what == "2":
        #Here either the daily or the weekly habits are returned for the user als analzying action
        #This code block first asks the user to input which habit type he wants to see and then pulls and prints them out of the database

        print()
        print("Do you wish to see the daily or weekly habits?".center(50))
        print()
        print()
        selector = input("Enter habit type you want to see (daily or weekly): ")

        while selector != "daily" and selector != "weekly":
            #This makes sure the user is providing the right input instead of stopping the program upon fail entry
            print()
            print("...You entered a wrong value for the type...".center(50))
            print("Please enter the type properly".center(50))
            print()
            selector = input("Enter habit type you want to see (daily or weekly): ")
            print()

        database_cursor.execute(('''SELECT * FROM habits WHERE habit_period = ?'''),(selector,))
        selection = database_cursor.fetchall()
        num_rows = len(selection)
        print()
        print("__________________________________________________".center(50))
        print("\033[31m" + "You have {} {} habits".format(num_rows,selector).center(50) + '\033[0m')

        for row  in selection:


            habit_name = "\033[31m" + "Habit name: {}".format(row[0]) + '\033[0m'
            habit_description = "Habit description: {}".format(row[1])
            habit_period = "Habit period: {}".format(row[2])
            habit_streak = "Habit streak: {}".format(row[5])
            spacer = "__________________________________________________".center(50)

            results.append(f"\n{habit_name}\n{habit_description}\n{habit_period}\n{habit_streak}\n{spacer}\n")

    if what == "3":
        #Here the analzying action is to display the highest, secon and third hightest streaks of all habits. Since
        #there are weekly and daily habits and i want to compare all of them there is a status depening label (weeks,days)
        #to have the user see what kind of streak the habit has

        database_cursor.execute('''SELECT habit_name, CAST(habit_streak AS INTEGER),habit_period FROM habits ORDER BY CAST(habit_streak AS INTEGER) DESC LIMIT 3''')
        three_highest = database_cursor.fetchall()

        for i, row in enumerate(three_highest):
            rank = ""
            if i == 0:
                rank = "Highest"
            elif i == 1:
                rank = "Second highest"
            elif i == 2:
                rank = "Third highest"

            if row[2] == "daily":
                label = "days"
            elif row[2] == "weekly":
                label = "weeks"


            streak = "{} streak: {} {}".format(rank, row[1],label)
            habit_name = "Habit name: {}".format(row[0])
            results.append(f"\n{streak}\n{habit_name}\n")

        print()
        print("\033[33m" + "Streaks of daily habits will be displayed as days and of weekly habits as week"+ '\033[0m')
        print("\033[33m" +"For example:" + '\033[0m')
        print("\033[33m" +"A streak of 2 weeks is defined as the habit was checked off once in two consecutive weeks" + '\033[0m')
        print("\033[33m" +"A streak of 2 days is defined as the habit was cheked off on two consecutive days" + '\033[0m')

    if what == "4":
        #This is returning the highest record of a weekly and a daily habit ever counted.

        database_cursor.execute('''SELECT habit_name, CAST(habit_record AS INTEGER) FROM habits WHERE 
        habit_period = 'daily' ORDER BY CAST(habit_record AS INTEGER) DESC LIMIT 1''')

        record_daily = database_cursor.fetchone()

        database_cursor.execute('''SELECT habit_name, CAST(habit_record AS INTEGER) FROM habits WHERE 
                habit_period = 'weekly' ORDER BY CAST(habit_record AS INTEGER) DESC LIMIT 1''')
        record_weekly = database_cursor.fetchone()


        highest_daily = ("The highest"+ '\033[31m' + " daily " + '\033[0m'+ "streak record is:").center(50)
        highest_daily_name = "Habit name: {} with a streak record of {} days".format(record_daily[0],record_daily[1])


        hightest_weekly = ("The highest"+ '\033[31m' + " weekly " + '\033[0m'+ "streak record is:").center(50)
        hightest_weekly_name = "Habit name: {} with a streak record of {} weeks".format(record_weekly[0], record_weekly[1])

        results.append(f"\n{highest_daily}\n{highest_daily_name}\n\n{hightest_weekly}\n{hightest_weekly_name}\n")

    return "".join(results)













































