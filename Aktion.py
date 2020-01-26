#!/usr/bin/python
# coding=utf-8
# Aktion.py
# Version 1.0
# nimmt Veränderungen an den Aktoren und am Bildschirem vor

    
# verändert das Erscheinungsbild auf dem Bildschirm
# entweder nach manueller oder nach sensorgetriggerter Veränderung (oder durch Zeitschaltung)
# nach Aktion werden die Ist- im KOntrollarray auf die Sollwerte gesetzt

import datetime
import Check_Center as Ch
import RPi.GPIO as GPIO
import time
import tkinter as Tk

def change_sensordaten(_screen, wa):

    # wa-Key und dazugehörige Labelnamen, sowie Feuchtigkeitscode als verschachtelter array.
    # Funktion eval führt Textstring als Code aus
    
    Erde = [["Erdfeuchte1",
            "_screen.flf.labelA_F1.config(bg = 'blue')",
                            "_screen.flf.labelA_F1.config(bg = 'lightblue')",
                            "_screen.flf.labelA_F1.config(bg = 'green')",
                            "_screen.flf.labelA_F1.config(bg = 'PaleVioletRed2')",
                            "_screen.flf.labelA_F1.config(bg = 'red')"],
            ["Erdfeuchte2","_screen.flf.labelA_F2.config(bg = 'blue')",
                            "_screen.flf.labelA_F2.config(bg = 'lightblue')",
                            "_screen.flf.labelA_F2.config(bg = 'green')",
                            "_screen.flf.labelA_F2.config(bg = 'PaleVioletRed2')",
                            "_screen.flf.labelA_F2.config(bg = 'red')"],
            ["Erdfeuchte3","_screen.flf.labelA_F3.config(bg = 'blue')",
                            "_screen.flf.labelA_F3.config(bg = 'lightblue')",
                            "_screen.flf.labelA_F3.config(bg = 'green')",
                            "_screen.flf.labelA_F3.config(bg = 'PaleVioletRed2')",
                            "_screen.flf.labelA_F3.config(bg = 'red')"],
            ["Erdfeuchte4","_screen.flf.labelA_F4.config(bg = 'blue')",
                            "_screen.flf.labelA_F4.config(bg = 'lightblue')",
                            "_screen.flf.labelA_F4.config(bg = 'green')",
                            "_screen.flf.labelA_F4.config(bg = 'PaleVioletRed2')",
                            "_screen.flf.labelA_F4.config(bg = 'red')"],
            ["Erdfeuchte5","_screen.flf.labelA_F5.config(bg = 'blue')",
                            "_screen.flf.labelA_F5.config(bg = 'lightblue')",
                            "_screen.flf.labelA_F5.config(bg = 'green')",
                            "_screen.flf.labelA_F5.config(bg = 'PaleVioletRed2')",
                            "_screen.flf.labelA_F5.config(bg = 'red')"],
            ["Erdfeuchte6","_screen.flf.labelA_F6.config(bg = 'blue')",
                            "_screen.flf.labelA_F6.config(bg = 'lightblue')",
                            "_screen.flf.labelA_F6.config(bg = 'green')",
                            "_screen.flf.labelA_F6.config(bg = 'PaleVioletRed2')",
                            "_screen.flf.labelA_F6.config(bg = 'red')"]]

            
    
    _screen.tlf.label_lo.config(text=str(wa["T_Luft_oben"]))
    _screen.tlf.label_lu.config(text= str(wa["T_Luft_unten"]))
    _screen.tlf.label_w1.config(text= str(wa["T_Wasser1"]))
    _screen.tlf.label_a.config(text= str(wa["T_aussen"]))
    _screen.slf.label_licht.config(text= str(wa["Luxwert_1"]))
    _screen.slf.label_a.config(text= str(wa["Sonnenaufgang"]))
    _screen.slf.label_u.config(text= str(wa["Sonnenuntergang"]))
    _screen.slf.labelvolt.config(text = str(wa["Volt"]))

    
    # Zahlenwerte von MCP3008 für Feuchte werden in Farbcodes umgewandelt:
    # Funktion eval führt Textstring aus Erde-Array als Code aus
    
    for i in range(0,6):
        if wa[Erde[i][0]] > 800:
            eval(Erde[i][5])
        elif wa[Erde[i][0]] > 650 and wa[Erde[i][0]] <= 800:
            eval(Erde[i][4])
        elif wa[Erde[i][0]] > 500 and wa[Erde[i][0]] <= 650:
            eval(Erde[i][3])
        elif wa[Erde[i][0]] > 350 and wa[Erde[i][0]] <= 500:
            eval(Erde[i][2])
        elif wa[Erde[i][0]] <= 350:
            eval(Erde[i][1])
    

