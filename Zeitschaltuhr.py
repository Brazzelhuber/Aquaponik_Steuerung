#!/usr/bin/python3.5
# coding=utf-8
# zeitschaltuhr.py

import datetime
import time
import threading
import sys
import random

def timecontrol(stop_event, conar, zeiten, q1, q2):
    
    while not stop_event.wait(1):
        
        q1.put(conar)
        q2.put(zeiten)    
        t2 = datetime.datetime.now()


# Blumenwiese       
        blu1 = datetime.datetime.strptime(zeiten["Blumenwiese_Anfang"],"%H:%M").time()
        blu2 = datetime.datetime.strptime(zeiten["Blumenwiese_Ende"], "%H:%M").time()
        blu1 = datetime.datetime.combine(t2,blu1)
        blu2 = datetime.datetime.combine(t2,blu2)

        if t2 >= blu1 and t2<blu2:
            conar["Bewässerung"][1] = 1
        else:
            conar["Bewässerung"][1] = 0

# Fütterung      
        fuz1 = datetime.datetime.strptime(zeiten["Fuetterung_Anfang"],"%H:%M").time()
        fuz2 = datetime.datetime.strptime(zeiten["Fuetterung_Ende"], "%H:%M").time()
        fuz1 = datetime.datetime.combine(t2,fuz1)
        fuz2 = datetime.datetime.combine(t2,fuz2)

        if t2 >= fuz1 and t2<fuz2:
            conar["Fütterung"][1] = 1
        else:
            conar["Fütterung"][1] = 0

# Beleuchtung     
        bel1 = datetime.datetime.strptime(zeiten["Beleuchtung_Anfang"],"%H:%M").time()
        bel2 = datetime.datetime.strptime(zeiten["Beleuchtung_Ende"], "%H:%M").time()
        bel1 = datetime.datetime.combine(t2,bel1)
        bel2 = datetime.datetime.combine(t2,bel2)

        if t2 >= bel1 and t2<bel2:
            conar["Beleuchtung"][1] = 1
        else:
            conar["Beleuchtung"][1] = 0
            

    
   
    sys.exit()
