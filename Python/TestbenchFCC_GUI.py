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
from TestBench_ADC import *
import DAQmxFunctions

class TestbenchFCC_GUI(Frame):
    def __init__(self,parent):
        self.parent = parent

        # DAQ Config
        digital_configure()
        analog_configure()
        FANStart()

        # initialize Analog Inputs
        self.FCTemp1 = DoubleVar()
        self.FCTemp2 = DoubleVar()
        self.FCCurr = DoubleVar()
        self.FCVolt = DoubleVar()
        self.FCPres = DoubleVar()
        self.MassFlow = DoubleVar()
        self.CapVolt = DoubleVar()
        self.FCChargeSLP = DoubleVar()
        self.FCTemp1.set(get_FCTEMP1())
        self.FCTemp2.set(get_FCTEMP2())
        self.FCCurr.set(get_FCCURR())
        self.FCVolt.set(get_FCVOLT())
        self.FCPres.set(get_FCPRES())
        self.MassFlow.set(0)
        self.CapVolt.set(get_CAPVOLT())
        self.FCChargeSLP.set(0)

        # Colours for digital signals
        self.on_colour = "green"
        self.off_colour = "blue"

        # Initialize Digital Inputs
        self.H2OK = IntVar()
        self.FCStart = IntVar()
        self.H2OK.set(pin_value_get_dig_output(H20K))
        self.FCStart.set(pin_value_get_dig_output(START))

        # Initialize Digital Outputs
        self.FCSupply = IntVar()
        self.FCPurge = IntVar()
        self.StartupRelay = IntVar()
        self.MotorRelay = IntVar()
        self.CapRelay = IntVar()
        self.ResistorRelay = IntVar()
        self.FCFan1 = IntVar()
        self.FCSupply.set(pin_value_get_dig_output(H2_VALVE))
        self.FCPurge.set(pin_value_get_dig_output(PURGE_VALVE))
        self.StartupRelay.set(pin_value_get_dig_output(STARTUP_RELAY))
        self.MotorRelay.set(pin_value_get_dig_output(MOTOR_RELAY))
        self.CapRelay.set(pin_value_get_dig_output(CAP_RELAY))
        self.ResistorRelay.set(pin_value_get_dig_output(RESISTOR_RELAY))

        # Initialize CVM Section
        self.PurgeNow = IntVar()
        self.PurgeDisconnect = IntVar()
        self.PurgeNow.set(0)
        self.PurgeDisconnect.set(0)
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

        # Initialize Debug section
        self.FC_state = "FC_STATE_STANDBY"
        self.errormsg = ""

        # Build_gui
        self.parent.title("Fuel Cell TestBench of Awesomeness")
        self.window_width = 1200 # Most common laptop screen resolution size
        self.window_height = 675
        # self.parent.maxsize(self.window_width,self.window_height)
        self.parent.minsize(self.window_width,self.window_height)

        self.entry_width = 10
        self.analog_inputs()
        self.digital_inputs()
        self.digital_outputs()
        self.debug()
        self.cvm()

        # print "init done"

    def update_digital_entries(self,digital_signals):
        for (value, entry) in digital_signals.values():
            if value == 0:
                colour = self.off_colour
            else:
                colour = self.on_colour
            entry.configure(bg=colour)

    def update_analog_entries(self,analog_signals):
        for (value, entry) in analog_signals.values():
            entry.delete(0, END)
            entry.insert(0, str(value))

    def analog_inputs(self):
        analog_title_row = 0
        analog_in_row1 = 1
        analog_in_row2 = 2
        analog_in_row3 = 3

        self.parent.grid_rowconfigure(analog_title_row, pad=50)
        self.parent.grid_rowconfigure(analog_in_row1, pad=25)
        self.parent.grid_rowconfigure(analog_in_row2, pad=25)
        self.parent.grid_rowconfigure(analog_in_row3, pad=25)

        self.parent.grid_columnconfigure(0, pad=50)
        self.parent.grid_columnconfigure(2, pad=50)
        self.parent.grid_columnconfigure(4, pad=50)


        Label(self.parent, text="Analog Inputs").grid(\
            row=analog_title_row, column=0, columnspan=8)

        Label(self.parent, text="FC Temp 1: ").grid(\
            row=analog_in_row1, column=0)
        self.fctemp1_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fctemp1_entry.grid(row=analog_in_row1, column=1)

        Label(self.parent, text="FC Temp 2: ").grid(\
            row=analog_in_row1, column=2)
        self.fctemp2_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fctemp2_entry.grid(row=analog_in_row1, column=3)

        Label(self.parent, text="FC Voltage: ").grid(\
            row=analog_in_row2, column=0)
        self.fcvolt_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcvolt_entry.grid(row=analog_in_row2, column=1)

        Label(self.parent, text="FC Current: ").grid(\
            row=analog_in_row2, column=2)
        self.fccurr_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fccurr_entry.grid(row=analog_in_row2, column=3)

        Label(self.parent, text="FC Pressure: ").grid(\
            row=analog_in_row2, column = 4)
        self.fcpres_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcpres_entry.grid(row=analog_in_row2, column=5)

        Label(self.parent, text="Cap Voltage: ").grid(\
            row=analog_in_row3, column=0)
        self.capvolt_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.capvolt_entry.grid(row=analog_in_row3, column=1)

        Label(self.parent, text="Mass Flow: ").grid(\
            row=analog_in_row3, column=2)
        self.massflow_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.massflow_entry.grid(row=analog_in_row3, column=3)

        Label(self.parent, text="FC Charge since last purge: ").grid(\
            row=analog_in_row3, column=4)
        self.fcchargeslp_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcchargeslp_entry.grid(row=analog_in_row3, column=5)

        # print "analog input vals done"

    def update_analog_inputs(self):
        self.FCTemp1.set(get_FCTEMP1())
        self.FCTemp2.set(get_FCTEMP2())
        self.FCCurr.set(get_FCCURR())
        self.FCVolt.set(get_FCVOLT())
        self.FCPres.set(get_FCPRES())
        # self.MassFlow.set(0)
        self.CapVolt.set(get_CAPVOLT())
        # self.FCChargeSLP.set(0)
        analog_in = {
            'fctemp1': (self.FCTemp1.get(), self.fctemp1_entry),
            'fctemp2': (self.FCTemp2.get(), self.fctemp2_entry),
            'fcvolt': (self.FCVolt.get(), self.fcvolt_entry),
            'fccurr': (self.FCCurr.get(), self.fccurr_entry),
            'fcpres': (self.FCPres.get(), self.fcpres_entry),
            'capvolt': (self.CapVolt.get(), self.capvolt_entry),
            'massflow': (self.MassFlow.get(), self.massflow_entry),
            'fcchargeslp': (self.FCChargeSLP.get(), self.fcchargeslp_entry)}

        self.update_analog_entries(analog_in)

        # print "updated analog input vals"

    def digital_inputs(self):
        dig_title_row = 4
        dig_in_row1 = 5

        self.parent.grid_rowconfigure(dig_title_row, pad=50)
        self.parent.grid_rowconfigure(dig_in_row1, pad=25)

        self.parent.grid_columnconfigure(0, pad=50)
        self.parent.grid_columnconfigure(2, pad=50)

        Label(self.parent, text="Digital Inputs").grid(\
            row=dig_title_row, column=0, columnspan=8)

        Label(self.parent, text="H20K: ").grid(row=dig_in_row1, column=0)
        self.h2ok_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.h2ok_entry.grid(row=dig_in_row1, column=1)

        Label(self.parent, text="FC Start: ").grid(row=dig_in_row1, column=2)
        self.fcstart_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcstart_entry.grid(row=dig_in_row1, column=3)

        # print "digital input vals done"

    def update_digital_inputs(self):
        self.H2OK.set(pin_value_get_dig(H20K))
        self.FCStart.set(pin_value_get_dig_output(START))

        dig_in = {
            'h20k': (self.H2OK.get(), self.h2ok_entry),
            'fcstart': (self.FCStart.get(), self.fcstart_entry)}

        self.update_digital_entries(dig_in)

        # print "updated digital input vals"

    def digital_outputs(self):
        dig_out_title_row = 6
        dig_out_row1 = 7
        dig_out_row2 = 8
        dig_out_row3 = 9

        self.parent.grid_rowconfigure(dig_out_title_row, pad=50)
        self.parent.grid_rowconfigure(dig_out_row1, pad=25)
        self.parent.grid_rowconfigure(dig_out_row2, pad=25)

        self.parent.grid_columnconfigure(0, pad=50)
        self.parent.grid_columnconfigure(2, pad=50)
        self.parent.grid_columnconfigure(4, pad=50)

        Label(self.parent, text="Digital Outputs").grid(\
            row=dig_out_title_row, column=0, columnspan=8)

        Label(self.parent, text="FC Supply: ").grid(row=dig_out_row1, column=0)
        self.fcsupply_entry = \
            Entry(self.parent,justify='center', width=self.entry_width)
        self.fcsupply_entry.grid(row=dig_out_row1, column=1)

        Label(self.parent, text="FC Purge: ").grid(row=dig_out_row1, column=2)
        self.fcpurge_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcpurge_entry.grid(row=dig_out_row1, column=3)

        Label(self.parent, text="FC Fan: ").grid(row=dig_out_row1, column=4)
        self.fcfan_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.fcfan_entry.grid(row=dig_out_row1, column=5)

        Label(self.parent, text="Startup Relay: ").grid(\
            row=dig_out_row2, column=0)
        self.startup_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.startup_relay_entry.grid(row=dig_out_row2, column=1)

        Label(self.parent, text="Motor Relay: ").grid(\
            row=dig_out_row2, column=2)
        self.motor_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.motor_relay_entry.grid(row=dig_out_row2, column=3)

        Label(self.parent, text="Cap Relay: ").grid(row=dig_out_row3, column=0)
        self.cap_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.cap_relay_entry.grid(row=dig_out_row3, column=1)

        Label(self.parent, text="Resistor Relay: ").grid(\
            row=dig_out_row3, column=2)
        self.resistor_relay_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.resistor_relay_entry.grid(row=dig_out_row3, column=3)

        # print "digital output values done"

    def update_digital_outputs(self):
        self.FCSupply.set(pin_value_get_dig_output(H2_VALVE))
        self.FCPurge.set(pin_value_get_dig_output(PURGE_VALVE))
        self.StartupRelay.set(pin_value_get_dig_output(STARTUP_RELAY))
        self.MotorRelay.set(pin_value_get_dig_output(MOTOR_RELAY))
        self.CapRelay.set(pin_value_get_dig_output(CAP_RELAY))
        self.ResistorRelay.set(pin_value_get_dig_output(RESISTOR_RELAY))

        dig_out= {
            'fcsupply': (self.FCSupply.get(), self.fcsupply_entry),
            'fcpurge': (self.FCPurge.get(), self.fcpurge_entry),
            'fcfan': (self.FCFan1.get(), self.fcfan_entry),
            'startup_relay': (self.StartupRelay.get(), \
                self.startup_relay_entry),
            'motor_relay': (self.MotorRelay.get(), self.motor_relay_entry),
            'cap_relay': (self.CapRelay.get(), self.cap_relay_entry),
            'resistor_relay': (self.ResistorRelay.get(), \
                self.resistor_relay_entry)}

        self.update_digital_entries(dig_out)

        # print "updated digital output values"

    def debug(self):
        debug_title_row = 10
        debug_row_1 = 11
        debug_row_2 = 12

        self.parent.grid_rowconfigure(debug_title_row, pad=50)
        self.parent.grid_rowconfigure(debug_row_1, pad=25)
        self.parent.grid_rowconfigure(debug_row_2, pad=25)

        self.parent.grid_columnconfigure(0, pad=50)
        self.parent.grid_columnconfigure(2, pad=50)
        self.parent.grid_columnconfigure(4, pad=50)

        Label(self.parent, text="Debug").grid(\
            row=debug_title_row, column=0, columnspan=8)

        Label(self.parent, text="FC State: ").grid(row=debug_row_1, column=0)
        self.fcstate_entry = \
            Entry(self.parent,justify='center', width=3*self.entry_width)
        self.fcstate_entry.grid(row=debug_row_1, column=1)

        Label(self.parent, text="Error Msg: ").grid(row=debug_row_2, column=0)
        self.errormsg_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.errormsg_entry.grid(row=debug_row_2, column=1)
        # self.errormsg_text = Text(self.parent, width=25, height=10)
        # self.errormsg_text.grid(row=debug_row_2, column=1)

    def update_debug(self):
        self.fcstate_entry.delete(0, END)
        self.fcstate_entry.insert(0, self.FC_state)

    def cvm(self):
        cvm_title_row = 0
        cvm_start_row = 1
        cell_volt_start_row = 2
        cell_volt_start_col = 8

        self.parent.grid_rowconfigure(cvm_title_row, pad=50)
        self.parent.grid_rowconfigure(cvm_start_row, pad=25)

        self.parent.grid_columnconfigure(8, pad=50)
        self.parent.grid_columnconfigure(9, pad=50)
        self.parent.grid_columnconfigure(10, pad=50)
        self.parent.grid_columnconfigure(11, pad=50)
        self.parent.grid_columnconfigure(12, pad=50)

        Label(self.parent, text="CVM").grid(\
            row=cvm_title_row, column=8, columnspan=8)

        Label(self.parent, text="Purge Now").grid(\
            row=cvm_start_row, column=8)
        self.purge_now_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.purge_now_entry.grid(row=cvm_start_row, column=9)

        Label(self.parent, text="Purge Disconnect").grid(\
            row=cvm_start_row, column=10)
        self.purge_disconnect_entry = \
            Entry(self.parent, justify='center', width=self.entry_width)
        self.purge_disconnect_entry.grid(row=cvm_start_row, column=11)

        cell_num = 0
        for y in range(self.FCCellVoltRows):
            self.parent.grid_rowconfigure(cell_volt_start_row + y, pad=25)
            for x in range(self.FCCellVoltCols):
                label_text = "Cell" + str(cell_num) + ": "
                label_config = {'text':label_text,
                                'width':self.entry_width}
                l = Label(self.parent, **label_config)
                l.grid(row=cell_volt_start_row + y, \
                        column=cell_volt_start_col + 2*x)

                print(self.CellVoltages_display[cell_num])
                entry_config = {'text':self.CellVoltages_display[cell_num],
                                'justify':'center',
                                'width':self.entry_width}
                e = Entry(self.parent, **entry_config)
                e.grid(row=cell_volt_start_row + y, \
                        column=cell_volt_start_col + 2*x + 1)

                cell_num += 1
                if cell_num >= self.FCCellCount:
                    break
            if cell_num >= self.FCCellCount:
                break

        # print "cell voltages done"

    def update_cvm(self):
        # Somehow update cell voltage values
        cvm_dig_signals = {
            'purge_now': (self.PurgeNow.get(), self.purge_now_entry),
            'purge_disconnect_entry': (self.PurgeDisconnect.get(), \
                self.purge_disconnect_entry)}

        self.update_digital_entries(cvm_dig_signals)

        for i in range(self.FCCellCount):
            self.CellVoltages_display[i].set(str(self.CellVoltages[i].get()))

    def main_state_machine(self):
        while True:
            if (self.FC_state == "FC_STATE_STANDBY"):
                self.FC_state = FC_standby()
            elif (self.FC_state == "FC_STATE_SHUTDOWN"):
                self.FC_state = FC_shutdown()
            # elif (self.FC_state == "FC_STATE_STARTUP_FANS"):
            #     # Ignore implementation for now, since fan stuff not working atm
            #     pass
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

            self.update_analog_inputs()
            self.update_digital_inputs()
            self.update_digital_outputs()
            self.update_cvm()
            self.update_debug()
            self.parent.update_idletasks()
            self.parent.update()
        # print "state machine"

if __name__ == "__main__":
    window = Tk()
    gui = TestbenchFCC_GUI(window)
    gui.main_state_machine()
