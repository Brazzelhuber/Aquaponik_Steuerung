#!/usr/bin/python
# coding=utf-8
# Aktion.py
# Version 1.0
# nimmt Veränderungen an den Aktoren und am Bildschirem vor

    
# verändert das Erscheinungsbild auf dem Bildschirm
# entweder nach manueller oder nach sensorgetriggerter Veränderung (oder durch Zeitschaltung)
# nach Aktion werden die Ist- im KOntrollarray auf die Sollwerte gesetzt

def change_sensordaten(_screen, wa):
    
    _screen.tlf.label_lo.config(text=str(wa["T_Luft_oben"]))
    _screen.tlf.label_lu.config(text= str(wa["T_Luft_unten"]))
    _screen.tlf.label_w1.config(text= str(wa["T_Wasser1"]))
    _screen.tlf.label_a.config(text= str(wa["T_aussen"]))
    _screen.slf.label_licht.config(text= str(wa["Luxwert_1"]))
    _screen.slf.label_a.config(text= str(wa["Sonnenaufgang"]))
    _screen.slf.label_u.config(text= str(wa["Sonnenuntergang"]))

def change_buttons(_screen , ca):
    
    
    if ca["normaler CHOP-Circle"][1] == 1:
        _screen.wlf.Anzeige_CCN.configure(text = "normaler CHOP\nCircle ist an", bg = "lightgreen")
        _screen.wlf.check_btn_CCN_an.configure(text = "normalen CHOP\nCircle ausschalten")
    if ca["normaler CHOP-Circle"][1] == 0:
        _screen.wlf.Anzeige_CCN.configure(text = "normaler CHOP\nCircle ist aus", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_CCN_an.configure(text = "normalen CHOP\nCircle anschalten")

    if ca["warmer CHOP-Circle"][1] == 1:
        _screen.wlf.Anzeige_CCW.configure(text = "CHOP-Circle mit\nWarmluft ist an", bg = "lightgreen")
        _screen.wlf.check_btn_CCW_an.configure(text = "CHOP-Circle mit\nWarmluft ausschalten")
    if ca["warmer CHOP-Circle"][1] == 0:
        _screen.wlf.Anzeige_CCW.configure(text = "CHOP-Circle mit\nWarmluft ist aus", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_CCW_an.configure(text = "CHOP-Circle mit\nWarmluft anschalten")
 
    if ca["Hauptpumpe"][1] == 1:
        _screen.wlf.Anzeige_Pumpe.configure(text = "Pumpe ist an", bg = "lightgreen")
        _screen.wlf.check_btn_P_an.configure(text = "Pumpe ausschalten")
    if ca["Hauptpumpe"][1] == 0:
        _screen.wlf.Anzeige_Pumpe.configure(text = "Pumpe ist aus", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_P_an.configure(text = "Pumpe anschalten")

    if ca["Wasser auffüllen"][1] == 0:
        _screen.wlf.Anzeige_WA.configure(text = "Brunnenventil ist zu", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_WA_an.configure(text = "Wasser auffüllen")
    if ca["Wasser auffüllen"][1] == 1:
        _screen.wlf.Anzeige_WA.configure(text = "Brunnenventil ist auf", bg = "lightgreen")
        _screen.wlf.check_btn_WA_an.configure(text = "Brunnenventil schließen")

    if ca["Wasser ablassen"][1] == 0:
        _screen.wlf.Anzeige_WB.configure(text = "Verieselung ist zu", bg = "PaleVioletRed2")
        _screen.wlf.check_btn_WB_an.configure(text = "Wasser ablassen")
    if ca["Wasser ablassen"][1] == 1:
        _screen.wlf.Anzeige_WB.configure(text = "Verieselung ist auf", bg = "lightgreen")
        _screen.wlf.check_btn_WB_an.configure(text = "Wasserablass Stop")
    
    if ca["Kühlung mit Bewässerung"][1] == 1:
        _screen.mlf.Anzeige_KUBEW.configure(text = "Kühlung mit\nBewässerung ist an", bg = "lightgreen")
        _screen.mlf.check_btn_KUBEW_an.configure(text = "Kühlung mit\nBewässerung ausschalten")
    if ca["Kühlung mit Bewässerung"][1] == 0:
        _screen.mlf.Anzeige_KUBEW.configure(text = "Kühlung mit\nBewässerung ist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_KUBEW_an.configure(text = "Kühlung mit\nBewässerung anschalten")

    if ca["Kühlung mit Verieselung"][1] == 1:
        _screen.mlf.Anzeige_KURIE.configure(text = "Kühlung mit\nVerieselung ist an", bg = "lightgreen")
        _screen.mlf.check_btn_KURIE_an.configure(text = "Kühlung mit\nVerieselung ausschalten")
    if ca["Kühlung mit Verieselung"][1] == 0:
        _screen.mlf.Anzeige_KURIE.configure(text = "Kühlung mit\nVerieselung ist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_KURIE_an.configure(text = "Kühlung mit\nVerieselung anschalten")

    if ca["Heizung"][1] == 0:
        _screen.mlf.Anzeige_LampFi.configure(text = "Heizung\nist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_Fi_an.configure(text = "Heizung\nanschalten")
    if ca["Heizung"][1] == 1:
        _screen.mlf.Anzeige_LampFi.configure(text = "Heizung\nist an", bg = "lightgreen")
        _screen.mlf.check_btn_Fi_an.configure(text = "Heizung\nausschalten")

    if ca["Fütterung"][1] == 1:
        _screen.mlf.Anzeige_Fue.configure(text = "Fütterung\nist an", bg = "lightgreen")
        _screen.mlf.check_btn_Fue_an.configure(text = "Fütterung\nausschalten")
    if ca["Fütterung"][1] == 0:
        _screen.mlf.Anzeige_Fue.configure(text = "Fütterung\nist aus", bg = "PaleVioletRed2")
        _screen.mlf.check_btn_Fue_an.configure(text = "Fütterung\nanschalten")

    if ca["Logeintrag"][1] == 1:
        _screen.mlf.Anzeige_Log.configure(text = "Logdatei hat\nneuen Eintrag", bg = "lightblue")
        
    if ca["Logeintrag"][1] == 0:
        _screen.mlf.Anzeige_Log.configure(text = "Log hat keinen\nneuen Eintrag", bg = "lightgrey")
        

    if ca["Screen_schreiben"][1] == 0:
        _screen.click_screen.configure(text = "Bildschirmwerte an")
    if ca["Screen_schreiben"][1] == 1:
        _screen.click_screen.configure(text = "Bildschirmwerte aus")
        
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

    
##    print("change_buttons: " + str(ca["warmer CHOP-Circle"][1]))
    
    
def change_aktoren(my_array):
    
    
    import RPi.GPIO as GPIO

    #------------------------------------------------------------------------------
    # GPIO settings für Relais Steuerung 

    GPIO.setmode(GPIO.BCM)

    Grow1_anschalt = GPIO.LOW       # Relais geht bei LOW an , daher umbenennen, um Verwirrung zu vermeiden
    Grow1_ausschalt = GPIO.HIGH

    GPIO.setwarnings(False)


    Grow1_AnAus_Relais = 27                     # BCM 27 schaltet?? an und aus
    #######################
    GPIO.setup(Grow1_AnAus_Relais, GPIO.OUT)


    Grow2_anschalt = GPIO.LOW       # Relais geht bei LOW an , daher umbenennen, um Verwirrung zu vermeiden
    Grow2_ausschalt = GPIO.HIGH

    GPIO.setwarnings(False)


    Grow2_AnAus_Relais = 22                     # BCM 22 schaltet ??  an und aus
    #######################
    GPIO.setup(Grow2_AnAus_Relais, GPIO.OUT)

## falscher Ansatz, hier müssen die Einzelventile gesteuert werden
    
##     
##    if my_array["Kühlung mit Bewässerung"][1] == 1:
##
##        GPIO.output(Grow1_AnAus_Relais, Grow1_anschalt)
##
##    if my_array["Kühlung mit Bewässerung"][1] == 0:
##        
##        GPIO.output(Grow1_AnAus_Relais, Grow1_ausschalt)
##       
##
##
##    if my_array["Kühlung mit Verieselung"][1] == 1:
##
##        GPIO.output(Grow2_AnAus_Relais, Grow2_anschalt)
##
##    if my_array["Kühlung mit Verieselung"][1] == 0:
##        
##        GPIO.output(Grow2_AnAus_Relais, Grow2_ausschalt)
##
