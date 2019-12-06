#!/usr/bin/python
##
##import spidev
##import time
##
##class Mcp3008:
##
##    def __init__(self,bus=0,device=0):
##        # Open SPI bus
##        self.__spi = spidev.SpiDev()
##        self.__spi.open(bus,device)
##
##
##
##    # Function to read SPI data from MCP3008 chip
##    # Channel must be an integer 0-7
##    def ReadChannel(self,channel):
##        adc = self.__spi.xfer2([1, (8 + channel) << 4, 0])
##        data = ((adc[1] & 3) << 8) + adc[2]
##        return data
##

##    # Deze functie zal de data converteren volgens voltage level
##    # 1 graad = 10mV
##    def convert_volts(self, data, places):
##        volts = (data * 3.3) / float(1023)  # 3.3V van de pi en 2^10 = 1024 = 0 tot 1023
##        volts = round(volts, places)  # round() wordt gebruikt om een bepaalde waarde af te ronden
##        return volts
##
##
##    # Deze functie zal de temperatuurwaarde van de TMP35 berekenen
##    def convert_temp(self, data, places):
##        temp = ((data * 205) / float(1023)) - 55  # maal 205 want temp heeft waarde van -55 tot 150 = 205tussenstappen
##        # temp = (((data * 205) / float(1023)) * 320.0886918) - 55
##        temp = round(temp, places)
##        return temp
from spidev import SpiDev

 
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
 
    def open(self):
        self.spi.open(self.bus, self.device)
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()
