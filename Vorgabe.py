import csv
import tkinter as Tk
import datetime
from tkinter import messagebox


def LeseVorgabe(Screen_App, _array):
    vo = open("Vorgabe.csv", "r")
    reader1= csv.reader(vo)
    daten = list(reader1)
    for line in daten:
        Linie = str(line)
        Komma = Linie.find(",")
        Schluessel = Linie[2:Komma-1]
        Wert = Linie[Komma +3:len(Linie)-2]

        for key in _array.keys():
            if key == Schluessel:
    
                _array[key] = Wert

    Screen_App.xlf.entry_wmi.insert(0,  str(_array["TempWasserMin"]))
    Screen_App.xlf.entry_wma.insert(0,  str(_array["TempWasserMax"]))
    Screen_App.xlf.entry_lmi.insert(0,  str(_array["TempLuftMin"]))
    Screen_App.xlf.entry_pmi.insert(0,  str(_array["WasserpegelMin"]))
    Screen_App.xlf.entry_pma.insert(0,  str(_array["WasserpegelMax"]))
    Screen_App.xlf.entry_phmi.insert(0,  str(_array["PhWertMin"]))
    Screen_App.xlf.entry_phma.insert(0,  str(_array["PhWertMax"]))

    vo.close()
    
def ZeitenEinfuegen(Screen_App, z_array):
    
    Screen_App.entry_fuz_a.delete(0,  Tk.END)
    Screen_App.entry_fuz_e.delete(0,  Tk.END)
    Screen_App.entry_bel_a.delete(0,  Tk.END)
    Screen_App.entry_bel_e.delete(0,  Tk.END)
    Screen_App.entry_blu_a.delete(0,  Tk.END)
    Screen_App.entry_blu_e.delete(0,  Tk.END)
    
    
    Screen_App.entry_fuz_a.insert(0,  str(z_array["Fuetterung_Anfang"]))
    Screen_App.entry_fuz_e.insert(0,  str(z_array["Fuetterung_Ende"]))
    Screen_App.entry_bel_a.insert(0,  str(z_array["Beleuchtung_Anfang"]))
    Screen_App.entry_bel_e.insert(0,  str(z_array["Beleuchtung_Ende"]))
    Screen_App.entry_blu_a.insert(0,  str(z_array["Blumenwiese_Anfang"]))
    Screen_App.entry_blu_e.insert(0,  str(z_array["Blumenwiese_Ende"]))
    
def LeseZeiten(Screen_App, z_array):
    
    zo = open("Zeiten.csv", "r")
    reader1= csv.reader(zo)
    daten = list(reader1)
    for line in daten:
        Linie = str(line)
        Komma = Linie.find(",")
        Schluessel = Linie[2:Komma-1]
        Wert = Linie[Komma +3:len(Linie)-2]

        for key in z_array.keys():
            if key == Schluessel:
    
                z_array[key] = Wert
                
    ZeitenEinfuegen(Screen_App, z_array)
    
##    Screen_App.entry_fuz_a.insert(0,  str(z_array["Fuettereung_Anfang"]))
##    Screen_App.entry_fuz_e.insert(0,  str(z_array["Fuetterung_Ende"]))
##    Screen_App.entry_bel_a.insert(0,  str(z_array["Beleuchtung_Anfang"]))
##    Screen_App.entry_bel_e.insert(0,  str(z_array["Beleuchtung_Ende"]))
##    Screen_App.entry_blu_a.insert(0,  str(z_array["Blumenwiese_Anfang"]))
##    Screen_App.entry_blu_e.insert(0,  str(z_array["Blumenwiese_Ende"]))
    
    
    zo.close()


    
def Fehlermeldung():
    win = Tk.Toplevel()
    win.transient()
    
    win.title('Warnung')
    win.geometry("380x100+500+300")
    Tk.Label(win, text="Bitte Uhrzeit korrekt in der Form XX:XX eingeben").grid(ipady = 35, ipadx =30)
    win.after(5000, win.quit)
    win.mainloop()
    win.destroy()
        

def RefreshZeiten(Screen_App, z_array):
    
##    print("bin in RefreshZeiten")
    
    while True:
        try:
          z_array["Fuetterung_Anfang"] = datetime.datetime.strptime(Screen_App.entry_fuz_a.get(), "%H:%M").strftime("%H:%M")
          z_array["Fuetterung_Ende"] = datetime.datetime.strptime(Screen_App.entry_fuz_e.get(), "%H:%M").strftime("%H:%M")
          z_array["Beleuchtung_Anfang"] = datetime.datetime.strptime(Screen_App.entry_bel_a.get(), "%H:%M").strftime("%H:%M")
          z_array["Beleuchtung_Ende"] = datetime.datetime.strptime(Screen_App.entry_bel_e.get(), "%H:%M").strftime("%H:%M")
          z_array["Blumenwiese_Anfang"] = datetime.datetime.strptime(Screen_App.entry_blu_a.get(), "%H:%M").strftime("%H:%M")
          z_array["Blumenwiese_Ende"] = datetime.datetime.strptime(Screen_App.entry_blu_e.get(), "%H:%M").strftime("%H:%M")
          return
        except (ValueError, TypeError):
          Fehlermeldung()
          return


    
def RefreshWerte(Screen_App, _array):
    
   # wird von Kontrollfenster aufgerufen
    
    _array["TempWasserMin"] = Screen_App.xlf.entry_wmi.get()
    _array["TempWasserMax"] = Screen_App.xlf.entry_wma.get()
    _array["TempLuftMin"] = Screen_App.xlf.entry_lmi.get()
    _array["WasserpegelMin"] = Screen_App.xlf.entry_pmi.get()
    _array["WasserpegelMax"] = Screen_App.xlf.entry_pma.get()
    _array["PhWertMin"] = Screen_App.xlf.entry_phmi.get()
    _array["PhWertMax"] = Screen_App.xlf.entry_phma.get()
  

def WriteZeiten(z_array):
##    print("ich schreibe")
    zo = open("Zeiten.csv", "w")
    writerz = csv.writer(zo)
    for item in z_array.items():
        writerz.writerow(item)        

    zo.close()
    
    
def WriteWerte(_array):
    
    vo = open('Vorgabe.csv' , 'w')
    writerl = csv.writer(vo)
    for item in _array.items():
        writerl.writerow(item)        

    vo.close()
