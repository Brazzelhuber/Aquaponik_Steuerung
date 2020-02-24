#!/usr/bin/python
# coding=utf-8
# Werte_in_Datei_schreiben.py
# Version 1.2

#
# schreibt die Sensoradten samt Zeitstempel in die CSV-Dateien
#

import csv, time, datetime


import Lichtlesen as Ls
import EMailsenden as Es



def Werte_schreiben(my_array, control):
   
    t=time.strftime("%d.%m.%Y %H:%M:%S")
                  
    ######################################
    # schreibt Änderung in Logdatei:
    for (key, value) in control.items():
        if value[0] != value[1] and key != "Logeintrag" and key != "Screen_schreiben" \
              and key != "Es ist Tag"  :
                                                        #!= Logeintrag, sonst würde eine endlosschleife ausgelöst
                                                        # solange nicht die Logdatei geöffnet wird
                                                        # ebensowenig soll ein Logeintrag erfolgen, wenn von Tag auf Nacht
                                                        # umgestellt oder das Bildschirmschreiben abgestellt wird"
            ld = open("Logdatei.csv", "a")
            writerld = csv.writer(ld)
            if value[1] == 1:
                Wert = "ein"
            elif value[1] == 0: Wert = "aus"
            Wertzusatz = " -- To = "+ str(my_array["T_Luft_oben"])+ ", Tu = " + str(my_array["T_Luft_unten"]) \
                         + " ,Tw1 = " + str(my_array["T_Wasser1"]) + " ,Tw2 = "+ str(my_array["T_Wasser2"]) \
                         + " ,Ta = " + str(my_array["T_aussen"])
            Wert = Wert + Wertzusatz
               
            if not (" to " in str(key) or "Hauptpumpe" in str(key)):  # Einzelventile sollen nicht protokolliert werden
                Meldung = str(key) + ":  " + Wert                     # auch nicht die Hauptpumpe
                row_ld = [t, Meldung]
                writerld.writerow(row_ld)
            ld.close()
            control["Logeintrag"][1] = 1      # es hat ein neuer Logeintrag stattgefunden
            
    


    #####################################
    # schreibt Sensordaten in jeweilige Datei:

    lf = open('Tempdatenaussen.csv' , 'a')
    writerl = csv.writer(lf)
    row1 = [t,my_array["T_aussen"] ]
    
    writerl.writerow(row1)
    lf.close()

    wf = open('Tempdaten_Wasser1.csv' , 'a')
    writerw = csv.writer(wf)
    row2 = [t,  my_array["T_Wasser1"]]
    
    writerw.writerow(row2)
    wf.close()

    vl = open("Volt.csv","a")
    writerv = csv.writer(vl)
    rowv = [t,my_array["Volt"]]
    writerv.writerow(rowv)
    vl.close()

    ws = open("Wasserstand.csv","a")
    writerw = csv.writer(ws)
    roww = [t,my_array["Wasserstand"]]
    writerw.writerow(roww)
    ws.close()


    
    if control["Es ist Tag"][0] == 1:
        
        
        Li = open('Lichtdaten1.csv' , 'a')                        # Lichtdatendatei öffnen
    
        writerx = csv.writer(Li)
        # Schreibt Date/Time und Luxwert in Lichtdatei
        row3 = [t,  my_array["Luxwert_1"]]
                
        writerx.writerow(row3)
        Li.close()

        
# passiert nur kurz nach Mitternacht, wird von Mainloop gesteuert
def DLI_schreiben():
    
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
   
    ty=yesterday.strftime("%d.%m.%Y")

    Li = open('Lichtdaten1.csv' , 'r')                        # Lichtdatendatei öffnen
    reader_licht   = csv.reader(Li)
    data = list(reader_licht)
    Dli = open('DLI_Eichen.csv', 'a')
    writerDli = csv.writer(Dli)
    
    Datentemp = []
    for line in reversed(data):
            
        datum=line[0][0:10]
        wert = line[1][0:]      
        wert = float(wert)
             
        
           
        if datum == ty:
            
            Datentemp.append(wert)      # Kummulieren der Werte gleichen Datums
   
        else:
            if len(Datentemp) > 0 and not(datum > ty):     # sonst würde gleich beim ersten Durchgang gerechnet
            
            
                summe =int(sum(Datentemp))    # Summiert die Werte

                #0.0185 ist der Umrechnungsfaktor von Lux auf PPFD (µmol pro sek und m2)
                #/1000000 um von µmol auf mol zu kommen
                # es wird alle 6 Minuten aufgezeichnet, daher: mal 360 (PPFD ist pro Sekunde
                
                summeDLI = str(int(summe*0.0185/1000000*360))
                row4 = [ty,  summeDLI]
                writerDli.writerow(row4)


        if datum < ty:   # wenn früher als yesterday
            break

            
    Li.close()
    Dli.close()
        

    

    
    
   
