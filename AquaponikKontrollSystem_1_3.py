#!/usr/bin/python3.5
#coding=utf-8
# Aquaponik-Kontrollsystem.py
# Version 1.3
# Diese Version ist gegenüber Vorgängerversion in Module aufgeteilt. Diese müssen sich im selben Ordner befinden, es ist
# kein Pfad gesetzt
#------------------------------------------------------------
## Das Programm steuert im Augenblick 2 Temperatursensoren und einen Lichtsensor 
## für weitere Einzelheiten zu der verwendeten Hardware siehe: readme.md
##
##  zum Auslesen der Temperatursensoren
## in /boot/config.txt eingetragen:          dtoverlay = w1-gpio
##                                           gpiopin=4      
##
##
## für den Lichtsensor muss man in raspi-config unter Interface Options den I2C Bus aktivieren
##

from __future__ import division, print_function  # Maßnahme um pygame mit Python 3.x kompatible zu machen
import sys, time, csv
import tkinter as Tk                             # GUI-Bibliothek
import datetime
from smbus import SMBus

import ptvsd     # dient dem remote-debugging mit Visual Studio

# eigene Module

import Kontrollfenster as Kf
import Temperatursensoren as Ts
#import Lichtlesen as Ls
#import EMailsenden as Es
import Werte_auf_Screen_schreiben as Ws
import Werte_in_Datei_schreiben as Ds
import Wertelesen as Wl
import Check_Center as Ch
import Soll_Ist as Si
import Aktion as Ak

##
# remote Debugging mit Visual Studio (wenn Debugging, uncomment):
##
##ptvsd.enable_attach()
##ptvsd.wait_for_attach()

# in VS muß bei Debugging in "an Prozeß anhängen" ptsvd gewählt 
# und in Ziel: tcp://192.168.178.119:5678 eingegeben werden

#---------------------------------------------------------------------------------------------------------
#########################################################################################################
############        Programminitialisierung       #######################################################
#########################################################################################################

#######################################################################################################
# Initiieren: Array mit Sensordaten und Array mit Kontrollvariablen:

wa          = {"T_Luft_oben" : 0,      # der Werte-Array beinhaltet die ausgelesenen Sensordaten
               "T_Luft_unten" : 0,
               "T_Wasser1": 0,
               "T_Wasser2": 0,
               "T_aussen": 0,
               "Luxwert_1" : 0 ,
               "Luxwert_2" : 0,
               "Ph-Wert": 0 ,
               "Sauerstoff" : 0,
               "Ampere"  :0 ,
               "Wasserstand" : 0,
               "Sonnenaufgang": 0,
               "Sonnenuntergang": 0
                }
# Kontrollarray ca entält links die IST-, in der Mitte oder rechts  die SOLL-Zustände ([0,1] heißt: ist aus/zu soll
# aber an/auf).
# da wo das Item dreistellig ist, indizierte der letzte Wert, ob ein manual override vorliegt. Beispiel: die
# if-clauses für die Sensordaten sagen: "normaler CHOP-Circle", über den Bildschirm wurde
# aber "Kühlung mit Bewässerung" gewählt. Dann darf das nicht im nächsten Loop durch die Sensorbedingungen
# rückgängig gemacht werden, sondern muß entgegen der definierten Bedingungen aufrechterhalten werden,
# bis wieder eine manuelle Abschaltung erfolgt. 

ca          ={ "normaler CHOP-Circle":     [0,0,0],  # normaler Betrieb (FT -> GB -> ST ->FT) wobei Luft von unten
               "warmer CHOP-Circle":       [0,0,0],  # warmer Betrieb (FT -> GB -> ST ->FT) wobei Luft von unterm Dach
               "Kühlung mit Bewässerung":  [0,0,0],  
               "Kühlung mit Verieselung":  [0,0,0],
               "Brunnenwasser als Heizung":[0,0,0],  # Brunnenwasser hat 15 Grad, kann auch zum "Heizen" eingesetzt werden
               "Wasser auffüllen":         [0,0,0],  # Wasserverlust muss ausgeglichen werden
               "Wasser ablassen":          [0,0,0],  # zuviel Wasser im System
               "Hauptpumpe":               [0,0,0],
               "Screen_schreiben":         [0,1,0],  # Sensorwerte auf Screen schreiben, kann im Dauerbetrieb abgestellt werden
               "Heizung":                  [0,0,0],  # wenn es im Winter zu kalt wird
               "Es ist Tag"      :         [0,0],    # kommt aus den Sonnendaten, Luxwerte werden nur tagsüber geschrieben
               "Alarm"            :        [0,0],    # wenn was schiefgeht wird EMail geschrieben
               "Fütterung"  :              [0,0,0],  # Fütterungsautomat einschalten?
               "Logeintrag":               [0,0],
               "WQ to FT":                 [0,0,0],  # die Wasserventile einzel
               "WQ to VR":                 [0,0,0],
               "ST to VR":                 [0,0,0],   
               "ST to FT":                 [0,0,0],
               "ST to HB":                 [0,0,0],
               "LU to HP":                 [0,0,0],  # Luftventile
               "LO to HP":                 [0,0,0]}  #  saugt Luft von unterm Dach in die airpumpo


