#!/usr/bin/python
# coding=utf-8
# Wertelesen.py, liest die Sensordaten und schreibt sie in Wertearray
# Version 1.2

##########################################################


import Temperatursensoren as Ts
import Lichtlesen as Ls


def Werte_lesen(w_Array):

    Ts.ds1820auslesen()    # liest die Temperaturen aus den Sensoren
##    w_Array["T_Wasser1"] = Ts.tempSensorWert[0]
##    
##    w_Array["T_aussen"] = Ts.tempSensorWert[1]         
##    w_Array["Luxwert_1"] = Ls.readLight()
    
    return w_Array
