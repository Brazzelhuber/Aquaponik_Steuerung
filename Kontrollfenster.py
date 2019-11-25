#!/usr/bin/python
# coding=utf-8
# Kontrollfenster.py
# Aufgabe: Aufbau des Kontrollfensters
# Version 1.2
#######################################################################
#
# Das Programm baut das Kontrollfenster auf, mit dem das ganze System bedient wird
#
#######################################################################
from __future__ import division, print_function
import pygame, pygame.gfxdraw       # pygame ist eigentlich für Spieleentwicklung. \
                                        # Aber auch geeigent um Grafikfenster zu steuern
from pygame.locals import *
import tkinter as Tk           # GUI-Bibliothek
from tkinter import messagebox
import csv, time, sys, os
import PIL
from PIL import Image, ImageTk
from smbus import SMBus


#####################
# eigene Module:
#import Lichtsteuerung as Ms
#import Wassersteuerung as Ws
import Werte_Zeichnen as Wz
import Check_Center as Ch
import Datepicker as Dp


# Höhe und Breite des Kontrollfensters
K_H = 768
K_B = 1366

##port = 1                # (0 for rev.1, 1 for rev 2!)
##bus = SMBus(port)
##rtcAddr = 0x68
##
##def bcd2str(d):         # // for integer division; % for modulo
##    if (d <= 9):
##        return '0' + str(d)
##    else:
##        return str(d // 16) + str(d % 16)

########################################################################
class Kontrollpanel(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent,  bg_Farbe, control_array):
        pygame.init()                   # initiert die pygame-Bibliothek

        
        """Constructor"""

        self.parent = parent
        parent.title("Aquaponik Kontrollpanel")
        parent.geometry('%dx%d+%d+%d' % (K_B, K_H,0,0))
        
        self.tlf= Tk.LabelFrame(text = "Temperatur/Stromverbrauch", \
                                        bd = 5, height =350, width =480, relief = "groove")
        
        self.tlf.grid_propagate(0)   # zwingt den Labelframe die vorgegebenen Maße zu benutzen


        self.mlf = Tk.LabelFrame(text = "Bewässerung - Kühlung - Heizung - Fütterung", \
                                        bd = 5, height =350, width =340, relief = "groove", )
        
        self.mlf.grid_propagate(0)


        self.slf= Tk.LabelFrame(text = "Licht", \
                                        bd = 5, height =250, width =480, relief = "groove", )
        
        self.slf.grid_propagate(0)


        self.wlf = Tk.LabelFrame(text = "Wasserfluß", \
                                        bd = 5, height =250, width =340, relief = "groove", )
       
        self.wlf.grid_propagate(0)


        self.qlf = Tk.LabelFrame(text = "Wasserqualität", \
                                        bd = 5, height =250, width =510, relief = "groove", )
        
        self.qlf.grid_propagate(0)

        
        self.plf = Tk.LabelFrame(text = "Ventileinzelsteuerung",\
                                       bd = 5, height =350, width =510, relief = "groove" )
       
        self.plf.grid_propagate(0)


        # positioniert die Labelframes auf dem Fenster
        
        self.tlf.grid(row = 1, column = 0, padx = 5, pady =5 ,sticky = Tk.W + Tk.N)
        self.mlf.grid(row = 1, column = 1, padx = 5, pady =5, sticky = Tk.W + Tk.N)
        self.slf.grid(row = 0, column = 0, padx = 5, pady =5, sticky = Tk.W + Tk.N)
        self.wlf.grid(row = 0, column = 1, padx = 5, pady =5, sticky = Tk.W + Tk.N)
        self.qlf.grid(row = 0, column = 2, padx = 5, pady =5, sticky = Tk.W + Tk.N)
        self.plf.grid(row = 1, column = 2, padx = 5, pady =5, sticky = Tk.W + Tk.N)
#########################################################################################
      

###########################################################################################
# Bildschirmwerte-Button:
        
        self.click_screen = Tk.Button ( text = "Bildschirmwerte aus")
        self.click_screen.grid(row = 3, column = 1,padx = 10, sticky = Tk.W)
        self.click_screen.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.click_screen,control_array, None))

###########################################################################################
# Abkürzungen:
        
        self.Abk0 = Tk.Label ( text = "  Abkürzungen:")
        self.Abk0.grid(row = 3, column = 1, sticky = Tk.E)
        self.Abk1 = Tk.Label ( text = "WQ = Wasserquelle | FT = Fischtank | VR = Verieselung | HB = Hochbeet")
        self.Abk1.grid(row = 3, column = 2, sticky = Tk.W)
        self.Abk2 = Tk.Label ( text = "ST = Sumptank | LU = Lufteinlass unten | LO = Lufteinlass oben" )
        self.Abk2.grid(row = 4, column = 2, sticky = Tk.W)

       ###########################################################################################
### Fischbild: lassen wir ertmal
##
##        canvas_width = 510
##        canvas_height = 290 
##
##        canvas = Tk.Canvas(self.plf, 
##                   width=canvas_width, 
##                   height=canvas_height)
##        canvas.grid()
##        
##        mysize =(canvas_width,canvas_height)
##        img = Image.open("tilapia.png")
##        img = img.resize(mysize, PIL.Image.ANTIALIAS)
##        canvas.image = ImageTk.PhotoImage(img)
##        canvas.create_image(0,0, anchor=Tk.NW, image=canvas.image)
####        
##    def Datenloeschen(event):
##        print("habe fertig")

############################################################################################
       # Temperatur Box
