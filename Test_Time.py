###!/usr/bin/env python3
### -*- coding: utf-8 -*-
### interface_i2c_ds1307_1.py
##
##from smbus import SMBus
##from time import sleep
##
##port = 1                # (0 for rev.1, 1 for rev 2!)
##bus = SMBus(port)
##rtcAddr = 0x68
##
##def bcd2str(d):         # // for integer division; % for modulo
##    if (d <= 9):
##        return '0' + str(d)
##    else:
##        return str(d // 16) + str(d % 16)
##
###setclock (BCD: sec,min,hour,weekday,day,mon,year)
##td = [0x00, 0x22, 0x18, 0x06, 0x16, 0x11, 0x19]
##bus.write_i2c_block_data(rtcAddr, 0, td)
##
##try:
##    while (True):
##        rd = bus.read_i2c_block_data(rtcAddr, 0, 7)
##        print (bcd2str(rd[4]) + '.' + bcd2str(rd[5]) + '.' + bcd2str(rd[6]) + \
##               '  ' + bcd2str(rd[2]) + ':' + bcd2str(rd[1]) + ':' + bcd2str(rd[0]))
##        sleep(1)
##except KeyboardInterrupt:
##    print("Keyboard interrupt by user")
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rambarun Komaljeet
# License: Freeware
# ---------------------------------------------------------------------------
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rambarun Komaljeet
# License: Freeware
# 
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rambarun Komaljeet
# License: LGPL
# ---------------------------------------------------------------------

import calendar
import tkinter as tk
import time
from tkinter import ttk


class MyDatePicker(tk.Toplevel):
    """
    Description:
        A tkinter GUI date picker.
    """

    def __init__(self, parent=None):
        """
        Description:
            When instantiating in parent module/widget/Gui, pass in 'self' as argument.
            Ex:
                a = MyDatePicker(self)

        :param parent: parent instance.
        """

        super().__init__()
        self.parent = parent
        self.title("Date Picker")
        self.resizable(0, 0)
        self.geometry("+250+10")
        self.init_frames()
        self.init_needed_vars()
        self.init_month_year_labels()
        self.init_buttons()
        self.space_between_widgets()
        self.fill_days()
        self.make_calendar()

    def init_frames(self):
        self.frame1 = tk.Frame(self)
        self.frame1.pack()

        self.frame_days = tk.Frame(self)
        self.frame_days.pack()

    def init_needed_vars(self):
        self.month_names = tuple(calendar.month_name)
        self.day_names = tuple(calendar.day_abbr)
        self.year = time.strftime("%Y")
        self.month = time.strftime("%B")

    def init_month_year_labels(self):
        self.year_str_var = tk.StringVar()
        self.month_str_var = tk.StringVar()

        self.year_str_var.set(self.year)
        self.year_lbl = tk.Label(self.frame1, textvariable=self.year_str_var, width=3)
        self.year_lbl.grid(row=0, column=5)

        self.month_str_var.set(self.month)
        self.month_lbl = tk.Label(self.frame1, textvariable=self.month_str_var, width=8)
        self.month_lbl.grid(row=0, column=1)

    def init_buttons(self):
        self.left_yr = ttk.Button(self.frame1, text="←", width=5, command=self.prev_year)
        self.left_yr.grid(row=0, column=4)

        self.right_yr = ttk.Button(self.frame1, text="→", width=5, command=self.next_year)
        self.right_yr.grid(row=0, column=6)

        self.left_mon = ttk.Button(self.frame1, text="←", width=5, command=self.prev_month)
        self.left_mon.grid(row=0, column=0)

        self.right_mon = ttk.Button(self.frame1, text="→", width=5, command=self.next_month)
        self.right_mon.grid(row=0, column=2)

    def space_between_widgets(self):
        self.frame1.grid_columnconfigure(3, minsize=40)

    def prev_year(self):
        self.prev_yr = int(self.year_str_var.get()) - 1
        self.year_str_var.set(self.prev_yr)

        self.make_calendar()

    def next_year(self):
        self.next_yr = int(self.year_str_var.get()) + 1
        self.year_str_var.set(self.next_yr)

        self.make_calendar()

    def prev_month(self):
        index_current_month = int(self.month_names.index(self.month_str_var.get()))
        index_prev_month = index_current_month - 1

        #  index 0 is empty string, use index 12 instead, which is index of December.
        if index_prev_month == 0:
            self.month_str_var.set(self.month_names[12])
        else:
            self.month_str_var.set(self.month_names[index_current_month - 1])

        self.make_calendar()

    def next_month(self):
        index_current_month = int(self.month_names.index(self.month_str_var.get()))

        #  index 13 does not exist, use index 1 instead, which is January.
        try:
            self.month_str_var.set(self.month_names[index_current_month + 1])
        except IndexError:
            self.month_str_var.set(self.month_names[1])

        self.make_calendar()

    def fill_days(self):
        col = 0
        #  Creates days label
        for day in self.day_names:
            self.lbl_day = tk.Label(self.frame_days, text=day)
            self.lbl_day.grid(row=0, column=col)
            col += 1

    def make_calendar(self):
        #  Delete date buttons if already present.
        #  Each button must have its own instance attribute for this to work.
        try:
            for dates in self.m_cal:
                for date in dates:
                    if date == 0:
                        continue

                    self.delete_buttons(date)

        except AttributeError:
            pass

        year = int(self.year_str_var.get())
        month = self.month_names.index(self.month_str_var.get())
        self.m_cal = calendar.monthcalendar(year, month)

        #  build date buttons.
        for dates in self.m_cal:
            row = self.m_cal.index(dates) + 1
            for date in dates:
                col = dates.index(date)

                if date == 0:
                    continue

                self.make_button(str(date), str(row), str(col))

    def make_button(self, date, row, column):
        exec(
            "self.btn_" + date + "= ttk.Button(self.frame_days, text=" + date + ", width=5)\n"
            "self.btn_" + date + ".grid(row=" + row + " , column=" + column + ")\n"
            "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
        )

    def delete_buttons(self, date):
        exec(
            "self.btn_" + str(date) + ".destroy()"
        )

    def get_date(self, clicked=None):
        global DATA_OPERAZIONE
        clicked_button = clicked.widget
        year = self.year_str_var.get()
        month = self.month_names.index(self.month_str_var.get())
        date = clicked_button['text']

        #  Change string format for different date formats.
        self.full_date = '%s-%02d-%02d' % (year, month, date)
        #print(self.full_date)
        #  insert date in parent widget like these:
        #  in parent: 
        #   self.a = tk.StringVar()
        #   self.parent.a.set(self.full_date)
        #
        # if a is a tk.Entry
        #self.parent..insert(0, self.full_date)
        DATA_OPERAZIONE = self.full_date
        return DATA_OPERAZIONE
        print(DATA_OPERAZIONE)
        #print('data mia',  DATA_OPERAZIONE               )


if __name__ == '__main__':

    #DATA_OPERAZIONE = tk.StringVar()
    
    def application():
        app = MyDatePicker()
        print(DATA_OPERAZIONE)
        return DATA_OPERAZIONE


    root = tk.Tk()
    btn = tk.Button(root, text="test", command=application)
    btn.pack()

    # Data Operazione
    DATA_OPERAZIONE = tk.StringVar()
    data_operazione_lbl = tk.Label(root, text="Data Operazione", font= ('arial', 8), bd=10)
    data_operazione_lbl.pack()

    data_operazione = tk.Entry(root, textvariable=DATA_OPERAZIONE, width=10)
    data_operazione.pack()
    print('data mia',  DATA_OPERAZIONE  )            

    
