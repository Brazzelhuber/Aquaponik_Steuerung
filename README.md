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

Eingang = Schaltschrankintern  
Ausgang = Nach unten/draußen  



 |Position |Farbe | Nummerierung |Innen     | Außen/unten| Bemerkung|
-------- | -------|--------------|----------| -----------|----------|
|  1      |gelbgrün | keine      |Erde      | Erde       |
|   2    | grau    |  keine      | 3,3 V von Pi |        |2-7 sind verbunden
|   3    | grau    |  keine      | 3,3 V von Pi | Lichtsensor       |
|   4    | grau    |  keine      | 3,3 V von Pi |        |
|   5    | grau    |  keine      | 3,3 V von Pi |        |
|   6    | grau    |  keine      | 3,3 V von Pi |        |
|   7    | grau    |  keine      | 3,3 V von Pi |        |
|   8    | grau    |  keine      | Datenleitung W1 |     |8-13 sind verbunden
| 9    | grau    |  keine      | Datenleitung W1 |                  |
| 10    | grau    |  keine       | Datenleitung W1 |                |
| 11   | grau    |  keine      | Datenleitung W1 |                  |
| 12    | grau    |  keine       | Datenleitung W1 |                |
| 13    | grau    |  keine       | Datenleitung W1 |                |
| 14    | grau    |  keine       |Gnd von Pi|            |14 -18 sind verbunden
| 15    | grau    |  keine       |Gnd von Pi|  Lichtsensor          |
| 16    | grau    |  keine       |Gnd von Pi|            |
| 17    | grau    |  keine       |Gnd von Pi|            |
| 18    | grau    |  keine|Gnd von Pi |                  |
| 19    | grau    |  keine       |Gnd von Pi|            |
| 20    | grau  |   keine        | geht zu Block bei 8er Relais     |+12 V von ext. Batterie | Block verteilt Plus auf einzelne Relais|
|21 | grau| keine | Minus von ext.Batterie| | 3 Kontakte,21-27 sind verbunden|
|22 | grau | keine | Minus von Batt.| |21 -27 breiter
|23 | grau | keine | Minus von Batt.| |
|24 | grau | keine | Minus von Batt.| |
|25 | grau | keine | Minus von Batt.| |
|26 | grau | keine | Minus von Batt.| |
|27 | grau | keine | Minus von Batt.| |
|28 | grau | keine | Minus von Batt.| | letzer Kontakt ist kleiner (2 Kontakte)
|29  | hellblau| keine| SDA für RTC| SDA für Lichtsensor| Lichtsensor und RTC
|30 | hellblau| keine |SCL für RTC | SCL für Lichtsensor| gehen über I2C
|31  | blau  | keine | Plus von Relais | Hauptpumpe|
|32  | blau  | keine | Plus von Relais | 
|33  | blau  | keine | Plus von Relais | 
|34  | blau  | keine | Plus von Relais | 
|35  | blau  | keine | Plus von Relais | 
|36  | blau  | keine | Plus von Relais | 
|37  | blau  | keine | Plus von Relais | 
|38  | blau  | keine | Plus von Relais | 
|39| grau | keine |3,3 von Pi| Plus an Feuchtesensor 1|
|40| grau | keine |3,3 von Pi| Plus an Feuchtesensor 2|
|41| grau | keine |3,3 von Pi| Plus an Feuchtesensor 3|
|42| grau | keine |3,3 von Pi| Plus an Feuchtesensor 4|
|43| grau | keine |3,3 von Pi| Plus an Feuchtesensor 5|
|44| grau | keine |3,3 von Pi| Plus an Feuchtesensor 6|
|45| grau | keine |Gnd von Pi| Minus an Feuchtesensor 1|
|46| grau | keine |Gnd von Pi| Minus an Feuchtesensor 2|
|47| grau | keine |Gnd von Pi| Minus an Feuchtesensor 3|
|48| grau | keine |Gnd von Pi| Minus an Feuchtesensor 4|
|49| grau | keine |Gnd von Pi| Minus an Feuchtesensor 5|
|50| grau | keine |Gnd von Pi| Minus an Feuchtesensor 6|
|51| blau| keine |Datenleitung zu MCP3008| Analogdaten von Feuchtesensor 1|
|52| blau| keine |Datenleitung zu MCP3008| Analogdaten von Feuchtesensor 2|
|53| blau| keine |Datenleitung zu MCP3008| Analogdaten von Feuchtesensor 3|
|54| blau| keine |Datenleitung zu MCP3008| Analogdaten von Feuchtesensor 4|
|55| blau| keine |Datenleitung zu MCP3008| Analogdaten von Feuchtesensor 5|
|56| blau| keine |Datenleitung zu MCP3008| Analogdaten von Feuchtesensor 6|
|57 | grau| keine| Plus






