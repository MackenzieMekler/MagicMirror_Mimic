import time
import datetime

class Time:
    def __init__(self):
        self.today = datetime.date.today()
    def getTime(self):
        return time.strftime('%H:%M:%S')
    def getDate(self):
        return self.today.strftime('%A %b %d')