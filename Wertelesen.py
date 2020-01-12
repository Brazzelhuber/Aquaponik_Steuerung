#!/usr/bin/python
# coding=utf-8
# Wertelesen.py, liest die Sensordaten und schreibt sie in Wertearray
# Version 1.2

##########################################################


import Temperatursensoren as Ts
import Lichtlesen as Ls

import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
##CLK  = 18
##MISO = 23
##MOSI = 24
##CS   = 25
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
         

def Werte_lesen(w_Array):

    Ts.ds1820auslesen()    # liest die Temperaturen aus den Sensoren
    w_Array["T_Wasser1"] = Ts.tempSensorWert[0]
    
    w_Array["T_aussen"] = Ts.tempSensorWert[1]         
    w_Array["Luxwert_1"] = Ls.readLight()
    
    
    values = [0]*8
    for i in range(8):
        values[i] = mcp.read_adc(i)
   
    w_Array["Erdfeuchte1"]= values[1]
    w_Array["Erdfeuchte2"]= values[2]
    w_Array["Erdfeuchte3"]= values[3]
    w_Array["Erdfeuchte4"]= values[4]
    w_Array["Erdfeuchte5"]= values[5]
    w_Array["Erdfeuchte6"]= values[6]
    w_Array["Volt"] = "{0:5.2f}".format(values[7]/76.66)  # Umrechnung von MCP3008-Wert auf Volt
    
    return w_Array




