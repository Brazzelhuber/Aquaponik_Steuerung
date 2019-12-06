#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### interface_i2c_ds1307_1.py
##
###!/usr/bin/python
##from myclassMcp3008 import MCP3008
###from myclassMcp3008 import Mcp3008
##
##
##from time import sleep
##
##
##mcp = MCP3008()
##mcp.open()
##
##while 1:
##   
##    regenwert = mcp.read(channel = 0)
##    regenwert = float(regenwert)
##    print (str(regenwert))
##    #print("Anliegende Spannung: %.2f" % (regenwert / 1023.0 * 3.3) )
##
##    sleep(1)


 
import spidev
import os
import time
 
delay = 0.2
 
spi = spidev.SpiDev()
spi.open(0,0)
 
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data
 
if __name__ == "__main__":
  try:
    while True:
      val = readChannel(0)
      
      print(val)
      time.sleep(delay)
      
  except KeyboardInterrupt:
    print ("Cancel.")

   





