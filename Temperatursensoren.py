#!/usr/bin/python
# coding=utf-8
# Termperatursensoren.py
# Version 1.2
#--------------
#####################################################################
#
# Das Programm liest die angeschlossenen Temeperatursensoren aus
#
####################################################################


##########################################################################################################
# die Temperatursensoren sind 1-wire-devices, die in dem Verzeichnis /sys/bus/w1/devices regisitriert sind
# diese Funktion liest die Dateinamen und speichert sie in der Liste tmpSensorBezeichnung

#------------------------------------------------------------------------------------------------------

import os

# Global für vorhandene Temperatursensoren
tempSensorBezeichnung = []  #Liste mit den einzelnen Sensoren-Kennungen
tempSensorAnzahl = 0        #INT für die Anzahl der gelesenen Sensoren
tempSensorWert = []         #Liste mit den einzelnen Sensor-Werten
Temp = []
# Global für Programmstatus / 
programmStatus = 1 

def ds1820einlesen():
    
    
    global tempSensorBezeichnung, tempSensorAnzahl, programmStatus, Temp
    #Verzeichnisinhalt auslesen mit allen vorhandenen Sensorbezeichnungen 28-xxxx
    try:
        for x in os.listdir("/sys/bus/w1/devices"):
            if (x.split("-")[0] == "28") or (x.split("-")[0] == "10"):
                tempSensorBezeichnung.append(x)
                #print(str(tempSensorBezeichnung[tempSensorAnzahl]))
                tempSensorAnzahl = tempSensorAnzahl + 1
    except:
        # Auslesefehler
        print ("Der Verzeichnisinhalt konnte nicht ausgelesen werden.")
        programmStatus = 0   
#--------------------------------------------------------------------------------------------------------------


def ds1820auslesen():
    
    global tempSensorBezeichnung, tempSensorAnzahl, tempSensorWert, programmStatus
    x = 0
    try:
        # 1-wire Slave Dateien gem. der ermittelten Anzahl auslesen  und in Liste einfügen
        while x < tempSensorAnzahl:
            dateiName = "/sys/bus/w1/devices/" + tempSensorBezeichnung[x] + "/w1_slave"
            
            file = open(dateiName)
            filecontent = file.read()
            file.close()
            # Temperaturwerte auslesen und konvertieren
            stringvalue = filecontent.split("\n")[1].split(" ")[9]
            sensorwert = float(stringvalue[2:]) / 1000
            temperatur = '%6.2f' % sensorwert #Sensor- bzw. Temperaturwert auf 2 Dezimalstellen formatiert
            tempSensorWert.insert(x,temperatur) #Wert in Liste aktualisieren
            x = x + 1
    except:
        # Fehler bei Auslesung der Sensoren
        print ("Die Auslesung der DS1820 Sensoren war nicht möglich.")
        programmStatus = 0
