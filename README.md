<!-- Required extensions: pymdownx.betterem, pymdownx.tilde, pymdownx.emoji, pymdownx.tasklist, pymdownx.superfences,
markdown.extensions.tables-->
# Aquaponics Control System

The program controls a Raspberry Pi that is used in an aquaponics CHOP system.

## Physical Structure  
What is special about the system, which is installed in a 50 sqm greenhouse, is the combination with
normal raised beds filled with soil.

Since rainbow trouts are to be bred here, cooling of the fish tanks is required for the summer. This should be managed
through fresh well water (evenly 12 - 13 degrees Celsius), which is then used to irrigate the raised beds.


The soil in the raised beds is checked with moisture sensors. If the soil is too humid, the cooling water is sprayed outside.

The following sensors are in use:

- 6 soil moisture sensors via MCP3008
- The voltage of the 12-volt battery is also monitored via MCP3008.
- 5 temperature sensors via Wire-1
- 1 lux meter for monitoring the light intensity (via I2C bus)
- 1 Atlas Scientific pH sensor for pH measurement in fish tanks (via UART)
- 1 ultrasonic sensor for measuring the water level in the sump tank.

Actuators are:

- the main pump (an air pump that operates a geyser pump)
- 2 air valves (air from below / above)
- 5 water valves
- 12 volt motor for automatic feeder
- a 4 KW heating element in the sump tank if the water temperature in the fish tanks goes to zero in winter.

The pump in the sump tank is a geyser pump that is operated with air. The air under the roof can be used to heat the water in winter, if this is not enough, water heating can be started.
All actuators are controlled via GPIOs and two relay boards.

The structure of the combined aquaponic raised bed system is displayed in the first picture of the German section.  

## Configuration of the Raspberry Pi

The following sensors and devices are used

Device | Function | Volts | Bus | Configuration |
-------- | -------- | ---- | ---- | ---------------------- |
DS1820 | temperature | 3.3 | 1-Wire | insert in config.txt dtoverlay = w1-gpio and gpiopin = 4 |
BH1750 | Light | 3.3 | I2C | activate in Interface Options I2C |
DS1307 | Hardware Clock | 5.0 | I2C | see above |
MCP3008 | AD converter | 3.3 | SPI | import spidev, activate in Interface Options SPI (goes via MCP3008) |
SKU: AB142 | soil moisture | 3.3 | SPI | is connected to the analog side of the MCP3008 |
HC-SR04 | ultrasound | 5.0 | --- | goes directly via GPIO |
phProbe | Ph measering | 3,3 | open: I2C or UART

## Structure of the program

Displayed in the second picture of the German section  

## Special features of the program (1): control with arrays

The program is essentially controlled by three arrays (which are technically dictionaries):

- the default array
- the array of values
- the control array


### Default array

The array with default values ​​defines limit values ​​for sensor data. Conditions are defined in the program
when an action is triggered automatically, e.g. Temperature water> 23 degrees -> cooling
Additionally, the feeding time and duration are determined.
The values ​​are shown on the screen as entry specifications, so they can be changed (conclusion: return).
When the program ends, the values ​​are saved and called up when restarting.

| Array-Item | Meaning |
| -------------- | -------- |
| "TempWasserMin": 3, | Minimum temperature in the fish tanks |
| "TempWasserMax": 23, | Temperature maximum in the fish tanks |
"TempLuftMin": 3, | Temperature in the greenhouse below |
"Water level min": | Water level minimum in the sump tank |
"Water level max": | Water level max in the sump tank |
"PhWertMin": 6.7, | Minimum water pH
"PhWertMax": 7.1, | Maximum PhWert |
"Feeding": 10.00 | Feeding time |
"Fuett. Duration": 5} | Duration of feeding |
### Value array

The value array contains the read sensor data and the calculated data for sunrise and sunset

Array item | Meaning
-------------- | --------
"T_Luft_oben": | Air temperature under the roof of the greenhouse
"T_Luft_unten": | Air temperature below
"T_Wasser1": | Fish tank temperature 1
"T_Wasser2": | Fish tank temperature 2
"T_aussen": | outside temperature
"Luxwert_1": | Lux
"Ph value": | PH value water
"Oxygen": | O2 content water (still has to be decided whether this makes sense)
"Volt": | Voltage of the 12 volt battery
"Water level": | Water level in the sump tank
"Sunrise": | is calculated by sunset.py based on GPS and date
"Sunset": | the lux data are only saved during the day
"Moisture1": | Soil moisture measurement in the raised beds
"Moisture2": |
"Moisture3": |
"Moisture4": |
"moisture5": |
"moisture6": |

### control array