############################################################################################
        # Überschrift:
        
        label_T_U =Tk.Label(self.tlf, text = "Temperatur\n=========")
        label_T_U.configure(bg = bg_Farbe)
        label_T_U.grid(row = 0, column = 0, padx = 5, pady = 5, sticky =Tk.W)
        
        # Luft oben:
        ############
        
        # Beschriftung:
        label_T_lo =Tk.Label(self.tlf, text = "Luft oben:")
        label_T_lo.configure(bg = bg_Farbe)
        label_T_lo.grid(row = 1, column = 0, padx = 5, pady = 5, sticky =Tk.W)

        # Anzeige des Wertes:
        self.tlf.label_lo = Tk.Label(self.tlf, width = 4, height = 1, bg = "white", relief = "sunk")
        self.tlf.label_lo.grid(row=1, column = 1,  ipady = 4, sticky = Tk.W + Tk.E)

        # Pushbutton für Daten und Grafik:

        btn_T_lo_d = Tk.Button(self.tlf, text="Daten", \
                              command= lambda: self.Datenfenster(control_array,"T_Luft_oben"))
        btn_T_lo_d.grid(row = 1, column =2, padx = 5, pady = 5, ipadx = 7, sticky =Tk.E)

        btn_T_lo_g = Tk.Button(self.tlf, text="Grafik", \
                              command= lambda: self.Grafikfenster("T_Luft_oben"))
        btn_T_lo_g.grid(row = 1, column =3, padx = 5, pady = 5, ipadx = 17, sticky =Tk.W)

        # Luft unten:
        #############

        label_T_iu =Tk.Label(self.tlf, text = "Luft unten:")
        label_T_iu.configure(bg = bg_Farbe)
        label_T_iu.grid(row = 2, column = 0, padx = 5, pady = 5, sticky =Tk.W)

         # Anzeige des Wertes:
        self.tlf.label_lu = Tk.Label(self.tlf, width = 4, height = 1, bg = "white", relief = "sunk")
        self.tlf.label_lu.grid(row=2, column = 1,  ipady = 4, sticky = Tk.W + Tk.E)

        # Pushbutton für Daten und Grafik:

        btn_T_lu_d = Tk.Button(self.tlf, text="Daten", \
                              command= lambda: self.Datenfenster(control_array,"T_Luft_unten"))
        btn_T_lu_d.grid(row = 2, column =2, padx = 5, pady = 5, ipadx = 7, sticky =Tk.E)

        btn_T_lu_g = Tk.Button(self.tlf, text="Grafik", \
                              command= lambda: self.Grafikfenster("T_Luft_unten"))
        btn_T_lu_g.grid(row = 2, column =3, padx = 5, pady = 5, ipadx = 17, sticky =Tk.W)

        # Wasser Tank 1:
        #############
        
        label_T_w1 =Tk.Label(self.tlf, text = "Wasser Tank 1:")
        label_T_w1.grid(row = 3, column = 0, padx = 5, pady = 5, sticky =Tk.W)
        label_T_w1.configure(bg = bg_Farbe)
        
         # Anzeige des Wertes:
        self.tlf.label_w1 = Tk.Label(self.tlf, width = 4, height = 1, bg = "white", relief = "sunk")
        self.tlf.label_w1.grid(row=3, column = 1,  ipady = 4, sticky = Tk.W + Tk.E)

        # Pushbutton für Daten und Grafik:

        btn_T_w1_d = Tk.Button(self.tlf, text="Daten", \
                              command= lambda: self.Datenfenster(control_array,"T_Wasser1"))
        btn_T_w1_d.grid(row = 3, column =2, padx = 5, pady = 5, ipadx = 7, sticky =Tk.E)

        btn_T_w1_g = Tk.Button(self.tlf, text="Grafik", \
                              command= lambda: self.Grafikfenster("T_Wasser1"))
        btn_T_w1_g.grid(row = 3, column =3, padx = 5, pady = 5, ipadx = 17, sticky =Tk.W)



        # Wasser Tank 2:
        ################
        label_T_w2 =Tk.Label(self.tlf, text = "Wasser Tank 2:")
        label_T_w2.grid(row = 4, column = 0, padx = 5, pady = 5, sticky =Tk.W)
        label_T_w2.configure(bg = bg_Farbe)

          # Anzeige des Wertes:
        self.tlf.label_w2 = Tk.Label(self.tlf, width = 4, height = 1, bg = "white", relief = "sunk")
        self.tlf.label_w2.grid(row=4, column = 1,  ipady = 4, sticky = Tk.W + Tk.E)

        # Pushbutton für Daten und Grafik:

        btn_T_w2_d = Tk.Button(self.tlf, text="Daten", \
                              command= lambda: self.Datenfenster(control_array,"T_Wasser2"))
        btn_T_w2_d.grid(row = 4, column =2, padx = 5, pady = 5, ipadx = 7, sticky =Tk.E)

        btn_T_w2_g = Tk.Button(self.tlf, text="Grafik", \
                              command= lambda: self.Grafikfenster("T_Wasser2"))
        btn_T_w2_g.grid(row = 4, column =3, padx = 5, pady = 5, ipadx = 17, sticky =Tk.W)

        # außen:
        ############
        
        label_T_a =Tk.Label(self.tlf, text = "außen:")
        label_T_a.grid(row = 5, column = 0, padx = 5, pady = 5, sticky =Tk.W)
        label_T_a.configure(bg = bg_Farbe)

        # Anzeige des Wertes:
        self.tlf.label_a = Tk.Label(self.tlf, width = 4, height = 1, bg = "white", relief = "sunk")
        self.tlf.label_a.grid(row=5, column = 1,  ipady = 4, sticky = Tk.W + Tk.E)

        # Pushbutton für Daten und Grafik:

        btn_T_a_d = Tk.Button(self.tlf, text="Daten", \
                              command= lambda: self.Datenfenster(control_array,"T_außen"))
        btn_T_a_d.grid(row = 5, column =2, padx = 5, pady = 5, ipadx = 7, sticky =Tk.E)

        btn_T_a_g = Tk.Button(self.tlf, text="Grafik", \
                              command= lambda: self.Grafikfenster("T_außen"))
        btn_T_a_g.grid(row = 5, column =3, padx = 5, pady = 5, ipadx = 17, sticky =Tk.W)
        
##        Bild = Tk.PhotoImage(file="loeschen.bmp", master= self.tlf)
##        btn_T_a_l = Tk.Button(self.tlf, image = Bild)
##        btn_T_a_l.grid(row = 5, column =4, padx = 5, pady = 5, sticky =Tk.W)
        ### Fischbild: lassen wir ertmal

