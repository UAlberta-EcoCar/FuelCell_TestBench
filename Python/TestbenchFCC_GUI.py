# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 03:40:29 2016

@author: Adnan
"""
from Tkinter import *
from ttk import Button, Style

class TestbenchFCC_GUI(Frame):
    def __init__(self,parent):
        self.parent = parent

        # Analog Inputs
        self.FCTemp1 = DoubleVar()
        self.FCTemp1.set(0)
        self.FCTemp2 = DoubleVar()
        self.FCTemp2.set(0)
        self.FCCurr = DoubleVar()
        self.FCCurr.set(0)
        self.FCVolt = DoubleVar()
        self.FCVolt.set(0)
        self.FCPres = DoubleVar()
        self.FCPres.set(0)
        self.MassFlow = DoubleVar()
        self.MassFlow.set(0)
        self.CapVolt = DoubleVar()
        self.CapVolt.set(0)
        self.FCCellVoltRows = 2
        self.FCCellVoltCols = 12

        # Digital Inputs
        self.H2OK = IntVar()
        self.H2OK.set(0)
        self.FCStart = IntVar()
        self.FCStart.set(0)
        self.CapConn = IntVar()
        self.CapConn.set(0)
        self.FCConn = IntVar()
        self.FCConn.set(0)
        self.ResConn = IntVar()
        self.ResConn.set(0)

        # Digital Outputs
        self.FCSupply = IntVar()
        self.FCSupply.set(0)
        self.FCPurge = IntVar()
        self.FCPurge.set(0)
        self.StartupRelay = IntVar()
        self.StartupRelay.set(0)
        self.MotorRelay = IntVar()
        self.MotorRelay.set(0)
        self.CapRelay = IntVar()
        self.CapRelay.set(0)
        self.ResistorRelay = IntVar()
        self.ResistorRelay.set(0)
        self.FCFan1 = IntVar()
        self.FCFan1.set(0)

        # GUI Initialization
        self.parent.title("Fuel Cell TestBench of Awesomeness")

        print "init done"

    def analog_input_values(self):
        Label(self.parent, text="FC Temp 1: ").grid(row=0, column=0)
        self.fctemp1_display = Label(self.parent, text=str(self.FCTemp1.get()))
        self.fctemp1_display.grid(row=0, column=1)

        Label(self.parent, text="FC Temp 2: ").grid(row=1, column=0)
        self.fctemp2_display = Label(self.parent, text=str(self.FCTemp2.get()))
        self.fctemp2_display.grid(row=1, column=1)

        Label(self.parent, text="FC Voltage: ").grid(row=0, column=2)
        self.fcvolt_display = Label(self.parent,text=str(self.FCVolt.get()))
        self.fcvolt_display.grid(row=0, column=3)

        Label(self.parent, text="FC Current: ").grid(row=1, column=2)
        self.fccurr_display = Label(self.parent,text=str(self.FCCurr.get()))
        self.fccurr_display.grid(row=1, column=3)

        Label(self.parent, text="FC Pressure: ").grid(row=0, column = 4)
        self.fcpres_display = Label(self.parent, text=str(self.FCPres.get()))
        self.fcpres_display.grid(row=0, column=5)

        Label(self.parent, text="Cap Voltage: ").grid(row=1, column=4)
        self.capvolt_display = Label(self.parent, text=str(self.CapVolt.get()))
        self.capvolt_display.grid(row=1, column=5)

        Label(self.parent, text="Mass Flow: ").grid(row=0, column=6)
        self.massflow_display = Label(self.parent,text=str(self.MassFlow.get()))
        self.massflow_display.grid(row=0, column=7)

        print "analog input vals done"

    def digital_input_values(self):
        dig_in_row = 2
        self.parent.grid_rowconfigure(dig_in_row, pad=25)

        Label(self.parent, text="H20K: ").grid(row=dig_in_row, column=0)
        self.h20k_display = Label(self.parent, text=str(self.H2OK.get()))
        self.h20k_display.grid(row=dig_in_row, column=1)

        Label(self.parent, text="FC Start: ").grid(row=dig_in_row, column=2)
        self.fcstart_display = Label(self.parent, text=str(self.FCStart.get()))
        self.fcstart_display.grid(row=dig_in_row, column=2)

        Label(self.parent, text="FC Conn: ").grid(row=dig_in_row, column=4)
        self.fcconn_display = Label(self.parent, text=str(self.FCConn.get()))
        self.fcstart_display.grid(row=dig_in_row, column=5)

        Label(self.parent, text="Res Conn: ").grid(row=dig_in_row, column=6)
        self.resconn_display = Label(self.parent, text=str(self.ResConn.get()))
        self.resconn_display.grid(row=dig_in_row, column=7)

        Label(self.parent, text="Cap Conn: ").grid(row=dig_in_row, column=8)
        self.capconn_display = Label(self.parent, text=str(self.CapConn.get()))
        self.capconn_display.grid(row=dig_in_row, column=9)

        print "digital input vals done"

    def digital_output_values(self):

        Label(self.parent, text="FC Supply: ").grid(row=3, column=0)
        self.fcsupply_display = StringVar()
        self.fcsupply_display.set(str(self.FCSupply.get()))
        Label(self.parent, textvariable=self.fcsupply_display).grid(\
            row=3, column=1)

        Label(self.parent, text="FC Purge: ").grid(row=4, column=0)
        self.fcpurge_display = StringVar()
        self.fcpurge_display.set(str(self.FCPurge.get()))
        Label(self.parent, textvariable=self.fcpurge_display).grid(\
            row=4, column=1)

        Label(self.parent, text="FC Fan: ").grid(row=3, column=2)
        self.fcfan_display = StringVar()
        self.fcfan_display.set(str(self.FCFan1.get()))
        Label(self.parent, textvariable=self.fcfan_display).grid(\
            row=3, column=3)

        Label(self.parent, text="Startup Relay: ").grid(row=3, column=4)
        self.startup_relay_display = StringVar()
        self.startup_relay_display.set(str(self.StartupRelay.get()))
        Label(self.parent, textvariable=self.startup_relay_display).grid(\
            row=3, column=5)

        Label(self.parent, text="Motor Relay: ").grid(row=4, column=4)
        self.motor_relay_display = StringVar()
        self.motor_relay_display.set(str(self.MotorRelay.get()))
        Label(self.parent, textvariable=self.motor_relay_display).grid(\
            row=4, column=5)

        Label(self.parent, text="Cap Relay: ").grid(row=3, column=6)
        self.cap_relay_display = StringVar()
        self.cap_relay_display.set(str(self.CapRelay.get()))
        Label(self.parent, textvariable=self.cap_relay_display).grid(\
            row=3, column=7)

        Label(self.parent, text="Resistor Relay: ").grid(row=4, column=6)
        self.resistor_relay_display = StringVar()
        self.resistor_relay_display.set(str(self.ResistorRelay.get()))
        Label(self.parent, textvariable=self.resistor_relay_display).grid(\
            row=4, column=7)

        print "digital output values done"

    def main_state_machine(self):
        self.analog_input_values()
        self.digital_input_values()
        self.digital_output_values()
        print "state machine done"



if __name__ == "__main__":
    window = Tk()
    gui = TestbenchFCC_GUI(window)
    gui.main_state_machine()
    window.mainloop()
