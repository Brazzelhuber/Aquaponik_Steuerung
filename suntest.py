import datetime as dt
import time
import sunrise as sr
import ptvsd


s = sr.sun(lat =51.755,long =8.6)
jetzt=(dt.datetime.now().time())
print(jetzt)
auf =(s.sunrise(when=dt.datetime.now()))
unter =(s.sunset(when=dt.datetime.now()))
print (auf)
print (unter)


print(jetzt > auf)
print(jetzt < unter)