##        canvas_width = 25
##        canvas_height = 25
##
##        canvas = Tk.Canvas(self.tlf, 
##                   width=canvas_width, 
##                   height=canvas_height)
##        canvas.grid(row = 5, column =4, padx = 5, pady = 5, sticky =Tk.W)
##        
##        mysize =(canvas_width,canvas_height)
##        img = Image.open("loeschen.bmp")
##        img = img.resize(mysize, PIL.Image.ANTIALIAS)
##        canvas.image = ImageTk.PhotoImage(img)
##        blank = canvas.create_image(0,0, anchor=Tk.NW, image=canvas.image)
##        canvas.tag_bind(blank, "<Button-1>", self.Datenloeschen())
##        
        
         # Überschrift:
        
        label_T_U =Tk.Label(self.tlf, text = "Strom\n=========")
        label_T_U.configure(bg = bg_Farbe)
        label_T_U.grid(row = 6, column = 0, padx = 5, pady = 5, sticky =Tk.W)

         ########### Ladestrom

        self.tlf.label_Amp = Tk.Label(self.tlf,text = "Ladestrom:  " )
        self.tlf.label_Amp.grid(row=7, column = 0, padx = 5, pady = 15, sticky =Tk.W)
        self.tlf.label_Amp.configure(bg = bg_Farbe)

        self.tlf.labelamp = Tk.LabelFrame(self.tlf, width = 100, height = 25, bg = "white")
        self.tlf.labelamp.grid(row=7, column = 1 , sticky = Tk.W+Tk.E)

        btn_A_v= Tk.Button(self.tlf, text="Daten", \
                               command= lambda: self.Datenfenster(control_array,"Volt"))
        btn_A_v.grid(row = 7, column =2, padx = 5, pady = 5, ipadx = 7, sticky =Tk.W)

        btn_A_g = Tk.Button(self.tlf, text="Grafik", \
                                command= lambda: self.Grafikfenster("Volt"))
        btn_A_g.grid(row = 7, column =3, padx = 5, pady = 5, ipadx = 17, sticky =Tk.W)

###########################################################################################
        # Licht Box
###########################################################################################
        # Anzeige Sonnenaufgang und Untergang:

        label_auf = Tk.Label(self.slf,text = "Sonnenaufgang:" )
        label_auf.grid(row=0, column = 0, padx = 5, pady = 15, sticky =Tk.W)
        label_auf.configure(bg = bg_Farbe)

        self.slf.label_a = Tk.Label(self.slf, width = 10, height = 1, bg = "white", relief ="sunk")
        self.slf.label_a.grid(row=0, column = 1 , ipady = 4, sticky = Tk.W+Tk.E)

        
        label_unter = Tk.Label(self.slf,text = "Sonnenuntergang:" )
        label_unter.grid(row=0, column = 2, padx = 5, pady = 15, sticky =Tk.W)
        label_unter.configure(bg = bg_Farbe)

        self.slf.label_u = Tk.Label(self.slf, width = 10, height = 1, bg = "white", relief ="sunk")
        self.slf.label_u.grid(row=0, column = 3 , ipady = 4, sticky = Tk.W+Tk.E)

        
        ########## Lichtmessung
        label_licht = Tk.Label(self.slf,text = "Luxwert 1:     " )
        label_licht.grid(row=1, column = 0, padx = 5, pady = 15, sticky =Tk.W)
        label_licht.configure(bg = bg_Farbe)

        self.slf.label_licht = Tk.Label(self.slf, width = 10, height = 1, bg = "white", relief ="sunk")
        self.slf.label_licht.grid(row=1, column = 1 , ipady = 4, sticky = Tk.W+Tk.E)

        btn_Licht_v= Tk.Button(self.slf, text="Daten", \
                               command= lambda: self.Datenfenster(control_array,"Licht1"))
        btn_Licht_v.grid(row = 1, column =2, padx = 5, pady = 15, ipadx = 7, sticky =Tk.E)

        btn_Licht_g = Tk.Button(self.slf, text="Grafik", \
                                command= lambda: self.Grafikfenster("Licht1"))
        btn_Licht_g.grid(row = 1, column =3, padx = 5, pady = 15, ipadx = 17, sticky =Tk.W)
        

############################################################################################

        # Bewässerung - Kühlung - Heizung - Fütterung - Logdaten Box

############################################################################################

        
        self.mlf.check_btn_KUBEW_an = Tk.Button(self.mlf, text = "Kühlung mit\nBewässerung anschalten",  \
                                    relief = "groove", width = 18, height = 2 )
        self.mlf.check_btn_KUBEW_an.grid(row = 0, column =0, padx = 10, pady = 5 ,
                             ipady = 2,sticky =Tk.W+ Tk.E)
        self.mlf.check_btn_KUBEW_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.mlf.check_btn_KUBEW_an,control_array, None))

        self.mlf.Anzeige_KUBEW = Tk.Label(self.mlf, text = "Kühlung mit\nBewässerung ist aus",  \
                            relief = "groove", width = 16, height = 2 )
        self.mlf.Anzeige_KUBEW.grid(row = 0, column =1, padx = 0, pady = 3 ,
                             ipady = 6,sticky =Tk.W+ Tk.E)
        
       

        self.mlf.check_btn_KURIE_an = Tk.Button(self.mlf, text = "Kühlung mit\nVerieselung anschalten", \
                            relief = "groove", width = 18, height = 2)
        self.mlf.check_btn_KURIE_an.grid(row = 1, column =0, padx = 10, pady = 5 ,
                             ipady = 2, sticky =Tk.W+Tk.E)
        self.mlf.check_btn_KURIE_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.mlf.check_btn_KURIE_an,control_array, None))
        self.mlf.Anzeige_KURIE = Tk.Label(self.mlf, text = "Kühlung mit\nVerieselung ist aus",  \
                            relief = "groove", width = 16, height = 2 )
        self.mlf.Anzeige_KURIE.grid(row = 1, column =1, padx = 0, pady = 3 ,
                             ipady = 6,sticky =Tk.W+ Tk.E)

        self.mlf.check_btn_Fi_an = Tk.Button(self.mlf, text = "Heizung\nanschalten", \
                            relief = "groove", width = 18, height = 2 )
        self.mlf.check_btn_Fi_an.grid(row = 2, column =0, padx = 10, pady = 5 ,
                             ipady = 2, sticky =Tk.W+Tk.E)
        self.mlf.check_btn_Fi_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.mlf.check_btn_Fi_an,control_array, None))
        
        self.mlf.Anzeige_LampFi = Tk.Label(self.mlf, text = "Heizung\nist aus",  \
                            relief = "groove", width = 16, height = 2 )
        self.mlf.Anzeige_LampFi.grid(row = 2, column =1, padx = 0, pady = 3 ,
                             ipady = 6,sticky =Tk.W+ Tk.E)


        self.mlf.check_btn_Fue_an = Tk.Button(self.mlf, text = "Fütterung\nanschalten", \
                            relief = "groove", width = 18, height = 2 )
        self.mlf.check_btn_Fue_an.grid(row = 3, column =0, padx = 10, pady = 5 ,
                             ipady = 2, sticky =Tk.W+Tk.E)
        self.mlf.check_btn_Fue_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.mlf.check_btn_Fue_an,control_array, None))
        
        self.mlf.Anzeige_Fue = Tk.Label(self.mlf, text = "Fütterung\nist aus",  \
                            relief = "groove", width = 16, height = 2 )
        self.mlf.Anzeige_Fue.grid(row = 3, column =1, padx = 0, pady = 3 ,
                             ipady = 6,sticky =Tk.W+ Tk.E)

        self.mlf.check_btn_Log_auf = Tk.Button(self.mlf, text = "Logdatei\nöffnen", \
                            command = lambda: self.Datenfenster(control_array,"Logdatei") ,\
                            relief = "groove", width = 18, height = 2 )
        self.mlf.check_btn_Log_auf.grid(row = 4, column =0, padx = 10, pady = 5 ,
                             ipady = 2, sticky =Tk.W+Tk.E)
        
        self.mlf.Anzeige_Log = Tk.Label(self.mlf, text = "Log hat keinen\nneuen Eintrag",  \
                            relief = "groove", width = 16, height = 2 )
        self.mlf.Anzeige_Log.grid(row = 4, column =1, padx = 0, pady = 3 ,
                             ipady = 6,sticky =Tk.W+ Tk.E)




