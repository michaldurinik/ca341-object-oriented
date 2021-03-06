#!/usr/bin/python3
import pickle
from sys import exit as exit_program, executable, argv
from bisect import bisect_right
import os
from time import sleep


class Day:

    def __init__(self, day="default"):
        self.day = day
        self.schedule = []      # [[name1, start1, finish1], [name2, start2, finish2]]
        self.schedule_lst = []  # start followed by finish time for each app (in minutes) [start, finish, start, finish]

    def get_day(self):
        return self.day

    def get_schedule(self):
        return self.schedule

    def __str__(self):
        s =  "|=================================================|\n"
        s += "|{:<10s}#  {:<20s} {:s}   {:s} |\n".format(self.day, "Name", "Start", "Finish")
        s += "|=================================================|\n"

        for i, appointment in enumerate(self.schedule):
            name, start, finish = appointment
            s += "|{:>11d}. {:<20s} {:s} - {:s}  |\n".format(i+1, name, start, finish)
        s += "|=================================================|\n"
        return s

    def __repr__(self):
        s = "|{:<11}".format(self.day)
        for num, appointment in enumerate(self.schedule):
            name, start, finish = appointment
            short_version = "{} {}-{}".format(name_to_initials(name), start, finish)
            # only 4 appointments per line
            if num % 4 == 0 and num != 0:
                s += "\n|{:<11}".format("")

            s += (short_version + "   ")
            # after 4 apps add "|"
            if num % 4 == 3:
                s = s.rstrip()
                s += " |"

        # last appointment
        if len(self.schedule) % 4 != 0:
            num = 4 - len(self.schedule) % 4
            s = s.rstrip()
            s += (num * "                 " + " |")

        if len(self.schedule) == 0:
            s += "                                                                  |"

        return s + "\n"


class Week(Day):

    def __init__(self):
        super().__init__()
        self.week = [Day("Monday"), Day("Tuesday"), Day("Wednesday"), Day("Thursday"), Day("Friday"), Day("Saturday"),
                     Day("Sunday")]

    def __iter__(self):
        for d in self.week:
            yield d

    def __getitem__(self, idx):
        return self.week[idx]

    def __str__(self):
        s = "|=============================================================================|\n"
        for d in self.week:
            s += d.__repr__()
        return s + "|=============================================================================|\n"


class Calendar(Week, Day):

    def __init__(self):
        super().__init__()
        pass

    def add_appointment(self, d, description="N/A", start_time=0, finish_time=0):
        start, finish = hrs_to_min(start_time), hrs_to_min(finish_time)
        if start > finish:
            print("Error, finish time cannot be lower than start time, returning...")
            return "error"

        valid = False
        idx = bisect_right(self.week[d].schedule_lst, start)
        if idx % 2 == 0:
            # start is not between start and finish time of other appointment
            # and we are not at the end of array
            if idx == len(self.week[d].schedule_lst):
                valid = True
            else:
                if finish <= self.week[d].schedule_lst[idx]:
                    valid = True

            if valid:
                # schedule is half the size of schedule_lst
                self.week[d].schedule.insert(idx // 2, [description, printable_hrs_min(start_time),
                                                        printable_hrs_min(finish_time)])
                self.week[d].schedule_lst.insert(idx, start)
                self.week[d].schedule_lst.insert(idx + 1, finish)
                print("Appointment has been added successfully")
                return

        print("Error, appointments are overlapping")
        return "error"

    def remove_appointment(self, d, idx):
        if idx >= len(self.week[d].schedule):
            print("No such appointment number, returning...")
            return "error"
        else:
            del self.week[d].schedule[idx]
            del self.week[d].schedule_lst[idx * 2]
            # elements will shift after deletion
            del self.week[d].schedule_lst[idx * 2]
            print("Appointment has been removed successfully")
            return

    def __str__(self):
        return super().__str__()


def parse_day(key):
    key = key.lower()
    d = {"1": 0,
         "m": 0,
         "mon": 0,
         "monday": 0,
         "2": 1,
         "tue": 1,
         "tuesday": 1,
         "3": 2,
         "wed": 2,
         "Wednesday": 2,
         "4": 3,
         "thu": 3,
         "thursday": 3,
         "5": 4,
         "f": 4,
         "fri": 4,
         "friday": 4,
         "6": 5,
         "sat": 5,
         "saturday": 5,
         "7": 6,
         "sun": 6,
         "sunday": 6,
    }
    if key not in d:
        return None
    else:
        return d[key]


def parse_time(time):
    if time.find(":") != -1:
        if time.count(":") > 1:
            return None

        h, m = time.split(":")
        try:
            h, m = int(h), int(m)
        except ValueError:
            return None

        if h <= 24 and m <= 59:
            return [h, m]

    try:
        h = int(time)
    except ValueError:
        return None

    if h <= 24:
        return [h, 0]

    return None


