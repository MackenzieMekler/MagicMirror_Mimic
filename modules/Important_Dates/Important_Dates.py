import datetime
import json

class Important_Dates:
    def __init__(self):
        self.today = datetime.date.today()

    def writeBirthdays(self, name, birthday):
        with open("birthday_list.json", 'r') as f:
            loaded_birthdays = json.load(f)
        try:
            loaded_birthdays[f"{birthday}"].append(name)
        except:
            loaded_birthdays[f"{birthday}"] = [f"{name}"]

        # writing to a file
        with open('birthday_list.json', 'w') as f:
            json.dump(loaded_birthdays, f)

    def readData(self):
        with open("C:\\Users\\mackm\\PycharmProjects\\MagicMirror\\modules\\Important_Dates\\birthday_list.json", 'r') as f:
            data = json.load(f)

        return data

    def getBirthdays(self):
        birthdays_json = self.readData()["birthdays"]
        vips = self.readData()["VIPs"]
        dates = [
            self.today + datetime.timedelta(days=0),
            self.today + datetime.timedelta(days=1),
            self.today + datetime.timedelta(days=2),
            self.today + datetime.timedelta(days=3),
            self.today + datetime.timedelta(days=4),
            self.today + datetime.timedelta(days=5),
            self.today + datetime.timedelta(days=6)
        ]

        # turn json into a list of tuples where the 0 value is the date (datetime obj) and the 1 value is the list of people
        birthdays_list = []
        for i in range(len(birthdays_json)):
            value = (datetime.datetime.strptime(birthdays_json[i][0], "%Y-%m-%d"), birthdays_json[i][1])
            birthdays_list.append(value)

        this_week = []
        this_month = []
        for day in birthdays_list:
            status = True
            for date in dates:
                if day[0].day == date.day and day[0].month == date.month:
                    this_week.append(day)
                    status = False
            if status:
                for person in day[1]:
                    for vip in vips:
                        if person == vip:
                            if day[0].month == self.today.month or (self.today.day > 15 and day[0].month == self.today.month + 1):
                                this_month.append(day)

        return this_week, this_month