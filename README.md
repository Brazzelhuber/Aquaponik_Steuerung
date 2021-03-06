<!-- Required extensions: pymdownx.betterem, pymdownx.tilde, pymdownx.emoji, pymdownx.tasklist, pymdownx.superfences,
markdown.extensions.tables-->

# Aquaponik_Steuerung

Das Programm steuert einen Raspberry Pi, der in einem Aquaponik CHOP-System zum Einsatz kommt.


## Realstruktur

Das Besondere an der Anlage, die in einem 50 qm-Gewächshaus installiert ist, ist die Kombination mit
normalen Erd-Hochbeeten

Da hier Regenbogenforellen gezüchtet werden sollen, braucht es für den Sommer eine Kühlung der Fischtanks. Diese soll
durch frisches Brunnenwasser (gleichmäßig 12 - 13 Grad Celsius) erfolgen, das anschließend zur Bewässerung der Erd-Hochbeete genutzt wird.

Die Erde in den Hochbeete wird mit Feuchtigkeitssensoren kontrolliert. Falls die Erde zu feucht ist, wird das Kühlungswasser verieselt.

Folgende Sensoren sind im Einsatz: 

- 6 Erdfeuchtesensoren über MCP3008
- über MCP3008 wird auch die Spannung der 12-Volt Batterie überwacht.
- 5 Temperatursensoren über Wire-1
- 1 Lux-Messer zur Überwachung der Lichtintensität (über I2C-Bus)
- 1 Ph-Sensor von Atlas Scientific zur Ph-Messung in den Fischtanks (über UART)
- 1 Ultraschallsensor zur Messung der Wasserhöhe im Sumptank



Aktoren sind:  


- die Hauptpumpe (eine Luftpumpe, die eine Ejectionpump betreibt)   
- 6 Wasserventile  
- 12-Volt Motor für Fütterungsautomat.

Ein Wasserventil dient dazu eine Blumenwiese außerhalb zu wässern.

Die Pumpe im Sumptank ist eine Ejection-Pumpe, die mit Luft betrieben wird.     
Alle Aktoren werden über GPIOs und zwei Relais-Boards gesteuert.

Hier die Struktur des kombinierten Aquaponik-Erdhochbeet-Systems:

![RealStruktur](RealStruktur.png)

Bis auf das Ventil ST to FT sind alle Wasserventile nc (normally closed)

## Konfiguration des Raspberry Pi

Folgende Sensoren und Devices kommen zum Einsatz

Device  | Funktion  | Volt | Bus  | Konfiguration       |
-------- | -------- | ---- | ---- | ----------------------  |
DS1820  |Temperatur | 3,3  | 1-Wire| in config.txt dtoverlay = w1-gpio  und gpiopin=4 einfügen|
BH1750 | Licht      | 3,3  | I2C   | in Interface Options I2C aktivieren  |
DS1307 | Hardwareclock| 5,0| I2C  | siehe oben |
MCP3008| AD-Wandler|3,3 | SPI| import spidev, in Interface Options SPI aktivieren (geht über MCP3008)|
SKU: AB142 | Erdfeuchte| 3,3 | SPI | wird an der Analogseite des MCP3008 angeschlossen|
HC-SR04 | Ultraschall| 3,3| ---| geht direkt über GPIO |
phProbe|PhMessung|3,3|offen: I2C oder UART 


## Programmstruktur

Hier die grobe Struktur des Programms
|
![Programmstruktur](ProgrammStruktur.png)

Was in der Zeichnung nicht dargestellt wird, ist die Tatsache, dass neben dem Hauptprogramm ein zweiter Thread läuft, der die Zeitschaltuhr steuert. Über Queuing sind beide Treads verbunden, so dass im Hauptprogramm bequem die Zeiten bestimmt werden, der Zeitschaltthread die entsprechenden Aktionen auslöst.

## Besonderheiten des Programms (1): Steuerung mit Arrays

Das Programm wird im Wesentlichen über vier Arrays gesteuert (die technisch gesehen Dictionaries sind):

- der Vorgabe-Array 
- der Werte-Array
- der Zeiten-Array
- der Control-Array

### Vorgabe-Array

Der Array mit Vorgabewerten definiert Grenzwerte für Sensordaten. Im Programm sind Bedingungen definiert,
ab wann automatisch eine Aktion ausgelöst wird, z.B. Temperatur Wasser > 23 Grad -> Kühlung