##################################################################################################
# Sensoren initiieren:

Ts.ds1820einlesen() #Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen
##################################################################################################
#Fenster initiieren : 

Hintergrund = "lightgrey"
del_dat = ""
fenster = Tk.Tk()
fenster.configure(background = Hintergrund)

###############################################################################
# Kontrollpanel, mit dem das System vom Bildschirm aus gesteuert werden kann: #
                                                                              #
screen_app = Kf.Kontrollpanel(fenster, Hintergrund, ca)                       #
###############################################################################

# widget und Callback für den Button "Beenden":

def Beenden(after_id):                  # wird von clickma aufgerufen und beendet das Programm
    fenster.after_cancel(after_id)
    fenster.destroy()
    sys.exit()
   
clickma = Tk.Button (fenster, text = "Beenden", command = lambda: Beenden(after_id))
clickma.grid(row = 3, column = 0, padx = 10, sticky = Tk.E)

#############################################################################################################
# Definitionen für die Hardware-Uhr:

##port = 1                # (0 for rev.1, 1 for rev 2!)
##bus = SMBus(port)
##rtcAddr = 0x68
##
##def bcd2str(d):         # // for integer division; % for modulo
##    if (d <= 9):
##        return '0' + str(d)
##    else:
##        return str(d // 16) + str(d % 16)
##rd = bus.read_i2c_block_data(rtcAddr, 0, 7)
##screen_app.Datum_Zeit = Tk.Label (text = (bcd2str(rd[4]) + '.' + bcd2str(rd[5]) + '.' + bcd2str(rd[6]) + '  '\
##                                        + bcd2str(rd[2]) + ':' + bcd2str(rd[1]) ))
##screen_app.Datum_Zeit.grid(row = 3, column = 0 , sticky = Tk.W)
screen_app.Datum_Zeit = Tk.Label (text = time.strftime("%d.%m.%Y - %H:%M"))
screen_app.Datum_Zeit.grid(row = 3, column = 0 , sticky = Tk.W)
################################################################################################################    
# Programm starten 
# loop wird durch die fenster.after-Methode jede Sekunde wiederholt
###################################################################
# Variablen für loop:

t1 = datetime.datetime.now()         # dient der Zeitsteuerung in der Schleife
after_id = 0

#####################################################
def loop():
    
    # Datum und Uhrzeit aus RTC gelesen:
    
    screen_app.Datum_Zeit.configure (text = time.strftime("%d.%m.%Y - %H:%M"))
    
    global wa, ca, t1, after_id

    t2 = datetime.datetime.now()

    
    tdiff = t2 -t1

    wa = Wl.Werte_lesen(wa)                 # liest Werte aus Sensoren und schreibt sie in Array wa

    ca,wa = Ch.SensorCheck(screen_app, ca, wa)          # checkt bei den Sensoren,ob etwas zu tun ist
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
    

    
    if ca["Screen_schreiben"][0] == 1: Ak.change_sensordaten (screen_app, wa) # schreibt Sensordaten auf Screen
    
    if not Si.soll_gleich_ist(ca):          # es wurde durch Sensoren, Zeitschaltung oder Button-Druck etwas verändert
        
        Ds.Werte_schreiben(wa, ca)          # schreibt Veränderung in Logdatei

        Ak.change_buttons(screen_app, ca)    # Anpassung der Buttons auf dem Bildschirm
             
        Ak.change_aktoren(ca)               # Aktoren werden gesteuert
        
        Si.ist_gleich_soll(ca)              # IST-Werte werden an SOLL-Werte angeglichen

    
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

