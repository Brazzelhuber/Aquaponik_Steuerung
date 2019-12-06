#!/usr/bin/python
# coding=utf-8
# Werte_Zeichnen.py
# Aufgabe: Zeichnet die unterschiedlichen Datenwerte auf den Screen
# Version 1.2

from __future__ import division, print_function
import pygame, pygame.gfxdraw       # pygame ist eigentlich für Spieleentwicklung. \
                                        # Aber auch geeigent um Grafikfenster zu steuern
from pygame.locals import *
import tkinter as Tk           # GUI-Bibliothek
import csv

def Zeichne_Werte(dateiname, grafikwindow, hoehe,breite,anzahlwerte, pos, EOF, BOF, MINMAX, SYNC):

    if anzahlwerte == 0:             #kleiner Trick, um DLI zu identifizieren
        dateiname = "DLI_Eichen.csv"
        anzahlwerte = 11
    
     #Konstanten für pygame:
    WHITE = (255, 255, 255)
    RED   = (255,0,0)
    GREEN = (0,255,0)
    BLUE  = (0,0,255)
    BLACK = (0,0,0)
   
    
    # diverse Festlegungen für das Grafikfenster:

    (WMIN, WMAX) = (0, 50)      # Minimal und Maximalwerte, die angezeigt werden
                                    # ändert sich, je nach Art der Daten
    XEIN = 100                   # Einrückung für die x-Achse vom linken Rand
    YEIN = 200                   # Einrückung für die y-Achse vom unteren Rand
    
    (XOEIN , YOEIN) = (50,50)     # oben und rechts Bereiche, in denen nicht geplottet wird



    bespH = hoehe - YEIN -YOEIN      # Länge der Y-Achse (bespielbare Höhe)
    bespB = breite - XEIN -XOEIN      # Länge der X-Achse (bespielbare Breite)
    YEINTEIL = 11                # Anzahl der Einteilungen auf der Y-Achse (11, weil 0-Punkt mitzählt)
    


    BLACK  = (0,0,0)
    myfont = pygame.font.SysFont("freesans,ttf", 14)


####################################################################
    # Festlegung der Minimal- und Maximalwerte, je nach Art der Daten


    if "Temp" in dateiname:             # einzelne Sensordaten haben unterschiedliche Skalen
        #print(dateiname)
        if "innen" in dateiname or "Wasser" in dateiname:
            
            WMAX = 45                   # im Gewächshaus hoffentlich nie unter null
            WMIN= -5

        else:
            WMAX = 35
            WMIN = -15                # Temperaturextreme außen, die vorkommen können
    elif "Licht" in dateiname:
        WMAX = 100000
        WMIN = 0
    elif "Ph" in dateiname:
        WMAX = 9                        # ph-Wert
        WMIN = 4
    elif "Volt" in dateiname:           # Batteriespannung
        WMAX = 14
        WMIN = 11
    else: print("kein gültiger Dateiname")

