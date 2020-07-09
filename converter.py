import datetime
import json
from datetime import datetime as dt

class Converter:
    def __init__(self):
        self.diacritice = {}
        self.diacs = {
            'ă': 'a',
            'â': 'a',
            'î': 'i',
            'ț': 't',
            'ș': 's'
        }

    def eliminateDiac(self, word):
        newWord = ""
        found = False
        for c in word:
            try:
                newWord += self.diacs[c]
                found = True
            except:
                newWord += c
        if found:
            self.diacritice.update({newWord: word})
        return newWord

    def withDiac(self, word):
        try:
            return self.diacritice[word]
        except:
            return word

    def convertRequest(self):   # pe 2 merge
        with open("modele_json/intreabaVremeaAfara/1.json", "r", encoding="utf8") as read_file:
            data = json.load(read_file)

        for entity in data['entities']:
            s = entity['value']
            s = s.split()
            # print(s)
            entity['value'] = self.eliminateDiac(entity['value'])

        with open("requestFaraDiac.json", "w", encoding="utf8") as write_file:
            json.dump(data, write_file)

class DateHandler:
    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def get_days_ahead(self, nr, hour):
        d = datetime.datetime(dt.today().year, dt.today().month, dt.today().day, hour, 0, 0)
        return d + datetime.timedelta(nr)

    def getNumOfDay(self, day):
        switcher = {
            'luni'      : 0,
            'marti'     : 1,
            'miercuri'  : 2,
            'joi'       : 3,
            'vineri'    : 4,
            'sambata'   : 5,
            'duminica'  : 6,
            'azi'       : 7,
            'maine'     : 8,
            'poimaine'  : 9
        }
        try:
            return switcher.get(day)
        except:
            return -1

    def getMonth(self, month):
        switcher = {
            'ianuarie'      : 1,
            'februarie'     : 2,
            'martie'        : 3,
            'aprilie'       : 4,
            'mai'           : 5,
            'iunie'         : 6,
            'iulie'         : 7,
            'august'        : 8,
            'septembrie'    : 9,
            'octombrie'     : 10,
            'noiembrie'     : 11,
            'decembrie'     : 12
        }
        try:
            return switcher[month]
        except:
            return -1
    
    def getDayAndMonth(self, date):
        parsedDate = date.split()
        if(self.getMonth(parsedDate[0]) != -1):
            month = self.getMonth(parsedDate[0])
            day = int(parsedDate[1])

        elif(self.getMonth(parsedDate[1]) != -1):
            month = self.getMonth(parsedDate[1])
            day = int(parsedDate[0])

        else:
            return (-1,-1)

        return (day, month)

    def getDate(self, day, month, hour):
        return datetime.datetime(dt.today().year, int(month), int(day), hour, 0, 0)


    def getNextWeekday(self, day, hour):
        date = self.getNumOfDay(day)
        d = datetime.datetime(dt.today().year, dt.today().month, dt.today().day, hour, 0, 0)
        return self.next_weekday(d, date) # 0 = Monday, 1=Tuesday, 2=Wednesday...

    def getTodayOrTomorrow(self, day, hour):
        if day == 7:
            return datetime.datetime(dt.today().year, dt.today().month, dt.today().day, hour, 0, 0)
        elif day == 8:
            return self.get_days_ahead(1, hour)
        elif day == 9:
            return self.get_days_ahead(2, hour)
