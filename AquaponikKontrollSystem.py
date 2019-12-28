#!/usr/bin/python3.5
# coding=utf-8
# Aquaponik-Kontrollsystem.py

#------------------------------------------------------------
## Für weitere Einzelheiten siehe: readme.md


from __future__ import division, print_function  # Maßnahme um pygame mit Python 3.x kompatible zu machen
import sys, time, csv
import tkinter as Tk                             # GUI-Bibliothek
import datetime
from smbus import SMBus

import ptvsd     # dient dem remote-debugging mit Visual Studio

# eigene Module

import Kontrollfenster as Kf
import Temperatursensoren as Ts
import Werte_auf_Screen_schreiben as Ws
import Werte_in_Datei_schreiben as Ds
import Wertelesen as Wl
import Check_Center as Ch
import Soll_Ist as Si
import Aktion as Ak
import Vorgabe as Vw

##
# remote Debugging mit Visual Studio (wenn Debugging --> uncomment):
##
##ptvsd.enable_attach()
##ptvsd.wait_for_attach()

# in VS muß bei Debugging in "an Prozeß anhängen" ptsvd gewählt 
# und in Ziel: tcp://XXX.XXX.XXX:5678 eingegeben werden (XXX.. steht für die Adresse des Raspi)

#---------------------------------------------------------------------------------------------------------
#########################################################################################################
############        Programminitialisierung       #######################################################
#########################################################################################################

#######################################################################################################
# Initiieren: Array mit Vorgabewerten, Array für Sensordaten und Array mit Kontrollvariablen:

# Array mit Vorgabewerten definiert Grenzwerte für Sensordaten,
# im Programm sind Bedingungen definiert,
# ab wann automatisch eine Aktion ausgelöst wird, z.B. Temp Wasser > 23  -> Kühlung
# Am Schlß noch Fütterungszeit und -dauer
# die Werte werden als Entry-Vorgaben auf dem Screen gezeigt, können also geänderte werden (Abschluß: Return)

vw         =  {"TempWasserMin" : 3,         # Temperatur in den Fischtanks
               "TempWasserMax" : 23,
               "TempLuftMin"   : 3,         # Temperatur im Gewächshaus unten
               "WasserpegelMin": 0,         # Wasserspiegel im Sumpftank
               "WasserpegelMax": 0,
               "PhWertMin"     : 6.7,
               "PhWertMax"     : 7.1,
               "Fuetterung"    : 10.00,
               "Fuett.dauer"  : 5
               }
               

# der Werte-Array beinhaltet die ausgelesenen Sensordaten,
# bzw. die errechneten Daten für Sonnenauf- und -untergang 

wa          = {"T_Luft_oben" : 0,      # Lufttemperatur unterm Dach des Gewächshauses, kann zum Heizen eingesetzt werden 
               "T_Luft_unten" : 0,     # Lufttemperatur unten
               "T_Wasser1": 0,         # Temperatur Fischtank 1
               "T_Wasser2": 0,          # Fischtank 2
               "T_aussen": 0,           # Außentemperatur
               "Luxwert_1" : 0 ,        # Luxwert
               "Ph-Wert": 0 ,           # Ph-Wert Wasser
               "Sauerstoff" : 0,        # O2-Gehalt Wasser
               "Volt"  :0 ,             # Spannung der 12-Voltbatterie
               "Wasserstand" : 0,       # Wasserstand im Sumptank 
               "Sonnenaufgang": 0,      #  wird von sunset.py auf der Grundlage von GPS und Datum ausgerechnet
               "Sonnenuntergang": 0,
               "Erdfeuchte1" : 0,       # Erdfeuchtmessung in den Erd-Hochbeeten, wenn nicht zu feucht, wird das
               "Erdfeuchte2" : 0,       # Brunnenwasser, das zur Kühlung zugeführt wird zur Bewässerung genutzt
               "Erdfeuchte3" : 0,       # ansonsten verrieselt
               "Erdfeuchte4" : 0,
               "Erdfeuchte5" : 0,
               "Erdfeuchte6" : 0
                }