###########################################################################################
    # Festlegung des Diagrammtitels
        
    Titel = ""
    if "Temp" in dateiname:
        Y_Delta = 5    # Delta von 5 Grad bei Temperaturen
        if SYNC == True:
            Titel = "Temperaturen im Vergleich"
        else:
            if "Wasser1" in dateiname: Titel = "Temperatur Fischtank 1"
            elif "aussen" in dateiname: Titel = "Außentemperatur"
        
    elif "Licht" in dateiname:
        Titel ="Lichtintensität in Lux"
        Y_Delta = 2000
    elif "DLI" in dateiname:
        Titel = "Daylight Integral"
        Y_Delta = 2.5  
    elif "Phwerte" in dateiname:
        Titel = "Ph-Werte"
        Y_Delta = 0.5  # Delta von 0.5 bei Ph-Wert
    else:
      print("Fehler bei Lesen Dateiname")
      
    if anzahlwerte == 12:
        Titel = Titel + " - eine Stunden"
    elif anzahlwerte == 240:
        Titel = Titel + "-  24 Stunden"
    elif anzahlwerte == 1470:
        Titel = Titel + "- Woche"
    
    pygame.display.set_caption(Titel)
   
    ####################################################################################  
    # zeichnet die beiden Achsen
    #( bei Außentemperatur muss die Achse höher, da sie von -15 bis plus 35 Grad geht )

    
    pygame.draw.line(grafikwindow, BLACK, (XEIN, hoehe - YEIN) , (XEIN, YOEIN), 3)       # y - Achse 


    if "Temp" in dateiname:                           # da bei Temperatur Minuswerte möglich sind
        if "aussen" in dateiname or SYNC == True:                                             # wird hier die x-Achse nicht unten gezeichnet
            l_ypunkt   =  int(hoehe - (3*Y_Delta/ 50) * bespH)
        else:  l_ypunkt   =  int(hoehe - (1*Y_Delta/ 50) * bespH) 
        pygame.draw.line(grafikwindow, BLACK, (XEIN, l_ypunkt - YEIN), (breite - XOEIN, l_ypunkt-YEIN), 3)

    else:

        
        pygame.draw.line(grafikwindow, BLACK, (XEIN, hoehe - YEIN) , (breite-XOEIN, hoehe - YEIN), 3) # x - Achse unten
    ############################################################################################

    # Einteilungen auf y-Achse:

    # Die unterschiedlichen Beschriftungen für Innen- und Außentemperatur, Licht- und Ph-Werte

    Beschriftungsrange_T_innen = ["-5", "0", "5", "10", "15", "20", "25", "30", "35", "40", "45"]
    Beschriftungsrange_T_aussen = ["-15", "-10", "-5","0", "5", "10", "15", "20", "25", "30", "35"]
    Beschriftungsrange_Licht = ["0", "10000", "20000", "30000", "40000", "50000", "60000", "70000", "80000", "90000", "100000"]
    Beschriftungsrange_Ph_Werte = ["4.0", "4.5", "5.0", "5.5", "6.0", "6.5", "7.0", "7.5", "8.0", "8.5", "9.0"]
    Beschriftungsrange_DLI = ["0", "2.5", "5.0", "7.5", "10.0", "12.5", "15.0", "17.5", "20.0", "22.5", "25.0"]



    

    for i in range (0,YEINTEIL):
    # definierte die jeweiligen y-Höhe
      
      if "Temp" in dateiname:
          
          o_ypunkt   =  int(hoehe - (i*Y_Delta/ 50) * bespH)   
      elif "Licht" in dateiname:
          
          o_ypunkt   =  int(hoehe - (i*Y_Delta/ 20000) * bespH)

      elif "DLI" in dateiname:
          
          o_ypunkt   =  int(hoehe - (i*Y_Delta/ 25) * bespH) 
      elif "Ph" in dateiname:

          o_ypunkt   =  int(hoehe - (i*Y_Delta/ 5) * bespH) 

      else:
          print("Fehler")
          
      # zieht die Orientierunglinien :

      pygame.draw.line(grafikwindow, BLACK, (XEIN, o_ypunkt - YEIN), (breite - XOEIN, o_ypunkt-YEIN), 2)

      # Beschriftung der Y-Achse:

      
      if "Temp" in dateiname:
          

          if "aussen" in dateiname or SYNC == True:
              txtGrad=   (Beschriftungsrange_T_aussen[i]) + " C°"
          else:
              txtGrad=   (Beschriftungsrange_T_innen[i]) + " C°"
           

           # Beschriftung der Y-Achse mit Zahlenwerten in Grad C°:
          
          myfont = pygame.font.SysFont("freesans,ttf", 14)             # font für die Achsenbeschriftung
          textsurf= myfont.render(txtGrad.encode("latin-1"),1,(0,0,0))
          grafikwindow.blit(textsurf,(XEIN -50, o_ypunkt-YEIN-10))
            
      elif "Licht" in dateiname:
            
           # Beschriftung der Y-Achse mit Zahlenwerten :
            
           txtLicht= (Beschriftungsrange_Licht[i]) + " Lx" 
           myfont = pygame.font.SysFont("freesans,ttf", 14)    # font für die Achsenbeschriftung
           textsurf= myfont.render(txtLicht.encode("latin-1"),1,(0,0,0))
           grafikwindow.blit(textsurf,(XEIN -60, o_ypunkt-YEIN-10))

      elif "DLI" in dateiname:
            
           # Beschriftung der Y-Achse mit Zahlenwerten :
            
           txtDLI= (Beschriftungsrange_DLI[i]) + " mol" 
           myfont = pygame.font.SysFont("freesans,ttf", 14)    # font für die Achsenbeschriftung
           textsurf= myfont.render(txtDLI.encode("latin-1"),1,(0,0,0))
           grafikwindow.blit(textsurf,(XEIN -60, o_ypunkt-YEIN-10))
      elif "Ph" in dateiname:
            
           # Beschriftung der Y-Achse mit Zahlenwerten :
            
           txtPh= (Beschriftungsrange_Ph_Werte[i]) 
           myfont = pygame.font.SysFont("freesans,ttf", 14)    # font für die Achsenbeschriftung
           textsurf= myfont.render(txtPh.encode("latin-1"),1,(0,0,0))
           grafikwindow.blit(textsurf,(XEIN -60, o_ypunkt-YEIN-10))
            
      else:
            
           print("Fehler")
    #############################################################################################

    # öffnet CSV-Datei und liest sie in Liste ein:
    
    with open(dateiname) as csvfile:

        reader = csv.reader(csvfile,delimiter = ",")
        data = list(reader)
        csvfile.close()
        
    Zaehl_liste = enumerate(data)
    row_count = len(data)
    print("len(data) = " + str(len(data)))
    print("SYNC = "+ str(SYNC))
    if MINMAX:
        Datenwerte = [],[],[]
    else:
        Datenwerte=[]
        
    mydate = []
    if not MINMAX:
        mytime = []
   
    if EOF:
        pos = row_count
    
    if (pos - anzahlwerte) <= 0: # korrigiert die Variable pos, damit nicht über bof hinaus gelesen wird
        pos = anzahlwerte+1
        BOF = 1                 # auszulesende Strecke liegt am Begin of File
    else :
        BOF = 0
        

    if pos > row_count:            # verhindert, dass grafischer Abschnitt
        pos = row_count             # über Dateiende hinaus wandert
        EOF = 1                 # auszulesende Strecke liegt am end of file
    else:
        EOF = 0
  
  

    Data_Anfang = pos - anzahlwerte     # die auszulesende Datenbankstrecke
