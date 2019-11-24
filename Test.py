# Kontroll-Block
# 1 = an 0 = aus
# erster Wert in der Liste ist der IST-Wert, der zweite der  SOLL-Wert

cb = { "Growlamps1 ein":      [1,1],
       "Growlamps2 ein":      [1,1],
       "Hauptpumpe ein":      [1,1],
       "Sauerstoffpumpe ein": [1,1],
       "Ventil1 offen":       [1,1],
       "Ventil2 offen":       [1,1],
       "Screen_schreiben":    [1,1],
       "Es ist Tag"      :    [1,1]}
for key, value in cb.items():
    print(key, value)
print("\n")
cb["Growlamps2 ein"] = [1,0]

for key, value in cb.items():
    print(key, value)
print("\n")
#print(cb["Growlamps2 ein"][0])
#print(cb["Growlamps2 ein"][1])

for key, value in cb.items():
    if  value[0] != value[1]:
        value[0] = value[1]
print("\n")
for key, value in cb.items():
    print(key, value)
