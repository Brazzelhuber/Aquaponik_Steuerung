#!/usr/bin/python3.5
#coding=utf-8
# Check_Center.py
# Version 1.0

########################################
# CheckCenter prüft, ob aufgrund der


# der Sensordaten und definierter Bedingungen

# oder eines Button-Drucks am Bildschirm

# etwas zu tun ist

# Zeitschaltung wird in dem parallel laufenden Thread in der Funktion timecontrol.py geprüft

#############################################


import re
import datetime as dt
import sunrise as sr
from tkinter import messagebox

# folgende beiden Arrays werden vom Hauptprogramm als Parameter übergeben
# Erläuterung: siehe README.md

# Vorgabewerte, können manuell über Screen geändert werden
##vw         =  {"TempWasserMin" : 3,         
##               "TempWasserMax" : 23,
##               "TempLuftMin"   : 3,         
##               "WasserpegelMin": 0,        
##               "WasserpegelMax": 0,
##               "PhWertMin"     : 6.7,
##               "PhWertMax"     : 7.1,
##               "Fuetterung"    : 10.00,
##               "Fuett.dauer"  : 5
##               }

# Sensorwerte:
##wa          = {"T_Luft_oben" : 0,      
##               "T_Luft_unten" : 0,     
##               "T_Wasser1": 0,         
##               "T_Wasser2": 0,          
##               "T_aussen": 0,           
##               "Luxwert_1" : 0 ,        
##               "Ph-Wert": 0 ,           
##               "Sauerstoff" : 0,        
##               "Volt"  :0 ,             
##               "Wasserstand" : 0,        
##               "Sonnenaufgang": 0,      
##               "Sonnenuntergang": 0,
##               "Erdfeuchte1" : 0,       
##               "Erdfeuchte2" : 0,       
##               "Erdfeuchte3" : 0,       
##               "Erdfeuchte4" : 0,
##               "Erdfeuchte5" : 0,
##               "Erdfeuchte6" : 0
##                }

## Kontrollarray
##ca          ={ "normaler CHOP-Circle":     [0,0,0],  # normaler Betrieb (FT -> GB -> ST ->FT) wobei Luft von unten
##               "Bewässerung":              [0,0,0],       # Bewässerung der Blumenwiese
##               "Kühlung mit Bewässerung":  [0,0,0],  
##               "Kühlung mit Verrieselung":  [0,0,0],
##               "Brunnenwasser als Heizung":[0,0,0],  # Brunnenwasser hat 15 Grad, kann auch zum "Heizen" eingesetzt werden
##               "Wasser auffüllen":         [0,0,0],  # Wasserverlust muss ausgeglichen werden
##               "Wasser ablassen":          [0,0,0],  # zuviel Wasser im System
##               "Hauptpumpe":               [0,0,0],
##               "Screen_schreiben":         [0,1,0],  # Sensorwerte auf Screen schreiben, kann im Dauerbetrieb abgestellt werden
##               "Heizung":                  [0,0,0],  # wenn es im Winter zu kalt wird
##               "Es ist Tag"      :         [0,0],    # kommt aus den Sonnendaten, Luxwerte werden nur tagsüber geschrieben
##               "Alarm"            :        [0,0],    # wenn was schiefgeht wird EMail geschrieben
##               "Fütterung"  :              [0,0,0],  # Fütterungsautomat einschalten?
##               "Logeintrag":               [0,0],
##               "WQ to FT":                 [0,0,0],  # die Wasserventile einzel
##               "WQ to VR":                 [0,0,0],
##               "ST to VR":                 [0,0,0],   
##               "ST to FT":                 [0,0,0],
##               "ST to HB":                 [0,0,0],
##               "LU to HP":                 [0,0,0],  # Luftventile
##               "LO to HP":                 [0,0,0]}  #  saugt Luft von unterm Dach in die airpumpo



def Ist_es_Tag(t1,t2,ca,wa):


    if (t2.time() > wa["Sonnenaufgang"]) and (t2.time() < wa["Sonnenuntergang"]):
        ca["Es ist Tag"][0] = 1
        ca["Es ist Tag"][1] = 1
            
    else:
        ca["Es ist Tag"][0] = 0
        ca["Es ist Tag"][1] = 0