##        print ("EOF = " + str(EOF))
##        print ("Anzahlwerte = " + str(anzahlwerte))
           
    Data_Ende   = pos
   
    
    
   

    datumvorher = ""  
    if MINMAX:
        Datentemp= []
    
    
    for line in data[Data_Anfang : Data_Ende]:
        try:
            
            temp1 =line[0][:6]
            temp2 = line[0][8:10]
            datum = str(temp1) + str(temp2)  # Datum mit zweistelligem Jahr
            
            uhrzeit= line[0][11:16]   # Uhrzeit
            
            wert = line[1][0:]      # Temperatur, Lux (oder später Ph-Wert, Batteriewert)
            wert = float(wert)
            
            if MINMAX == False:
                Datenwerte.append(wert)         # einfaches Einlesen in Liste
                mydate.append(datum)
                mytime.append(uhrzeit)
            else:
               
                if datum == datumvorher:
                    
                    Datentemp.append(wert)      # speichert Werte gleichen Datums in temporäre Liste
                    
           
                else:
                    if len(Datentemp) > 0:     # sonst würde gleich bei ersten Durchgang gerechnet
                        
                        tmin = min(Datentemp)              # bestimmt Minimum, Maximum und Durchschnitt
                        tmax = max(Datentemp)
                        tdurch =sum(Datentemp)/len(Datentemp)

                        Datenwerte[0].append(tmin)
                        Datenwerte[1].append(tdurch)
                        Datenwerte[2].append(tmax)

                        # neue Liste für den nächsten Tag:
                        Datentemp = []
                        
                        mydate.append(datumvorher) # Datum hat inzwischen gewechselt, daher vorher

                datumvorher = datum

        except:
            print("Syntaxfehler bei Dateiauslesen, Fehlerhafte Reihe lautet")
            print(line)
    
        
        ###################################################################################################
        # liest die Daten aus und zeichnet die Werte auf die Fläche:
              
        x = 0
        i = 0
        ypunkt = 0
        
        eint = 0
          
        if MINMAX:
            anzahlwerte = len(Datenwerte[0])  # kann bei Durchschnittswerten variieren
            
         # Vor Einteilungsstriche auf der X-Achse zeichnen, Sonderbehandlung für Woche:
        einteilungswerte = anzahlwerte

        if einteilungswerte == 240: einteilungswerte = einteilungswerte/10 # 240 Einteilungen sind zu viel
        einteilungswerte = int(einteilungswerte)
        einteilung = []
        #print("einteilungswerte = " + str(einteilungswerte))
        
        # Einteilungsstriche auf der X-Achse:
        for e in range(0,einteilungswerte+1):
            
            einteilung.append(int(bespB/einteilungswerte*e))
            pygame.draw.line(grafikwindow, BLACK, (XEIN+ einteilung[e], hoehe - YEIN +10) , (XEIN + einteilung[e], hoehe - YEIN - 10), 2)