The control array contains the ACTUAL states on the left, the TARGET states in the middle or on the right.
([0,1] means: the item (e.g. a valve) is off / closed but should be opened.
Where the item has three digits, the last value indicated whether there was a manual override. The reason for this is,
that a status change can be requested both via defined sensor data or manually via the screen.
Example: the if clauses for the sensor data say: "normal CHOP circle", but "cooling with irrigation" has been selected via the screen. Then this must not be withdrawn in the next loop due to the sensor conditions.
It must be maintained contrary to the defined conditions,
until there is a manual shutdown on the screen.

The first five items are complex states, since several valves have to be controlled simultaneously.



| Array-Item | Meaning |
-------------- | -------- |
| "normal CHOP circle": [0,0,0], | normal operation (FT -> GB -> ST -> FT) whereby air from below |
| "warm CHOP Circle": [0,0,0], | warm operation (FT -> GB -> ST -> FT) whereby air from under the roof |
"Cooling with irrigation": [0,0,0], | The well water supplied is used to irrigate the earth beds
"Cooling with sprinkling": [0,0,0], | cooling water  is irrigated outside
"Well water as heating": [0,0,0], | Well water has 13 degrees, can also be used for "heating"
"filling water": [0,0,0], | Water loss must be compensated for
"Drain water": [0,0,0], | too much water in the system
"Main pump": [0,0,0], |
"Screen_writing": [0,1,0], | Writing sensor values ​​to the screen can be switched off in continuous operation
"Heating": [0,0,0], | when it gets too cold in winter
"It is day": [0,0], | comes from the sun data, lux values ​​are only written during the day
"Alarm": [0.0], | if something goes wrong, email is written
"Feeding": [0,0,0], | Switch on the automatic feeder?
"Log entry": [0.0], | a log entry is made when the status changes
"WQ to FT": [0,0,0], | the water valves individually: water source (well) to fish tank
"WQ to VR": [0,0,0], | Water source to irrigation outside
"ST to VR": [0,0,0], | Sumptank to irrigation outside
"ST to FT": [0,0,0], | Sumptank to fish tanks
"ST to HB": [0,0,0], | Sumptank to raised bed
"LU to HP": [0,0,0], | air valves
"LO to HP": [0,0,0] | sucks air from under the roof into the airpump

## Special features of the program (2): Double use of the ButtonCheck function ()

In controlpanel.py module, the individual click buttons are connected to the ButtonCheck () function in CheckCenter.py using the "bind" method.
Here you can use the method button.configure ("text")[- 1] to get text of the pressed button.

The SensorCheck () function checks whether changes should be requested based on the sensor values.
In order to avoid duplicate program structures for sensor-triggered change requests, the ButtonCheck () function is
also used by SensorCheck ().

A button press is simulated for this. The text of the virtual button is passed as a parameter, while with a real buttonpress this parameter is always equal to None (known from button.configure ("text") [- 1]).

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


- die Hauptpumpe (eine Luftpumpe, die eine Geysirpump betreibt)  
- 2 Luftfventile (Luft von unten/oben)  
- 5 Wasserventile  
- 12-Volt Motor für Fütterungsautomat  
- ein 4 KW-Heizstab im Sumptank, falls die Wassertemperatur in den Fischtanks im Winter gegen Null geht.

Die Pumpe im Sumptank ist eine Geysir-Pumpe, die mit Luft betrieben wird. Zur Heizung des Wassers im Winter kann die Luft von 
unterm Dach angesaugt werden.Wenn das nicht reicht, kann eine Wasserheizung gestartet werden.    
Alle Aktoren werden über GPIOs und zwei Relais-Boards gesteuert.

Hier die Struktur des kombinierten Aquaponik-Erdhochbeet-Systems:

![RealStruktur](RealStruktur.png)

Bis auf das Ventil ST to FT sind alle Wasserventile nc (normally closed)
Bei den Luftventilen ist LU to HP no, LO to HP nc.
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

## Besonderheiten des Programms (1): Steuerung mit Arrays

Das Programm wird im Wesentlichen über drei Arrays gesteuert (die technisch gesehen Dictionaries sind):

- der Vorgabe-Array 
- der Werte-Array
- der Control-Array

### Vorgabe-Array

Der Array mit Vorgabewerten definiert Grenzwerte für Sensordaten. Im Programm sind Bedingungen definiert,
ab wann automatisch eine Aktion ausgelöst wird, z.B. Temperatur Wasser > 23 Grad -> Kühlung
Am Schluß werden noch Fütterungszeit und -dauer festgelegt.
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
"Fuetterung"    : 10.00  	  | Fütterungszeit |
"Fuett.dauer"  : 5}  	| Fütterungsdauer |	  
                 
               
### Werte-Array

Der Werte-Array beinhaltet die ausgelesenen Sensordaten, bzw. die errechneten Daten für Sonnenauf- und -untergang 

Array-Item | Bedeutung
-------------- | --------  
"T_Luft_oben" : |      Lufttemperatur unterm Dach des Gewächshauses
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
"Erdfeuchte6" : |
                



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
|"warmer CHOP-Circle":       [0,0,0], |  warmer Betrieb (FT -> GB -> ST ->FT) wobei Luft von unterm Dach |
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
"LU to HP":                 [0,0,0], |  Luftventile
"LO to HP":                 [0,0,0] |  saugt Luft von unterm Dach in die airpump

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







