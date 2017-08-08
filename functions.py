import datetime
import os


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def border_finder(entry_length, header_length):
    num1 = entry_length - header_length
    if num1 < 0:
        return 0
    else:
        return num1

def get_name(custom_text):
    while True:
        clear()
        print("{}\n".format(custom_text))
        name = input("Please enter a name: ")
        # Task name
        if name.strip():
            if len(name) <= 255:
                return name
                break
            else:
                print("Name contains too many characters."
                    + " Maximum Characters: 255")
                input("Press Enter")
        else:
            print("Invalid Task Name")
            input("Press Enter")


def get_date(custom_text):
    """Gets user to input valid date"""
    fmt = '%m/%d/%Y'
    while True:
        clear()
        print("Date Format: month/day/year --/--/----\n")
        print("{}\n".format(custom_text))
        task_date = input("Please input a date: ")
        try:
            datetime.datetime.strptime(task_date, fmt)
        except ValueError:
            print("'{}' doesn't seem to be a valid date.".format(task_date))
            input("Press Enter")
        except AttributeError:
            print("'{}' doesn't seem to be a valid date.".format(task_date))
            input("Press Enter")
        else:
            return datetime.datetime.strptime(task_date, fmt).date()
            break


def get_time(custom_text):
    """Gets user to input valid time"""
    fmt = '%H:%M:%S'
    while True:
        clear()
        print("Time Format: hours:minutes:seconds --:--:--\n")
        print("{}\n".format(custom_text))
        task_date = input("Please input a duration of time: ")
        try:
            datetime.datetime.strptime(task_date, fmt)
        except ValueError:
            print("'{}' doesn't seem to be a valid time.".format(task_date))
            input("Press Enter")
        except AttributeError:
            print("'{}' doesn't seem to be a valid time.".format(task_date))
            input("Press Enter")
        else:
            return datetime.datetime.strptime(task_date, fmt).time()
            break


def get_notes():
    clear()
    notes = input("Enter additional notes (Optional): ")
    if notes.strip() == False:
        notes = 'N/A'
        return notes
    else:
        return notes


def new_database_entry(Entry):
    date_fmt = '%m/%d/%Y'
    time_fmt = '%H:%M:%S'
    entry_number_list = [0]
    entries = Entry.select()
    for entry in entries:
        entry_number_list.append(entry.entrynumber)
    entry_number = max(entry_number_list) + 1
    task_date = get_date("|Task Date|")
    username = get_name("|Username|")
    task_name = get_name("|Task Name|")
    time_spent = get_time("|Time Spent|")
    notes = get_notes()
    date_and_time = datetime.datetime.combine(task_date, time_spent)
    read_date = datetime.datetime.strftime(date_and_time, date_fmt)
    read_time = datetime.datetime.strftime(date_and_time, time_fmt)
    clear()
    print("Task Date: {}".format(read_date))
    print("Username: {}".format(username))
    print("Task Name: {}".format(task_name))
    print("Time Spent: {}".format(time_spent))
    print("Notes: {}".format(notes))
    print("\nDo you wish to save this entry")
    choice = input("Y/N\n> ")
    if choice.upper() == "Y":
        Entry.create(entrynumber=entry_number, date=task_date,
                     username=username, taskname=task_name,
                     timespent=time_spent, notes=notes)


def view_table(entries):
    clear()
    date_fmt = '%m/%d/%Y'
    time_fmt = '%H:%M:%S'
    sp1 = []
    sp2 = []
    sp11 = 0
    sp22 = 0
    for entry in entries:
        sp1.append(len(entry.username))
        sp2.append(len(entry.taskname))
    sp11 = border_finder(max(sp1), 8)
    sp22 = border_finder(max(sp2), 9)
    header = "Entry Number" + "|" + "Date      " + "|" + "Username" + (" " * sp11) + "|" + "Task Name" + (" " * sp22) + "|" + "Time Spent" + "|" + "Notes"
    print(header)
    username_spacing = len("Username" + (" " * sp11))
    taskname_spacing = len("Task Name" + (" " * sp22))
    for entry in entries:
        date_and_time = datetime.datetime.combine(entry.date, entry.timespent)
        read_date = datetime.datetime.strftime(date_and_time, date_fmt)
        read_time = datetime.datetime.strftime(date_and_time, time_fmt)
        name_spacing = username_spacing - len(entry.username)
        task_spacing = taskname_spacing - len(entry.taskname)
        number_spacing = 12 - len(str(entry.entrynumber))
        print("-" * len(header))
        print("{}|{}|{}|{}|{}|{}".format(
                                    str(entry.entrynumber) + " " * number_spacing,
                                    read_date,
                                    entry.username + " " * name_spacing,
                                    entry.taskname + " " * task_spacing,
                                    " " + read_time + " ",
                                    entry.notes
                                    )
                                    )
    print("\nEnter the Entry Number of an entry you wish to edit.")
    print("If you DO NOT wish to edit/delete an entry Press Enter")
    user_input = input("> ")
    try:
        int(user_input)
    except ValueError:
        print("You chose not to edit/delete")
    else:
        range_checker = 0
        for entry in entries:
            if entry.entrynumber == int(user_input):
                selected_entry(int(user_input), entries)
                range_checker += 1
        if range_checker == 0:
            print("There were no entries that matched your chosen entry number"
                 )
            input("Press Enter")