# Kontrollarray ca entält links die IST-, in der Mitte oder rechts  die SOLL-Zustände ([0,1] heißt: ist aus/zu soll
# aber an/auf).
# da wo das Item dreistellig ist, indizierte der letzte Wert, ob ein manual override vorliegt. Beispiel: die
# if-clauses für die Sensordaten sagen: "normaler CHOP-Circle", über den Bildschirm wurde
# aber "Kühlung mit Bewässerung" gewählt. Dann darf das nicht im nächsten Loop durch die Sensorbedingungen
# rückgängig gemacht werden, sondern muß entgegen der definierten Bedingungen aufrechterhalten werden,
# bis wieder eine manuelle Abschaltung über den Bildschirm erfolgt.
# Die ersten fünf Items sind komplexe Zustände, da mehrere Ventile gleichzeitig gesteuert werden müssen.
# Hauptpumpe funktioniert mit Luft (Geysir Pumpe).

ca          ={ "normaler CHOP-Circle":     [0,0,0],  # normaler Betrieb (FT -> GB -> ST ->FT) wobei Luft von unten
               "warmer CHOP-Circle":       [0,0,0],  # warmer Betrieb (FT -> GB -> ST ->FT) wobei Luft von unterm Dach
               "Kühlung mit Bewässerung":  [0,0,0],  # zugeführtes Brunnenwasser wird zur Bewässerung der Erdbeete genutzt
               "Kühlung mit Verieselung":  [0,0,0],  # dito mit Verieselung
               "Brunnenwasser als Heizung":[0,0,0],  # Brunnenwasser hat 15 Grad, kann auch zum "Heizen" eingesetzt werden
               "Wasser auffüllen":         [0,0,0],  # Wasserverlust muss ausgeglichen werden
               "Wasser ablassen":          [0,0,0],  # zuviel Wasser im System
               "Hauptpumpe":               [0,0,0],
               "Screen_schreiben":         [0,1,0],  # Sensorwerte auf Screen schreiben, kann im Dauerbetrieb abgestellt werden
               "Heizung":                  [0,0,0],  # wenn es im Winter zu kalt wird
               "Es ist Tag"      :         [0,0],    # kommt aus den Sonnendaten, Luxwerte werden nur tagsüber geschrieben
               "Alarm"            :        [0,0],    # wenn was schiefgeht wird EMail geschrieben
               "Fütterung"  :              [0,0,0],  # Fütterungsautomat einschalten?
               "Logeintrag":               [0,0],    # bei Zustandsänderung erfolgt ein Logeintrag
               "WQ to FT":                 [0,0,0],  # die Wasserventile einzel: Wasserquelle (Brunnen) zu Fischtank
               "WQ to VR":                 [0,0,0],  # Wasserquelle zu Verieselung
               "ST to VR":                 [0,0,0],  #Sumptank zu Verieselung
               "ST to FT":                 [0,0,0],  #Sumptank zu Fischtanks
               "ST to HB":                 [0,0,0],  #Sumptank zu Hochbeet
               "LU to HP":                 [0,0,0],  # Luftventile
               "LO to HP":                 [0,0,0]}  #  saugt Luft von unterm Dach in die airpump



##################################################################################################
# Sensoren initiieren:

Ts.ds1820einlesen() #Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen
##################################################################################################
#Fenster initiieren : 

Hintergrund = "lightgrey"
fenster = Tk.Tk()
fenster.configure(background = Hintergrund)

###############################################################################
# Kontrollpanel, mit dem das System vom Bildschirm aus gesteuert werden kann: #
                                                                              #
screen_app = Kf.Kontrollpanel(fenster, Hintergrund, ca, vw)                       #
###############################################################################
# Einlesen der Vorgabewerte:

Vw.LeseVorgabe(screen_app, vw)

# widget und Callback für den Button "Beenden":