##############################################################################################################
# das sind Devices, die bei komplexen Zustandsänderungen simultan geändert werden:

devices = ["WQ to FT",      # die devices werden durch die Liste bei Zustaende gesteuert
           "ST to FT",      
           "ST to HB",      #
           "ST to VR",
           "Hauptpumpe",
           "WQ to WI"]
# in Config_Zustaende wird durch devices und Zustände durchgegangen und die Sollwerte verändert
# 0 ist geschlossen, 1 ist offen, bzw. bei Hauptpumpe an und aus

Zustaende ={"normaler CHOP-Circle":              [0,1,0,0,1,0],   # CHOP (ST -> FT -> GB -> ST) wobei LU to HP on
            "Kühlung mit Bewässerung":           [1,0,1,0,1,0],   # WQ -> FT -> GB -> ST -> HB
            "Kühlung mit Verrieselung":          [1,0,0,1,1,0],   # WQ -> FT -> GB -> ST -> VR
            "Wasser ablassen":                   [0,0,0,1,1,0],   # pumpt Wasser aus dem ST nach draußen
            "Wasser auffüllen":                  [1,0,0,0,0,0],   # läßt frisches Wasser in das System
            "Fütterung":                         [0,0,0,0,0,0],   # bei Fütterung wird alles andere abgestellt
            "Nichts":                            [0,0,0,0,0,0]}   # Nichts auf oder an

# Zunächst eine Routine, die weitere Zustandsänderungen auslöst, wenn ein komplexer Vorgang auslöst wurde

def Config_Zustaende(Zustand, _array):
    
    print(Zustand)
    if Zustand == "Bewässerung" and _array["Bewässerung"][1] == 1:    # Bewässerung ist Sonderfall, 
        _array["WQ to WI"][1]= 1                                      # da parallel aktiv zu anderen Zuständen
        return                      # die if-clause öffnet das WQ to WI-Ventil parallel zu anderen Aktivitäten
                           
    for i in range(0,6):
        print(str(devices[i] )+ " = " + str(_array[devices[i]]))
        _array[devices[i]][1] = Zustaende[Zustand][i]   # setzt das Soll-Tag der devices auf die Werte in der
                                                        # entsprechenden Zeile von Zustaende
        
        

#########################################################################################################        
""" prüft, ob manuell, am Bildschirm etwas ausgelöst wurde (kann man, auch wenn es den Bedingungen in
Sensorcheck widerspricht)
"""

def Manualoverride(co):
    
    
    if co["normaler CHOP-Circle"][2] == 1 or co["Bewässerung"][2] == 1 or\
        co["Kühlung mit Bewässerung"][2] == 1 or co["Kühlung mit Verrieselung"][2]== 1 or\
        co["Wasser ablassen"][2] == 1 or co["Wasser auffüllen"][2]== 1 or co["Fütterung"][2] == 1:
        return True

    return False

# erst man alles auschalten, bevor im nächsten loop etwas Neues eingeschaltet wird:
def Alles_aus(myscreen, co):
    
    ButtonCheck(myscreen.mlf.check_btn_KUBEW_an,co, "Kühlung mit\nBewässerung ausschalten")  # simulierte Buttonpress
    ButtonCheck(myscreen.mlf.check_btn_KURIE_an,co, "Kühlung mit\nVerrieselung ausschalten")  # simulierte Buttonpress
    ButtonCheck(myscreen.wlf.check_btn_CCN_an,co, "normalen CHOP\nCircle ausschalten")  # simulierte Buttonpress
    ButtonCheck(myscreen.wlf.check_btn_WB_an,co, "Wasserablass Stop")  # simulierte Buttonpress
    ButtonCheck(myscreen.wlf.check_btn_WA_an,co, "Brunnenventil schließen")  # simulierte Buttonpress
    ButtonCheck(myscreen.wlf.check_btn_BLW_an,co, "Bewässerung\nBlumenwiese ausschalten")  # simulierte Buttonpress
    
########################################################################################################       
"""
SensorCheck() prüft, ob aufgrund von Sensordaten und Vorgabewerten eine Aktion auszulösen ist, wenn
ja wird der entsprechende Sollwert auf 1 gesetzt und in Aktion.py durchgeführt
"""
def SensorCheck(screen, co, we, vw):    # screen = screen_app, co = Controllarray, we = Wertearray
    
