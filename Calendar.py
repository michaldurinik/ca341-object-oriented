import tkinter
from sys import exit


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

    def add_appointment(self, d, start_time=0, finish_time=0, description="N/A"):
        if d < 7:
            self.week[d].schedule.append([len(self.week[d].schedule) + 1, start_time, finish_time, description])
            print("Appointment has been added successfully")

    def remove_appointment(self, d, idx):
        del self.week[d].schedule[idx - 1]
        print("Appointment has been removed successfully")

    def __str__(self):
        return super().__str__()


def wrong_input():
    print("Wrong input format!")


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
         "w": 2,
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


#def parse_day(day):
#    return day_dict(day)


def parse_time(time):
    h, m = 0, 0
    if time.find(":"):
        h, m = time.split(":")


def print_day(calendar, d):
    print(calendar[d - 1])


def print_week(calendar):
    print(calendar)


def choose_day(calendar):
    print("Please enter a Day:\nexample: mon, Mon, 1")
    d = int(input())
    try:
        print_day(calendar, d)
    except:
        wrong_input()
        choose_day(calendar)


def add_app(calendar):
    print("Please enter DAY of an appointment:")
    day = parse_day(input())
    if day is None:
        wrong_input()
        add_app(calendar)

    print("Please enter appointment NAME:")
    name = input()

    print("Start time:")
    start = input()

    print("Finish time:")
    finish = input()

    calendar.add_appointment(day, start, finish, name)


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
            correct = True
        except ValueError:
            wrong_input()
    print("yo")


def function_dict(key, calendar):
    key = key.lower()
    d = {
        "w": print_week,
        "week": print_week,
        "d": choose_day,
        "day": choose_day,
        "a": add_app,
        "add": add_app,
        "r": rem_app,
        "rem": rem_app,
        "remove": rem_app,
        "del": rem_app,
        "delete": rem_app,
    }
    if key.lower() == "e":
        exit()
    return d[key](calendar)


def main():
    c = Calendar()

    while True:
        print("Please input action:")
        user_in = input()
        try:
            function_dict(user_in, c)
        except KeyError:
            wrong_input()


if __name__ == "__main__":
    main()