#############################################################################################

        # Wasserfluß Box
        ############################
        #normaler CHOP-Circle

        self.wlf.check_btn_CCN_an = Tk.Button(self.wlf, text = "normalen CHOP\nCircle anschalten",  \
                                    relief = "groove", width = 16, height = 2 )
        self.wlf.check_btn_CCN_an.grid(row = 0, column =0, padx = 10, pady = 3 , \
                             ipady = 3,sticky =Tk.W+ Tk.E)
        self.wlf.check_btn_CCN_an.bind("<Button-1>", lambda event,\
                             var=control_array: Ch.ButtonCheck(self.wlf.check_btn_CCN_an,control_array, None))

        self.wlf.Anzeige_CCN = Tk.Label(self.wlf, text = "normaler CHOP\nCircle ist aus",  \
                            relief = "groove", width = 16, height = 2 )
        self.wlf.Anzeige_CCN.grid(row = 0, column =1, padx = 10, pady = 3 ,\
                             ipady = 3,sticky =Tk.W+ Tk.E)


        #CHOP-Circle mit Wärmetauscher (zieht die warme Luft unterm Dach an)

        self.wlf.check_btn_CCW_an = Tk.Button(self.wlf, text = "CHOP-Circle mit\nWarmluft anschalten",  \
                                    relief = "groove", width = 16, height = 2 )
        self.wlf.check_btn_CCW_an.grid(row = 1, column =0, padx = 10, pady = 3 , \
                             ipady = 3,sticky =Tk.W+ Tk.E)
        self.wlf.check_btn_CCW_an.bind("<Button-1>", lambda event,\
                             var=control_array: Ch.ButtonCheck(self.wlf.check_btn_CCW_an,control_array, None))

        self.wlf.Anzeige_CCW = Tk.Label(self.wlf, text = "CHOP-Circle mit\nWarmluft ist aus",  \
                            relief = "groove", width = 16, height = 2 )
        self.wlf.Anzeige_CCW.grid(row = 1, column =1, padx = 10, pady = 3 ,\
                             ipady = 3,sticky =Tk.W+ Tk.E)
        ######################################################
        # Hauptpumpe
        
        self.wlf.check_btn_P_an = Tk.Button(self.wlf, text = "Pumpe anschalten", \
                            relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.wlf.check_btn_P_an.grid(row = 2, column =0, padx = 12, pady = 3 ,
                            ipady =3,  sticky =Tk.W+ Tk.E)
        self.wlf.check_btn_P_an.bind("<Button-1>", lambda event,
                            var=control_array: Ch.ButtonCheck(self.wlf.check_btn_P_an,control_array, None))
        self.wlf.Anzeige_Pumpe = Tk.Label(self.wlf, text = "Pumpe ist aus",  \
                            relief = "groove", width = 16, height = 1 )
        self.wlf.Anzeige_Pumpe.grid(row = 2, column =1, padx = 10, pady = 3 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
        # Wasser auffüllen:

        self.wlf.check_btn_WA_an = Tk.Button(self.wlf, text = "Wasser auffüllen", \
                            relief = "groove", width = 16, height = 1 )
        self.wlf.check_btn_WA_an.grid(row = 3, column =0, padx = 10, pady = 3 ,
                             ipady = 3, sticky =Tk.W+Tk.E)
        self.wlf.check_btn_WA_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.wlf.check_btn_WA_an,control_array, None))
        
        self.wlf.Anzeige_WA = Tk.Label(self.wlf, text = "Brunnenventil ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.wlf.Anzeige_WA.grid(row = 3, column =1, padx = 10, pady = 3 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
         # Wasser ablassen:

        self.wlf.check_btn_WB_an = Tk.Button(self.wlf, text = "Wasser ablassen", \
                            relief = "groove", width = 16, height = 1 )
        self.wlf.check_btn_WB_an.grid(row = 4, column =0, padx = 10, pady = 3 ,
                             ipady = 3, sticky =Tk.W+Tk.E)
        self.wlf.check_btn_WB_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.wlf.check_btn_WB_an,control_array, None))
        
        self.wlf.Anzeige_WB = Tk.Label(self.wlf, text = "Verieselung ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.wlf.Anzeige_WB.grid(row = 4, column =1, padx = 10, pady = 3 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)

       

        
##############################################################################################
        #Wasserqualität
    
        label_Ph = Tk.Label(self.qlf,text = "Ph-Wert:" )
        label_Ph.grid(row=0, column = 0, padx = 5, pady = 15, sticky =Tk.W)
        label_Ph.configure(bg = bg_Farbe)

        self.qlf.labelpl = Tk.LabelFrame(self.qlf, width = 50, height = 25, bg = "white")
        self.qlf.labelpl.grid(row=0, column = 1 , sticky = Tk.W+Tk.E)

        btn_Ph_v= Tk.Button(self.qlf, text="Daten", \
                               command= lambda: self.Datenfenster(control_array,"Ph"))
        btn_Ph_v.grid(row = 0, column =2, padx = 5, pady = 15, ipadx = 7, sticky =Tk.W)

        btn_Ph_g = Tk.Button(self.qlf, text="Grafik", \
                                command= lambda: self.Grafikfenster("Ph"))
        btn_Ph_g.grid(row = 0, column =3, padx = 5, pady = 15, ipadx = 17, sticky =Tk.W)

        self.qlf.label_O = Tk.Label(self.qlf,text = "O2-Wert:" )
        self.qlf.label_O.grid(row=1, column = 0, padx = 5, pady = 15, sticky =Tk.W)
        self.qlf.label_O.configure(bg = bg_Farbe)

        self.qlf.labelo = Tk.LabelFrame(self.qlf, width = 50, height = 25, bg = "white")
        self.qlf.labelo.grid(row=1, column = 1 , sticky = Tk.W+Tk.E)

        btn_O= Tk.Button(self.qlf, text="Daten", \
                               command= lambda: self.Datenfenster(control_array,"O2"))
        btn_O.grid(row = 1, column =2, padx = 5, pady = 15, ipadx = 7, sticky =Tk.W)

        btn_O_g = Tk.Button(self.qlf, text="Grafik", \
                                command= lambda: self.Grafikfenster("O2"))
        btn_O_g.grid(row = 1, column =3, padx = 5, pady = 15, ipadx = 17, sticky =Tk.W)

        self.qlf.check_btn_O_an = Tk.Button(self.qlf, text = "Sauerstoff\npumpe\nanschalten", \
                            relief = "groove", width = 10, height = 3 , anchor = Tk.W)
        self.qlf.check_btn_O_an.grid(row = 2, column =0, padx = 12, pady = 10 ,
                            ipady= 3,sticky =Tk.W+ Tk.E)
        self.qlf.check_btn_O_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.qlf.check_btn_O_an,control_array, None))
        self.qlf.Anzeige_O = Tk.Label(self.qlf, text = "Sauerstoff\npumpe\nist aus",  \
                            relief = "groove", width = 10, height = 3 )
        self.qlf.Anzeige_O.grid(row = 2, column =1, padx = 10, pady = 10 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)

        
