#!/usr/bin/python
# coding=utf-8
# Werte_auch_Screen_schreiben.py
# Version 1.2

##########################################################
#
# schreibt die Sensordaten von Temperatur-, Licht und später Ph- sowie andere auf den Bildschirm
#
import Kontrollfenster as Kf
import tkinter as Tk

def Werte_schreiben(Screen, my_array):

    None
             
##    label_t1w = Tk.Label(T_Frame, text = "    ", bg ="white")
##    label_t1w.grid(row = 0, column = 1, padx = 3, sticky =Tk.E+Tk.W)  # macht das Schtreibfeld sauber
##
##
##    label_t1s = Tk.Label(T_Frame, text = str(my_array["TempLuft"]), fg = "black", bg = "white") # schreibt Temperaturwert
##    label_t1s.grid(row=0, column = 1, padx = 13, pady = 13, sticky = Tk.W + Tk.E )
##
##    label_t2w = Tk.Label(T_Frame, text = "    ", bg ="white")
##    label_t2w.grid(row = 1, column = 1, padx = 3, sticky =Tk.E+Tk.W)  # macht das Schtreibfeld sauber
##
##
##    label_t2s = Tk.Label(T_Frame, text = str(my_array["TempWasser"]), fg = "black", bg = "white") # schreibt Temperaturwert
##    label_t2s.grid(row=1, column = 1, padx = 13, pady = 13, sticky = Tk.W + Tk.E )
##
##
##    
##    Lux_Wert_String = str('%5.1f' % float(my_array["Luxwert_1"]))
##
##    label_licht_Wert = Tk.Label(L_Frame, text = "            ", bg ="white")
##    label_licht_Wert.grid(row = 0, column = 1, padx = 3, sticky =Tk.E+Tk.W)     # macht das Schtreibfeld sauber
##
##
##    label_licht_Wert = Tk.Label(L_Frame, text = Lux_Wert_String, bg = "white")
##    label_licht_Wert.grid(row=0, column = 1)
##                      
##    