#######################################################################
    # checkt, ob Erde in Hochbeeten zu feucht ist zum Bewässern:
    
    feuchtwert = ( float(we["Erdfeuchte1"]) + \
                   float(we["Erdfeuchte2"]) + \
                   float(we["Erdfeuchte3"]) + \
                   float(we["Erdfeuchte4"]) + \
                   float(we["Erdfeuchte5"]) + \
                   float(we["Erdfeuchte6"])) /6
    
    if feuchtwert < 350 :
        zuvielErdfeuchte = True
    else:
        zuvielErdfeuchte = False
    
##"""       
##    
##bevor nicht alle Temperatursensoren installiert sind, werden T_Luft_unten und T_Luft oben ignoriert
###########################################
##Bedingungen für "normaler CHOP-Circle an":    1. "normaler CHOP-Circle" ist nicht schon an 
##                                              2. Wasser nicht zu warm und nicht zu kalt
##                                              3. kein manual override
##                                              4. keine Fütterung
##                                              5. kein Wasserablassen
   
    if co["normaler CHOP-Circle"][0] != 1 and float(we["T_Wasser1"]) <= float(vw["TempWasserMax"]) and \
            float(we["T_Wasser1"]) > float(vw["TempWasserMin"]) and not Manualoverride(co) and \
            co["Fütterung"][0] == 0 and co["Wasser ablassen"][0] == 0:
        
           
        Config_Zustaende("Nichts", co)
        Alles_aus(screen, co)
        co["normaler CHOP-Circle"][1] = 1
        ButtonCheck(screen.wlf.check_btn_CCN_an,co, "normalen CHOP\nCircle anschalten")  # simulierte Buttonpress

   
#################################################
##Bedingungen für "Kühlung mit Bewässerung an":     1. "Kühlung mit Bewässerung" ist nicht schon an
##                                                  2. Wasser ist zu warm
##                                                  3. kein manual override
##                                                  4. keine Fütterung
##                                                  5. Erde nicht zu feucht """
                                                      

    if (co["Kühlung mit Bewässerung"][0] != 1 ) and \
            float(we["T_Wasser1"]) > float(vw["TempWasserMax"]) and \
            not Manualoverride(co) and \
            zuvielErdfeuchte == False and \
            co["Fütterung"][0] == 0:

        Config_Zustaende("Nichts", co)
        Alles_aus(screen, co)
        co["Kühlung mit Bewässerung"][1] = 1
        
################################################
##Bedingungen für "Kühlung mit Verrieselung an":     1. "Kühlung mit Verieslung" ist nicht schon an
##                                                   2. Wasser ist zu warm
##                                                   3. kein manual override
##                                                   4. keine Fütterung
##                                                   5. Erde ist zu feucht """


    if co["Kühlung mit Verrieselung"][0] != 1 and float(we["T_Wasser1"]) > float(vw["TempWasserMax"]) and   \
       not Manualoverride(co) and zuvielErdfeuchte == True and co["Fütterung"][0] == 0:

       Config_Zustaende("Nichts", co)
       Alles_aus(screen, co)
       co["Kühlung mit Verrieselung"][1] = 1
       ButtonCheck(screen.mlf.check_btn_KURIE_an,co, "Kühlung mit\nVerrieselung anschalten")  # simulierte Buttonpress
       

##################################################
# Bedingungen für Wasser ablassen                       1. Wasser wir nicht schon abgelassen
#                                                       2. Abstand Wasserflächte Sumptank zu Ultraschallsensor < 5 cm
#                                                       3. kein manual override

    if co["Wasser ablassen"][0] != 1 and float(we["Wasserstand"]) < 5 and not Manualoverride(co):
                                               
       Config_Zustaende("Nichts", co)
       Alles_aus(screen, co)
       co["Wasser ablassen"][1] = 1
   
    if float(we["Wasserstand"]) >= 5 and float(we["Wasserstand"]) < 80:  # wenn Wasserstand im Normbereich
       co["Wasser ablassen"][1] = 0
         
        
