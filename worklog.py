import datetime
import csv
import os


class Entries:
    log_entries = []
    
    def __init__(self):
        exists = os.path.isfile('log.csv')
        if exists:
            with open('log.csv', 'r') as csv_file:
                csv_r = csv.DictReader(csv_file)
                for row in csv_r:
                    self.log_entries.append([row['Date'], row['Task Name'], row['Task Mins'], row['Task Notes']])
        else:
            self.log_entries = []

    def new_entry(self, task_date, task_name, task_mins, task_notes):
        self.log_entries.append([task_date, task_name, task_mins, task_notes])
        self.write_to_csv()
        
    def update_entry(self, entry, update_choice, update_value):
        indx = self.log_entries.index(entry)
        self.log_entries[indx][update_choice] = update_value
        self.write_to_csv()
    
    def delete_entry(self, entry):
        self.log_entries.remove(entry)
        self.write_to_csv()
    
    def display_all_entries(self):
        for entry in self.log_entries:
            print(entry)
            
    def write_to_csv(self):
        open('log.csv', 'w').close()
        with open('log.csv', 'w') as csv_file:
            field_names = ['Date', 'Task Name', 'Task Mins', 'Task Notes']
            csv_w = csv.DictWriter(csv_file, fieldnames = field_names)
            csv_w.writeheader()
            for entry in self.log_entries:
                csv_w.writerow({'Date': entry[0], 'Task Name': entry[1], 'Task Mins': entry[2], 'Task Notes': entry[3]})

    
        
    
    