def hrs_to_min(time):
    h, m = time
    return h*60 + m


def printable_hrs_min(time):
    h, m = time
    h, m = str(h), str(m)
    if len(h) == 1:
        h = "0" + h
    if len(m) == 1:
        m = "0" + m

    return h + ":" + m


def name_to_initials(name):
    first, surname = "X", ["X"]
    if name.find(" ") != -1:
        first, *surname = name.split(" ")
    return first[0].upper() + surname[0][0].upper()


def print_day(calendar, d):
    print(calendar[d])


def print_week(calendar):
    print(calendar)


def add_app(calendar):
    print("Enter DAY of an appointment: ", end="")
    day = parse_day(input())
    if day is not None:
        d = calendar[day]
    else:
        wrong_input()
        add_app(calendar)

    print(d)

    correct = False
    while not correct:
        print("Appointment NAME (max.20 characters): ", end="")
        name = input()
        if len(name) <= 20:
            correct = True

    correct = False
    while not correct:
        print("Start time ('HH:MM'): ", end="")
        start = parse_time(input())
        if start is not None:
            correct = True
        else:
            wrong_input()

    correct = False
    while not correct:
        print("Finish time ('HH:MM'): ", end="")
        finish = parse_time(input())
        if finish is not None:
            correct = True
        else:
            wrong_input()

    if calendar.add_appointment(day, name, start, finish) is "error":
        return

    with open("data.pkl", "wb") as output_file:
        pickle.dump(calendar, output_file, pickle.HIGHEST_PROTOCOL)


def rem_app(calendar):
    print("Please enter DAY of an appointment: ", end="")
    day = parse_day(input())
    if day is not None:
        d = calendar[day]
    else:
        wrong_input()
        rem_app(calendar)

    print(d)

    correct = False

    while not correct:
        print("Please enter NUMBER of an appointment to be removed: ", end="")
        num = input()
        try:
            num = int(num)
        except ValueError:
            wrong_input()
        else:
            correct = True

    num = int(num) - 1  # list index start at zero not 1
    if calendar.remove_appointment(day, num) is "error":
        return

    with open("data.pkl", "wb") as output_file:
        pickle.dump(calendar, output_file, pickle.HIGHEST_PROTOCOL)


def clear_calendar(calendar):
    cal = Calendar()
    with open("data.pkl", "wb") as output_file:
        pickle.dump(cal, output_file, pickle.HIGHEST_PROTOCOL)

    # restarting script
    print("Calendar will be cleared after restart")
    sleep(0.5)
    i = 3
    while i > 0:
        print("Restarting...{:}".format(i))
        sleep(1)
        i -= 1
    os.execl(executable, os.path.abspath(__file__), *argv)


def wrong_input():
    print("Error wrong input format!")


def welcome_message():
    print("|=======================================================================|")
    print("| For information about all commands and shortcuts, enter 'h' or 'help' |")
    print("|=======================================================================|")
    print()
    print("Enter 'w' for week schedule, '5' or 'fri' for friday schedule")
    print("Enter 'add' to add appointment, 'rem' to remove it.")
    print()
    

def help_commands(*args):
    print("|===================================================================|")
    print("| Display WEEK schedule: 'w' or 'week'                              |")
    print("| Display DAY schedule, example Monday: '1', 'm', 'mon' or 'Monday' |")
    print("| To ADD appointment: 'a', 'add'                                    |")
    print("| To REMOVE appointment: 'r', 'rem', 'remove', 'del' or 'delete'    |")
    print("| To CLEAR ALL appointments for week: 'clear'                       |")
    print("|===================================================================|")
    print()


def function_dict(key, calendar):
    key = key.lower()
    dict = {
        "w": print_week,
        "week": print_week,
        "a": add_app,
        "add": add_app,
        "r": rem_app,
        "rem": rem_app,
        "remove": rem_app,
        "del": rem_app,
        "delete": rem_app,
        "clear": clear_calendar,
        "h": help_commands,
        "help": help_commands,
    }

    if key == "ex" or key == "exit":
        exit_program()

    if parse_day(key) is not None:
        print_day(calendar, parse_day(key))
        return

    return dict[key](calendar)


def main():

    try:
        with open("data.pkl", "rb") as input_file:
            cal = pickle.load(input_file)
    except FileNotFoundError:
        cal = Calendar()

    welcome_message()

    while True:
        print(">>> ", end="")
        user_in = input()
        try:
            function_dict(user_in, cal)
        except KeyError:
            wrong_input()


if __name__ == "__main__":
    main()
