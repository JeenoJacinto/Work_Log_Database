import datetime
import os
import sys

from peewee import *

from functions import clear, selected_entry, border_finder
from functions import get_name, get_time, get_notes, get_date, table_or_page
from functions import new_database_entry, view_table, page_through

db = SqliteDatabase('worklog.db')


class Entry(Model):
    entrynumber = IntegerField()
    date = DateField(default=datetime.datetime.now)
    username = CharField(max_length=255)
    taskname = CharField(max_length=255)
    timespent = TimeField()
    notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def menuloop():
    while True:
        entries = Entry.select().order_by(Entry.entrynumber)
        clear()
        print("Work Log Terminal: Main Menu\n")
        print("1. Add New Entry")
        print("2. View Entire Database")
        print("3. Search by Date")
        print("4. Search by Username")
        print("5. Search by Time Spent")
        print("6. Search by Term")
        print("7. Quit\n")
        print("Please enter the number of the option you wish to choose.")
        choice = input("> ")
        if choice == '1':
            new_database_entry(Entry)
        elif choice == '2':
            table_or_page(entries)
        elif choice == '3':
            clear()
            print("Search by Date\n")
            print("1. Enter Specific Date")
            print("2. Enter Date Range")
            print("Please enter the number of the option you wish to choose.")
            choice = input("> ")
            if choice == '1':
                chosen_date = get_date("Choose by Specific Date")
                date_entries = entries.where(Entry.date.contains(chosen_date))
                if date_entries:
                    table_or_page(date_entries)
                else:
                    clear()
                    print("There are no entries that match the specific date.")
                    input("Press Enter")
            elif choice == '2':
                starting_date = get_date("Choose Starting Date")
                ending_date = get_date("Choose Ending Date")
                date_entries = entries.where(Entry.date.between(starting_date,
                                                                ending_date))
                if date_entries:
                    table_or_page(date_entries)
                else:
                    clear()
                    print("There are no entries within date range.")
                    input("Press Enter")
        elif choice == '4':
            clear()
            print("Search by Username\n")
            usernames = []
            for entry in entries:
                usernames.append(entry.username)
            unique_usernames = set(usernames)
            for user in unique_usernames:
                print(user)
            print("Please type the username of the"
                  + " user you wish to view entries from")
            choice_username = input("> ")
            selected_entries = entries.where(Entry.username.contains(
                                             choice_username))
            if selected_entries:
                table_or_page(selected_entries)
            else:
                print("There are no entries that matched selected username.")
                input("Press Enter")
        elif choice == '5':
            chosen_duration = get_time("Search by Time Spent")
            date_entries = entries.where(Entry.timespent.contains(
                                         chosen_duration))
            if date_entries:
                table_or_page(date_entries)
            else:
                clear()
                print("There are no entries that match the specific duration.")
                input("Press Enter")
        elif choice == '6':
            clear()
            print("Search by Term\n")
            print("Only Entries that contain the term within their"
                  + " task name or notes will be listed")
            print("Please enter a term you wish to match entries with.")
            search_term = input("> ")
            matching_entries = entries.where(
                Entry.taskname.contains(search_term)
                |Entry.notes.contains(search_term))
            if matching_entries:
                table_or_page(matching_entries)
            else:
                print("There are no entries that contain your term")
                input("Press Enter")
        elif choice == '7':
            clear()
            break
        else:
            print("Invalid Input")
            input("Press Enter")
if __name__ == '__main__':
    initialize()
    menuloop()
