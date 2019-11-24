import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

HIGH = True  # HIGH-Pegel
LOW  = False # LOW-Pegel

# Funktionsdefinition
def readAnalogData(adcChannel, SCLKPin, MOSIPin, MISOPin, CSPin):
    # Pegel vorbereiten
    GPIO.output(CSPin,   HIGH)    
    GPIO.output(CSPin,   LOW)
    GPIO.output(SCLKPin, LOW)
        
    sendcmd = adcChannel
    sendcmd |= 0b00011000 # Entspricht 0x18 (1:Startbit, 1:Single/ended)

    # Senden der Bitkombination (Es finden nur 5 Bits Beruecksichtigung)
    for i in range(5):
        if (sendcmd & 0x10): # (Bit an Position 4 pruefen. Zaehlung beginnt bei 0)
            GPIO.output(MOSIPin, HIGH)
        else:
            GPIO.output(MOSIPin, LOW)
        # Negative Flanke des Clocksignals generieren
        GPIO.output(SCLKPin, HIGH)
        GPIO.output(SCLKPin, LOW)
        sendcmd <<= 1 # Bitfolge eine Position nach links schieben
        
    # Empfangen der Daten des ADC
    adcvalue = 0 # Ruecksetzen des gelesenen Wertes
    for i in range(11):
        GPIO.output(SCLKPin, HIGH)
        GPIO.output(SCLKPin, LOW)
        
        adcvalue <<= 1 # 1 Postition nach links schieben
        if(GPIO.input(MISOPin)):
            adcvalue |= 0x01
    time.sleep(0.5)
    return adcvalue

# Variablendefinition
adcChannel =   0  # Analog/Digital-Channel
SCLK        = 11  # Serial-Clock
MOSI        = 10  # Master-Out-Slave-In (Din)
MISO        =  9  # Master-In-Slave-Out (Dout)
CS          =  8  # Chip-Select

# Pin-Programmierung
GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CS,   GPIO.OUT)

while True:
    
    rohData =readAnalogData(adcChannel, SCLK, MOSI, MISO, CS)
    #print(str(rohData))
    VoltData= rohData*3.22/1000
    print("Spannung = %2.2f" %VoltData)