Die Werte werden als Entry-Vorgaben auf dem Screen gezeigt, können also geänderte werden (Abschluß: Return).
Bei Beendigung des Programms werden die Werte gespeichert und bei Neustart aufgerufen.

|Array-Item | Bedeutung  |
|-------------- | -------- | 
|"TempWasserMin" : 3,     |Temperaturminimum in den Fischtanks |  
|"TempWasserMax" : 23,    |Temperaturmaximum in den Fischtanks |	  	
"TempLuftMin"   : 3,      |Temperatur im Gewächshaus unten     |   
"WasserpegelMin":       |Wasserspiegelminimum im Sumpftank          |
"WasserpegelMax": 	|Wasserspiegelmax im Sumptank|	
"PhWertMin"     : 6.7,	| Minimum Ph-Wert Wasser|	    
"PhWertMax"     : 7.1,  	  	 |Maximum PhWert|

               
### Werte-Array

Der Werte-Array beinhaltet die ausgelesenen Sensordaten, bzw. die errechneten Daten für Sonnenauf- und -untergang 

Array-Item | Bedeutung
-------------- | --------  
"T_Frühbeet" : |      Temperatur im Frühbeet
"T_Luft_unten" : |     Lufttemperatur unten
"T_Wasser1": |         Temperatur Fischtank 1
"T_Wasser2": |         Temperatur Fischtank 2
"T_aussen": |          Außentemperatur
"Luxwert_1" : |      Luxwert
"Ph-Wert": |          Ph-Wert Wasser
"Sauerstoff" : |       O2-Gehalt Wasser (muß noch entschieden werden, ob das sinnvoll ist)
"Volt"  :|            Spannung der 12-Voltbatterie
"Wasserstand" : |      Wasserstand im Sumptank 
"Sonnenaufgang": |     wird von sunset.py auf der Grundlage von GPS und Datum ausgerechnet
"Sonnenuntergang": |   die Luxdaten werden nur am Tag gespeichert
"Erdfeuchte1" : |      Erdfeuchtmessung in den Erd-Hochbeeten
"Erdfeuchte2" : |       
"Erdfeuchte3" : |       
"Erdfeuchte4" : |
"Erdfeuchte5" : |
"Erdfeuchte6" : | 0





### Zeiten-Array
Der Zeiten-Array beinhaltet Anfangs- und Endzeiten veschiedener Items, die in einem parallel laufenden Thread permanent abgefragt werden.


Array-Item | Wert
-------------- | --------  
"Fuetterung_Anfang":   |   09:00
"Fuetterung_Ende" :     |  "09:10"
"Beleuchtung_Anfang": |   "06:00",
"Beleuchtung_Ende":    |  "20:00",
"Blumenwiese_Anfang":   | "09:30",
"Blumenwiese_Ende":     | "09:35"

Neben den Fütterungszeiten werden die Wässerungszeiten der Blumenwiese und die Beleuchtungszeiten im Frühbeet gespeichert.
Die Werte können im Hauptprogramm verändert werden und werden so in Zeiten.csv geschrieben.

### Control-Array


