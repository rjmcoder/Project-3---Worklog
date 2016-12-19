from worklog import Entries
from datetime import datetime
import re
import sys
import os

entries = Entries()
def clear():
    """ Clears the screen """
    
    os.system("clear")

def main_menu():
    """ Main menu of the program asking user to either add new entry, search existing ones or quit the program """
    clear()
    print("""
MAIN MENU
-------------------------------
Would you like to:

[N]: Add a new entry.
[S]: Search existing entries. 
[Q]: Quit and exit the program. 
    """)
    entry_choice = input("Please select an option from above menu: ").lower().strip()
    
    if entry_choice == 'q':
        clear()
        sys.exit()
    elif entry_choice == 'n':
        clear()
        add_new_entry()
    elif entry_choice == 's':
        clear()
        search_menu()
    else:
        input("""Invalid choice, please check the menu options.
              Press enter to continue""")
        clear()
        main_menu()        
    

def add_new_entry():
    """ Adds a new entry to the program """
    
    task_date = get_task_date()
    task_name = get_task_name()
    task_mins = get_task_mins()
    task_notes = input("Please enter any notes you would like to go with the task, press enter if none: ").lower().strip()
    print("""
Would you like to:
[S]: Save this entry.
[E]: Edit this entry.
[D]: Delete this entry and go to main menu.
        """)
    add_entry_choice = input("Please select an option from the above menu: ").lower().strip()
    if add_entry_choice == 's': 
        entries.new_entry(task_date, task_name, task_mins, task_notes=" ")
        main_menu()
    elif add_entry_choice == 'e':
        while True:
            print("""
What would you like to edit:
[D]: Date.
[T]: Time spent.
[N]: Task Name.
[S]: Task Notes.
[X]: Done.
                """)
            edit_choice = input("Please select an option from the above menu: ").lower().strip()
            if edit_choice == 'd':
                task_date = get_task_date()
            elif edit_choice == 't':
                task_mins = get_task_mins()
            elif edit_choice == 'n':
                task_name = get_task_name()
            elif edit_choice == 's':
                task_notes = input("Please enter any notes you would like to go with the task, press enter if none: ").lower().strip()
            elif edit_choice == 'x':
                entries.new_entry(task_date, task_name, task_mins, task_notes=" ")
                input("Entry added! Press enter to continue")
                main_menu()
    elif add_entry_choice == 'd':
        clear()
        main_menu()


def get_task_date():
    """ Gets the task date """

    task_date = input("""Please enter the date for the task in mm/dd/yyyy format or type 't' for today's date: """)
    if task_date == 't': 
        task_date = datetime.today().strftime("%m/%d/%Y")
        return task_date
    try:
        datetime.strptime(task_date, "%m/%d/%Y")
    except ValueError:
        print("Not a valid dat entry, please enter in mm/dd/yyyy format.")
        get_task_date()
    else:
        return task_date


def get_task_name():
    """ Gets the task name """

    task_name = input("Please enter a task name: ").lower().strip()
    if len(task_name) == 0:
        print("Task name cannot be empty!")
        get_task_name()
    return task_name

def get_task_mins():
    """ Gets the task mins """

    task_mins = input("Please enter the number of mins spent on the task: ").strip()
    try:
        int(task_mins)
    except ValueError:
        print("Not a valid entry, task mins should be a integer.")
        get_task_mins()
    else:
        return task_mins

def search_menu():
    """ Searches existing entries either by date, time spent, exact string match or pattern/regex match """
    
    print("""
Would you like to by:

[M]: Go back to main menu.
[D]: Search by date.
[T]: Search by time spent.
[E]: Search by exact string match.
[P]: Search by pattern match.
[Q]: Quit and exit the program.
    """)
    find_by_choice = input("Please select an option from the above search menu: ").lower().strip()
    
    if find_by_choice == 'q':
        clear()
        sys.exit()
    elif find_by_choice == 'd':
        clear()
        search_by_date_menu()
    elif find_by_choice == 't':
        clear()
        search_by_time_spent()
    elif find_by_choice == 'e':
        clear()
        search_by_exact_match()
    elif find_by_choice == 'p':
        clear()
        search_by_pattern()
    elif find_by_choice == 'm':
        clear()
        main_menu()
    else:
        input("""Invalid choice, please check the menu options.
              Press enter to continue""")
        clear()
        search_menu()
        

