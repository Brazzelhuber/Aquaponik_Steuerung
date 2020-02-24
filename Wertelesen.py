#!/usr/bin/python
# coding=utf-8
# Wertelesen.py, liest die Sensordaten und schreibt sie in Wertearray
# Version 1.2

##########################################################
import sys

##
##if not ("Temperatursensoren" in sys.modules):
##    import Temperatursensoren
##else:
##    print("Temperatursensoren ist schon in sys.modules")
import Temperatursensoren
##import importlib

##spec = importlib.util.find_spec('Temperatursensoren')
##print('Loader:', spec.loader)
##
##m = spec.loader.load_module()
##print('Module:', m)
##temp_specs = importlib.util.find_spec("Temperatursensoren")
##Temperatursensoren = importlib.util.module_from_spec(temp_specs)
##temp_specs.loader.exec_module(Temperatursensoren)

import Lichtlesen as Ls
import RPi.GPIO as GPIO
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:

def Wasserstand():
    
    from Bluetin_Echo import Echo

##    distance = 25
##
##    return distance
##    
     
    TRIGGER_PIN = 6
    ECHO_PIN = 17
    # Initialise Sensor with pins, speed of sound.
    speed_of_sound = 315
    echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
    # Measure Distance 5 times, return average.
    samples = 5
    result = echo.read('cm', samples)
    result = ("%4.1f" % result)
    
##    # Reset GPIO Pins.
##    echo.stop()
 
    return result
     
     

def Werte_lesen(w_Array):
    
    # Temperaturen :

    Temperatursensoren.ds1820auslesen()    
    w_Array["T_Wasser1"] = Temperatursensoren.tempSensorWert[0]
    
    w_Array["T_aussen"] = Temperatursensoren.tempSensorWert[1]
    
    w_Array["Luxwert_1"] = Ls.readLight()
    
    # MCP3008 - Abfrage für Erdfeuchte und Batteriespannung:
    CLK  = 11
    MISO = 9
    MOSI = 10
    CS   = 8

    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
    
    
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

    # Ultraschall über GPIO:
    w_Array["Wasserstand"]= Wasserstand()
    
    return w_Array




