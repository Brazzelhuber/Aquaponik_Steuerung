#!/usr/bin/python3.5
# coding=utf-8
# Aquaponik-Kontrollsystem.py

#------------------------------------------------------------
## Für weitere Einzelheiten siehe: readme.md


from __future__ import division, print_function  # Maßnahme um pygame mit Python 3.x kompatible zu machen

import sys
import time
import csv
import tkinter as Tk                             # GUI-Bibliothek
import datetime
from smbus import SMBus
import logging
import importlib
import threading
from threading import Thread
from queue import Queue


# eigene Module

import Kontrollfenster as Kf


import Temperatursensoren 
import Werte_in_Datei_schreiben as Ds
import Wertelesen as Wl
import Check_Center as Ch
import Soll_Ist as Si
import Aktion as Ak
import Vorgabe as Vw
import Zeitschaltuhr as Zsu

##
#import ptvsd     # dient dem remote-debugging mit Visual Studio

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
# Initiieren: Array mit Vorgabewerten, Array für Sensordaten, Array mit Kontrollvariablen und mit Werten
# für die Zeitschaltuhr:

# Zur Erklärung siehe README.md

vw         =  {"TempWasserMin" : 3,         
               "TempWasserMax" : 23,
               "TempLuftMin"   : 3,         
               "WasserpegelMin": 0,        
               "WasserpegelMax": 0,
               "PhWertMin"     : 6.7,
               "PhWertMax"     : 7.1,
               
               }
               



wa          = {"T_Luft_Frühbeet" : 0,      
               "T_Luft_unten" : 0,     
               "T_Wasser1": 0,         
               "T_Wasser2": 0,          
               "T_aussen": 0,           
               "Luxwert_1" : 0 ,        
               "Ph-Wert": 0 ,           
               "Sauerstoff" : 0,        
               "Volt"  :0 ,             
               "Wasserstand" : 0,        
               "Sonnenaufgang": 0,      
               "Sonnenuntergang": 0,
               "Erdfeuchte1" : 0,       
               "Erdfeuchte2" : 800,       
               "Erdfeuchte3" : 700,       
               "Erdfeuchte4" : 500,
               "Erdfeuchte5" : 0,
               "Erdfeuchte6" : 0
                }


ca          ={ "normaler CHOP-Circle":     [0,0,0],  
               "Bewässerung":              [0,0,0],  
               "Kühlung mit Bewässerung":  [0,0,0],  
               "Kühlung mit Verrieselung": [0,0,0],  
               "Brunnenwasser als Heizung":[0,0,0],  
               "Wasser auffüllen":         [0,0,0],  
               "Wasser ablassen":          [0,0,0],  
               "Hauptpumpe":               [0,0,0],
               "Screen_schreiben":         [0,1,0],   
               "Heizung":                  [0,0,0],  
               "Es ist Tag"      :         [0,0],    
               "Alarm"            :        [0,0],    
               "Fütterung"  :              [0,0,0],
               "Beleuchtung":              [0,0,0],
               "Logeintrag":               [0,0],    
               "WQ to FT":                 [0,0,0],  
               "WQ to VR":                 [0,0,0],  
               "ST to VR":                 [0,0,0],  																																						
               "ST to FT":                 [0,0,0],  
               "ST to HB":                 [0,0,0],   																																																																																																																																																																																																																																																																																				
               "WQ to WI":                 [0,0,0]}																																																																	

zeiten =     {"Fuetterung_Anfang":      "09:00",
              "Fuetterung_Ende" :       "09:10",
              "Beleuchtung_Anfang":    "06:00",
              "Beleuchtung_Ende":      "20:00",
              "Blumenwiese_Anfang":    "09:30",
              "Blumenwiese_Ende":      "09:35"
              }


###################################################################################################

# Thread für Zeitschaltuhr initiieren:


queue1 = Queue()
queue2 = Queue()
pill2kill = threading.Event()
zsu = threading.Thread(target=Zsu.timecontrol, args =(pill2kill, ca, zeiten, queue1,queue2))
zsu.start()



##################################################################################################
# Sensoren initiieren:

Temperatursensoren.ds1820einlesen() #Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen
##################################################################################################
#Fenster initiieren : 

