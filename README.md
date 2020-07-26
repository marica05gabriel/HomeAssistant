# Documentatie HomeAssistant
#### Catelina Ioan & Marica Gabriel
#### Faculate: CTI-ro, Seria B, grupa 30237

### 1.Despre proiect
Prin acest proiect dorim sa realizam un API care primeste obiecte tip json cu actiuni privitoare la **calendar** sau **vreme** reprezentand comanda vocala a unei persoane. Aceasta comanta este transformata in text si apoi intr-un fisier json. Se vor valida aceste obiecte si se vor apela API-uri exterioare pentru realizarea actiunilor.

### 2.Implementare
In ceea ce priveste implementarea, sunt folosite 2 limbaje de programare: Python si Prolog.

### 2.1 Python
Parte implementata in python are urmatoarele atributii:
* Se ocupa de management-ul requesturilor (el primeste obiectul de tip json).
* elimina diacriticele (modului de prolog are o problema cu ele)
* il timite mai departe modulului de Prolog, unde este validat.
* primeste raspunsul de la modulul de Prolog. Genereaza un mesaj pentru cazul in care obiectul nu e valid. Apeleaza API-uri exterioare pentru realizarea actiunilor pentru cazul in care obiectul este valid.

#### Clasa EventHandler

Apeleaza API-uri exterioare pentru realizarea actiunilor pentru cazul in care obiectul este valid.
In fisierul **MyClass.py** avem clasa **EventHandler** care este orchestratorul principal. Face legatura dintre converter, API de prolog, calendar si vreme.

Totul incepe de la metoda **start** care primeste ca parametru un path spre un obiect **json** care reprezinta obiectul primit ca request. Foloseste clasa **Converter** pentru a converti obiectul primit intr-unul fara diacritice. Apoi apeleaza API-ul de prolog pentru a popula predicatele definite dinamic: **intent/1**, **entity/2**.

Metoda **manageRequest** gestioneaza erorile si warning-urile din predicatele populate anterior si in functie de intent-ul prezent distribuie sloturile la o metoda specifica prin intermediul metodei **intentManager** (posibilitate de extindere: definirea de clase pentru fiecare intent).

#### Clasa Converter
Clasa **Converter** are rolul de a rolul de a gestiona cuvintele cu diacritice. Contine un dictionar care face corespondenta dintre diacritice si literele normale. Metoda **eliminateDiac** elimina diacriticele dintr-un cuvant si retine cele 2 cuvinte (cu si fara diacritice) intr-un dictionar pentru a putea reveni la forma cu diacritice la formularea raspunsului (prin metoda **withDiac**).

 Metoda **convertRequest** primeste un path catre un fisier json care se presupune a fi in request. Folosind metodele mentionate anterior, elinina diacriticele si salveaza rezultatul in fisierul **requestFaraDiac.json**. Acesta va fi folosit in continuare de prolog.

#### Clasa DateHandler

Aceasta clasa foloseste libraria **datetime**. Rolul ei este de a formata obiectele de tip data si timp venite din request intr-o forma standardizata.

#### Clasa calendarController

Aceasta clasa foloseste API-ul de la Google <sup>[1]</sup> pentru a adauga sau cauta evenimente.

#### Clasa EventPrototype

Defineste scheletul obiectului ce urmeaza a fi trimis inspre Google calendar API. Metoda **build** populeaza un eveniment cu argumentele date si il returneaza.

#### Clasa WeatherApiBuilder

Aceasta clasa foloseste weatherstack API <sup>[3]</sup> pentru a face request-uri de tip ask weather. Varianta gratuita a acestui API ne permite sa facem doar request-uri pentru o anumita locatie in ziua curenta. Exista si variante platite care ne ofera accesul la un istoric al vremii.

### 2.2 Prolog
Partea de prolog realizeaza validarea datelor si detecteaza prezenta sloturilor necesare pentru efectuarea unei actiuni. Acestea sunt trimise la modulul de Python care va realiza actiunea sau care va genera un mesaj corespunzator pentru cazul in care unele sloturi lipsesc.

### Cum se utilizeaza
Se poate rula din terminal, folosint comanda:
> **python MyClass.py PATH_TO_JSON**

ex: python MyClass.py modele_json/intreabaVremeaAfara/1.json , unde 1.json arata in felul urmator:
```
{
  "text": "aș vrea să îmi spui ce vreme este aici la noapte.",
  "intent": "intreabaVremeaAfara",
  "entities": [
    {
      "end": 38,
      "entity": "loc",
      "start": 34,
      "value": "Cluj"
    },
    {
      "end": 48,
      "entity": "timp",
      "start": 39,
      "value": "la noapte"
    }
  ]
}
```

# HomeAssistant

1. Google calendar API
https://developers.google.com/calendar/v3/reference

2. Date Time Library - prolog<br>
https://github.com/fnogatz/date_time

3. Open Weather Map
https://openweathermap.org/
https://openweathermap.org/api/one-call-api