###########################################################################################################
# Ventileinzelsteuerung:
        
        # Ventil, das Wasserquelle in den Fischtank leitet. Wird geöffnet, entweder um Wasserverlust zu kompensieren
        # oder um zu kühlen
     
        self.plf.check_btn_WQFT_an = Tk.Button(self.plf, text = "WQ to FT öffnen", \
                                relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_WQFT_an.grid(row = 0, column =0, padx = 12, pady = 5 ,
                            ipady =3, sticky =Tk.W+ Tk.E)
        self.plf.check_btn_WQFT_an.bind("<Button-1>", lambda event,
                            var=control_array: Ch.ButtonCheck(self.plf.check_btn_WQFT_an,control_array, None))
        self.plf.Anzeige_WQFT = Tk.Label(self.plf, text = "WQ to FT ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_WQFT.grid(row = 0, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
        
        self.plf.check_btn_STFT_an = Tk.Button(self.plf, text = "ST to FT öffnen", \
                                relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_STFT_an.grid(row = 1, column =0, padx = 12, pady = 5 ,
                            ipady =3, sticky =Tk.W+ Tk.E)
        self.plf.check_btn_STFT_an.bind("<Button-1>", lambda event,
                            var=control_array: Ch.ButtonCheck(self.plf.check_btn_STFT_an,control_array, None))
        self.plf.Anzeige_STFT = Tk.Label(self.plf, text = "ST to FT ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_STFT.grid(row = 1, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
        
        self.plf.check_btn_STHB_an = Tk.Button(self.plf, text = "ST to HB öffnen", \
                            relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_STHB_an.grid(row = 2, column =0, padx = 12, pady = 5 ,
                            ipady= 7,sticky =Tk.W+ Tk.E)
        self.plf.check_btn_STHB_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.plf.check_btn_STHB_an,control_array, None))
        self.plf.Anzeige_STHB = Tk.Label(self.plf, text = "ST to HB ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_STHB.grid(row = 2, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
        
        self.plf.check_btn_STVR_an = Tk.Button(self.plf, text = "ST to VR öffnen", \
                                relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_STVR_an.grid(row = 3, column =0, padx = 12, pady = 5 ,
                            ipady =3, sticky =Tk.W+ Tk.E)
        self.plf.check_btn_STVR_an.bind("<Button-1>", lambda event,
                            var=control_array: Ch.ButtonCheck(self.plf.check_btn_STVR_an,control_array, None))
        self.plf.Anzeige_STVR = Tk.Label(self.plf, text = "ST to VR ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_STVR.grid(row = 3, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)

        
        self.plf.check_btn_WQVR_an = Tk.Button(self.plf, text = "WQ to VR öffnen", \
                                relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_WQVR_an.grid(row = 4, column =0, padx = 12, pady = 5 ,
                            ipady =7, sticky =Tk.W+ Tk.E)
        self.plf.check_btn_WQVR_an.bind("<Button-1>", lambda event,
                            var=control_array: Ch.ButtonCheck(self.plf.check_btn_WQVR_an,control_array, None))
        self.plf.Anzeige_WQVR = Tk.Label(self.plf, text = "WQ to VR ist zu",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_WQVR.grid(row = 4, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
        


        ##        #####################################################
        # Luftventile
     
        self.plf.check_btn_LUHP_an = Tk.Button(self.plf, text = "LU to HP schließen", \
                                relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_LUHP_an.grid(row = 5, column =0, padx = 12, pady = 5 ,
                            ipady =3, sticky =Tk.W+ Tk.E)
        self.plf.check_btn_LUHP_an.bind("<Button-1>", lambda event,
                            var=control_array: Ch.ButtonCheck(self.plf.check_btn_LUHP_an,control_array, None))
        self.plf.Anzeige_LUHP = Tk.Label(self.plf, text = "LU to HP ist auf",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_LUHP.grid(row = 5, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)
        
        self.plf.check_btn_LOHP_an = Tk.Button(self.plf, text = "LO to HP schließen", \
                            relief = "groove", width = 16, height = 1 , anchor = Tk.W)
        self.plf.check_btn_LOHP_an.grid(row = 6, column =0, padx = 12, pady = 5 ,
                            ipady= 3,sticky =Tk.W+ Tk.E)
        self.plf.check_btn_LOHP_an.bind("<Button-1>", lambda event,
                             var=control_array: Ch.ButtonCheck(self.plf.check_btn_LOHP_an,control_array, None))
        self.plf.Anzeige_LOHP = Tk.Label(self.plf, text = "LO to HP ist auf",  \
                            relief = "groove", width = 16, height = 1 )
        self.plf.Anzeige_LOHP.grid(row = 6, column =1, padx = 10, pady = 5 ,
                             ipady = 7,sticky =Tk.W+ Tk.E)

    

################################################################################################################
    
       

##############################################################################################################        

         # Datenfenster wird als Kindfenster geöffnet, Grafik als Pygame-Fenster   

    def Datenfenster(self, ca, param):

        
        
        Kindfenster = Tk.Toplevel()
        if param == "Logdatei":
            Kindfenster.geometry("720x550+200+200")         # definiert Größe für Verlauffenster
            ca["Logeintrag"][1] = 0                   # setzt "Neuen Eintrag" wieder zurück
            
        else:
            #Kindfenster.geometry("270x550+825+265")         # definiert Größe für Verlauffenster
            Kindfenster.geometry("280x550+200+100")

##        if param == "T_außen":
##            Kindfenster.title("Daten Außentemperatur") # Titel
##            t = open('Tempdatenaussen.csv', 'r')         
##        elif param == "T_Luft_unten":
##            Kindfenster.title("Temperatur unten") # Titel
##            t = open('Tempdateninnen_unten.csv', 'r')             
##        elif param == "T_Luft_oben":
##            Kindfenster.title("Temperatur oben") # Titel
##            t = open('Tempdateninnen_oben.csv', 'r')             
##        elif param == "T_Wasser1":
##            Kindfenster.title("Temperatur Tank 1") # Titel
##            t = open('Tempdaten_Wasser1.csv', 'r')             
##        elif param == "T_Wasser2":
##            Kindfenster.title("Temperatur Tank 2") # Titel
##            t = open('Tempdaten_Wasser2.csv', 'r')             
##        elif param == "Licht1":
##            Kindfenster.title("Daten Luxwerte 1") # Titel
##            t = open('Lichtdaten1.csv', 'r')         
##        elif param == "Ph":
##            Kindfenster.title("Daten Ph-Werte") # Titel
##            t = open('Phwerte_Eichen.csv', 'r')     
##        elif param == "Logdatei":
##            Kindfenster.title("Logdatei") # Titel
##            t = open('Logdatei.csv', 'r')         
##        else:
##            print("kein gültiger Paramter übergeben")
        if param == "T_außen":
            Kindfenster.title("Daten Außentemperatur") # Titel
            dat_nam =('Tempdatenaussen.csv')         
        elif param == "T_Luft_unten":
            Kindfenster.title("Temperatur unten") # Titel
            dat_nam =('Tempdateninnen_unten.csv')             
        elif param == "T_Luft_oben":
            Kindfenster.title("Temperatur oben") # Titel
            dat_nam =('Tempdateninnen_oben.csv')             
        elif param == "T_Wasser1":
            Kindfenster.title("Temperatur Tank 1") # Titel
            dat_nam =('Tempdaten_Wasser1.csv')             
        elif param == "T_Wasser2":
            Kindfenster.title("Temperatur Tank 2") # Titel
            dat_nam =('Tempdaten_Wasser2.csv')             
        elif param == "Licht1":
            Kindfenster.title("Daten Luxwerte 1") # Titel
            dat_nam =('Lichtdaten1.csv')         
        elif param == "Ph":
            Kindfenster.title("Daten Ph-Werte") # Titel
            dat_nam =('Phwerte_Eichen.csv')     
        elif param == "Logdatei":
            Kindfenster.title("Logdatei") # Titel
            dat_nam =('Logdatei.csv')         
        else:
            print("kein gültiger Paramter übergeben")


        
        def center(win):                                # zentriert das Datenfenster 
            win.update_idletasks()
            width = win.winfo_width()
            height = win.winfo_height()
            x = (win.winfo_screenwidth() // 2) - (width // 2)
            y = (win.winfo_screenheight() // 2) - (height // 2)
            win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


        def Schluss(window):
            window.destroy()

##            
##        def tatsaechlich_loeschen(Lwindow, Kindfen):
##            #del_text = Lwindow.get([0] + my_list[1]+my_list[2] + "löschen?"
##            my_list = Lwindow.get()
##            Tag = my_list[0]
##            Monat = my_list[1]
##            Jahr = my_list[2]
##            del_text = "Daten, älter als " + Tag + "." + Monat +"." + Jahr + " wirklich löschen?"
##            Kindfen.withdraw()
##            result = messagebox.askokcancel( "Warnung",del_text)
##            print(result)

        def welches_Datum(ee, Datei):

            datepick = Dp.MyDatePicker(widget = ee)
           
             
        def print_it(mydate, Datei, Datumsfenster):
            
            del_text = "Daten, älter als " + mydate.get() + " in Datei " + Datei + " wirklich löschen?"
            result = messagebox.askokcancel( "Bitte bestätigen",del_text, parent = Datumsfenster)
            if result == True:
                myinput = open(dat_nam, 'r')
                output = open('first_edit.csv', 'w')
                writer = csv.writer(output)
                dat_loesch = time.strptime(mydate.get(), "%d.%m.%Y")
                for row in csv.reader(myinput):
                    row_string =(str(row[0]))
                    dat_string = row_string[0:10]
                    dat_incsv = time.strptime(dat_string, "%d.%m.%Y")
                    
                    if dat_incsv > dat_loesch:
                        writer.writerow(row)
                myinput.close()
                output.close()
                os.remove("/home/pi/Programme/Aquaponik_Steuerung/"+Datei)
                os.rename("/home/pi/Programme/Aquaponik_Steuerung/first_edit.csv", \
                          "/home/pi/Programme/Aquaponik_Steuerung/"+Datei)
        
            
        def Daten_loeschen(Datei):

            mydate = Tk.StringVar()
            Datumsfenster = Tk.Toplevel()
            Datumsfenster.geometry ("250x100+50+50")
            Datumsfenster.title("Datum zum Löschen")
           

            ed = Tk.Label(Datumsfenster,text = "Grenzdatum: ")
            ed.grid(row = 0, column = 0, padx = 5, pady = 5 ,ipady= 3, ipadx = 5, sticky = Tk.W)

            ee = Tk.Entry(Datumsfenster, textvariable = mydate)
            ee.grid(row = 0, column =1, padx = 5, pady = 5 )
            ee.config(width =9)
            mydate.trace("w", lambda name, index, mode, mydate=mydate: print_it(mydate, dat_nam, Datumsfenster))
            ee.bind("<Button-1>", lambda event: welches_Datum(ee, Datei))
            
    
        

        #center(Kindfenster)         
        Frame1 = Tk.Frame(Kindfenster)


        bb = Tk.Button(Frame1, text = "Beenden", command = lambda: Schluss(Kindfenster))
        bb.grid(row = 0, column = 0, padx =13, pady = 5, ipadx = 3, ipady =3)

        
        loeschen = Tk.Button(Frame1, text = "Daten löschen", command = lambda: Daten_loeschen("Test"))
        loeschen.grid(row = 0, column = 1, padx =13, pady = 5, ipadx = 3, ipady =3)
        Frame1.grid(sticky = Tk.W)
        

        Frame2 = Tk.Frame(Kindfenster) 

       

        # Erstellt die Listbox
        if param == "Logdatei":
            listbox = Tk.Listbox(Frame2, width=85, height=30)
        else:
            listbox = Tk.Listbox(Frame2, width=30, height=30)
        listbox.grid(row=1, column=0, padx = 5)

        # fügt die Scrollbar rechts an
        yscroll = Tk.Scrollbar(Frame2, command=listbox.yview, orient=Tk.VERTICAL, width = 20)
        yscroll.grid(row=1, column=1, sticky='ns')
        listbox.configure(yscrollcommand=yscroll.set)

        ##################################
        Frame2.grid(row = 2)
         
        

        # liest die Daten aus der jeweiligen CSV-Datei in eine Liste
        t = open (dat_nam, "r")
        cr = csv.reader(t)
       

        for line in cr:
            myline = str(line)
            datum = myline[2:12]
            Zeit = myline[13:18]
            Temp = myline[24:len(myline)]
            Temp = Temp.replace("'","")
            Temp = Temp.replace("]","")
            
            Wert = Temp
            
            listbox.insert("end",datum + "    " + Zeit + "    " + Wert)    # fügt die Werte in das Scrollfenster ein
        listbox.yview_moveto(1.0)
        t.close()

########################################################################################
# Grafikfenster:
            
    def Grafikfenster(self, param):
        Dateiname = ""               # wird durch Parameter bestimmt

        
        #Konstanten für pygame:
        WHITE = (255, 255, 255)
        RED   = (255,0,0)
        GREEN = (0,255,0)
        BLUE  = (0,0,255)
        BLACK = (0,0,0)
        
        # Breite und Höhe des Grafikfensters:
        # alle Werte in Pixel

        
        #(B , H) = (1200 , 800)
        (B , H) = (1000 , 600)
        

       
        if param == "T_außen":
            Dateiname ='Tempdatenaussen.csv'
        elif param == "T_Luft_unten":
            Dateiname = 'Tempdateninnen_unten.csv'            
        elif param == "T_Luft_oben":
            Dateiname = 'Tempdateninnen_oben.csv'             
        elif param == "T_Wasser1":
            Dateiname = 'Tempdaten_Wasser1.csv'
        elif param == "T_Wasser2":
            Dateiname = 'Tempdaten_Wasser2.csv'
            
        elif param == "Licht1":
            
            Dateiname = "Lichtdaten1.csv"
            
        elif param == "Phwerte":
            
            Dateiname = "Phwerte_Eichen.csv"
            

        else:
            print("kein gültiger Paramter übergeben")


        #######################################################
        # pygamefenster erzeugen #########################
        
        os.environ['SDL_VIDEO_CENTERED'] = "1"     # zentriert das Grafikfenster auf dem Bildschirm

##        pygame.init()                   # initiert die pygame-Bibliothek
        Grafikfenster = pygame.display.set_mode( (B , H ), 0, 32)

        Grafikfenster.fill(WHITE)
        

        ####################################################

        x= B
        y= H
        white         = (255,255,255)
        Button_Farbe  = (148,148,148)    # Gray48
        Button_Farbe2 = (179,179,179)    # Gray70
        Button_Blocked = (229,229,229)   # Gray90, wenn Botton geblocked ist

        Testfarbe     = (179,17,179)     # nur vorrübergehend
        Testfarbe1    = (0,0,139)
        Testfarbe2    = (0,0,205)
        Testfarbe3    = (16, 28, 209)
        
        global drawgrafic, allererst, ANZWERTE, pos , eof, bof, durch
        allererst = True        # wenn das Fenster zum ersten Mal geöffnet wird kommt 24-Stunden-Anzeige
        drawgrafic = True                                    # beim ersten Durchlauf der Enlosschleife (s.u.)
                                                        # wird das Schaubild gezeichnet, danach wird nur
                                                        # der Bereich der Buttons upgedated
                                                    

##                                                            # oder zurück zu gehen (z.B. 1 Woche vor/zurück)
        my_font = pygame.font.SysFont("Arial", 14 , bold=False, italic=False)
        
        ANZWERTE = 0    # wieviele Werte sollen eingelesen werden? wird unten festgelegt
        pos = 0         # Leseposition in der CSV-Datei
        eof = 1         # Ende of file (0 und 1, da pos, eof und bof in einer Liste von Werte_zeichnen zurück gegeben werden
        bof = 0         # begin of file
        durch = False   # sollen Einzel- oder Durchschnittswerte gezeigt werden (Woche und mehr geht nur mit Durchschnitt)


        def Grafik_Stunde ():
            global drawgrafic, ANZWERTE,pos, durch
            ANZWERTE =  10              # = 60/6 Minuten 
            drawgrafic = True           # nach einem Click wird die Grafik neu gezeichnet
            durch = False
        def Grafik_Tag():
            global drawgrafic, ANZWERTE, pos, durch
            ANZWERTE =    240            # =60/ 6 Minuten * 24
            drawgrafic = True
            durch = False
            
        def Grafik_Woche():
            global drawgrafic, ANZWERTE, durch
            ANZWERTE= 1680              #  funktioniert nur mit Durchschnittswerten
                                        # da Anzahl der Daten größer als Anzahl der Pixel auf x-Achse           
            drawgrafic = True
            durch = True                # soll Durchschnittswerte berechnen
            
        def Grafik_Vor():                                   # bewegt im jeweiligen Scope (Stunde ...) vor oder zurück
            global drawgrafic, ANZWERTE, pos, eof, bof
            if eof:
                return
            pos = pos + ANZWERTE
            drawgrafic = True
            
        def Grafik_Zurueck():
            global drawgrafic, ANZWERTE, pos, bof, eof
            if bof:
                return
            elif eof:
                eof = 0
            pos = pos - ANZWERTE
            drawgrafic = True
           
        def Grafik_DLI():
            
            global drawgrafic, ANZWERTE, durch
            ANZWERTE= 0                         # ist ein Trick, um in Werte_zeichnen DLI zu identifizieren                
            drawgrafic = True
            durch = False               
            
        def Aufhoeren():
            
            pygame.quit()
            sys.exit(1)

        def text_objects(text, font, color):
            
            textSurface = font.render(text, True, color)
            return textSurface, textSurface.get_rect()

        def Auswahl_Button(Grafikfenster, msg,x,y,w,h,c,ic,action):

            
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            pygame.draw.rect(Grafikfenster, c,(x,y,w,h))

            smallText = my_font
            textSurf, textRect = text_objects(msg, smallText, white)
            textRect.center = ( (x+(w/2)), (y+(h/2)) )
            Grafikfenster.blit(textSurf, textRect)

            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                pygame.draw.rect(Grafikfenster, ic,(x,y,w,h))
                if click[0] == 1 != None:
                    action()
                smallText = my_font
                textSurf, textRect = text_objects(msg, smallText, white)
                textRect.center = ( (x+(w/2)), (y+(h/2)) )
                Grafikfenster.blit(textSurf, textRect)




        alt_ANZWERTE = ANZWERTE    
        
        while 1:
            for event in pygame.event.get():
                
                Grafikfenster.fill(white)
                

                Auswahl_Button(Grafikfenster, "Beenden",B-110,H-50,100,40,Button_Farbe,Button_Farbe2,Aufhoeren)
                Auswahl_Button(Grafikfenster, "Stunde",B-220,H-50,100,40,Button_Farbe,Button_Farbe2,Grafik_Stunde)
                Auswahl_Button(Grafikfenster, "24 Stunden",B-330,H-50,100,40,Button_Farbe,Button_Farbe2,Grafik_Tag)
                Auswahl_Button(Grafikfenster, "Woche", B-440,H-50,100,40,Button_Farbe,Button_Farbe2,Grafik_Woche)
                # spezielle Grafik, die die Anzahl der photosynthetisch aktiven Photonen pro Tag und Fläche darstellt
                if "Licht" in param:
                    Auswahl_Button(Grafikfenster, "Day Light Integral",           
                                   B-570,H-50,120,40,Button_Farbe,Button_Farbe2,Grafik_DLI)
              
                if eof:    # wenn Leseposition bei neuesten Daten, geht es nicht weiter
                    Auswahl_Button(Grafikfenster, "Vor",10,H-50,100,40,Button_Blocked,Button_Blocked,Grafik_Vor)
                    
                else:
                    Auswahl_Button(Grafikfenster, "Vor",10,H-50,100,40,Button_Farbe,Button_Farbe2,Grafik_Vor)
                if bof:
                    Auswahl_Button(Grafikfenster, "Zurück",130,H-50,100,40,Button_Blocked,Button_Blocked,Grafik_Zurueck)
                else:
                    Auswahl_Button(Grafikfenster, "Zurück",130,H-50,100,40,Button_Farbe,Button_Farbe2,Grafik_Zurueck)

                if drawgrafic:
                    if alt_ANZWERTE != ANZWERTE:        
                        eof = 1
                    if allererst:
                        ANZWERTE = 10               # default bei Start: letzte Stunde
                        allererst = False           # setzt das Start-Boolean auf False

                    # übergibt an das Modul, das die Grafik zeichnet:

                    (pos, eof, bof) = Wz.Zeichne_Werte(Dateiname, Grafikfenster, H , B, ANZWERTE, pos, eof, bof, durch)
                   ####################################################################################################
                    pygame.display.update()    # updatet ganzes Fenster, um Grafik aufzubauen
                    drawgrafic = False
                   
                else:
                    pygame.display.update(5,H-50,B - 5,50)  # updated nur Region, wo Click-Buttons sind

                alt_ANZWERTE = ANZWERTE



 
    
        
#----------------------------------------------------------------------
    def onCloseKindfenster(self, Kindfenster):          
        """"""                                          
        Kindfenster.destroy()
        self.show()

        #----------------------------------------------------------------------
    def show(self):
        """"""
        self.fenster.update()
        self.fenster.deiconify()
###############################################################################################

##    
##class DateEntry(Tk.Frame):
##    def __init__(self, master, frame_look={}, **look):
##        args = dict(relief=Tk.SUNKEN, border=1)
##        args.update(frame_look)
##        Tk.Frame.__init__(self, master, **args)
##
##        args = {'relief': Tk.FLAT}
##        args.update(look)
##
##        self.entry_1 = Tk.Entry(self, width=2, **args)
##        self.label_1 = Tk.Label(self, text='/', **args)
##        self.entry_2 = Tk.Entry(self, width=2, **args)
##        self.label_2 = Tk.Label(self, text='/', **args)
##        self.entry_3 = Tk.Entry(self, width=4, **args)
##
##        self.entry_1.pack(side=Tk.LEFT)
##        self.label_1.pack(side=Tk.LEFT)
##        self.entry_2.pack(side=Tk.LEFT)
##        self.label_2.pack(side=Tk.LEFT)
##        self.entry_3.pack(side=Tk.LEFT)
##
##        self.entries = [self.entry_1, self.entry_2, self.entry_3]
##
##        self.entry_1.bind('<KeyRelease>', lambda e: self._check(0, 2))
##        self.entry_2.bind('<KeyRelease>', lambda e: self._check(1, 2))
##        self.entry_3.bind('<KeyRelease>', lambda e: self._check(2, 4))
##
##    def _backspace(self, entry):
##        cont = entry.get()
##        entry.delete(0, Tk.END)
##        entry.insert(0, cont[:-1])
##
##    def _check(self, index, size):
##        entry = self.entries[index]
##        next_index = index + 1
##        next_entry = self.entries[next_index] if next_index < len(self.entries) else None
##        data = entry.get()
##
##        if len(data) > size or not data.isdigit():
##            self._backspace(entry)
##        if len(data) >= size and next_entry:
##            next_entry.focus()
##
##    def get(self):
##        return [e.get() for e in self.entries]
