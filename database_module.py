import sqlite3 as sql
import json as js
import os.path
from class_module import *


# This module contains the database setup and management

def inizialize_database():
    print("....Setting up database....".center(50))
    database_path = "/Users/victor_cax/Library/Mobile Documents/com~apple~CloudDocs/Knowledge/Coding/Python/Habit Tracker/habits_database.db"
    if os.path.isfile(database_path):
        database_connection = sql.connect("habits_database.db")
        database_cursor = database_connection.cursor()

        print("Found existing database: habits_database.db".center(50))
        print()

    else:
        # Connects/ creates a database file and define curser for interaction
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

    if what == "names_description_period":
        for row in selection:

            print()
            print("Habit name: {}".format(row[0]))
            print("Habit description {}".format(row[1]))
            print("Habit period: {}".format(row[2]))

    if what == "names_period_lastup-streak":

        for row in selection:
            print()
            print("Habit name: {}".format(row[0]))
            print("Habit streak: {}".format(row[5]))
            print("Habit period: {}".format(row[2]))
            print("Last time updated/checked: {}".format(row[4]))


def analyze_habits(what):



    if what == "1":

        database_cursor.execute('''SELECT * FROM habits ''')
        selection = database_cursor.fetchall()
        num_selection = len(selection)
        print()
        print(("\033[31m" + "You have {} total habits".format(num_selection)+ '\033[0m').center(50))
        for row in selection:

            print()
            print("\033[31m" + "Habit name: {}".format(row[0])+ '\033[0m')
            print("Habit description: {}".format(row[1]))
            print("Habit period: {}".format(row[2]))
            print("Habit creation date: {}".format(row[3]))
            print("Last time updated/checked: {}".format(row[4]))
            print("Habit streak: {}".format(row[5]))
            print("Habit streak record: {}".format(row[6]))
            print("__________________________________________________".center(50))

    if what == "2":
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
            print()
            print("\033[31m" + "Habit name: {}".format(row[0]) + '\033[0m')
            print("Habit description: {}".format(row[1]))
            print("Habit period: {}".format(row[2]))
            print("Habit streak: {}".format(row[5]))
            print("__________________________________________________".center(50))


    if what == "3":

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

            print()
            print("{} streak: {} {}".format(rank, row[1],label))
            print("Habit name: {}".format(row[0]))

        print()
        print("\033[33m" + "Streaks of daily habits will be displayed as days and of weekly habits as week"+ '\033[0m')
        print("\033[33m" +"For example:" + '\033[0m')
        print("\033[33m" +"A streak of 2 weeks is defined as the habit was checked off once in two consecutive weeks" + '\033[0m')
        print("\033[33m" +"A streak of 2 days is defined as the habit was cheked off on two consecutive days" + '\033[0m')


    if what == "4":

        database_cursor.execute('''SELECT habit_name, CAST(habit_record AS INTEGER) FROM habits WHERE 
        habit_period = 'daily' ORDER BY CAST(habit_record AS INTEGER) DESC LIMIT 1''')

        record_daily = database_cursor.fetchone()

        database_cursor.execute('''SELECT habit_name, CAST(habit_record AS INTEGER) FROM habits WHERE 
                habit_period = 'weekly' ORDER BY CAST(habit_record AS INTEGER) DESC LIMIT 1''')
        record_weekly = database_cursor.fetchone()

        print()
        print( ("The highest"+ '\033[31m' + " daily " + '\033[0m'+ "streak record is:").center(50))
        print("Habit name: {} with a streak record of {} days".format(record_daily[0],record_daily[1]))
        print()

        print()
        print( ("The highest"+ '\033[31m' + " weekly " + '\033[0m'+ "streak record is:").center(50))
        print("Habit name: {} with a streak record of {} weeks".format(record_weekly[0], record_weekly[1]))













































