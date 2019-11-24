#!/usr/bin/python
# coding=utf-8
# FensterGrafik.py
# Version 1.0


import tkinter as Tk

def zeichneLabelFrames(fenster, myframes , bg):
    global myframes

    fenster.T_labelframe = Tk.LabelFrame(fenster,text = "Temperatur", \
                                bd = 5, height =300, width =200, relief = "groove")
    tlf = fenster.T_labelframe
    myframes[0] = tlf
    fenster.M_labelframe = Tk.LabelFrame(fenster,text = "Motor", \
                                bd = 5, height =300, width =200, relief = "groove")
    mlf = fenster.M_labelframe
    myframes[1] = mlf

    
        
