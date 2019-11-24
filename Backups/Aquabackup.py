#!/usr/bin/python3.5
#coding=utf-8
# Aquaponik-Kontrollsystem.py
# Version 1.3
# Diese Version ist gegenüber Vorgängerversion in Module aufgeteilt. Diese müssen sich im selben Ordner befinden, es ist
# kein Pfad gesetzt
#------------------------------------------------------------
## Das Programm steuert im Augenblick 2 Temperatursensoren und einen Lichtsensor sowie einen 230 V Motor
## der später im Winter Alubeschichtete Rollos innen vor die Stegplatten ziehen soll
##
## für weitere Einzelheiten zu der verwendeten Hardware siehe: readme.md
##
#für die Temperatursensoren muss man mit sudo nano etc/modules eintragen:     wire
##                                                                              w1-GPIO
##                                                                              w1-therm
##
## Zusätzliche habe ich in mit sudo nano /boot/config.txt eingetragen:          dtoverlay = w1-gpio
##                                                                              gpiopin=4      
##
##
## für den Lichtsensor muss man in raspi-config unter Interface Options den I2C Bus aktivieren
##
##
##
##



from __future__ import division, print_function  # Maßnahme um pygame mit Python 3.x kompatible zu machen
import pygame, pygame.gfxdraw                    # pygame ist eigentlich für Spieleentwicklung. \
from pygame.locals import *                      # Aber auch geeigent um Grafikfenster zu steuern
import sys, time, csv
from time import process_time


import tkinter as Tk                             # GUI-Bibliothek
#from tkinter import messagebox

import ptvsd
# eigene Module

import Kontrollfenster as Kf
import Motorsteuerung as Ms
import Temperatursensoren as Ts
import Uhrzeit as Uz
import Lichtlesen as Ls
import EMailsenden as Es
import Werte_auf_Screen_schreiben as Ws
import Werte_in_Datei_schreiben as Ds
import Buttons as Bt


global Motor_ist_an
global Motor_links
Motor_links = False
Motor_ist_an = False

#---------------------------------------------------------------------------------------------------------
#########################################################################################################
############        Programminitialisierung       #######################################################
#########################################################################################################

ptvsd.enable_attach()
ptvsd.wait_for_attach()



Ts.ds1820einlesen() #Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen

#Fensteraufbauen : 

Hintergrund = "lightgrey"
fenster = Tk.Tk()
fenster.configure(background = Hintergrund)

#####################################################################################################
#definiert mit Labelframe grafischen Gruppen, in die in task() geschrieben wird:


fenster.T_labelframe = Tk.LabelFrame(fenster,text = "Temperatur", \
                                bd = 5, height =300, width =550, relief = "groove")
tlf = fenster.T_labelframe
tlf.grid_propagate(0)   # zwingt den Labelframe die vorgegebenen Maße zu benutzen


fenster.M_labelframe = Tk.LabelFrame(fenster,text = "Motor/Rollo", \
                                bd = 5, height =200, width =340, relief = "groove", )
mlf = fenster.M_labelframe
mlf.grid_propagate(0)


fenster.V_labelframe = Tk.LabelFrame(fenster,text = "Stromversorgung", \
                                bd = 5, height =400, width =550, relief = "groove", )
vlf = fenster.V_labelframe
vlf.grid_propagate(0)


fenster.W_labelframe = Tk.LabelFrame(fenster,text = "Wasserfluß", \
                                bd = 5, height =400, width =340, relief = "groove", )
wlf = fenster.W_labelframe
wlf.grid_propagate(0)


fenster.W_labelframe = Tk.LabelFrame(fenster,text = "Wasserqualität", \
                                bd = 5, height =400, width =550, relief = "groove", )
qlf = fenster.W_labelframe
qlf.grid_propagate(0)


#####################################################################################################

app = Kf.Kontrollpanel(fenster, tlf, mlf, vlf, wlf, qlf, Hintergrund)

###################################################################################################


screen_write = True                 # Werte der Sensoren werden auf dem Bildschirm angezeigt,
                                    # kann mit click_screen-Button abgeschaltet werden


# Motor sichern
##tempVar1 = PY_VAR0                                    # Variablen nur zum Start
##tempVar2 = 1                                    # werden soäter durch Checkbox gesteuert

#Ms.Motor_an_aus(mlf, tempVar1 )                           # stellt sicher, dass der Motor beim Programmstart nicht an geht
##time.sleep(2)                                       # bischen warten
##Ms.Motor_Drehrichtung(mlf, tempVar2)               # stellt die Drehrichtung auf rechts

# Variablen für Zeitschleife

anfang =    [0,0,0]
ende =      [0,0,0]
intervall = 0
anfang=Uz.Uhrzeit()

Beginn= anfang[0]*3600 + anfang[1]*60 + anfang[2]




after_id = 0                            # dient der Identifierung der Task-Schleife

def Beenden(after_id):                  # wird von Clickbutton aufgerufen und beendet das Programm
    fenster.after_cancel(after_id)
    fenster.destroy()
    sys.exit()

def Screen(click_screen):
    global screen_write
    screen_write = not screen_write
    if screen_write:
        click_screen.config(text = "Bildschirmwerte aus")
    else:
        click_screen.config(text = "Bildschiremwerte an")
    
clickma = Tk.Button (fenster, text = "Beenden", command = lambda: Beenden(after_id))
clickma.grid(row = 3, column = 1, sticky = Tk.E)

click_screen = Tk.Button (fenster, text = "Bildschirmwerte aus", command = lambda: Screen(click_screen))
click_screen.grid(row = 3, column = 2, sticky = Tk.W)
    
# Task schreibt Sensordaten ins Fenster und in die CSV Datenbanken
# Task wird später durch die fenster.after-Methode jede Sekunde wiederholt

def task():
    
    global anfang, ende, intervall, erstesMal, after_id, Beginn, S_Ende, screen_write

    status = Ms.GPIO.input(Ms.IR_GPIO)              # Infrarot-Endstop
           
    #if status == 0:                                 #schaltet den Motor aus, wenn Infrarot-Endstopp aktiviert ist
        #Ms.Motor_aus(mlf, Hintergrund)
    ende = Uz.Uhrzeit()
   
        
    S_Ende = ende[0]*3600 + ende[1]*60 +ende[2]

    # Falls die Zeitdifferenz über die 24-Stundengrenze geht:
    
    if ( anfang[0] == 23) and (anfang[1] < 60 and anfang[1] > 50) and ( ende[0]== 0 ):
       S_Ende = S_Ende + 86400
    
    
    intervall =  S_Ende - Beginn
    
    if screen_write:

        Ws.Wert_schreiben(fenster, tlf, vlf, Hintergrund)      # schreibt Werte auf den Bildschiren

   


    if intervall  > 20:                            # schreibt Sensordaten nur einmal pro  6 Minute in Datei
                                                    # = 10/Stunde, 240 / Tag
        Ds.Werte_schreiben()
        #print(str(intervall))
        anfang = Uz.Uhrzeit()
        Beginn= anfang[0]*3600 + anfang[1]*60 + anfang[2]                
      
    
    
    

    after_id = fenster.after(10000, task)                           # wiederholt Task , Zeitwert in Millisekunden
 
fenster.after(0,task)

fenster.mainloop()

