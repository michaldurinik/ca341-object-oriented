#!/usr/bin/python3
import pickle
from sys import exit as exit_program


class Day:

    def __init__(self, day="default"):
        self.day = day
        self.schedule = []

    def get_day(self):
        return self.day

    def get_schedule(self):
        return self.schedule

    def __str__(self):
        return "{:<10} {}" .format(self.day, " ".join([str(t) for t in self.get_schedule()]) + "\n")


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
        s = ""
        for d in self.week:
            s += d.__str__()
        return s


class Calendar(Week, Day):

    def __init__(self):
        super().__init__()
        pass

    def add_appointment(self, d, description="N/A", start_time=0, finish_time=0):
        if hrs_to_mins(start_time) < hrs_to_mins(finish_time):
            print("Error, finish time cannot be lower than start time")
            return "error"

        self.week[d].schedule.append([len(self.week[d].schedule) + 1, description, start_time, finish_time])
        print("Appointment has been added successfully")

    def remove_appointment(self, d, idx):
        del self.week[d].schedule[idx - 1]
        print("Appointment has been removed successfully")

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
    if time.find(":"):
        if time.count(":") > 1:
            return None

        h, m = time.split(":")
        try:
            h, m = int(h), int(m)
        except ValueError:
            return None

        if h <= 24 and m <= 59:
            return [h, m]

    return None


def hrs_to_mins(time):
    h, m = time
    return h*60 + m


def printable_hrs_mins(h, m):
    h, m = str(h), str(m)
    if len(h) == 1:
        h = "0" + h
    if len(m) == 1:
        m = "0" + m

    return h + ":" + m


def print_day(calendar, d):
    print(calendar[d])


def print_week(calendar):
    print(calendar)


def add_app(calendar):
    print("Enter DAY of an appointment:")
    day = parse_day(input())
    if day is None:
        wrong_input()
        add_app(calendar)

    correct = False
    while not correct:
        print("Appointment NAME (max.30 characters):")
        name = input()
        if len(name) <= 30:
            correct = True

    correct = False
    while not correct:
        print("Start time ('HH:MM'):")
        start = parse_time(input())
        if start is not None:
            correct = True

    correct = False
    while not correct:
        print("Finish time ('HH:MM'):")
        finish = parse_time(input())
        if finish is not None:
            correct = True

    if calendar.add_appointment(day, name, start, finish) is "error":
        return

    with open("data.pkl", "wb") as output_file:
        pickle.dump(calendar, output_file, pickle.HIGHEST_PROTOCOL)


def rem_app(calendar):
    print("Please enter DAY of an appointment:")
    day = parse_day(input())
    if day is not None:
        d = calendar[day]
    else:
        wrong_input()
        rem_app(calendar)

    print(d)

    correct = False
    while not correct:
        print("Please enter NUMBER of an appointment to be removed:")
        num = input()
        try:
            num = int(num)
        except ValueError:
            wrong_input()

    print("yo")


def wrong_input():
    print("Error wrong input format!")


def welcome_message():
    print("For information about all commands and shortcuts, enter 'h' or 'help'")
    print("To start, enter 'w' for week schedule, '5' or 'fri' for friday schedule")
    print("Enter 'add' to add appointment, 'rem' to remove it.")


def help_commands(*args):
    print("#################################################################")
    print("Display WEEK schedule: 'w' or 'week'")
    print("Display DAY schedule, example Monday: '1', 'm', 'mon' or 'Monday'")
    print("To ADD appointment: 'a', 'add'")
    print("To REMOVE appointment: 'r', 'rem', 'remove', 'del' or 'delete'")
    print("#################################################################")


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
        print("Please enter action:")
        user_in = input()
        try:
            function_dict(user_in, cal)
        except KeyError:
            wrong_input()


if __name__ == "__main__":
    main()
