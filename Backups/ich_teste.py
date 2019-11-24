import csv


##with open('Tempdatenaussen.csv', 'r') as textfile:
##    for row in reversed(list(csv.reader(textfile))):
##        print(', '.join(row))
Dateiname = 'Tempdatenaussen.csv'
Datenwerte=[]
mydate = []
mytime = []
with open(Dateiname) as csvfile:
    
    reader = csv.reader(csvfile,delimiter = ",")
    data = list(reader)
    row_count = len(data)

     
    for line in data[row_count-30:]:
        
        try:
            datum = line[0][:10]      # Datum
            uhrzeit= line[0][11:16]   # Uhrzeit
            wert = line[1][0:]      # Temperatur, Lux (oder später Ph-Wert)
            Datenwerte.append(wert)
            mydate.append(datum)
            mytime.append(uhrzeit)
          
        except:
            print("Syntaxfehler bei Dateiauslesen")
print(Datenwerte)
print(mydate)
print(mytime)
    # begrenzet die Anzahl der gezeigten Werte (kann später dazu dienen, verschiedene Zeitäume zu zeigen
##
##    Datenwerte = Datenwerte[-ANZWERTE:]
##    mydate = mydate[-ANZWERTE:]
##    mytime = mytime[-ANZWERTE:]
