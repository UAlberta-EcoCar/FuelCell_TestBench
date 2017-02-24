# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 03:40:29 2016

@author: Adnan
"""
DAQ_Connected = False # Allows Testing GUI without DAQ
from Tkinter import *
from ttk import Button, Style
import time
if DAQ_Connected:
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
        self.FCTemp2 = DoubleVar()
        self.FCCurr = DoubleVar()
        self.FCVolt = DoubleVar()
        self.FCPres = DoubleVar()
        self.MassFlow = DoubleVar()
        self.CapVolt = DoubleVar()
        self.FCChargeSLP = DoubleVar()
        if DAQ_Connected:
            pass
        self.FCTemp1.set(10.11)
        self.FCTemp2.set(1000.11)
        self.FCCurr.set(0)
        self.FCVolt.set(0)
        self.FCPres.set(0)
        self.MassFlow.set(0)
        self.CapVolt.set(0)
        self.FCChargeSLP.set(0)

        # Digital Inputs
        self.H2OK = IntVar()
        self.FCStart = IntVar()
        if DAQ_Connected:
            self.H2OK.set(pin_value_get_dig(H20K))
            self.FCStart.set(pin_value_get_dig_output(START))
        else:
            self.H2OK.set(0)
            self.FCStart.set(0)
        # self.CapConn = IntVar()
        # self.CapConn.set(0)
        # self.FCConn = IntVar()
        # self.FCConn.set(0)
        # self.ResConn = IntVar()
        # self.ResConn.set(0)

        # Digital Outputs
        self.FCSupply = IntVar()
        self.FCPurge = IntVar()
        self.StartupRelay = IntVar()
        self.MotorRelay = IntVar()
        self.CapRelay = IntVar()
        self.ResistorRelay = IntVar()
        self.FCFan1 = IntVar()
        if DAQ_Connected:
            self.FCSupply.set(pin_value_get_dig_output(H2_VALVE))
            self.FCPurge.set(pin_value_get_dig_output(PURGE_VALVE))
            self.StartupRelay.set(pin_value_get_dig_output(STARTUP_RELAY))
            self.MotorRelay.set(pin_value_get_dig_output(MOTOR_RELAY))
            self.CapRelay.set(pin_value_get_dig_output(CAP_RELAY))
            self.ResistorRelay.set(pin_value_get_dig_output(RESISTOR_RELAY))
        else:
            self.FCSupply.set(0)
            self.FCPurge.set(0)
            self.StartupRelay.set(0)
            self.MotorRelay.set(0)
            self.CapRelay.set(0)
            self.ResistorRelay.set(0)
            self.FCFan1.set(0)

        # Cell Voltages
        self.FCCellVoltRows = 16
        self.FCCellVoltCols = 3
        self.FCCellCount = 46
        self. CellVoltages = []
        self.CellVoltages_display = []
        for i in range(self.FCCellCount):
            self.CellVoltages.append(DoubleVar())
            self.CellVoltages_display.append(StringVar())
            self.CellVoltages[i].set(0.0)
            self.CellVoltages_display[i].set(str(self.CellVoltages[i].get()))

        # print(self.CellVoltages_display)

        # Build_gui
        self.parent.title("Fuel Cell TestBench of Awesomeness")

        self.entry_width = 10
        self.analog_input_values()
        self.digital_input_values()
        self.digital_output_values()
        self.cell_voltages()

        self.on_colour = "green"
        self.off_colour = "blue"
        self.window_width = 1366 # Most common laptop screen resolution size
        self.window_height = 768
        self.parent.maxsize(self.window_width,self.window_height)
        self.parent.minsize(self.window_width,self.window_height)

        print "init done"

    def analog_input_values(self):
        analog_in_row1 = 0
        analog_in_row2 = 1

        Label(self.parent, text="FC Temp 1: ").grid(\
            row=analog_in_row1, column=0)
        self.fctemp1_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fctemp1_entry.grid(row=analog_in_row1, column=1)

        Label(self.parent, text="FC Temp 2: ").grid(\
            row=analog_in_row2, column=0)
        self.fctemp2_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fctemp2_entry.grid(row=analog_in_row2, column=1)

        Label(self.parent, text="FC Voltage: ").grid(\
            row=analog_in_row1, column=2)
        self.fcvolt_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcvolt_entry.grid(row=analog_in_row1, column=3)

        Label(self.parent, text="FC Current: ").grid(\
            row=analog_in_row2, column=2)
        self.fccurr_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fccurr_entry.grid(row=analog_in_row2, column=3)

        Label(self.parent, text="FC Pressure: ").grid(\
            row=analog_in_row1, column = 4)
        self.fcpres_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcpres_entry.grid(row=analog_in_row1, column=5)

        Label(self.parent, text="Cap Voltage: ").grid(\
            row=analog_in_row2, column=4)
        self.capvolt_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.capvolt_entry.grid(row=analog_in_row2, column=5)

        Label(self.parent, text="Mass Flow: ").grid(\
            row=analog_in_row1, column=6)
        self.massflow_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.massflow_entry.grid(row=analog_in_row1, column=7)

        Label(self.parent, text="FC Charge since last purge: ").grid(\
            row=analog_in_row2, column=6)
        self.fcchargeslp_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcchargeslp_entry.grid(row=analog_in_row2, column=7)

        print "analog input vals done"

    def update_analog_input_values(self):
        if DAQ_Connected:
            pass

        analog_inputs = {
            'fctemp1': (self.FCTemp1.get(), self.fctemp1_entry),
            'fctemp2': (self.FCTemp2.get(), self.fctemp2_entry),
            'fcvolt': (self.FCVolt.get(), self.fcvolt_entry),
            'fccurr': (self.FCCurr.get(), self.fccurr_entry),
            'fcpres': (self.FCPres.get(), self.fcpres_entry),
            'capvolt': (self.CapVolt.get(), self.capvolt_entry),
            'massflow': (self.MassFlow.get(), self.massflow_entry),
            'fcchargeslp': (self.FCChargeSLP.get(), self.fcchargeslp_entry)}

        for name, (value, entry) in analog_inputs.items():
            entry.delete(0, END)
            entry.insert(0, str(value))

        print "updated analog input vals"

    def digital_input_values(self):
        dig_in_row1 = 2
        dig_in_row2 = 3
        self.parent.grid_rowconfigure(dig_in_row1, pad=25)

        Label(self.parent, text="H20K: ").grid(row=dig_in_row1, column=0)
        self.h2ok_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.h2ok_entry.grid(row=dig_in_row1, column=1)

        Label(self.parent, text="FC Start: ").grid(row=dig_in_row1, column=2)
        self.fcstart_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcstart_entry.grid(row=dig_in_row1, column=3)

        print "digital input vals done"

    def update_digital_input_values(self):
        if DAQ_Connected:
            self.H2OK.set(pin_value_get_dig(H20K))
            self.FCStart.set(pin_value_get_dig_output(START))
        else:
            self.FCStart.set( not self.FCStart.get())

        dig_inputs = {
            'h20k': (self.H2OK.get(), self.h2ok_entry),
            'fcstart': (self.FCStart.get(), self.fcstart_entry)}

        for name, (value, entry) in dig_inputs.items():
            if value == 0:
                colour = self.off_colour
            else:
                colour = self.on_colour
            entry.configure(bg=colour)

        print "updated digital input vals"

    def digital_output_values(self):
        dig_out_row1 = 4
        dig_out_row2 = 5
        self.parent.grid_rowconfigure(dig_out_row1, pad=25)

        Label(self.parent, text="FC Supply: ").grid(row=dig_out_row1, column=0)
        self.fcsupply_entry = \
            Entry(self.parent,justify='center', width=self.entry_width)
        self.fcsupply_entry.grid(row=dig_out_row1, column=1)

        Label(self.parent, text="FC Purge: ").grid(row=dig_out_row2, column=0)
        self.fcpurge_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcpurge_entry.grid(row=dig_out_row2, column=1)

        Label(self.parent, text="FC Fan: ").grid(row=dig_out_row1, column=2)
        self.fcfan_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcfan_entry.grid(row=dig_out_row1, column=3)

        Label(self.parent, text="Startup Relay: ").grid(\
            row=dig_out_row1, column=4)
        self.startup_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.startup_relay_entry.grid(row=dig_out_row1, column=5)

        Label(self.parent, text="Motor Relay: ").grid(\
            row=dig_out_row2, column=4)
        self.motor_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.motor_relay_entry.grid(row=dig_out_row2, column=5)

        Label(self.parent, text="Cap Relay: ").grid(row=dig_out_row1, column=6)
        self.cap_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.cap_relay_entry.grid(row=dig_out_row1, column=7)

        Label(self.parent, text="Resistor Relay: ").grid(\
            row=dig_out_row2, column=6)
        self.resistor_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.resistor_relay_entry.grid(row=dig_out_row2, column=7)

        print "digital output values done"

    def update_digital_output_values(self):
        if DAQ_Connected:
            self.FCSupply.set(pin_value_get_dig_output(H2_VALVE))
            self.FCPurge.set(pin_value_get_dig_output(PURGE_VALVE))
            self.StartupRelay.set(pin_value_get_dig_output(STARTUP_RELAY))
            self.MotorRelay.set(pin_value_get_dig_output(MOTOR_RELAY))
            self.CapRelay.set(pin_value_get_dig_output(CAP_RELAY))
            self.ResistorRelay.set(pin_value_get_dig_output(RESISTOR_RELAY))
        else:
            self.FCFan1.set(not self.FCFan1.get())

        dig_outputs = {
            'fcsupply': (self.FCSupply.get(), self.fcsupply_entry),
            'fcpurge': (self.FCPurge.get(), self.fcpurge_entry),
            'fcfan': (self.FCFan1.get(), self.fcfan_entry),
            'startup_relay': (self.StartupRelay.get(), \
                self.startup_relay_entry),
            'motor_relay': (self.MotorRelay.get(), self.motor_relay_entry),
            'cap_relay': (self.CapRelay.get(), self.cap_relay_entry),
            'resistor_relay': (self.ResistorRelay.get(), \
                self.resistor_relay_entry)}

        for name, (value, entry) in dig_outputs.items():
            if value == 0:
                colour = self.off_colour
            else:
                colour = self.on_colour
            entry.configure(bg=colour)

        print "updated digital output values"

    def cell_voltages(self):
        start_row = 6
        self.parent.grid_rowconfigure(start_row, pad=25)

        cell_num = 0
        for y in range(self.FCCellVoltRows):
            for x in range(self.FCCellVoltCols):
                label_text = "Cell" + str(cell_num) + ": "
                label_config = {'text':label_text,
                                'width':self.entry_width}
                Label(self.parent, **label_config).grid(\
                    row=start_row + y, column=2*x)

                print(self.CellVoltages_display[cell_num])
                entry_config = {'text':self.CellVoltages_display[cell_num],
                                'justify':'center',
                                'width':self.entry_width}
                Entry(self.parent, **entry_config).grid(\
                    row =start_row + y, column=2*x + 1)

                cell_num += 1
                if cell_num >= self.FCCellCount:
                    break
            if cell_num >= self.FCCellCount:
                break

        print "cell voltages done"

    def update_cell_voltages(self):
        self.CellVoltages_display = [
            [str(self.CellVoltages[row][col].get()) for col in \
            range(self.FCCellVoltCols)] for row in \
                range(self.FCCellVoltRows)]

    def main_state_machine(self):
        while True:
            if DAQ_Connected:
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

            self.update_analog_input_values()
            self.update_digital_input_values()
            self.update_digital_output_values()
            self.parent.update_idletasks()
            self.parent.update()

        print "state machine"

if __name__ == "__main__":
    if DAQ_Connected:
        digital_configure()
        analog_configure()
    window = Tk()
    gui = TestbenchFCC_GUI(window)
    gui.main_state_machine()