# Wasserqualität:
    
    if we["Sauerstoff"] < 4.5 and False:        # Sauerstoff wird noch nicht gemessen
        co["Sauerstoffpumpe"][1] = 1
    if ((we["Ph-Wert"] < 6) or (we["Ph-Wert"] > 7)) and False:  # Ph-Wert wird noch nicht gemessen
        co["Alarm"][1] =1
        
    # Berechnet Sonnenauf- und -untergang:
    
    if we["Sonnenaufgang"] == 0:
        s= sr.sun(lat =51.755,long =8.6)
        we["Sonnenaufgang"] = s.sunrise(when=dt.datetime.now())
    if we["Sonnenuntergang"] == 0:
        s= sr.sun(lat =51.755,long =8.6)
        we["Sonnenuntergang"] = s.sunset(when=dt.datetime.now())

    return (co, we)
#########################################################################################################
# Vorbereitungen für Button-Check:

# Kontrolle, welcher Button gedrückt wurde, bzw. Buttonpress-Simulation für Sensor- oder zeitgetriggerte Aktionen sowie
# Vorbereitung der Aktionen, durch Veränderung des Sollwertes


############################################################################
# überprüft Status des manual override(mo) und reagiert entsprechend indem mo auf 1 oder 0 gesetzt wird
# gewährleistet, 1.dass nicht manuell etwas angestellt wird, während ein anderer Zustand aktiv ist
# und dass das was manuell angeschaltet wurde, auch manuell wieder ausgeschaltet  wird (bzw. umgekehrt)
# sonst würde der gewählte Zustand im nächsten loop evtl durch die Sensoren rückgängig gemacht
 

def ManualCheck(ar, manov, text, i):
    
    
    for key in Zustaende:
        
        if key != text and key != "Nichts" and  text != "Heizung" and ar[key][0] == 1 \
             and text != "Bewässerung" and manov == True and i <= 30:
            messagebox.showwarning("Warnung",key + " ist an\n\nbitte erst ausmachen, bevor\n\n" + \
                                text + "\n\n" + "gestartet werden kann")
            # Bewässerung und Heizung können manuell geschaltet werden parallel zu anderen Aktivitäten
            return False
        
    if manov and ar[text][0] == 1 and ar[text][2] == 0: # ist durch Sensor an, soll manuell abgeschaltet werden
        ar[text][2] = 1
    elif manov and ar[text][0] == 0 and ar[text][2] == 0: # ist durch Sensor aus, soll manuell angeschaltet werden
         ar[text][2] = 1
    elif manov and ar[text][0] == 1 and ar[text][2] == 1: # ist manuell angemacht, soll manuell ausgeschaltet werden
         ar[text][2] = 0
    elif manov and ar[text][0] == 0 and ar[text][2] == 1: # ist manuell ausgemacht, soll manuell angeschaltet werden
         ar[text][2] = 0
    
    return True
###########################################################################################    
def do_it(liste,ar, manov,i):
    
    listenkey = liste[i][1]
  
         
    if ManualCheck(ar, manov, liste[i][1], i) == True:
        
##        print("listenkey = " + listenkey)   
      
        ar[listenkey][1] = liste[i][2]          # setzt den ca-Key auf an oder aus
        if i <= 16 :                           # 1 - 16 sind komplexe Zustände, daher müssen in der Folge
            if liste[i][2] == 1 :                   # diverse andere Veränderungen (an Ventilen) vorgnommen werden
                Config_Zustaende(listenkey, ar)
            elif listenkey == "Bewässerung" and liste[i][2] == 0:
                ar["WQ to WI"][1] = 0
                return                              # sonst stellt die Beendigung der Bewässerung auch die Ventile
                                                    # des CHOP-Circles auf Null

            else: Config_Zustaende("Nichts",ar)

                                                                                 

##################################################################################
# ButtonCeck
##################################################################################
# in Kontrollpanel.py wird die Methode "bind" angewandt, damit hier identifiziert werden kann, welcher Button 
# gedrückt wurde. Direktes callback geht nicht, da sich der Text des Buttons ändern kann
# wird entweder aufgerufen, wenn ein Button gedrückt wurde, dann ist _button = None

