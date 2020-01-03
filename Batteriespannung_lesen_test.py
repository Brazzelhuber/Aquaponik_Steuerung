###!/usr/bin/python
### coding=utf-8
### Batteriespannung_lesen.py
## #Version 1.0
##import tkinter
##import time
##import spidev
##
##class MCP3008:
##    def __init__(self, bus = 0, device = 0):
##        self.bus, self.device = bus, device
##        self.spi = spidev.SpiDev()
##        self.open()
##
##    def open(self):
##        self.spi.open(self.bus, self.device)
##    
##    def read(self, channel = 0):
##        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
##        data = ((adc[1] & 3) << 8) + adc[2]
##        return data
##            
##    def close(self):
##        self.spi.close()
##
##while True:
##    adc = MCP3008()
##    value = adc.read( channel = 0 ) # Den auszulesenden Channel kannst du natürlich anpassen
##    print("Anliegende Spannung: %.2f" % (value / 1023.0 * 3.3) )
##    time.sleep(0.5)
##
##
###mainloop()
##
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False) 
#
HIGH = True   # High-Pegel
LOW  = False  # LOW-Pegel

def readAnalogData(adcChannel, SCLKPin, MOSIPin, MISOPin,CSPin):
    # Pegel vorbereiten:
    GPIO.output(CSPin,  HIGH)
    GPIO.output(CSPin,  LOW)
    GPIO.output(SCLKPin, LOW)

    sendcmd = adcChannel
    sendcmd |= 0b00011000

    # Senden der Bitkombinationen (Es finden nur 5 Bits Berücksichtigung)
                   
    for i in range(5):
        if(sendcmd & 0x10): # Bit an Position 4 prüfen. Zählung beginnt mit 0
            GPIO.output(MOSIPin, HIGH)
        else:
            GPIO.output(MOSIPin, LOW)
        #Negative Flanke des Clocksignals generieren
        GPIO.output(SCLKPin, HIGH)
        GPIO.output(SCLKPin, LOW)
        sendcmd <<=1   # Bitfolge eine Position nach links schieben

    # Empfangen der Daten des ADC
    adcvalue = 0  # Rücksetzen des gesetzten Wertes
    for i in range(11):
        GPIO.output(SCLKPin, HIGH)
        GPIO.output(SCLKPin, LOW)
        adcvalue <<=1  # Poisiton nach links verschieben
        if(GPIO.input(MISOPin)):
            adcvalue |- 0x01
    time.sleep(0.5)
    return float(adcvalue)

# Variablendefinition:

ADC_Channel = 0     # Analog/Digital-Channel
SCLK        = 11   # Serial-Clock
MOSI        = 10    # Master-Out-Slave-in
MISO        = 9    # Master-in-Slave-out
CS          = 8    # Chip-Select


# Pin-Programmierung

GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)

while True:
    print(str(readAnalogData(ADC_Channel, SCLK, MOSI,MISO, CS)/1024))
          
    
    