def search_by_date_menu():
    """ Search by date or date range """
    
    print(""" 
Would you like to:

[M]: Go back to main menu.
[D]: Search by individual date.
[R]: Search by date range.
[Q]: Quit and exit the program.
    """)
    
    date_search_choice = input("Please select an option from the above date search menu: ").lower().strip()
    
    if date_search_choice == 'q':
        clear()
        sys.exit()
    elif date_search_choice == 'd':
        clear()
        search_by_date()
    elif date_search_choice == 'r':
        clear()
        search_by_date_range()
    elif date_search_choice == 'm':
        clear()
        main_menu()
    else:
        input("""Invalid choice, please check the menu options.
              Press enter to continue""")
        search_by_date_menu()
        

def search_by_date():
    """ Search by date """

    temp_list = []
    dates = []
    idx = 0
    for entry in entries.log_entries:
        if entry[0] in dates: continue
        idx += 1
        print("{}: {}".format(idx, entry[0]))
        dates.append(entry[0])
    date_index = input("Choose the index of the date from the above list to lookup entries on that date: ")
    print("")
    for entry in entries.log_entries:
        if entry[0] == dates[int(date_index) - 1]:
            temp_list.append(entry)
            #print('{}: {}'.format(len(temp_list), ', '.join(entry)))
    print_entries(temp_list)
    del_or_update_entry_menu(temp_list)

        
def search_by_date_range():
    """ Search by date range """

    temp_list = []
    dates = []
    idx = 0
    for entry in entries.log_entries:
        if entry[0] in dates: continue
        idx += 1
        print("{}: {}".format(idx, entry[0]))
        dates.append(entry[0])
    date_range = input("Provide a range of dates from the above list, in mm/dd/yyyy format (e.g. 12/01/2016,12/08/2016) to lookup entries between those dates: ")
    print("")
    for entry in entries.log_entries:
        if datetime.strptime(date_range.split(',')[0].strip(), "%m/%d/%Y") <= datetime.strptime(entry[0], "%m/%d/%Y") <= datetime.strptime(date_range.split(',')[1].strip(), "%m/%d/%Y"):
            temp_list.append(entry)
            #print('{}: {}'.format(len(temp_list), ', '.join(entry)))
    print_entries(temp_list)
    del_or_update_entry_menu(temp_list)
                

def del_or_update_entry_menu(temp_list, paging = False):
    """ Menu for deleting or updating entries from a given list """

    if paging == False: print("""
Would you like to:

[M]: Go back to the main menu.
[S]: Go back to the search menu.
[U]: Update any of the above entries.
[D]: Delete any of the above entries.
[Q]: Quit and exit the program.
""")
    else: print("""
Would you like to:

[M]: Go back to the main menu.
[S]: Go back to the search menu.
[U]: Update any of the above entries.
[D]: Delete any of the above entries.
[Q]: Quit and exit the program.
[C]: Continue paging.
""")

    del_update_choice = input("Please select an option from the above menu: ").lower().strip()
    
    if del_update_choice == 'q':
        clear()
        sys.exit()
    elif del_update_choice == 'm':
        clear()
        main_menu()
    elif del_update_choice == 's':
        clear()
        search_menu()
    elif del_update_choice == 'u':
        update_entry(temp_list)
        search_menu()
    elif del_update_choice == 'd':
        delete_entry(temp_list)
        search_menu()
    elif del_update_choice == 'c' and paging == True:
        return
    else:
        input("""Invalid choice, please check the menu options.
              Press enter to continue""")
        del_or_update_entry_menu(temp_list)

        
def update_entry(entries_to_update_from):
    """ Updates an entry from a list of entries """

    update_entry_idx = input("Which entry would you like to update, please select the index for that entry (e.g.,1): ")
    if update_entry_idx:
        print("""
What would you like to update:
        
[D]: Date
[T]: Time spent
[N]: Task Name
[S]: Task Notes
        
        """)
        if len(entries_to_update_from) == 1: update_entry_idx = 1
        update_choice = input("Please select an option from the above menu: ").lower().strip()
        if update_choice == 'd':
            new_date = get_task_date()
            entries.update_entry(entries_to_update_from[int(update_entry_idx) - 1], 0, new_date)
        if update_choice == 'n':
            new_task_name = get_task_name()
            entries.update_entry(entries_to_update_from[int(update_entry_idx) - 1], 1, new_task_name)
        if update_choice == 't':
            new_time_spent = get_task_mins()
            entries.update_entry(entries_to_update_from[int(update_entry_idx) - 1], 2, new_time_spent)                            
        if update_choice == 's':
            new_notes = input("Please enter new notes: ")
            entries.update_entry(entries_to_update_from[int(update_entry_idx) - 1], 3, new_notes) 
        input(""" Entry/Entries updated! Press enter to continue """)
        clear()

