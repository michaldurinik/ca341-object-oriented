import calendar as cal
import tkinter


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

    def add_appointment(self, d, description="", start_time=0, finish_time=0):
        if d < 7:
            self.week[d].schedule.append([description, start_time, finish_time])

    def remove_appointment(d, start_time):
        pass
        # will see number of appointments in day can remove by index

    def __str__(self):
        return super().__str__()


def parse_time(time):
    h, m = 0, 0
    if time.find(":"):
        h, m = time.split(":")

def main():
    #top = tkinter.Tk()
    #top.mainloop()
    c = Calendar()
    c.add_appointment(4, 9, 2)
    c.add_appointment(4, 12, 2)
    c.add_appointment(4, "Tom", 15, 2)
    c.add_appointment(4, 18, 2)
    c.add_appointment(2, 13, 5)


    print(c)

    print(c[1])

if __name__ == "__main__":
    main()
