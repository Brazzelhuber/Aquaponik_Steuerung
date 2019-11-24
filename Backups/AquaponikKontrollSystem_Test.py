#!/usr/bin/python
# coding=utf-8
# Aquaponik-Kontrollsystem.py
# Version 1.2
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
import tkinter as Tk                             # GUI-Bibliothek
from tkinter import messagebox


# eigene Module

import Kontrollfenster as Kf
import Motorsteuerung as Ms
import Temperatursensoren as Ts
import Uhrzeit as Uz
import Lichtlesen as Ls
import EMailsenden as Es
import Werte_auf_Screen_schreiben as Ws
import Werte_in_Datei_schreiben as Ds

Hintergrund = "lightblue"

#---------------------------------------------------------------------------------------------------------
#########################################################################################################
############        Programminitialisierung
#########################################################################################################

#Fensteraufbauen()

Ts.ds1820einlesen() #Anzahl und Bezeichnungen der vorhandenen Temperatursensoren einlesen

fenster = Tk.Tk()
fenster.geometry("1200x600")
fenster.configure(background = Hintergrund)
app = Kf.Kontrollpanel(fenster, Hintergrund)

# Motor sichern

Ms.Motor_aus(Hintergrund)                         # stellt sicher, dass der Motor beim Programmstart nicht an geht
time.sleep(2)                       # bischen warten
Ms.Motor_Drehrich_rechts(Hintergrund)      # stellt die Drehrichtung auf rechts

# Variablen für Zeitschleife

anfang =    [0,0,0]
ende =      [0,0,0]
intervall = 0
anfang=Uz.Uhrzeit()
Beginn= anfang[0]*3600 + anfang[1]*60 + anfang[2]

# Task schreibt Sensordaten ins Fenster und in die CSV Datenbanken
# Task wird später durch die fenster.after-Methode jede Sekunde wiederholt

def task():
    
    global anfang, ende, intervall, Beginn, S_Ende

    status = Ms.GPIO.input(Ms.IR_GPIO)              # Infrarot-Endstop
           
    if status == 0:                                 #schaltet den Motor aus, wenn Infrarot-Endstopp aktiviert ist
        Ms.Motor_aus(Hintergrund)
        
    S_Ende = ende[0]*3600 + ende[1]*60 +ende[2]
    
    intervall =  (S_Ende - Beginn) 

    Ws.Wert_schreiben(fenster, Hintergrund)
    
    if intervall  > 300:        # schreibt Sensordaten nur einmal pro  5 Minute in Datei

        Ds.Werte_schreiben()
          
        anfang=Uz.Uhrzeit()
        Beginn= anfang[0]*3600 + anfang[1]*60 + anfang[2]   #setzt Intervallmessung zurück
        
    ende = Uz.Uhrzeit()
 
    fenster.after(1000, task)                           # wiederholt Task , Zeitwert in Millisekunden
 
fenster.after(1000,task)

fenster.mainloop()


