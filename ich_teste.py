#!/usr/bin/env python
#
# [SNIPPET_NAME: Calendar/Date picker]
# [SNIPPET_CATEGORIES: PyQt4]
# [SNIPPET_DESCRIPTION: A calendar/date picker example]
# [SNIPPET_AUTHOR: Darren Worrall <dw@darrenworrall.co.uk>]
# [SNIPPET_LICENSE: GPL]
# [SNIPPET_DOCS: http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qcalendarwidget.html]

# example calendar.py

import sys
import datetime
from datetime import timedelta
from PyQt4 import QtGui, QtCore
import tkinter as Tk

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

   def __init__(self):
      super(Example, self).__init__()

      self.initUI()
		
   def initUI(self):
	
      cal = QtGui.QCalendarWidget(self)
      cal.setGridVisible(True)
      cal.move(20, 20)
      cal.clicked[QtCore.QDate].connect(self.showDate)
		
      self.lbl = QtGui.QLabel(self)
      date = cal.selectedDate()
      self.lbl.setText(date.toString())
      self.lbl.move(20, 200)
		
      self.setGeometry(100,100,300,300)
      self.setWindowTitle('Calendar')
      self.show()
		
   def showDate(self, date):
	
      self.lbl.setText(date.toString())
      
   def getValues(self):
       return (date.toString())
		
def main():

   app = QtGui.QApplication(sys.argv)
   ex = Example()
   if ex.exec():
    value = ex.GetValues()
    print(value)
       
   
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