Hintergrund = "lightgrey"
fenster = Tk.Tk()
fenster.configure(background = Hintergrund)


###############################################################################
# Kontrollpanel, mit dem das System vom Bildschirm aus gesteuert werden kann: #
                                                                              #
screen_app = Kf.Kontrollpanel(fenster, Hintergrund, ca, vw, zeiten)                       #
###############################################################################
# Einlesen der Vorgabewerte und Werte für Zeitschaltung:

Vw.LeseVorgabe(screen_app, vw)
##Vw.LeseZeiten(screen_app, zeiten)

# widget und Callback für den Button "Beenden":

def Beenden(after_id, vw):                  # wird von clickma aufgerufen und beendet das Programm
    
    pill2kill.set()             # killt den zeitschaltuhrthread
    Vw.WriteWerte(vw)           # schreibt die Vorgabewerte in Datei
    Vw.WriteZeiten(zeiten)      # schreibt die Zeitschaltuhrherte in Datei
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
# Ende der Programminitialisierung

######################################################################

# Programm starten 
# loop wird durch die (fenster.)after-Methode jede Sekunde wiederholt
###################################################################
# Variablen für loop:

t1 = datetime.datetime.now()         # dient der Zeitsteuerung in der Schleife
after_id = 0

def loop():
    myvar = queue1.get()
    #print(str(myvar))
    zeiten = queue2.get()
    #print(str(zeiten))
    t2 = datetime.datetime.now()
    
    global wa, ca, vw, t1, after_id
    
     # Datum und Uhrzeit auf Screen aktualisieren:
    
    screen_app.Datum_Zeit.configure (text = time.strftime("%d.%m.%Y - %H:%M"))

    tdiff = t2 -t1

    wa = Wl.Werte_lesen(wa)                         # liest Werte aus Sensoren und schreibt sie in Array wa

    ca,wa = Ch.SensorCheck(screen_app, ca, wa, vw)  # checkt bei den Sensoren,ob etwas zu tun ist
                                                    # manuelle Befehle vom Bildschirm aus werden von Modul
                                                    # "Kontrollpanel" über button-callback
                                                    # aufgerufen und in Modul "Ch.Buttoncheck" in den ca-Array
                                                    # eingetragen
    
    Ch.Ist_es_Tag(t1,t2,ca,wa)          # Feststellen, ob es Tag ist (nur dann werden Lichtdaten in Datei geschrieben)
    
    
    if ca["Screen_schreiben"][0] == 1:         # im Dauerbetrieb = 0
        Ak.change_sensordaten (screen_app, wa) # schreibt Sensordaten auf Screen
    
    
    if not Si.soll_gleich_ist(ca):             # es wurde durch Sensoren, Zeitschaltung oder Button-Press etwas verändert
                                               # daraus folgt, dass der Sollwert verändert wurde
                                               
        Ds.Werte_schreiben(wa, ca)             # schreibt Veränderung in Logdatei

        Ak.change_aktoren(ca)                  # Aktoren werden gesteuert

        Ak.change_buttons(screen_app, ca)      # Anpassung der Buttons auf dem Bildschirm   
        
        Si.ist_gleich_soll(ca)                 # IST-Werte werden an SOLL-Werte angeglichen
    
    Ak.Fuetterung(t2, ca,vw, screen_app)       # prüft ob Fütterungszeit ist
    
    if tdiff > datetime.timedelta(seconds = 360):    # schreibt Sensordaten nur einmal pro 6 Minute in Datei
                                                     # = 10 pro Stunde, 240 pro Tag
        Ds.Werte_schreiben(wa, ca)
        
        if t2.day != t1.day:           # nach 24 Uhr:
        
           wa["Sonnenaufgang"]=0       # bewirkt, dass in sensorcheck sunrise und sunset neu berechnet werden
           wa["Sonnenuntergang"]=0
           Ds.DLI_schreiben()          # schreibt die Lichtwerte als Daylight Integral in csv-database
        t1 = t2                        # setzt Zeitdelta zurück               
      
    after_id = fenster.after(1000, loop)           # after-Methode wiederholt loop , Zeitwert in Millisekunden
 
##### Ende loop ###########################################################################

fenster.after(0,loop)                             # 0 heißt, es geht sofort los

fenster.mainloop()