# oder ButtonCheck kann aus anderen Modulen (Sensorgetriggert oder Zeitschaltung) aufgerufen werden,
# dann ist BUTTON = _button (simulierter Buttondruck, der Name des Buttons wird als String übergeben)

def ButtonCheck(butt,ar, _button):              # butt ist der Button, der gedrückt wurde, ar ist ca (Controlarray)
#
# Steuerung mit verschachtelter Liste, damit nicht endlos Code wiederholt werden muß

#                    Buttontext                             ca-Key               an/aus
#                    ##########                             ######               ######
    b_liste =[["normalen CHOP\nCircle anschalten",      "normaler CHOP-Circle",     1],
              ["normalen CHOP\nCircle ausschalten",     "normaler CHOP-Circle",     0],
              ["Bewässerung\nBlumenwiese anschalten",   "Bewässerung",              1],
              ["Bewässerung\nBlumenwiese ausschalten",  "Bewässerung",              0],
              ["Kühlung mit\nBewässerung anschalten",   "Kühlung mit Bewässerung",  1],
              ["Kühlung mit\nBewässerung ausschalten",  "Kühlung mit Bewässerung",  0],
              ["Kühlung mit\nVerrieselung anschalten",   "Kühlung mit Verrieselung",  1],
              ["Kühlung mit\nVerrieselung ausschalten",  "Kühlung mit Verrieselung",  0],
              ["Wasser ablassen",                       "Wasser ablassen",          1],
              ["Wasserablass Stop",                     "Wasser ablassen",          0],
              ["Pumpe anschalten",                      "Hauptpumpe",               1],
              ["Pumpe ausschalten",                     "Hauptpumpe",               0],
              ["Wasser auffüllen",                      "Wasser auffüllen",         1],
              ["Brunnenventil schließen",               "Wasser auffüllen",         0],
              ["Fütterung\nanschalten",                 "Fütterung",                1],
              ["Fütterung\nausschalten",                "Fütterung",                0],
              ["WQ to VR öffnen",                       "WQ to VR",                 1],
              ["WQ to VR schließen",                    "WQ to VR",                 0],
              ["WQ to FT öffnen",                       "WQ to FT",                 1],
              ["WQ to FT schließen",                    "WQ to FT",                 0],
              ["ST to VR öffnen",                       "ST to VR",                 1],
              ["ST to VR schließen",                    "ST to VR",                 0],
              ["ST to FT öffnen",                       "ST to FT",                 1],
              ["ST to FT schließen",                    "ST to FT",                 0],
              ["ST to HB öffnen",                       "ST to HB",                 1],
              ["ST to HB schließen",                    "ST to HB",                 0],
              ["LO to HP öffnen",                       "LO to HP",                 1],
              ["LO to HP schließen",                    "LO to HP",                 0],
              ["LU to HP öffnen",                       "LU to HP",                 1],
              ["LU to HP schließen",                    "LU to HP",                 0],
              ["Heizung\nanschalten",                   "Heizung",                  1],
              ["Heizung\nausschalten",                  "Heizung",                  0],
              ["Bildschirmwerte an",                    "Screen_schreiben",         1],
              ["Bildschirmwerte aus",                   "Screen_schreiben",         0]]
              
                                      
       
##    print ("Button = " + (str(_button)))
    
                        # manov = True bedeutet manual override, d.h. vom Bildschirm aus wird eine Aktion ausgelöst,
                                                # die evtl. den definierten Sensorbedingungen oder Zeitschaltung
                                                # widersprechen
                                                
    if _button == None:                         # butt.configure("text")[-1] gibt Buttontext
        BUTTON = butt.configure("text")[-1]     # aus Kontrolpanel.py zurück. Dort ist _button immer None
        manov = True                            # manov = True, da manuell ausgelöst
    else:
        BUTTON = _button                        # simuliert Buttonpress (Text des Buttons wird direkt über
        manov = False                           # Variable _button übergeben), um Sensor- oder zeitgetriggert
                                                # Aktion auszulösen
                                                # manual override trifft nicht zu
##    print ("BUTTON = "+ BUTTON)                               
                                                        
    
    for i in range(0,34):
        if BUTTON == b_liste[i][0]: do_it(b_liste,ar,manov,i)
    
    