Der Kontrollarray ca entält links die IST-, in der Mitte oder rechts  die SOLL-Zustände.
([0,1] heißt: das Item (z.B. ein Ventil) ist aus/zu soll aber an/aufgemacht werden.
Da wo das Item dreistellig ist, indizierte der letzte Wert, ob ein manual override vorliegt. Der Grund dafür ist,
dass eine Zustandsänderung sowohl durch definierte Sensordaten als auch manuell über den Bildschirm angefordert werden kann.
Beispiel: die if-clauses für die Sensordaten sagen: "normaler CHOP-Circle", über den Bildschirm wurde
aber "Kühlung mit Bewässerung" gewählt. Dann darf das nicht im nächsten Loop durch die Sensorbedingungen
rückgängig gemacht werden, sondern muß entgegen der definierten Bedingungen aufrechterhalten werden,
bis wieder eine manuelle Abschaltung über den Bildschirm erfolgt.

Die ersten fünf Items sind komplexe Zustände, da mehrere Ventile gleichzeitig gesteuert werden müssen.

|Array-Item | Bedeutung  |
-------------- | --------  |
|"normaler CHOP-Circle":     [0,0,0], |  normaler Betrieb (FT -> GB -> ST ->FT) wobei Luft von unten |
|"Bewässerung":            [0,0,0], |  Bewässerung der Blumenwiese außerhalb  |
"Kühlung mit Bewässerung":  [0,0,0], |  zugeführtes Brunnenwasser wird zur Bewässerung der Erdbeete genutzt
"Kühlung mit Verieselung":  [0,0,0], |  dito mit Verieselung
"Brunnenwasser als Heizung":[0,0,0], |  Brunnenwasser hat 13 Grad, kann auch zum "Heizen" eingesetzt werden
"Wasser auffüllen":         [0,0,0], |  Wasserverlust muss ausgeglichen werden
"Wasser ablassen":          [0,0,0], |  zuviel Wasser im System
"Hauptpumpe":               [0,0,0], |
"Screen_schreiben":         [0,1,0], |  Sensorwerte auf Screen schreiben, kann im Dauerbetrieb abgestellt werden
"Heizung":                  [0,0,0], |  wenn es im Winter zu kalt wird
"Es ist Tag"      :         [0,0], |    kommt aus den Sonnendaten, Luxwerte werden nur tagsüber geschrieben
"Alarm"            :        [0,0], |    wenn was schiefgeht wird EMail geschrieben
"Fütterung"  :              [0,0,0], |  Fütterungsautomat einschalten?
"Logeintrag":               [0,0], |    bei Zustandsänderung erfolgt ein Logeintrag
"WQ to FT":                 [0,0,0], |  die Wasserventile einzel: Wasserquelle (Brunnen) zu Fischtank
"WQ to VR":                 [0,0,0], |  Wasserquelle zu Verieselung
"ST to VR":                 [0,0,0], |  Sumptank zu Verieselung
"ST to FT":                 [0,0,0], |  Sumptank zu Fischtanks
"ST to HB":                 [0,0,0], |  Sumptank zu Hochbeet
"WQ to WI | Leitet dasa Brunnen wasser zu den Versenkregnern in der Blumenwiese

##  Besonderheiten des Programms (2): Doppelnutzung der Funktion ButtonCheck()

Im Modul Kontrollpanel.py werden die einzelnen Clickbuttons über die Methode "bind" 
mit der Funktion ButtonCheck() in CheckCenter.py verbunden. Hier kann mit der Methode button.configure("text")[-1] 
der Text des gedrückten Buttons abgefragt werden.

Die Funktion  SensorCheck() prüft auf der Grundlage der Sensorwerte,  ob Veränderungen angefragt werden sollen.
Um nun für sensorgetriggerte Veränderungsanfragen Programmdoppelstrukturen zu vermeiden wird die Funktion ButtonCheck()
auch von SensorCheck()  genutzt.

Hierfür wird ein Buttonpress simuliert. Der Text des virtuellen Buttons wird als Paramter übergeben, während bei einem 
wirklichen Buttonpress dieser Parameter immer gleich None ist (ist ja durch button.configure("text")[-1] bekannt).

# Interne Dokumentation

## Durchgangsklemmen Schaltschrank




|Position                           |Farbe | Nummerierung|Innen             | Außen/unten     | Bemerkung|
-------- | --------------------------------|-------------|------------------| ----------------|----------|
|  1                                |gelbgrün| keine     |Erde              | Erde            |
|   2    | grau                             |  keine     | 3,3 V von Pi     |                 |2-7 sind verbunden
|   3    | grau                             |  keine     | 3,3 V von Pi     | Lichtsensor                |
|   4    | grau                             |  keine     | 3,3 V von Pi     |                 |
|   5    | grau                             |  keine     | 3,3 V von Pi     |                 |
|   6    | grau                             |  keine     | 3,3 V von Pi     |                 |
|   7    | grau                             |  keine     | 3,3 V von Pi     |                 |
|   8    | grau                             |  keine     | Datenleitung W1             |      |8-13 sind verbunden
| 9    | grau                              |  keine     | Datenleitung W1   |                            |
| 10    | grau                             |  keine      | Datenleitung W1             |                 |
| 11   | grau                              |  keine     | Datenleitung W1   |                            |
| 12    | grau                             |  keine      | Datenleitung W1             |                 |
| 13    | grau                             |  keine      | Datenleitung W1             |                 |
| 14    | grau                             |  keine      |Gnd von Pi        |                 |14 -18 sind verbunden
| 15    | grau                             |  keine      |Gnd von Pi        |  Lichtsensor               |
| 16    | grau                             |  keine      |Gnd von Pi        |                 |
| 17    | grau                             |  keine      |Gnd von Pi        |                 |
| 18    | grau                             |  keine|Gnd von Pi             |                  |
| 19    | grau                             |  keine      |Gnd von Pi        |                 |
| 20    | grau                            |   keine      | geht zu Block bei 8er Relais                  |+12 V von ext. Batterie | Block verteilt Plus auf einzelne Relais|
|21| grau                           | keine| Minus von ext.Batterie        || 3 Kontakte,21-27 sind verbunden|
|22| grau                           | keine | Minus von Batt.|             |21 -27 breiter
|23| grau                           | keine | Minus von Batt.|             |
|24| grau                           | keine | Minus von Batt.|             |
|25| grau                           | keine | Minus von Batt.|             |
|26| grau                           | keine | Minus von Batt.|             |
|27| grau                           | keine | Minus von Batt.|             |
|28| grau                           | keine | Minus von Batt.|             | letzer Kontakt ist kleiner (2 Kontakte)
|29| hellblau| keine| SDA für RTC| SDA für Lichtsensor                                 | Lichtsensor und RTC
|30| hellblau| keine|SCL für RTC | SCL für Lichtsensor                                 | gehen über I2C
|31| blau    | keine| Plus von Relais                                      | Hauptpumpe|
|32| blau    | keine| Plus von Relais                                      | 
|33| blau    | keine| Plus von Relais                                      | 
|34| blau    | keine| Plus von Relais                                      | 
|35| blau    | keine| Plus von Relais                                      | 
|36| blau    | keine| Plus von Relais                                      | 
|37| blau    | keine| Plus von Relais                                      | 
|38| blau    | keine| Plus von Relais                                      | 
|39| blau| 5 V                               |Plus 5 V von Pi| 5V an Ultrasonic        |39 - 41 sind verbunden
|40| blau    | 5 V                          | 5V an RTC | 
|41|blau                            | 5 V  |
|42| grau                           | keine| Trigger Ultrasonic von GPIO 17| Trigger an Sensor|42, 43 und 44 sind kleiner als die blauen Klemmen < 42
|43| hellblau|keine | Echo an Platine mit Widerständen|Echo von Sensor| Echo muß auf Platine durch Widerstände laufen
44 | grau| keine | Gnd an Ultrasonic| Gnd an Platine mit Widerständen
|45| grau                           | keine|3,3V von Pi| Plus an Feuchtesensor 1       |
|46| grau                           | keine|3,3 von Pi| Plus an Feuchtesensor 2        |
|47| grau                           | keine|3,3 von Pi| Plus an Feuchtesensor 3        |
|48| grau                           | keine|3,3 von Pi| Plus an Feuchtesensor 4        |
|49| grau                           | keine|3,3 von Pi| Plus an Feuchtesensor 5        |
|50| grau                           | keine|3,3 von Pi| Plus an Feuchtesensor 6        |
|51| grau                           | keine|Gnd von Pi| Minus an Feuchtesensor 1       |
|52| grau                           | keine|Gnd von Pi| Minus an Feuchtesensor 2       |
|53| grau                           | keine|Gnd von Pi| Minus an Feuchtesensor 3       |
|54| grau                           | keine|Gnd von Pi| Minus an Feuchtesensor 4       |
|55| grau                           | keine|Gnd von Pi| Minus an Feuchtesensor 5       |
|56| grau                           | keine|Gnd von Pi| Minus an Feuchtesensor 6       |
|57| blau| keine                           |Datenleitung zu MCP3008        | Analogdaten von Feuchtesensor 1|
|58| blau| keine                           |Datenleitung zu MCP3008        | Analogdaten von Feuchtesensor 2|
|59| blau| keine                           |Datenleitung zu MCP3008        | Analogdaten von Feuchtesensor 3|
|60| blau| keine                           |Datenleitung zu MCP3008        | Analogdaten von Feuchtesensor 4|
|61| blau| keine                           |Datenleitung zu MCP3008        | Analogdaten von Feuchtesensor 5|
|62| blau| keine                           |Datenleitung zu MCP3008        | Analogdaten von Feuchtesensor 6|
|63| grau| keine                          | Plus von 4er Relais | Plus 12 V an Fütterungsautomat|
64|grau|keine|Plus von 4er Relais|
65 |grau |keine|Plus von 4er Relais||     |
66|grau|keine|Plus von 4er Relais|
67|hellblau|keine| Minus | Minus an Fütterungsautomat
68|grau|keine| Minus
69|grau|keine| Minus
70|grau|keine| Minus







