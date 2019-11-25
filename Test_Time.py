###!/usr/bin/env python3
### -*- coding: utf-8 -*-
### interface_i2c_ds1307_1.py
##
##from smbus import SMBus
##from time import sleep
##
##port = 1                # (0 for rev.1, 1 for rev 2!)
##bus = SMBus(port)
##rtcAddr = 0x68
##
##def bcd2str(d):         # // for integer division; % for modulo
##    if (d <= 9):
##        return '0' + str(d)
##    else:
##        return str(d // 16) + str(d % 16)
##
###setclock (BCD: sec,min,hour,weekday,day,mon,year)
##td = [0x00, 0x22, 0x18, 0x06, 0x16, 0x11, 0x19]
##bus.write_i2c_block_data(rtcAddr, 0, td)
##
##try:
##    while (True):
##        rd = bus.read_i2c_block_data(rtcAddr, 0, 7)
##        print (bcd2str(rd[4]) + '.' + bcd2str(rd[5]) + '.' + bcd2str(rd[6]) + \
##               '  ' + bcd2str(rd[2]) + ':' + bcd2str(rd[1]) + ':' + bcd2str(rd[0]))
##        sleep(1)
##except KeyboardInterrupt:
##    print("Keyboard interrupt by user")
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rambarun Komaljeet
# License: Freeware
# ---------------------------------------------------------------------------
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rambarun Komaljeet
# License: Freeware
# 
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rambarun Komaljeet
# License: LGPL
# ---------------------------------------------------------------------
import time
t1 ="01.01.2000"
t2 = "05.01.2000"


dat_t1 = time.strptime(t1, "%d.%m.%Y")
dat_t2 = time.strptime(t2, "%d.%m.%Y")

if dat_t2 > dat_t1:
    print ("True")
else: print("False")



