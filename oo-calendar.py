import calendar as cal
import tkinter


class Day:

    def __init__(self, day="Monday", schedule=[]):
        self.day = day
        self.schedule = schedule
        self.day_data = (self.day, self.schedule)

    def get_day(self):
        return self.day

    def get_schedule(self):
        return self.schedule


class Week(Day):

    def __init__(self):
        super().__init__()
        self.week = [Day("Monday"), Day("Tuesday"), Day("Wednesday"), Day("Thursday"), Day("Friday"), Day("Saturday"),
                     Day("Sunday")]

    def __str__(self):
        s = ""
        for data in self.week:
            s += (data.get_day() + " " + " ".join([str(t) for t in data.get_schedule()]) + "\n")
        return s


class Calendar(Week, Day):

    def __init__(self):
        super().__init__()
        pass

    def add_appointment(self, d, start_time, duration):
        if d < 7:
            self.week[d].schedule = [start_time, duration]

    def remove_appointment(d, start_time):
        pass
        # will see number of appointments in day can remove by index

    def __str__(self):
        return super().__str__()

def main():
    #top = tkinter.Tk()
    #top.mainloop()
    c = Calendar()
    print(c)
    c.add_appointment(3, 9, 2)
    print(c)


if __name__ == "__main__":
    main()
