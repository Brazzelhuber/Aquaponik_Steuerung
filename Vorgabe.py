import csv


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
    
def RefreshWerte(Screen_App, _array):
    
   
    
    _array["TempWasserMin"] = Screen_App.xlf.entry_wmi.get()
    _array["TempWasserMax"] = Screen_App.xlf.entry_wma.get()
    _array["TempLuftMin"] = Screen_App.xlf.entry_lmi.get()
    _array["WasserpegelMin"] = Screen_App.xlf.entry_pmi.get()
    _array["WasserpegelMax"] = Screen_App.xlf.entry_pma.get()
    _array["PhWertMin"] = Screen_App.xlf.entry_phmi.get()
    _array["PhWertMax"] = Screen_App.xlf.entry_phma.get()
    _array["Fuetterung"] = Screen_App.xlf.entry_Fuz.get()
    _array["Fuett.dauer"] = Screen_App.xlf.entry_Fud.get()

  

    
    
def WriteWerte(_array):
    
    vo = open('Vorgabe.csv' , 'w')
    writerl = csv.writer(vo)
    for item in _array.items():
        writerl.writerow(item)        

    vo.close()