##        print(einteilung)
##        print(len(einteilung))
        ###############################
        # Zeichnet die Punkte :

        flipflop = 0                # Vriable, mit deren Hilfe Floatwert abwechselnd auf- und abgerundet wird 
        print ("anzahlwerte = " + str(anzahlwerte) + " i = " + str(i))
        for i in range(0, anzahlwerte):
        
           
            if x > bespB:
                
                break 
           
            if MINMAX:                          # zeichnet Maximal-, Minimal- und Durchschnittswert
                tmin    = Datenwerte[0][i]
                tdurch  = Datenwerte[1][i]
                tmax    = Datenwerte[2][i]

            else:


                t = int(Datenwerte[i])
                
            if MINMAX:
                
                ymipunkt = int(hoehe - (tmin- WMIN)  / (WMAX-WMIN) * bespH)    # definierte Y-Wert  für einzelnen Datenpunkt
                ydupunkt = int(hoehe - (tdurch- WMIN)  / (WMAX-WMIN) * bespH)    # definierte Y-Wert  für einzelnen Datenpunkt
                ymapunkt = int(hoehe - (tmax- WMIN)  / (WMAX-WMIN) * bespH)    # definierte Y-Wert  für einzelnen Datenpunkt
            else:
                ypunkt = int(hoehe - (t- WMIN)  / (WMAX-WMIN) * bespH)    # definierte Y-Wert  für einzelnen Datenpunkt

            if x > 0 :
     
                newx = x + XEIN
            else:
                newx = XEIN
                
            if MINMAX:
                newmiy = ymipunkt -YEIN
                newduy = ydupunkt -YEIN
                newmay = ymapunkt -YEIN
            else:
                newy = ypunkt -YEIN
                
            if MINMAX:
                pygame.gfxdraw.aacircle(grafikwindow, newx, newmiy, 2, BLUE)
                pygame.gfxdraw.filled_circle(grafikwindow, newx, newmiy , 2 , BLUE)   # zeichnet Datenpunkt für Minimum
                pygame.gfxdraw.aacircle(grafikwindow, newx, newduy, 2, BLACK)
                pygame.gfxdraw.filled_circle(grafikwindow, newx, newduy , 2 , BLACK)   # zeichnet Datenpunkt für Durchschnitt
                pygame.gfxdraw.aacircle(grafikwindow, newx, newmay, 2, RED)
                pygame.gfxdraw.filled_circle(grafikwindow, newx, newmay , 2 , RED)   # zeichnet Datenpunkt für Maximum
            else:
                pygame.gfxdraw.aacircle(grafikwindow, newx, newy, 0, RED)
                pygame.gfxdraw.filled_circle(grafikwindow, newx, newy , 0 , RED)   # zeichnet einfachen Datenpunkt

     
            ####################################################
              
            
