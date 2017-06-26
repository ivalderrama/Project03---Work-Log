import csv
import datetime
import json
import os
import re

date_entry = ''
title_task = ''
time_spent = None
notes = ''


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def user_date():
    global date_entry
    while True:
        date_entry = input("Date of task\nPlease use DD/MM/YYYY: ")
        try:
            datetime.datetime.strptime(date_entry, '%d/%m/%Y')
        except ValueError:
            print("""
{} is an invalid date. Please enter a correct date.""".format(date_entry))
            continue
        break


def user_task():
    global title_task
    while True:
        title_task = input("Title of task: ")
        try:
            if not title_task:
                raise ValueError('Cannot be blank')
        except ValueError as e:
            print(e)
            continue
        break


def user_time():
    global time_spent
    while True:
        time_spent = input("Time spent (rounded minutes): ")
        try:
            int(time_spent)
        except ValueError:
            print("""
Please input a rounded minute. i.e if 1.5, input 2; if 1.1 input 1""")
            continue
        break


def append_csv():
    with open('log.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([date_entry, title_task, time_spent, notes])


def create_csv():
    with open('log.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Date', 'Task title', 'Time spent', 'Notes'])


def convert_to(row):
    row_json = json.dumps(row)
    my_dict = json.loads(row_json)
    for keys, values in my_dict.items():
        print(keys + ": " + values)


def main():
    global notes

    while True:
        m_menu_ans = input("""
WORK LOG
What would you like to do?
a) Add new entry
b) Search in existing entries
c) Quit Program
> """).lower()

        if m_menu_ans == 'a':
            clear_screen()
            user_date()
            clear_screen()
            user_task()
            clear_screen()
            user_time()
            clear_screen()
            notes = input("Notes (Optional, you can leave this empty): ")

            if os.path.exists('log.csv'):
                append_csv()
                print("Entry has been added.")
            else:
                create_csv()
                append_csv()
                print("Entry has been added.")

        elif m_menu_ans == 'b':
            clear_screen()
            while True:
                sub_menu = input("""
Do you want to search by:
a) Date
b) Time Spent
c) Exact Search
d) Regex Pattern
e) Return to menu
> """).lower()
                if sub_menu == 'a':
                    clear_screen()
                    user_date()
                    with open('log.csv', 'r') as file:
                        for row in csv.DictReader(file):
                            if row['Date'] == date_entry:
                                print("")
                                convert_to(row)

                if sub_menu == 'b':
                    clear_screen()
                    user_time()
                    with open('log.csv', 'r') as file:
                        for row in csv.DictReader(file):
                            if row['Time spent'] == time_spent:
                                print("")
                                convert_to(row)

                if sub_menu == 'c':
                    clear_screen()
                    exact_search = input("""
Enter the exact phrase to search for: """)
                    with open('log.csv', 'r') as file:
                        for row in csv.DictReader(file):
                            if row['Task title'] == exact_search:
                                print("")
                                convert_to(row)
                            elif row['Notes'] == exact_search:
                                print("")
                                convert_to(row)
                            elif row['Time spent'] == exact_search:
                                print("")
                                convert_to(row)
                            elif row['Date'] == exact_search:
                                print("")
                                convert_to(row)

                if sub_menu == 'd':
                    clear_screen()
                    names_file = open("log.csv", encoding="utf-8")
                    data = names_file.read()
                    names_file.close()

                    regex_input = input("""
Enter a regular expression, i.e. \d{2}[-/]\d{2}[-/]\d{4}: """)
                    #regex_pattern = r'{}'.format(regex_input)

                    line = re.compile(regex_input, re.I)
                    new_list = line.findall(data)

                    with open('log.csv', 'r') as file:
                        for row in csv.DictReader(file):
                            for value in new_list:
                                if value == row['Task title']:
                                    print("")
                                    convert_to(row)
                                elif value == row['Notes']:
                                    print("")
                                    convert_to(row)
                                elif value == row['Time spent']:
                                    print("")
                                    convert_to(row)
                                elif value == row['Date']:
                                    print("")
                                    convert_to(row)

                if sub_menu == 'e':
                    break

        elif m_menu_ans == 'c':
            clear_screen()
            print("Thanks for using the Work Log app. \nSee you soon!")
            break

        else:
            clear_screen()
            print("You did not enter a valid option!")


if __name__ == "__main__":
    main()
