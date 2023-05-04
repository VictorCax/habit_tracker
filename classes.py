import sqlite3 as sql
import database as dm
import datetime

date_today = datetime.date.today()


#This Module contains the habit class and the corresponding Methods


class habit:
    """This is the general habit class. It defines the habit arguments and the delete and streak management methods"""

    def __init__(self,habit_name, habit_desc, habit_period, habit_date = datetime.date.today(),
                 habit_lastup = datetime.date.today(), habit_streak = 0,habit_record = 0):


        self.habit_name = habit_name
        self.habit_desc = habit_desc
        self.habit_period = habit_period
        self.habit_date = habit_date
        self.habit_lastup = habit_lastup
        self.habit_streak = habit_streak
        self.habit_record = habit_record


    def delete_habit(self,habit_name):
        #This method delets all the habits with the same name as the habit objects that was put in here as argument out of the database

        print("....Deleting habit: {habit_name}....".format(habit_name = self.habit_name).center(50))
        dm.database_cursor.execute('''DELETE FROM habits WHERE habit_name =?''',(habit_name,))
        dm.database_connection.commit()

    def check_habit(self,habit_name):
        #This method is used to check off a habit object. It first estimates the time delta since the habit was last updated
        #and then decides to either check, do not check or brake the habit streak

        print("....Checking off habit: {habit_name}....".format(habit_name=self.habit_name).center(50))
        dm.database_cursor.execute(('''SELECT * FROM habits WHERE habit_name = ?'''),(habit_name,))
        selection = dm.database_cursor.fetchone()
        date_last_update = selection[4]
        datetime_lastupdate = datetime.datetime.strptime(date_last_update, '%Y-%m-%d').date()
        time_delta = date_today - datetime_lastupdate
        daily_or_weekly = selection[2]

        # Here it is  checked if the habit to be checked off is daily or weekly. There are different definiezins for both
        if daily_or_weekly == "daily":

            #If the time delta in days is zero this means that the habit was checked off today
            if time_delta.days == 0:
                print()
                print("Habit was already checked today".center(50))

            #if the time delta is one this means the habit was last checked off yesterday
            elif time_delta.days == 1:

                current_streak = int(selection[5])
                new_streak = current_streak + 1
                dm.database_cursor.execute(('''UPDATE habits SET habit_streak = ?, habit_lastup = ? WHERE habit_name = ? '''),(new_streak,date_today,habit_name))
                dm.database_connection.commit()
                print()
                print("__________________________________________________".center(50))
                print("Habit {} was checked off successfully".format(selection[0]).center(50))
                print("You are currently on a Streak of {}".format(new_streak).center(50))

                #This checks if the current streak is higher than the record and if so it updates the record
                if new_streak > self.habit_record:

                    dm.database_cursor.execute(
                        ('''UPDATE habits SET habit_record = ? WHERE habit_name = ? '''),
                        (new_streak, habit_name))
                    dm.database_connection.commit()

            #If the time delta is higher than one this means it has more than one day passed since the habit was last checked
            elif time_delta.days > 1:

                print()
                print("__________________________________________________".center(50))
                print("....STREAK WAS BROKEN....".center(50))
                print("You missed to check the habit yesterday".center(50))

                dm.database_cursor.execute(
                ('''UPDATE habits SET habit_streak = ?, habit_lastup = ? WHERE habit_name = ? '''),
                (0, date_today, habit_name))
                dm.database_connection.commit()

                print("The Streak was set to 0".center(50))

        #Checks if the habit to be checked is weekly
        elif daily_or_weekly == "weekly":
            week_delta = date_today.isocalendar()[1] - datetime_lastupdate.isocalendar()[1]


            # If the week delta is zero this means the habit was last checked in the same week as this week
            if week_delta == 0:

                print()
                print("__________________________________________________".center(50))
                print("Habit {} was already checked this week".format(habit_name).center(50))
                print("You are currently on a streak of {} week(s)".format(self.habit_streak).center(50))


            #If the week delta is 1 this means the habit was last checked in the week before and the streak is fulfilled
            #The term == -51 ensures that the streak is still successufl even if a new year is launched since the week
            #delta can only be -51 if you check the habit in week 1 and the last checked was week 52 of the previous year

            if  week_delta == 1 or week_delta == -51:

                current_streak = int(selection[5])
                new_streak = current_streak + 1
                dm.database_cursor.execute(
                    ('''UPDATE habits SET habit_streak = ?, habit_lastup = ? WHERE habit_name = ? '''),
                    (new_streak, date_today, habit_name))
                dm.database_connection.commit()
                print()
                print("__________________________________________________".center(50))
                print("Habit {} was checked off successfully".format(selection[0]).center(50))
                print("You are currently on a Streak of {} week(s)".format(new_streak).center(50))

                # This checks if the current streak is higher than the record and if so it updates the record
                if new_streak > self.habit_record:

                    dm.database_cursor.execute(
                        ('''UPDATE habits SET habit_record = ? WHERE habit_name = ? '''),
                        (new_streak, habit_name))
                    dm.database_connection.commit()



            #If the week delta is bigger than one meaning the week number of the date the habit was last checked is more
            #than one week ago. If there is a new year in between it might cause to have negative week deltas and every
            #negative delta except the -51 is meaning that there was an interruption

            if week_delta > 1 or week_delta < 0 and week_delta != -51:

                print()
                print("__________________________________________________".center(50))
                print("....STREAK WAS BROKEN....".center(50))
                print("You missed to check the habit last week".center(50))

                dm.database_cursor.execute(
                    ('''UPDATE habits SET habit_streak = ?, habit_lastup = ? WHERE habit_name = ? '''),
                    (0, date_today, habit_name))
                dm.database_connection.commit()

                print("The Streak was set to 0".center(50))







