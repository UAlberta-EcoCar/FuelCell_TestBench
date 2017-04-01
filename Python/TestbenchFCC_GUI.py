# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 03:40:29 2016

@author: Adnan
"""
from Tkinter import *
import tkMessageBox
from ttk import Button, Style
from TestBench_Functions import *
from TestBench_ADC import *
from TestBench_CheckAlarms import *
from TestBench_FileDatalogging import *
import argparse
import os

class TestbenchFCC_GUI(object):
    def __init__(self,parent):
        self.args = self.get_args()

        # Main State Machine
        self.running = True
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.on_gui_close)

        # Datalogging
        if self.args.DAQ_connected:
            self.logfile = init_datalogging()

        # initialize Analog Inputs section
        self.FCTemp1 = DoubleVar()
        self.FCTemp2 = DoubleVar()
        self.FCCurr = DoubleVar()
        self.FCVolt = DoubleVar()
        self.FCPres = DoubleVar()
        self.MassFlow = DoubleVar()
        self.CapVolt = DoubleVar()
        self.FCChargeSLP = DoubleVar()
        self.CapCurr = DoubleVar()

        # Colours for digital signals
        self.on_colour = "green"
        self.off_colour = "blue"

        # Initialize Digital Inputs section
        self.H2OK = IntVar()
        self.FCStart = IntVar()

        # Initialize Digital Outputs section
        self.FCSupply = IntVar()
        self.FCPurge = IntVar()
        self.StartupRelay = IntVar()
        self.MotorRelay = IntVar()
        self.CapRelay = IntVar()
        self.ResistorRelay = IntVar()
        self.FCFanDutyCycle = DoubleVar()

        # Initialize Debug section
        self.FC_state = "FC_STATE_STANDBY"
        self.errormsg = ""

        # Initialize FC Stack Selection section
        self.curr_stack = StringVar()
        self.curr_stack.set("Alice")
        self.last_stack = StringVar()
        self.last_stack.set("Alice")
        self.FCCellCounts = {
            "Alice": 46,
            "Prototype": 21
        }

        # Initialize CVM Section
        self.PurgeNow = IntVar()
        self.PurgeDisconnect = IntVar()
        self.FCCellVoltRows = 16
        self.FCCellVoltCols = 3
        self.MaxFCCellCount = self.FCCellCounts.get("Alice")
        self.CellVoltages = []
        self.CellVoltages_display = []
        self.CellVoltages_entries = []
        for i in range(self.MaxFCCellCount):
            self.CellVoltages.append(DoubleVar())
            self.CellVoltages_display.append(StringVar())
            self.CellVoltages[i].set(0.0)
            self.CellVoltages_display[i].set(str(self.CellVoltages[i].get()))

        # Build_gui
        self.parent = parent
        self.parent.title("Fuel Cell TestBench of Awesomeness")
        self.window_width = 1366 # Most common laptop screen resolution size
        self.window_height = 768
        self.parent.minsize(self.window_width,self.window_height)

        self.maincontainer = Frame(parent)
        self.maincontainer.pack(side='top', fill='both', expand='true')

        self.leftcontainer = Frame(self.maincontainer)
        self.leftcontainer.pack(side='left', fill='both', expand='true')
        self.leftcontainer_top = Frame(self.leftcontainer)
        self.leftcontainer_top.pack(fill='both', expand='true')
        self.leftcontainer_bottom = Frame(self.leftcontainer)
        self.leftcontainer_bottom.pack(fill='both', expand='true')
        self.leftcontainer_bottom_left = Frame(self.leftcontainer_bottom,)
        self.leftcontainer_bottom_left.pack(side='left', fill='both',
                                            expand='true')
        self.leftcontainer_bottom_right = Frame(self.leftcontainer_bottom,)
        self.leftcontainer_bottom_right.pack(side='right', fill='both',
                                            expand='true')

        self.rightcontainer = Frame(self.maincontainer)
        self.rightcontainer.pack(side='right', fill='both', expand='true')

        self.entry_width = 10
        self.analog_inputs()
        self.digital_inputs()
        self.digital_outputs()
        self.debug()
        self.stack_select()
        self.cvm()

        # print "init done"

    def get_args(self):
        parser = argparse.ArgumentParser(
            description='GUI for FCC Testbench',
            formatter_class=argparse.RawTextHelpFormatter,
            )

        parser.add_argument("--nodaq",
            help="Daq is not connected, allows for independent testing of GUI",
            action="store_false",
            dest="DAQ_connected")

        parser.set_defaults(DAQ_connected=True)

        args = parser.parse_args()

        return args

    def update_digital_entries(self, digital_signals,
                                off_colour="", on_colour=""):
        if off_colour == "":
            off_colour = self.off_colour
        if on_colour == "":
            on_colour = self.on_colour
        for (value, entry) in digital_signals.values():
            if value == 0:
                colour = off_colour
            else:
                colour = on_colour
            entry.configure(bg=colour)

    def update_analog_entries(self,analog_signals):
        for (value, entry) in analog_signals.values():
            entry.delete(0, END)
            entry.insert(0, str(value))

    def analog_inputs(self):
        container = self.leftcontainer_top
        analog_title_row = 0
        analog_in_row1 = 1
        analog_in_row2 = 2
        analog_in_row3 = 3

        container.grid_rowconfigure(analog_title_row, pad=50)
        container.grid_rowconfigure(analog_in_row1, pad=25)
        container.grid_rowconfigure(analog_in_row2, pad=25)
        container.grid_rowconfigure(analog_in_row3, pad=25)

        container.grid_columnconfigure(0, pad=50)
        container.grid_columnconfigure(2, pad=50)
        container.grid_columnconfigure(4, pad=50)

        Label(container, text="Analog Inputs", font=('bold')).grid(\
            row=analog_title_row, column=0, columnspan=6)

        Label(container, text="FC Temp 1 (*C): ").grid(\
            row=analog_in_row1, column=0)
        self.fctemp1_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fctemp1_entry.grid(row=analog_in_row1, column=1)

        Label(container, text="FC Temp 2 (*C): ").grid(\
            row=analog_in_row1, column=2)
        self.fctemp2_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fctemp2_entry.grid(row=analog_in_row1, column=3)

        Label(container, text="FC Pressure (PSI): ").grid(\
            row=analog_in_row1, column = 4)
        self.fcpres_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fcpres_entry.grid(row=analog_in_row1, column=5)

        Label(container, text="FC Voltage (V): ").grid(\
            row=analog_in_row2, column=0)
        self.fcvolt_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fcvolt_entry.grid(row=analog_in_row2, column=1)

        Label(container, text="FC Current (A): ").grid(\
            row=analog_in_row2, column=2)
        self.fccurr_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fccurr_entry.grid(row=analog_in_row2, column=3)

        Label(container,
            text="FC Charge since last purge (C): ").grid(
                row=analog_in_row2, column=4)
        self.fcchargeslp_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fcchargeslp_entry.grid(row=analog_in_row2, column=5)

        Label(container, text="Cap Voltage (V): ").grid(\
            row=analog_in_row3, column=0)
        self.capvolt_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.capvolt_entry.grid(row=analog_in_row3, column=1)

        Label(container, text="Cap Current (A): ").grid(\
            row=analog_in_row3, column=2)
        self.capcurr_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.capcurr_entry.grid(row=analog_in_row3, column=3)

        Label(container, text="Mass Flow (L/min): ").grid(\
            row=analog_in_row3, column=4)
        self.massflow_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.massflow_entry.grid(row=analog_in_row3, column=5)


        # print "analog input vals done"

    def update_analog_inputs(self):
        if self.args.DAQ_connected:
            self.FCTemp1.set(get_FCTEMP1())
            self.FCTemp2.set(get_FCTEMP2())
            self.FCCurr.set(get_FCCURR())
            self.FCVolt.set(get_FCVOLT())
            self.FCPres.set(get_FCPRES())
            self.MassFlow.set(get_MASSFLOW())
            self.CapVolt.set(get_CAPVOLT())
            self.FCChargeSLP.set(get_charge_since_last_purge())
            self.CapCurr.set(get_CAPCURR())
        analog_in = {
            'fctemp1': (self.FCTemp1.get(), self.fctemp1_entry),
            'fctemp2': (self.FCTemp2.get(), self.fctemp2_entry),
            'fcvolt': (self.FCVolt.get(), self.fcvolt_entry),
            'fccurr': (self.FCCurr.get(), self.fccurr_entry),
            'fcpres': (self.FCPres.get(), self.fcpres_entry),
            'capvolt': (self.CapVolt.get(), self.capvolt_entry),
            'capcurr': (self.CapCurr.get(), self.capcurr_entry),
            'massflow': (self.MassFlow.get(), self.massflow_entry),
            'fcchargeslp': (self.FCChargeSLP.get(), self.fcchargeslp_entry)}

        self.update_analog_entries(analog_in)

        # print "updated analog input vals"

    def digital_inputs(self):
        container = self.leftcontainer_top
        dig_title_row = 4
        dig_in_row1 = 5

        container.grid_rowconfigure(dig_title_row, pad=50)
        container.grid_rowconfigure(dig_in_row1, pad=25)

        container.grid_columnconfigure(0, pad=50)
        container.grid_columnconfigure(2, pad=50)

        Label(container, text="Digital Inputs", font=('bold')).grid(\
            row=dig_title_row, column=0, columnspan=6)

        Label(container, text="H20K: ").grid(row=dig_in_row1, column=0)
        self.h2ok_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.h2ok_entry.grid(row=dig_in_row1, column=1)

        Label(container, text="FC Start: ").grid(
            row=dig_in_row1, column=2)
        self.fcstart_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fcstart_entry.grid(row=dig_in_row1, column=3)

        # print "digital input vals done"

    def update_digital_inputs(self):
        if self.args.DAQ_connected:
            self.H2OK.set(pin_value_get_dig(H20K))
            self.FCStart.set(pin_value_get_dig(START))

        dig_in = {
            'fcstart': (self.FCStart.get(), self.fcstart_entry)}

        dig_in_2 = {
            'h20k': (self.H2OK.get(), self.h2ok_entry)}

        self.update_digital_entries(dig_in)
        self.update_digital_entries(dig_in_2, off_colour='red')

        # print "updated digital input vals"

    def digital_outputs(self):
        container = self.leftcontainer_top
        dig_out_title_row = 6
        dig_out_row1 = 7
        dig_out_row2 = 8
        dig_out_row3 = 9

        container.grid_rowconfigure(dig_out_title_row, pad=50)
        container.grid_rowconfigure(dig_out_row1, pad=25)
        container.grid_rowconfigure(dig_out_row2, pad=25)
        container.grid_rowconfigure(dig_out_row3, pad=25)

        container.grid_columnconfigure(0, pad=50)
        container.grid_columnconfigure(2, pad=50)
        container.grid_columnconfigure(4, pad=50)

        Label(container, text="Digital Outputs", font=('bold')).grid(\
            row=dig_out_title_row, column=0, columnspan=6)

        Label(container, text="FC Supply: ").grid(
            row=dig_out_row1, column=0)
        self.fcsupply_entry = \
            Entry(container,justify='center', width=self.entry_width)
        self.fcsupply_entry.grid(row=dig_out_row1, column=1)

        Label(container, text="FC Purge: ").grid(
            row=dig_out_row1, column=2)
        self.fcpurge_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fcpurge_entry.grid(row=dig_out_row1, column=3)

        Label(container, text="FC Fan Duty Cycle: ").grid(\
            row=dig_out_row1, column=4)
        self.fcfan_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.fcfan_entry.grid(row=dig_out_row1, column=5)

        Label(container, text="Startup Relay: ").grid(\
            row=dig_out_row2, column=0)
        self.startup_relay_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.startup_relay_entry.grid(row=dig_out_row2, column=1)

        Label(container, text="Motor Relay: ").grid(\
            row=dig_out_row2, column=2)
        self.motor_relay_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.motor_relay_entry.grid(row=dig_out_row2, column=3)

        Label(container, text="Cap Relay: ").grid(
            row=dig_out_row3, column=0)
        self.cap_relay_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.cap_relay_entry.grid(row=dig_out_row3, column=1)

        Label(container, text="Resistor Relay: ").grid(\
            row=dig_out_row3, column=2)
        self.resistor_relay_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.resistor_relay_entry.grid(row=dig_out_row3, column=3)

        # print "digital output values done"

    def update_digital_outputs(self):
        if self.args.DAQ_connected:
            self.FCSupply.set(pin_value_get_dig_output(H2_VALVE))
            self.FCPurge.set(pin_value_get_dig_output(PURGE_VALVE))
            self.StartupRelay.set(pin_value_get_dig_output(STARTUP_RELAY))
            self.MotorRelay.set(pin_value_get_dig_output(MOTOR_RELAY))
            self.CapRelay.set(pin_value_get_dig_output(CAP_RELAY))
            self.ResistorRelay.set(pin_value_get_dig_output(RESISTOR_RELAY))

        dig_out= {
            'fcsupply': (self.FCSupply.get(), self.fcsupply_entry),
            'fcpurge': (self.FCPurge.get(), self.fcpurge_entry),
            'startup_relay': (self.StartupRelay.get(), \
                self.startup_relay_entry),
            'motor_relay': (self.MotorRelay.get(), self.motor_relay_entry),
            'cap_relay': (self.CapRelay.get(), self.cap_relay_entry),
            'resistor_relay': (self.ResistorRelay.get(), \
                self.resistor_relay_entry)
            }

        pwm = {
            'fcfan duty_cycle': (self.FCFanDutyCycle.get(), self.fcfan_entry)
            }

        self.update_digital_entries(dig_out)
        self.update_analog_entries(pwm)

        # print "updated digital output values"

    def debug(self):
        container = self.leftcontainer_bottom_left
        debug_title_row = 0
        debug_row_1 = 1
        debug_row_2 = 2

        container.grid_rowconfigure(debug_title_row, pad=50)
        container.grid_rowconfigure(debug_row_1, pad=25)
        container.grid_rowconfigure(debug_row_2, pad=25)

        container.grid_columnconfigure(0, pad=50)
        container.grid_columnconfigure(2, pad=50)
        container.grid_columnconfigure(4, pad=50)

        Label(container, text="Debug", font=('bold')).grid(\
            row=debug_title_row, column=0, columnspan=6)

        Label(container, text="FC State: ").grid(
            row=debug_row_1, column=0)
        self.fcstate_entry = \
            Entry(container,justify='center', width=3*self.entry_width)
        self.fcstate_entry.grid(row=debug_row_1, column=1)

        Label(container, text="Error Msg: ").grid(
            row=debug_row_2, column=0)
        self.errormsg_text = Text(container, width=25, height=10)
        self.errormsg_text.grid(row=debug_row_2, column=1)
        self.errormsg_text.insert(END, self.errormsg_text)

    def update_debug(self):
        self.fcstate_entry.delete(0, END)
        self.fcstate_entry.insert(0, self.FC_state)
        self.errormsg_text.delete(1.0, END)
        self.errormsg_text.insert(1.0, self.errormsg)

    def stack_select(self):
        container = self.leftcontainer_bottom_right
        stack_select_title_row = 0
        stack_select_row1 = 1
        stack_select_row2 = 2

        container.grid_rowconfigure(stack_select_title_row, pad=50)
        container.grid_rowconfigure(stack_select_row1, pad=25)

        Label(container, text="Stack Selection", font=('bold')).grid(\
            row=stack_select_title_row, column=0, columnspan=6)

        rb_alice = Radiobutton(container, text="Alice",
            variable=self.curr_stack, value="Alice")
        rb_alice.grid(row=stack_select_row1, column=0, sticky='w')
        rb_prototype = Radiobutton(container, text="Prototype",
            variable=self.curr_stack, value="Prototype")
        rb_prototype.grid(row=stack_select_row2, column=0, sticky='w')

    def cvm(self):
        container = self.rightcontainer
        cvm_title_row = 0
        cvm_start_row = 1
        cell_volt_start_row = 2
        cell_volt_start_col = 0

        container.grid_rowconfigure(cvm_title_row, pad=50)
        container.grid_rowconfigure(cvm_start_row, pad=25)

        container.grid_columnconfigure(0, pad=50)
        container.grid_columnconfigure(1, pad=50)
        container.grid_columnconfigure(2, pad=50)
        container.grid_columnconfigure(3, pad=50)
        container.grid_columnconfigure(4, pad=50)

        Label(container, text="CVM", font=('bold')).grid(\
            row=cvm_title_row, column=0, columnspan=6)

        Label(container, text="Purge Now").grid(\
            row=cvm_start_row, column=0)
        self.purge_now_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.purge_now_entry.grid(row=cvm_start_row, column=1)

        Label(container, text="Purge Disconnect").grid(\
            row=cvm_start_row, column=2)
        self.purge_disconnect_entry = \
            Entry(container, justify='center', width=self.entry_width)
        self.purge_disconnect_entry.grid(row=cvm_start_row, column=3)

        cell_num = 0
        for y in xrange(self.FCCellVoltRows):
            container.grid_rowconfigure(cell_volt_start_row + y, pad=25)
            for x in xrange(self.FCCellVoltCols):
                label_text = "Cell" + str(cell_num) + ": "
                label_config = {'text':label_text,
                                'width':self.entry_width}
                l = Label(container, **label_config)
                l.grid(row=cell_volt_start_row + y, \
                        column=cell_volt_start_col + 2*x)

                entry_config = {
                    'textvariable':self.CellVoltages_display[cell_num],
                    'justify':'center',
                    'width':self.entry_width,
                    'disabledbackground':container['bg'],
                    'disabledforeground':container['bg'],
                }
                e = Entry(container, **entry_config)
                e.grid(row=cell_volt_start_row + y, \
                        column=cell_volt_start_col + 2*x + 1)

                self.CellVoltages_entries.append(e)
                cell_num += 1
                if cell_num >= self.MaxFCCellCount:
                    break
            if cell_num >= self.MaxFCCellCount:
                break

        # print "cell voltages done"

    def update_cvm(self):
        # Somehow get cell voltage values from cvm board
        cvm_dig_signals = {
            'purge_now': (self.PurgeNow.get(), self.purge_now_entry),
            'purge_disconnect_entry': (self.PurgeDisconnect.get(), \
                                        self.purge_disconnect_entry)
        }

        self.update_digital_entries(cvm_dig_signals)

        for i in xrange(0, self.FCCellCounts.get("Alice")):
            self.CellVoltages_display[i].set(str(self.CellVoltages[i].get()))

        if self.curr_stack.get() != self.last_stack.get():
            self.last_stack.set(self.curr_stack.get())

            start = self.FCCellCounts.get("Prototype")
            end = self.FCCellCounts.get("Alice")
            for i in xrange(start, end):
                if self.curr_stack.get() == "Prototype":
                    self.CellVoltages_entries[i].configure(state='disabled')
                else:
                    self.CellVoltages_entries[i].configure(state='normal')

    def main_state_machine(self):
        # DAQ Config
        if self.args.DAQ_connected:
            digital_configure()
            analog_configure()
            FANStart()

        # Main State Machine
        while self.running:
            if self.args.DAQ_connected:
                if (self.FC_state == "FC_STATE_STANDBY"):
                    self.FC_state = FC_standby()
                elif (self.FC_state == "FC_STATE_SHUTDOWN"):
                    self.FC_state = FC_shutdown()
                    # elif (self.FC_state == "FC_STATE_STARTUP_FANS"):
                    #     # Ignore implementation for now
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
                FC_check_alarms(self.FC_state)
                datalogging(self.logfile, self.FC_state)

            self.errormsg = get_error_msg()
            self.update_analog_inputs()
            self.update_digital_inputs()
            self.update_digital_outputs()
            self.update_cvm()
            self.update_debug()
            self.parent.update_idletasks()
            self.parent.update()
        # print "state machine"

    def on_gui_close(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            if self.args.DAQ_connected:
                end_datalogging(self.logfile)
                print("File closed (hopefully)")

            print("gui died!")
            self.running = False
            self.parent.destroy()

if __name__ == "__main__":
    window = Tk()
    gui = TestbenchFCC_GUI(window)
    gui.main_state_machine()
