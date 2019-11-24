#!/usr/bin/python
# coding=utf-8
# Soll_Ist.py
# Version 1.2

# checkt ob die Soll- mit den Ist-Werten übereinstimmen
def soll_gleich_ist(ca):
    
    for soll_ist in ca.values():
        if soll_ist[0] != soll_ist[1]:
            return False
    return True

# nach Aktion werden die Ist- auf die Sollwerte gesetzt

def ist_gleich_soll(ca):
    
    for soll_ist in ca.values():
        soll_ist[0] = soll_ist[1]
            
    
