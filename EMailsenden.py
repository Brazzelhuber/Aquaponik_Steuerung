#!/usr/bin/python
# coding=utf-8
# EMailsenden.py
# Version 1.2

##########################################################################

import smtplib                  # E-Mail Bibliothek
from email.mime.text import MIMEText
from email.header import Header

#------------------------------------------------------------------------------------------------------
        
def alarm():            # Funktion schickt eine E-Mail an mein Handy, wenn Temperatur oder (später) Sonstwas nicht in Ordnung ist
    
    frm = 'kbeiersdoerfer@hotmail.com'
    to  = 'kbeiersdoerfer@hotmail.com'
    subj= 'Temperatur Alarm'
    msg = 'Temperatur über 25 Grad'

    try:
        mime = MIMEText(msg, 'plain', 'utf-8')
        mime['From'] = frm
        mime['To']  = to
        mime['Subject'] =Header(subj, 'utf-8')

        smtp=smtplib.SMTP("outlook.com")
        smtp.starttls()
        smtp.login("kbeiersdoerfer@hotmail.com", "")
        smtp.sendmail(frm,[to],mime.as_string())
        smtp.quit()
    except:
        print("Fehler bei E-Mailversand", sys.exc_info())

#---------