def edit_delete(entry):
    date_fmt = '%m/%d/%Y'
    time_fmt = '%H:%M:%S'
    task = True
    while task:
        date_and_time = datetime.datetime.combine(entry.date, entry.timespent)
        read_date = datetime.datetime.strftime(date_and_time, date_fmt)
        read_time = datetime.datetime.strftime(date_and_time, time_fmt)
        clear()
        print("Selected Entry\n")
        print("Task Date: {}".format(read_date))
        print("Username: {}".format(entry.username))
        print("Task Name: {}".format(entry.taskname))
        print("Time Spent: {}".format(read_time))
        print("Notes: {}\n".format(entry.notes))
        print("Edit or Delete\n")
        print("1. Edit")
        print("2. Delete")
        print("3. Cancel\n")
        print("Please enter the number of the option you wish to choose.")
        choice = input("> ")
        if choice == '1':
            while True:
                clear()
                date_and_time = datetime.datetime.combine(entry.date, entry.timespent)
                read_date = datetime.datetime.strftime(date_and_time, date_fmt)
                read_time = datetime.datetime.strftime(date_and_time, time_fmt)
                print("Selected Entry\n")
                print("1. Task Date: {}".format(read_date))
                print("2. Username: {}".format(entry.username))
                print("3. Task Name: {}".format(entry.taskname))
                print("4. Time Spent: {}".format(read_time))
                print("5. Notes: {}".format(entry.notes))
                print("6. Done\n")
                print("Choose which detail you wish to edit")
                print("Please enter the number of the option you wish"
                      + " to choose.")
                choice = input("> ")
                if choice == '1':
                    entry.date = get_date("|Edit Task Date|")
                    entry.save()
                elif choice == '2':
                    entry.username = get_name("|Edit Username|")
                    entry.save()
                elif choice == '3':
                    entry.taskname = get_name("|Edit Task Name|")
                    entry.save()
                elif choice == '4':
                    entry.timespent = get_time("|Edit Time Spent|")
                    entry.save()
                elif choice == '5':
                    entry.notes = get_notes()
                    entry.save()
                elif choice == '6':
                    task = False
                    break
        elif choice == '2':
            if input("Are you sure? Y/N\n>  ").lower() == 'y':
                entry.delete_instance()
                entry.save()
                task = False
                print("Entry deleted!")
                input("Press Enter")
                break
        elif choice == '3':
            break
        else:
            print("Invalid Input")
            input("Press Enter")


def selected_entry(selected_entry_number, entries):
    for entry in entries:
        if entry.entrynumber == int(selected_entry_number):
            edit_delete(entry)


def page_through(entries):
    date_fmt = '%m/%d/%Y'
    time_fmt = '%H:%M:%S'
    page_number = 1
    max_page = 0
    entries_dict = {}
    for key, value in enumerate(entries):
        entries_dict[key + 1] = value
        max_page += 1
    if max_page < page_number:
        page_number -= 1
    while True:
        clear()
        date_and_time = datetime.datetime.combine(entries_dict[page_number].date, entries_dict[page_number].timespent)
        read_date = datetime.datetime.strftime(date_and_time, date_fmt)
        read_time = datetime.datetime.strftime(date_and_time, time_fmt)
        print("Page #{}\n".format(page_number))
        print("Task Date: {}".format(read_date))
        print("Username: {}".format(entries_dict[page_number].username))
        print("Task Name: {}".format(entries_dict[page_number].taskname))
        print("Time Spent: {}".format(read_time))
        print("Notes: {}\n".format(entries_dict[page_number].notes))
        print("1. Next Page")
        print("2. Previous Page")
        print("3. Edit or Delete")
        print("4. Previous Menu\n")
        print("Please enter the number of the option you wish to choose.")
        choice = input("> ")
        if choice == '1':
            if page_number == max_page:
                print("There are no more entries beyond this entry.")
                input("Press Enter")
            else:
                page_number += 1
        elif choice == '2':
            if page_number == 1:
                print("There are no previous entries beyond this entry.")
                input("Press Enter")
            else:
                page_number -= 1
        elif choice == '3':
            selected_number = 0
            selected_number += entries_dict[page_number].entrynumber
            selected_entry(selected_number, entries)
            break
        elif choice == '4':
            break
        else:
            print("Invalid Input")
            input("Press Enter")


def table_or_page(entries):
    while True:
        clear()
        print("Viewing Format\n")
        print("1. View as data table")
        print("2. View as individual pages")
        print("3. Previous Menu\n")
        print("Please enter the number of the option"
              + " you wish to choose.")
        choice = input("> ")
        if choice == '1':
            view_table(entries)
            break
        elif choice == '2':
            page_through(entries)
            break
        elif choice == '3':
            break
        else:
            print("Invalid Input")
            input("Press Enter")
