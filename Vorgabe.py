import csv
import tkinter as Tk


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
    Screen_App.xlf.entry_Fuz.insert(0,  str(_array["Fuetterung"]))
    Screen_App.xlf.entry_Fud.insert(0,  str(_array["Fuett.dauer"]))

    vo.close()
    
def Fehlermeldung():
    win = Tk.Toplevel()
    win.transient()
    
    win.title('Warnung')
    win.geometry("380x100+500+300")
    Tk.Label(win, text="Bitte Uhrzeit korrekt in der Form XX:XX eingeben").grid(ipady = 35, ipadx =30)
    win.after(5000, win.quit)
    win.mainloop()
    win.destroy()
        
def Uhrzeit_korrekt(string):
    
    zahlen = ["0","1","2","3","4","5","6","7","8","9"]
    
    
    if string[0] in zahlen:
        print("OK")
        Stunde1 = int(string[0])
    else:
        Fehlermeldung()
        return False
    if string[1] in zahlen:
        Stunde2 = int(string[1])
    else:
        Fehlermeldung()
        return False
    if string[2] != ":":
        Fehlermeldung()
        return False
    if string[3] in zahlen:
        Minute1 = int(string[3])
    else :
        Fehlermeldung()
        return False
    if string[4] in zahlen:
        Minute2 = int(string[4])
    else:
        Fehlermeldung()
        return False
    

    if (Stunde1 > 2) or Minute1 > 5 :
        Fehlermeldung()
        return False
    else:
        return True
        
    
def RefreshWerte(Screen_App, _array):
    
   
    
    _array["TempWasserMin"] = Screen_App.xlf.entry_wmi.get()
    _array["TempWasserMax"] = Screen_App.xlf.entry_wma.get()
    _array["TempLuftMin"] = Screen_App.xlf.entry_lmi.get()
    _array["WasserpegelMin"] = Screen_App.xlf.entry_pmi.get()
    _array["WasserpegelMax"] = Screen_App.xlf.entry_pma.get()
    _array["PhWertMin"] = Screen_App.xlf.entry_phmi.get()
    _array["PhWertMax"] = Screen_App.xlf.entry_phma.get()
    while True:
        eingabe = Screen_App.xlf.entry_Fuz.get()
        if Uhrzeit_korrekt(eingabe):
            _array["Fuetterung"] = eingabe
            break
        else:
            Screen_App.xlf.entry_Fuz.delete(0, len(Screen_App.xlf.entry_Fuz.get()))
            
        
       
        
    _array["Fuett.dauer"] = Screen_App.xlf.entry_Fud.get()

  

    
    
def WriteWerte(_array):
    
    vo = open('Vorgabe.csv' , 'w')
    writerl = csv.writer(vo)
    for item in _array.items():
        writerl.writerow(item)        

    vo.close()
