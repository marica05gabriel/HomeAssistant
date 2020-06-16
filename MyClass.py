from pyswip import Prolog
from converter import Converter, DateHandler
from calendarController import EventPrototype, CalendarController
from datetime import datetime as dt
import datetime

class MyClass:
    def __init__(self):
        self.prolog = Prolog()
        self.filename = 'test.pl'
        self.converter = Converter()
        self.dateHandler = DateHandler()
        self.eventPrototype = EventPrototype()
        self.calendar = CalendarController()

    def start(self):
        self.converter.convertRequest()
        self.prolog.consult(self.filename)
        list(self.prolog.query('handling_received.'))
        list(self.prolog.query('populate.'))

    def handleWarning(self, myList):
        myList.remove('warning')
    
    def getSlots(self, slotNames):
        slots = {}
        print(slotNames)
        for slotName in slotNames:
            q = "entity(%s, %s)." % (slotName, slotName.capitalize())
            x = list(self.prolog.query(q))[0][slotName.capitalize()]
        
            slots.update({slotName.capitalize(): x})
        return slots
    
    def getIntent(self):
        return list(self.prolog.query("intent(Intent)"))[0]['Intent']

    def manageDate(self, slots):
        startHour = int(slots['Ora_inceput'])
        endHour = slots.get('Ora_final')
        if(endHour == None):
            endHour = startHour + 1
        endHour = int(endHour)
        
        givenDate = slots['Data']
        dateIndex = self.dateHandler.getNumOfDay(givenDate)
        if dateIndex == None:
            dayMonth = self.dateHandler.getDayAndMonth(givenDate)
            if(dayMonth == (-1,-1)):
                print("Date not recognized" )
                return
            else:
                self.startDate = self.dateHandler.getDate(dayMonth[0], dayMonth[1], startHour)
        elif 0 <=  dateIndex and dateIndex < 7:
            self.startDate = self.dateHandler.getNextWeekday(givenDate, startHour)
        elif 7 <= dateIndex and dateIndex < 10:
            self.startDate = self.dateHandler.getTodayOrTomorrow(dateIndex, startHour)

        self.endDate = self.dateHandler.getDate(self.startDate.day, self.startDate.month, endHour)

    def handleAddEvent(self, slots):
        self.manageDate(slots)
        summary = self.converter.withDiac(slots['Event'])
        print(summary)

        event = self.eventPrototype.build(summary,self.startDate.isoformat(), self.endDate.isoformat())
        print(event)
        self.calendar.insert(event)
        

    def handleAskEvent(self, slots):
        self.manageDate(slots)
        timeMin = self.startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        timeMax = self.endDate.strftime("%Y-%m-%dT%H:%M:%SZ")

        events = self.calendar.getEvents(timeMin, timeMax)
        if len(events) == 0:
            print('Nu aveti evenimente')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                # start = event['start'].get('dateTime')
                # hour  = event['start'].get('dateTime', event['start'].get('hour'))
                # eventId = event['id']
                # e = self.calendar.getEventById(eventId)
                print(start, event['summary'])

    def intentManager(self, intent, slotNames):
        slots = self.getSlots(slotNames)
        
        if intent == 'adaugaCalendarEvent':
            self.handleAddEvent(slots)
        elif intent == 'intreabaCalendarEvent':
            self.handleAskEvent(slots)
        else:
            print("Intent not recognized")

    def manageRequest(self):
        s = list(self.prolog.query("manageRequest(Response)."))
        
        slotNames = []
        for elm in s[0]['Response']:
            slotNames.append(str(elm))
        
        if slotNames.__contains__('error'):
            print('Poti te rog sa repeti intrebarea mai specific?')
        else:
            if slotNames.__contains__('warning'):
                self.handleWarning(slotNames)

            intent = self.getIntent() 
            self.intentManager(intent, slotNames)

def main():
    myClass = MyClass()
    myClass.start()
    myClass.manageRequest()

if __name__ == "__main__":
    main()

    