def Beenden(after_id, vw):                  # wird von clickma aufgerufen und beendet das Programm
    
    Vw.WriteWerte(vw)
    fenster.after_cancel(after_id)
    fenster.destroy()
   
    sys.exit()
   
clickma = Tk.Button (fenster, text = "Beenden", command = lambda: Beenden(after_id, vw))
clickma.grid(row = 3, column = 0, padx = 10, sticky = Tk.E)

#############################################################################################################
#Anzeige von Datum und Urzeit links unten auf dem Screen (im Gewächshaus gibts kein Internet, daher hardwareclock)
screen_app.Datum_Zeit = Tk.Label (text = time.strftime("%d.%m.%Y - %H:%M"))
screen_app.Datum_Zeit.grid(row = 3, column = 0 , sticky = Tk.W)
################################################################################################################
# Variablen für loop:
t1 = datetime.datetime.now()         # dient der Zeitsteuerung in der Schleife
after_id = 0

# Ende der Programminitialisierung



# Programm starten 
# loop wird durch die fenster.after-Methode jede Sekunde wiederholt
###################################################################




#####################################################
def loop():
    
    # Datum und Uhrzeit aktualisieren:
    
    screen_app.Datum_Zeit.configure (text = time.strftime("%d.%m.%Y - %H:%M"))
    
    global wa, ca, t1, after_id

    t2 = datetime.datetime.now()

    
    tdiff = t2 -t1

    wa = Wl.Werte_lesen(wa)                     # liest Werte aus Sensoren und schreibt sie in Array wa

    ca,wa = Ch.SensorCheck(screen_app, ca, wa)  # checkt bei den Sensoren,ob etwas zu tun ist
                                                # direkte Befehle vom Bildschirm aus werden von Modul
                                                # "Kontrollpanel" über button-callback
                                                # aufgerufen und in Modul "Ch.Buttoncheck" in den ca-Array
                                                # eingetragen
  
                                            
    # Feststellen, ob es Tag ist (nur dann werden Lichtdaten in Datei geschrieben)
    
    
    if (t2.time() > wa["Sonnenaufgang"]) and (t2.time() < wa["Sonnenuntergang"]):
        ca["Es ist Tag"][0] = 1
        ca["Es ist Tag"][1] = 1
        
        
    else:
        ca["Es ist Tag"][0] = 0
        ca["Es ist Tag"][1] = 0
    

    
    if ca["Screen_schreiben"][0] == 1:
        Ak.change_sensordaten (screen_app, wa) # schreibt Sensordaten auf Screen
    
    if not Si.soll_gleich_ist(ca):             # es wurde durch Sensoren, Zeitschaltung oder Button-Press etwas verändert
                                               # daraus folgt, dass der Sollwert verändert wurde
                                               
        Ds.Werte_schreiben(wa, ca)             # schreibt Veränderung in Logdatei

        Ak.change_aktoren(ca)                  # Aktoren werden gesteuert

        Ak.change_buttons(screen_app, ca)      # Anpassung der Buttons auf dem Bildschirm
        
        Si.ist_gleich_soll(ca)                 # IST-Werte werden an SOLL-Werte angeglichen

    
    if tdiff > datetime.timedelta(seconds = 360):    # schreibt Sensordaten nur einmal pro 6 Minute in Datei
                                                     # = 10 pro Stunde, 240 pro Tag
        Ds.Werte_schreiben(wa, ca)
        
        if t2.day != t1.day:           # nach 24 Uhr:
        
           wa["Sonnenaufgang"]=0       # bewirkt, dass in sensorcheck sunrise und sunset neu berechnet werden
           wa["Sonnenuntergang"]=0
           Ds.DLI_schreiben()          # schreibt die Lichtwerte als Daylight Integral in csv-database
        t1 = t2                
      
    after_id = fenster.after(1000, loop)            # after-Methode wiederholt loop , Zeitwert in Millisekunden
 
##### Ende loop ###########################################################################

fenster.after(0,loop)                               # 0 heißt, es geht sofort los

fenster.mainloop()

