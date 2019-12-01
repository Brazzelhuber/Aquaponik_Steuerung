#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### interface_i2c_ds1307_1.py
##
#!/usr/bin/python
from myclassMcp3008 import MCP3008
#from myclassMcp3008 import Mcp3008


from time import sleep



#app = Flask(__name__)


mcp = MCP3008()
mcp.open()

while 1:
   
    regenwert = mcp.read(channel = 3)
    regenwert = float(regenwert)
    print (str(regenwert))
    sleep(1)


   





