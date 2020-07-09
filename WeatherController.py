import json

import requests


class WeatherApiBuilder:

    def __init__(self):
        self.url = 'http://api.weatherstack.com/current?access_key=0b91cd924cc3a28fd90bab26ac8a239c&query='
        self.defaultCity = 'Cluj-Napoca'

    def buildRequest(self, cityName):
        return self.url + cityName

    def askWeather(self, cityName):
        if cityName == None or cityName == "":
            print("Nu ati precizat nicio locatie. Locatia default este " + self.defaultCity + ". Continuati cu asta?")
            raspuns = input("Da | Nu\n")

            if (raspuns.__contains__('n') or raspuns.__contains__('N')):
                self.defaultCity = input("Alegeti alta locatie default: ")
            cityName = self.defaultCity

        url = self.buildRequest(cityName)
        r = requests.get(url)
        content = json.loads(r.content)

        if('success' in content and content['success'] == False):
            self.askWeather(self.defaultCity)
        else:
            temperature = content['current']['temperature']
            description = content['current']['weather_descriptions'][0]
            print("Temperatura in " + content['location']['name'] + ", " + content['location']['region'] + ", " + content['location']['country'] + " este de " + str(temperature) + " °C. Scurta descriere: " + description)