def change_buttons(_screen , ca):
    # passt die Buttons an die Soll-Anforderung an:
    
    
    if ca['normaler CHOP-Circle'][1] == 0:
        _screen.wlf.Anzeige_CCN.configure(text = 'normaler CHOP\nCircle ist aus', bg = 'PaleVioletRed2')
        _screen.wlf.check_btn_CCN_an.configure(text = 'normalen CHOP\nCircle anschalten')
    if ca['normaler CHOP-Circle'][1] == 1:
        _screen.wlf.Anzeige_CCN.configure(text = 'normaler CHOP\nCircle ist an', bg = 'lightgreen')
        _screen.wlf.check_btn_CCN_an.configure(text = 'normalen CHOP\nCircle ausschalten')

    
    if ca['warmer CHOP-Circle'][1] == 0:
        _screen.wlf.Anzeige_CCW.configure(text = 'CHOP-Circle mit\nWarmluft ist aus', bg = 'PaleVioletRed2')
        _screen.wlf.check_btn_CCW_an.configure(text = 'CHOP-Circle mit\nWarmluft anschalten')
    if ca['warmer CHOP-Circle'][1] == 1:
        _screen.wlf.Anzeige_CCW.configure(text = 'CHOP-Circle mit\nWarmluft ist an', bg = 'lightgreen')
        _screen.wlf.check_btn_CCW_an.configure(text = 'CHOP-Circle mit\nWarmluft ausschalten')
 
    
    if ca["Hauptpumpe"][1] == 0:
        _screen.wlf.Anzeige_Pumpe.configure(text = "Pumpe ist aus", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_P_an.configure(text = "Pumpe anschalten")
    if ca["Hauptpumpe"][1] == 1:
        _screen.wlf.Anzeige_Pumpe.configure(text = "Pumpe ist an", bg = "lightgreen")
        _screen.wlf.check_btn_P_an.configure(text = "Pumpe ausschalten")

    if ca["Wasser auffüllen"][1] == 0:
        _screen.wlf.Anzeige_WA.configure(text = "Brunnenventil ist zu", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_WA_an.configure(text = "Wasser auffüllen")
    if ca["Wasser auffüllen"][1] == 1:
        _screen.wlf.Anzeige_WA.configure(text = "Brunnenventil ist auf", bg = "lightgreen")
        _screen.wlf.check_btn_WA_an.configure(text = "Brunnenventil schließen")

    if ca["Wasser ablassen"][1] == 0:
        _screen.wlf.Anzeige_WB.configure(text = "Verrieselung ist zu", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_WB_an.configure(text = "Wasser ablassen")
    if ca["Wasser ablassen"][1] == 1:
        _screen.wlf.Anzeige_WB.configure(text = "Verrieselung ist auf", bg = "lightgreen")
        _screen.wlf.check_btn_WB_an.configure(text = "Wasserablass Stop")
    
    
    if ca["Kühlung mit Bewässerung"][1] == 0:
        _screen.mlf.Anzeige_KUBEW.configure(text = "Kühlung mit\nBewässerung ist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_KUBEW_an.configure(text = "Kühlung mit\nBewässerung anschalten")
    if ca["Kühlung mit Bewässerung"][1] == 1:
        _screen.mlf.Anzeige_KUBEW.configure(text = "Kühlung mit\nBewässerung ist an", bg = "lightgreen")
        _screen.mlf.check_btn_KUBEW_an.configure(text = "Kühlung mit\nBewässerung ausschalten")

    
    if ca["Kühlung mit Verrieselung"][1] == 0:
        _screen.mlf.Anzeige_KURIE.configure(text = "Kühlung mit\nVerrieselung ist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_KURIE_an.configure(text = "Kühlung mit\nVerrieselung anschalten")
    if ca["Kühlung mit Verrieselung"][1] == 1:
        _screen.mlf.Anzeige_KURIE.configure(text = "Kühlung mit\nVerrieselung ist an", bg = "lightgreen")
        _screen.mlf.check_btn_KURIE_an.configure(text = "Kühlung mit\nVerrieselung ausschalten")

    if ca["Heizung"][1] == 0:
        _screen.mlf.Anzeige_LampFi.configure(text = "Heizung\nist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_Fi_an.configure(text = "Heizung\nanschalten")
    if ca["Heizung"][1] == 1:
        _screen.mlf.Anzeige_LampFi.configure(text = "Heizung\nist an", bg = "lightgreen")
        _screen.mlf.check_btn_Fi_an.configure(text = "Heizung\nausschalten")

    
    if ca["Fütterung"][1] == 0:
        _screen.mlf.Anzeige_Fue.configure(text = "Fütterung\nist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_Fue_an.configure(text = "Fütterung\nanschalten")
    if ca["Fütterung"][1] == 1:
        _screen.mlf.Anzeige_Fue.configure(text = "Fütterung\nist an", bg = "lightgreen")
        _screen.mlf.check_btn_Fue_an.configure(text = "Fütterung\nausschalten")

        
    if ca["WQ to FT"][1] == 0:
        _screen.plf.check_btn_WQFT_an.configure(text = "WQ to FT öffnen")
        _screen.plf.Anzeige_WQFT.configure(text = "WQ to FT ist zu", bg = "PaleVioletRed2")      
    if ca["WQ to FT"][1] == 1:
        _screen.plf.check_btn_WQFT_an.configure(text = "WQ to FT schließen")
        _screen.plf.Anzeige_WQFT.configure(text = "WQ to FT ist auf", bg = "lightgreen")

    if ca["WQ to VR"][1] == 0:
        _screen.plf.check_btn_WQVR_an.configure(text = "WQ to VR öffnen")
        _screen.plf.Anzeige_WQVR.configure(text = "WQ to VR ist zu", bg = "PaleVioletRed2")     
    if ca["WQ to VR"][1] == 1:
        _screen.plf.check_btn_WQVR_an.configure(text = "WQ to VR schließen")
        _screen.plf.Anzeige_WQVR.configure(text = "WQ to VR ist auf", bg = "lightgreen")


    if ca["ST to VR"][1] == 0:
        _screen.plf.check_btn_STVR_an.configure(text = "ST to VR öffnen")
        _screen.plf.Anzeige_STVR.configure(text = "ST to VR ist zu", bg = "PaleVioletRed2")       
    if ca["ST to VR"][1] == 1:
        _screen.plf.check_btn_STVR_an.configure(text = "ST to VR schließen")
        _screen.plf.Anzeige_STVR.configure(text = "ST to VR ist auf", bg = "lightgreen")

    if ca["ST to FT"][1] == 0:
        _screen.plf.check_btn_STFT_an.configure(text = "ST to FT öffnen")
        _screen.plf.Anzeige_STFT.configure(text = "ST to FT ist zu", bg = "PaleVioletRed2")      
    if ca["ST to FT"][1] == 1:
        _screen.plf.check_btn_STFT_an.configure(text = "ST to FT schließen")
        _screen.plf.Anzeige_STFT.configure(text = "ST to FT ist auf", bg = "lightgreen")

    if ca["ST to HB"][1] == 0:
        _screen.plf.check_btn_STHB_an.configure(text = "ST to HB öffnen")
        _screen.plf.Anzeige_STHB.configure(text = "ST to HB ist zu", bg = "PaleVioletRed2")       
    if ca["ST to HB"][1] == 1:
        _screen.plf.check_btn_STHB_an.configure(text = "ST to HB schließen")
        _screen.plf.Anzeige_STHB.configure(text = "ST to HB ist auf", bg = "lightgreen")

    if ca["LU to HP"][1] == 0:
        _screen.plf.check_btn_LUHP_an.configure(text = "LU to HP öffnen")
        _screen.plf.Anzeige_LUHP.configure(text = "LU to HP\nist zu", bg = "PaleVioletRed2")       
    if ca["LU to HP"][1] == 1:
        _screen.plf.check_btn_LUHP_an.configure(text = "LU to HP schließen")
        _screen.plf.Anzeige_LUHP.configure(text = "LU to HP\nist auf", bg = "lightgreen")

    if ca["LO to HP"][1] == 0:
        _screen.plf.check_btn_LOHP_an.configure(text = "LO to HP öffnen")
        _screen.plf.Anzeige_LOHP.configure(text = "LO to HP\nist zu", bg = "PaleVioletRed2")       
    if ca["LO to HP"][1] == 1:
        _screen.plf.check_btn_LOHP_an.configure(text = "LO to HP schließen")
        _screen.plf.Anzeige_LOHP.configure(text = "LO to HP\nist auf", bg = "lightgreen")
        
    if ca["Logeintrag"][1] == 0:
        _screen.mlf.Anzeige_Log.configure(text = "Log hat keinen\nneuen Eintrag", bg = "lightgrey")
    if ca["Logeintrag"][1] == 1:
        _screen.mlf.Anzeige_Log.configure(text = "Logdatei hat\nneuen Eintrag", bg = "lightblue")
        

    if ca["Screen_schreiben"][1] == 0:
        _screen.click_screen.configure(text = "Bildschirmwerte an")
    if ca["Screen_schreiben"][1] == 1:
        _screen.click_screen.configure(text = "Bildschirmwerte aus")


    
    
def Fuetterung(jetzt, my_arr, vorg, _screen):
    
    fh= vorg["Fuetterung"][:2]
    fm = vorg["Fuetterung"][3:len(vorg["Fuetterung"])]
    fue_str = vorg["Fuetterung"]
    fue_zeit = datetime.datetime.strptime(fue_str, '%H:%M').time()
    fue_stopp_string  = fh + ":" + str(int(fm)+int(vorg["Fuett.dauer"]))
    fue_stopp = datetime.datetime.strptime(fue_stopp_string, '%H:%M').time()
    
    if jetzt.time() > fue_zeit and jetzt.time() <= fue_stopp:
        
       Ch.Alles_aus(_screen, my_arr)  
       my_arr["Fütterung"][1] = 1
    else:
       my_arr["Fütterung"][1] = 0

def Vorlauf(v_screen, my_array):
    from tkinter import messagebox
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    WQtoFT = 23           
    WQtoVR = 24

    GPIO.setup(WQtoFT, GPIO.OUT)
    GPIO.setup(WQtoVR, GPIO.OUT)

    GPIO.output(WQtoFT, GPIO.HIGH)
    GPIO.output(WQtoVR, GPIO.LOW)


    win = Tk.Toplevel()
    win.transient()
    
    win.title('Wait')
    win.geometry("280x100+500+300")
    Tk.Label(win, text="Brunnenwasser wird zur Abkühlung\neine Minute verrieselt").grid(ipady = 35, ipadx =30)

    
    
    win.after(15000, win.quit)
    win.mainloop()
    
    GPIO.output(WQtoFT, GPIO.HIGH)
    GPIO.output(WQtoVR, GPIO.HIGH)

    win.destroy()
    
    
def change_aktoren(my_screen, my_array):
    
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # verschachtelte Liste ordnet GPIO zu
        
    a_liste = [ ["Hauptpumpe", 18],            
                ["WQ to FT",   23],             
                ["WQ to VR",   24],             
                ["ST to VR",   25],             
                ["ST to FT",   12],              
                ["ST to HB",   16],              
                ["LU to HP",   20],              
                ["LO to HP",   21],
                ["Fütterung",  22],
                ["Heizung",    19]]
##"""                                     (1. Relais-Board)
##  a_liste = [ ["Hauptpumpe",   18],       1           
##                ["WQ to FT",   23],       2     
##                ["WQ to VR",   24],       3     
##                ["ST to VR",   25],       4     
##                ["ST to FT",   12],       5      
##                ["ST to HB",   16],       6      
##                ["LU to HP",   20],       7      
##                ["LO to HP",   21],       8
##                ["Fütterung",  22],       1 (2. Relais-Board)
##                ["Heizung",    19]]
##
##"""    
    for i in range(0, len(a_liste)):
        
        GPIO.setup(a_liste[i][1] , GPIO.OUT)


    for key in my_array:
        
        for i in range(0, len(a_liste)):
            if key == a_liste[i][0]:
                
                if my_array[key][1] == 1:
                    if key == "WQ to FT":
                        Vorlauf(my_screen, my_array)    # Vorlauf eine Minute, damit das Wasser abkühlt
                        
                    GPIO.output(a_liste[i][1],GPIO.LOW)
                    
                elif  my_array[key][1] == 0:
                    GPIO.output(a_liste[i][1],GPIO.HIGH)
    
    GPIO.cleanup()
                    
    #------------------------------------------------------------------------------
 
    
