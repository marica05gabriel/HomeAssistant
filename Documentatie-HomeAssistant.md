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
