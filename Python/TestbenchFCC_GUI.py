# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 03:40:29 2016

@author: Adnan
"""
from Tkinter import *
from ttk import Button, Style
import time
from TestBench_GPIO_Constants import *
from TestBench_GPIO_Functions import *
from TestBench_Constants import *
from TestBench_Functions import *
import DAQmxFunctions

class TestbenchFCC_GUI(Frame):
    def __init__(self,parent):
        self.parent = parent
        self.FC_state = "FC_STATE_STANDBY"

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

        # Cell Voltages
        self.FCCellVoltRows = 6
        self.FCCellVoltCols = 4
        self.CellVoltages = [
            [DoubleVar() for col in range(self.FCCellVoltCols)]
            for row in range(self.FCCellVoltRows)]

        self.CellVoltages_display = [
            [str(self.CellVoltages[row][col].get()) for col in \
                range(self.FCCellVoltCols)] for row in \
                    range(self.FCCellVoltRows)]

        print(self.CellVoltages_display)

        # Build_gui
        self.parent.title("Fuel Cell TestBench of Awesomeness")
        self.analog_input_values()
        self.digital_input_values()
        self.digital_output_values()
        self.cell_voltages()

        print "init done"

    def analog_input_values(self):
        analog_in_row1 = 0
        analog_in_row2 = 1

        Label(self.parent, text="FC Temp 1: ").grid(\
            row=analog_in_row1, column=0)
        self.fctemp1_display = StringVar()
        self.fctemp1_display.set(str(self.FCTemp1.get()))
        Entry(self.parent,textvariable=self.fctemp1_display, \
            justify='center').grid(row=analog_in_row1, column=1)

        Label(self.parent, text="FC Temp 2: ").grid(\
            row=analog_in_row2, column=0)
        self.fctemp2_display = StringVar()
        self.fctemp2_display.set(str(self.FCTemp2.get()))
        Entry(self.parent, textvariable=self.fctemp2_display, \
            justify='center').grid(row=analog_in_row2, column=1)

        Label(self.parent, text="FC Voltage: ").grid(\
            row=analog_in_row1, column=2)
        self.fcvolt_display = StringVar()
        self.fcvolt_display.set(str(self.FCVolt.get()))
        Entry(self.parent, textvariable=self.fcvolt_display, \
        justify='center').grid(row=analog_in_row1, column=3)

        Label(self.parent, text="FC Current: ").grid(\
            row=analog_in_row2, column=2)
        self.fccurr_display = StringVar()
        self.fccurr_display.set(str(self.FCCurr.get()))
        Entry(self.parent,textvariable=self.fccurr_display, \
            justify='center').grid(row=analog_in_row2, column=3)

        Label(self.parent, text="FC Pressure: ").grid(\
            row=analog_in_row1, column = 4)
        self.fcpres_display = StringVar()
        self.fcpres_display.set(str(self.FCPres.get()))
        Entry(self.parent, textvariable=self.fcpres_display, \
            justify='center').grid(row=analog_in_row1, column=5)

        Label(self.parent, text="Cap Voltage: ").grid(\
            row=analog_in_row2, column=4)
        self.capvolt_display = StringVar()
        self.capvolt_display.set(str(self.CapVolt.get()))
        Entry(self.parent, textvariable=self.capvolt_display, \
            justify='center').grid(row=analog_in_row2, column=5)

        Label(self.parent, text="Mass Flow: ").grid(\
            row=analog_in_row1, column=6)
        self.massflow_display = StringVar()
        self.massflow_display.set(str(self.MassFlow.get()))
        Entry(self.parent,textvariable=self.massflow_display, \
            justify='center').grid(row=analog_in_row1, column=7)

        print "analog input vals done"

    def update_analog_input_values(self):
        self.fctemp1_display.set(str(self.FCTemp1.get()))
        self.fctemp2_display.set(str(self.FCTemp2.get()))
        self.fcvolt_display.set(str(self.FCVolt.get()))
        self.fccurr_display.set(str(self.FCCurr.get()))
        self.fcpres_display.set(str(self.FCPres.get()))
        self.capvolt_display.set(str(self.CapVolt.get()))
        self.massflow_display.set(str(self.MassFlow.get()))

        print "updated analog input vals"

    def digital_input_values(self):
        dig_in_row1 = 2
        dig_in_row2 = 3
        self.parent.grid_rowconfigure(dig_in_row1, pad=25)

        Label(self.parent, text="H20K: ").grid(row=dig_in_row1, column=0)
        self.h20k_display = StringVar()
        self.h20k_display.set(str(self.H2OK.get()))
        Entry(self.parent, textvariable=self.h20k_display, \
            justify='center').grid(row=dig_in_row1, column=1)

        Label(self.parent, text="FC Start: ").grid(row=dig_in_row1, column=2)
        self.fcstart_display = StringVar()
        self.fcstart_display.set(str(self.FCStart.get()))
        Entry(self.parent, textvariable=self.fcstart_display, \
            justify='center').grid(row=dig_in_row1, column=3)

        Label(self.parent, text="FC Conn: ").grid(row=dig_in_row1, column=4)
        self.fcconn_display = StringVar()
        self.fcconn_display.set(str(self.FCConn.get()))
        Entry(self.parent, textvariable=self.fcconn_display, \
            justify='center').grid(row=dig_in_row1, column=5)

        Label(self.parent, text="Res Conn: ").grid(row=dig_in_row2, column=0)
        self.resconn_display = StringVar()
        self.resconn_display.set(str(self.ResConn.get()))
        Entry(self.parent, textvariable=self.resconn_display, \
            justify='center').grid(row=dig_in_row2, column=1)

        Label(self.parent, text="Cap Conn: ").grid(row=dig_in_row2, column=2)
        self.capconn_display = StringVar()
        self.capconn_display.set(str(self.CapConn.get()))
        Entry(self.parent, textvariable=self.capconn_display, \
            justify='center').grid(row=dig_in_row2, column=3)

        print "digital input vals done"

    def update_digital_input_values(self):
        self.h20k_display.set(str(self.H2OK.get()))
        self.fcstart_display.set(str(self.FCStart.get()))
        self.fcconn_display.set(str(self.FCConn.get()))
        self.resconn_display.set(str(self.ResConn.get()))
        self.capconn_display.set(str(self.CapConn.get()))

        print "updated digital input vals"

    def digital_output_values(self):
        dig_out_row1 = 4
        dig_out_row2 = 5
        self.parent.grid_rowconfigure(dig_out_row1, pad=25)

        Label(self.parent, text="FC Supply: ").grid(row=dig_out_row1, column=0)
        self.fcsupply_display = StringVar()
        self.fcsupply_display.set(str(self.FCSupply.get()))
        Entry(self.parent, textvariable=self.fcsupply_display, \
            justify='center').grid(row=dig_out_row1, column=1)

        Label(self.parent, text="FC Purge: ").grid(row=dig_out_row2, column=0)
        self.fcpurge_display = StringVar()
        self.fcpurge_display.set(str(self.FCPurge.get()))
        Entry(self.parent, textvariable=self.fcpurge_display, \
            justify='center').grid(row=dig_out_row2, column=1)

        Label(self.parent, text="FC Fan: ").grid(row=dig_out_row1, column=2)
        self.fcfan_display = StringVar()
        self.fcfan_display.set(str(self.FCFan1.get()))
        Entry(self.parent, textvariable=self.fcfan_display, \
            justify='center').grid(row=dig_out_row1, column=3)

        Label(self.parent, text="Startup Relay: ").grid(\
            row=dig_out_row1, column=4)
        self.startup_relay_display = StringVar()
        self.startup_relay_display.set(str(self.StartupRelay.get()))
        Entry(self.parent, textvariable=self.startup_relay_display, \
            justify='center').grid(row=dig_out_row1, column=5)

        Label(self.parent, text="Motor Relay: ").grid(\
            row=dig_out_row2, column=4)
        self.motor_relay_display = StringVar()
        self.motor_relay_display.set(str(self.MotorRelay.get()))
        Entry(self.parent, textvariable=self.motor_relay_display, \
            justify='center').grid(row=dig_out_row2, column=5)

        Label(self.parent, text="Cap Relay: ").grid(row=dig_out_row1, column=6)
        self.cap_relay_display = StringVar()
        self.cap_relay_display.set(str(self.CapRelay.get()))
        Entry(self.parent, textvariable=self.cap_relay_display, \
            justify='center').grid(row=dig_out_row1, column=7)

        Label(self.parent, text="Resistor Relay: ").grid(\
            row=dig_out_row2, column=6)
        self.resistor_relay_display = StringVar()
        self.resistor_relay_display.set(str(self.ResistorRelay.get()))
        Entry(self.parent, textvariable=self.resistor_relay_display, \
            justify='center').grid(row=dig_out_row2, column=7)

        print "digital output values done"

    def update_digital_output_values(self):
        self.fcsupply_display.set(str(self.FCSupply.get()))
        self.fcpurge_display.set(str(self.FCPurge.get()))
        self.fcfan_display.set(str(self.FCFan1.get()))
        self.startup_relay_display.set(str(self.StartupRelay.get()))
        self.motor_relay_display.set(str(self.MotorRelay.get()))
        self.cap_relay_display.set(str(self.CapRelay.get()))
        self.resistor_relay_display.set(str(self.ResistorRelay.get()))

        print "updated digital output values"

    def cell_voltages(self):
        start_row = 6
        self.parent.grid_rowconfigure(start_row, pad=25)

        cell_count = 0
        for y in range(self.FCCellVoltRows):
            for x in range(self.FCCellVoltCols):

                label_text = "Cell" + str(cell_count) + ": "
                Label(self.parent, text=label_text).grid(row=start_row + y, \
                    column=2*x)

                print(self.CellVoltages_display[y][x])
                entry_config = {'text':self.CellVoltages_display[y][x],
                                'justify':'center'}
                Entry(self.parent, **entry_config).grid(\
                    row =start_row + y, column=2*x + 1)

                cell_count += 1

        print "cell voltages done"

    def update_cell_voltages(self):
        self.CellVoltages_display = [
            [str(self.CellVoltages[row][col].get()) for col in \
            range(self.FCCellVoltCols)] for row in \
                range(self.FCCellVoltRows)]

    def main_state_machine(self):
        if (self.FC_state == "FC_STATE_STANDBY"):
            self.FC_state = FC_standby()
        elif (self.FC_state == "FC_STATE_SHUTDOWN"):
            self.FC_state = FC_shutdown()
        elif (self.FC_state == "FC_STATE_STARTUP_FANS"):
            # Ignore implementation for now, since fan stuff not working atm
            pass
        elif (self.FC_state == "FC_STATE_STARTUP_H2"):
            self.FC_state = FC_startup_h2()
        elif (self.FC_state == "FC_STATE_STARTUP_PURGE"):
            self.FC_state = FC_startup_purge()
        elif (self.FC_state == "FC_STATE_STARTUP_CHARGE"):
            self.FC_state = FC_startup_charge()
        elif (self.FC_state == "FC_STATE_RUN"):
            self.FC_state = FC_run()
        elif (self.FC_state == "FC_STATE_REPRESSURIZE"):
            self.FC_state = FC_repressurize()

        print "state machine"

if __name__ == "__main__":
    digital_configure()
    analog_configure()
    window = Tk()
    gui = TestbenchFCC_GUI(window)

    while True:
        gui.main_state_machine()
        gui.update_analog_input_values()
        gui.update_digital_input_values()
        gui.update_digital_output_values()
        window.update_idletasks()
        window.update()