##            # zeichnet die Beschriftung der x_ Achse:
##            
            if MINMAX:
                text = str(mydate[i])           # bei Woche nur Datum
            else:
                text = str(mydate[i])+"  "+str(mytime[i])

            if x != 0 and eint <= 25:
##                print("einteilung[eint] = " + str(einteilung[eint]) + \
##                      "  eint = " + str(eint) + " x = " + str(x) +" modulo = " + str(modulo) +\
##                      " i = "+ str(i))
               
                modulo = x % einteilung[eint]
            else: modulo = 0
##                
            if x ==0:                                                       # sehr unelegant, geht aber nicht anders, weil sonst 
                textsurf= myfont.render(text.encode("latin-1"),1,(0,0,0))   # Fehlermeldung "integer division by zero" kommt
                textsurf = pygame.transform.rotate(textsurf, 300)           # eigende Funktion braucht zuviele Variablen zum übergeben        
                grafikwindow.blit(textsurf,(x+ XEIN, hoehe-YEIN + 30))

                eint = eint +1
                
##            elif(x >= einteilung[eint]) or (modulo <= 2) or (einteilung[eint] - x) <=4 :      # muss nicht aufs Pixel genau stimmen
            elif( (modulo <= 3 and eint <=24) or MINMAX == True) \
                  or (eint == 24 and einteilung[eint] - x <=3):      # die Beschriftung muss nicht aufs Pixel genau mit Einteilungsstrich 
                                                                        # übereinstimmen
                                                                                   
                textsurf= myfont.render(text.encode("latin-1"),1,(0,0,0))
                textsurf = pygame.transform.rotate(textsurf, 300)           # dreht den Beschriftungstext auf 300 Grad
                grafikwindow.blit(textsurf,(x+ XEIN, hoehe-YEIN + 30))
                if eint <= len(einteilung)+1:

                    eint = eint +1
 
          # zeichnet eine Linie zwischen den Punkten:                     
          
            if x != 0:
                if MINMAX:
                    pygame.draw.line(grafikwindow, BLUE, (oldx, oldmiy) , (newx, newmiy), 2) # Linie zwischen den MinimumPunkten
                    pygame.draw.line(grafikwindow, BLACK, (oldx, oldduy) , (newx, newduy), 2) # Linie zwischen den DurchschnittsPunkten
                    pygame.draw.line(grafikwindow, RED, (oldx, oldmay) , (newx, newmay), 2) # Linie zwischen den MaximumsPunkten
                else:
                    pygame.draw.line(grafikwindow, RED, (oldx, oldy) , (newx, newy), 2) # Linie zwischen den Punkten

            
            x = x + ((bespB)/anzahlwerte)  # neue x-Position berechnet aus der Anzahl der Werte
            if anzahlwerte != 240:
                x = round(x)            # durch die obige Formel kommt ein float-Wert raus, daher runden
            else:
                if flipflop == 0:       # wenn dauernd aufgrundet wird, passen die 240 Werte der 24-Stundengrafik
                    x = round(x)        # nicht in bespB (= 850 Pixel), daher abwechselnd auf- und abrunden
                    flipflop = 1
                elif flipflop == 1:
                    x = int(x) 
                    flipflop = 0
            
            
            oldx = newx                                 # merkt sich die vorherige Position, um im nächsten Schritt eine Linie
            if MINMAX:                                  # zwischen die Punkte ziehen zu können (siehe oben unter if:)
                oldmiy = newmiy
                oldduy = newduy
                oldmay = newmay
            else:
                oldy = newy
           
    return (pos, EOF, BOF)              # die Parameter werden in Kontrollfenster.py gebraucht

    
        