def delete_entry(entries_to_delete_from):
    """ Deletes an entry from a list of entries """

    del_entry_idx_list = input("Which entry/entries would you like to delete, please select the index for that entry (e.g.,1 OR 1,2): ")
    if del_entry_idx_list:
        for k in del_entry_idx_list.split(','):
            entries.delete_entry(entries_to_delete_from[int(k) - 1])
    input("""Entry/Entries deleted! Press enter to continue """)
    clear()
     

def search_by_time_spent():
    """ Search the worklog entries by time spent """

    found = False
    temp_list = []
    find_by_time_spent = input("Please provide a time in mins to search in time spent: ")
    for idx, entry in enumerate(entries.log_entries):
        if find_by_time_spent == entry[2]:
            found = True
            temp_list.append(entry)
            #print('{}: {}'.format(len(temp_list), ', '.join(entry)))
    else:
        if found == False:
            print("No entries were found!!!")
            search_menu()
        else:
            print_entries(temp_list)
            del_or_update_entry_menu(temp_list)

                
def search_by_exact_match():
    """ Search the worklog entries by exact string match in task name or task notes """

    found = False
    temp_list = []
    find_by_match = input("Please provide the exact string you would like to search for in task names or task notes: ")
    for entry in entries.log_entries:
       if (find_by_match in entry[1]) or (find_by_match in entry[3]):
            found = True
            temp_list.append(entry)
            #print('{}: {}'.format(len(temp_list), ', '.join(entry)))
    else:
        if found == False:
            print("No entries were found!!!")
            search_menu()
        else:
            print_entries(temp_list)
            del_or_update_entry_menu(temp_list)

def search_by_pattern():
    """ Search the worklog entries by regex pattern in task name or task notes """

    found = False
    temp_list = []
    find_by_pattern = input("Please provide the regex/pattern string you would like to search for in task names or task notes: ")
    for entry in entries.log_entries:
        if (re.search(find_by_pattern, entry[1])) or (re.search(find_by_pattern, entry[3])):
            found = True
            temp_list.append(entry)
            #print('{}: {}'.format(len(temp_list), ', '.join(entry)))
    else:
        if found == False:
            print("No entries were found!!!")
            search_menu()
        else:
            print_entries(temp_list)
            del_or_update_entry_menu(temp_list)

def print_entries(entries_to_print):
    """ Gives an option to the user to either look all the entries at the same time or page through them """

    print("""
Would you like to:

[A]: Display all the entries at the same time.
[P]: Page through the entries one at a time.
        """)
    print_choice = input("Please select an option from the above menu: ").lower().strip()
    if print_choice == 'a':
        for i, entry in enumerate(entries_to_print):
            #print('{}: {}'.format(i + 1, ', '.join(entry)))
            print("\n{}: Task name: {}\n   Task date: {}\n   Task time spent: {}\n   Task notes: {}\n".format(i + 1, entry[1], entry[0], entry[2], entry[3]))
    elif print_choice == 'p':
        display_entries(entries_to_print)
        main_menu()


def display_paging_options(index, entries):
    """ Displays a menu that let's the user page through the entries."""

    print("\n")
    p = "[P] - Previous entry"
    n = "[N] - Next entry"
    q = "[Q] - Quit and return to Main Menu"
    menu = [p, n, q]

    if index == 0:
        menu.remove(p)
    elif index == len(entries) - 1:
        menu.remove(n)

    for option in menu:
        print(option)


def display_entries(entries):
    """ Pages the entries to the screen."""
    index = 0

    while True:
        clear()
        #print("{}: {}".format(index + 1, ','.join(entries[index])))
        print("\n{}: Task name: {}\n   Task date: {}\n   Task time spent: {}\n   Task notes: {}\n".format(index + 1, entries[index][1], entries[index][0], entries[index][2], entries[index][3]))
        del_or_update_entry_menu([entries[index]], paging = True)

        if len(entries) == 1:
            input("Press ENTER to continue to the main menu.")
            main_menu()

        display_paging_options(index, entries)

        page_choice = input("Please select an option from the above menu: ").lower().strip()

        if index == 0 and page_choice == 'n':
            index += 1
            clear()
        elif index > 0 and index < len(entries) - 1 and page_choice == 'n':
            index += 1
            clear()
        elif index > 0 and index < len(entries) - 1 and page_choice == 'p':
            index -= 1
            clear()
        elif index == len(entries) - 1 and page_choice == 'p':
            index -= 1
            clear()
        elif page_choice == 'q':
            main_menu()
        else:
            input("""Invalid choice, please check the menu options.
              Press enter to continue""")

if __name__ == '__main__':
    clear()
    main_menu()

