from datetime import datetime, timedelta
import json
import os
from tkinter import *
from tkinter import messagebox


class Account:
    def __init__(self, username, password, owner):
        self.username = username
        self.password = password
        self.owner = owner
        self.acc_lst = []
    

    def create_acc(self, username, password, owner):
        if any(acc.get('Username') == username for acc in self.acc_lst):
            messagebox.showinfo('Oops!', 'Username already exists. Please choose a different username.')
            welcome_window()
        else:
            acc_dict = {'Username': username, 'Password': password, 'Name': owner}
            self.acc_lst.append(acc_dict)
            with open('account.txt', 'a') as f:
                json.dump(self.acc_lst, f)
                f.write('\n')          
            messagebox.showinfo('Hello!', f'Welcome! {owner} !')
            

    def login(self, username, password):
        with open('account.txt', 'r+') as f:
            for line in f:
                acc_list = json.loads(line)
                for acc_dict in acc_list:
                    if acc_dict.get('Username') == username and acc_dict.get('Password') == password:
                        messagebox.showinfo('Hello!', 'Welcome Back!')
                        return
            messagebox.showinfo('Oops!', 'Username or password is incorrect. Please try again.')
            welcome_window()
        f.close()

        
class Event:
    def __init__(self, tasks, dates):
        self.tasks = tasks
        self.dates = dates
        self.event = {}


    def add_events(self, tasks, dates):
        if dates not in self.event:
            self.event[dates] = [tasks]
        else:
            self.event[dates].append(tasks)

        messagebox.showinfo('Successfully!', 'Task added!')

        e = self.event
        with open('event.txt', 'w') as f:
            for key, val in e.items():
                f.write(f'{key}\n')
                for v in val:
                    f.write(f'{v}\n')
                f.write('\n')
                


    def remove_events(self, tasks):
        for key, val in self.event.items():
            self.event[key] = [task for task in val if task != tasks]
        with open('event.txt', 'w') as f:
            for key, val in self.event.items():
                f.write(f'{key}\n')
                for v in val:
                    f.write(f'{v}\n')
                    f.write('\n')

        messagebox.showinfo('Successfully!', 'Your task has been removed!')


    def check_events(self):
        if not self.event:
            messagebox.showinfo('Hey!', 'You do not have any events!')
        else:
            with open('event.txt', 'r+') as f:
                schedule = f.read()
                if schedule:
                  messagebox.showinfo('Events', f'{schedule}')
                f.close()


    def remind_before_event(self):
        today = datetime.today().date()
        days_before = 7

        with open('event.txt', 'r') as f:
            event_lines = f.read().splitlines()

        event_date_str = None
        tasks = []

        for line in event_lines:
            if not line:
                if event_date_str:
                    try:
                        for task in tasks:
                            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
                            reminder_date = event_date - timedelta(days=days_before)

                            if today <= reminder_date <= today + timedelta(days_before):
                                self.show_notification(f"'{task}' is due in {days_before} days on {event_date_str}.")
                                self.play_sound()
                    except ValueError as e:
                        print(f"Error processing date '{event_date_str}': {e}")

                    event_date_str = None
                    tasks = []
            else:
                if event_date_str is None:
                    event_date_str = line
                else:
                    tasks.append(line)

        if event_date_str:
            try:
                for task in tasks:
                    event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
                    reminder_date = event_date - timedelta(days=days_before)

                    if today <= reminder_date <= today + timedelta(days_before):
                        self.show_notification(f"'{task}' is due in {days_before} days on {event_date_str}.")
                        self.play_sound()
            except ValueError as e:
                print(f"Error processing date '{event_date_str}': {e}")

                

    def show_notification(self, message):
        try:
            script_path = "notification_script.scpt"
            with open(script_path, "w") as script_file:
                script_file.write(f'display notification "{message}" with title "Ding Notification App" sound name "default"')

            os.system(f"osascript {script_path}")
        finally:
            os.remove(script_path)

    def play_sound(self):
        pass

    

def create_account_window():
    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        acc.create_acc(username, password, name)
        window.destroy()
        main_window()

    window = Tk()
    window.title("Create Account")
    window.geometry('200x200')

    username_label = Label(window, text="Username:")
    username_label.pack()
    username_entry = Entry(window)
    username_entry.pack()

    password_label = Label(window, text="Password:")
    password_label.pack()
    password_entry = Entry(window, show="*")
    password_entry.pack()

    name_label = Label(window, text="Your Name:")
    name_label.pack()
    name_entry = Entry(window)
    name_entry.pack()

    create_button = Button(window, text="Create Account", command=create_account)
    create_button.pack()

    window.mainloop()

def login_window():
    def login():
        user_login = user_entry.get()
        pass_login = pass_entry.get()
        acc.login(user_login, pass_login)
        window.destroy()
        main_window()

    window = Tk()
    window.title("Login")
    window.geometry('200x200')

    user_label = Label(window, text="Username:")
    user_label.pack()
    user_entry = Entry(window)
    user_entry.pack()

    pass_label = Label(window, text="Password:")
    pass_label.pack()
    pass_entry = Entry(window, show="*")
    pass_entry.pack()

    login_button = Button(window, text="Login", command=login)
    login_button.pack()

    window.mainloop()


def main_window():
    def add_task():
        task = task_entry.get()
        year = year_entry.get()
        month = month_entry.get()
        day = day_entry.get()
        date_enter = datetime(int(year), int(month), int(day)).date()
        sch.add_events(task, date_enter)

    def remove_task():
        re_task = re_task_entry.get()
        sch.remove_events(re_task)

    def check_schedule():
        sch.check_events()
        sch.remind_before_event()

    def exit_option():
        sch.remind_before_event()
        exit()


    window = Tk()
    window.title("Ding Notification App")
    window.geometry('300x400')

    task_label = Label(window, text="Task:")
    task_label.pack()
    task_entry = Entry(window)
    task_entry.pack()

    year_label = Label(window, text="Year:")
    year_label.pack()
    year_entry = Entry(window)
    year_entry.pack()

    month_label = Label(window, text="Month:")
    month_label.pack()
    month_entry = Entry(window)
    month_entry.pack()

    day_label = Label(window, text="Day:")
    day_label.pack()
    day_entry = Entry(window)
    day_entry.pack()

    add_button = Button(window, text="Add Task", command=add_task)
    add_button.pack()

    re_task_label = Label(window, text="Task to Remove:")
    re_task_label.pack()
    re_task_entry = Entry(window)
    re_task_entry.pack()

    remove_button = Button(window, text="Remove Task", command=remove_task)
    remove_button.pack()

    check_button = Button(window, text="Check Schedule", command=check_schedule)
    check_button.pack()

    exit_button = Button(window, text='Exit', command=exit_option)
    exit_button.pack()
    
    window.mainloop()


def welcome_window():
    def create_account_option():
        create_account_window()

    def login_option():
        login_window()

    window = Tk()
    window.title('Welcome to Ding Notification!')
    window.geometry("600x400")

    create_label = Label(window)
    create_label.pack()

    create_acc_button = Button(window, text="Create Account", command=create_account_option)
    create_acc_button.pack()

    login_label = Label(window)
    login_label.pack()

    login_acc_button = Button(window, text='Login', command=login_option)
    login_acc_button.pack()

    window.mainloop()


acc = Account('user', 'pass', 'name')
sch = Event('task', 'date')

welcome_window()