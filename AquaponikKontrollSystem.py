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

# Zur Erklärung siehe README.md

vw         =  {"TempWasserMin" : 3,         
               "TempWasserMax" : 23,
               "TempLuftMin"   : 3,         
               "WasserpegelMin": 0,        
               "WasserpegelMax": 0,
               "PhWertMin"     : 6.7,
               "PhWertMax"     : 7.1,
               "Fuetterung"    : 10.00,
               "Fuett.dauer"  : 5
               }
               



wa          = {"T_Luft_oben" : 0,      
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
               "warmer CHOP-Circle":       [0,0,0],  
               "Kühlung mit Bewässerung":  [0,0,0],  
               "Kühlung mit Verieselung":  [0,0,0],  
               "Brunnenwasser als Heizung":[0,0,0],  
               "Wasser auffüllen":         [0,0,0],  
               "Wasser ablassen":          [0,0,0],  
               "Hauptpumpe":               [0,0,0],
               "Screen_schreiben":         [0,1,0],   
               "Heizung":                  [0,0,0],  
               "Es ist Tag"      :         [0,0],    
               "Alarm"            :        [0,0],    
               "Fütterung"  :              [0,0,0],  
               "Logeintrag":               [0,0],    
               "WQ to FT":                 [0,0,0],  
               "WQ to VR":                 [0,0,0],  
               "ST to VR":                 [0,0,0],  
               "ST to FT":                 [0,0,0],  
               "ST to HB":                 [0,0,0],  
               "LU to HP":                 [0,0,0],  
               "LO to HP":                 [0,0,0]}  



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

    ca,wa = Ch.SensorCheck(screen_app, ca, wa, vw)  # checkt bei den Sensoren,ob etwas zu tun ist
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
    

    
    if ca["Screen_schreiben"][0] == 1:         # im Dauerbetrieb == 0
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

