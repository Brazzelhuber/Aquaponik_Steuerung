#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# interface_i2c_ds1307_1.py

#!/usr/bin/python
from myclassMcp3008 import MCP3008
#from myclassMcp3008 import Mcp3008


from time import sleep


mcp = MCP3008()
mcp.open()

while 1:
   
    regenwert = mcp.read(channel = 0)
    regenwert = float(regenwert)
    print (str(regenwert))
    #print("Anliegende Spannung: %.2f" % (regenwert / 1023.0 * 3.3) )

    sleep(1)

##
## 
##import spidev
##import os
##import time
## 
##delay = 0.2
## 
##spi = spidev.SpiDev()
##spi.open(0,0)
## 
##def readChannel(channel):
##  val = spi.xfer2([1,(8+channel)<<4,0])
##  data = ((val[1]&3) << 8) + val[2]
##  return data
## 
if __name__ == "__main__":
  try:
    while True:
      val = readChannel(0)
      if val != 0:
          print(val)
      time.sleep(delay)
      
  except KeyboardInterrupt:
    print ("Cancel.")

##
##
##import csv
##dateiname1 = "Tempdatenaussen.csv"
##dateiname2 = "Tempdaten_Wasser1.csv"
####with open(dateiname) as csvfile:
####
####        reader = csv.reader(csvfile,delimiter = ",")
####        data = list(reader)
####    
####        Zaehl_liste = enumerate(data)
####        row_count = len(data)
####        print("len(data) = " + str(row_count))
##
##myfile1 = open(dateiname1)
##myfile2 = open(dateiname2)
##reader1 = csv.reader(myfile1,delimiter = ",")
##reader2 = csv.reader(myfile2,delimiter = ",")
##data1 = list(reader1)
##data2 = list(reader2)
##
##
##row_count1 = len(data1)
##print("len(data1) = " + str(row_count1))
##myfile1.close()
##row_count2 = len(data2)
##print("len(data2) = " + str(row_count2))
##myfile1.close()
####for line in data1:
####  print(line)
##for i in range(0,row_count1):
##  print(str(data1[i]) + " " + str(data2[i]))
##




