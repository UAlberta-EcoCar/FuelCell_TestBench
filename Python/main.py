# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:52:00 2017

@author: Adnan
"""

from TestBench_GPIO_Constants import *
from TestBench_GPIO_Functions import *
from TestBench_Functions import *
from TestBench_Constants import *
import DAQmxFunctions

digital_configure()
analog_configure()
FANStart()
FC_state = "FC_STATE_STANDBY"

while 1:
    if (FC_state == "FC_STATE_STANDBY"):
        FC_state = FC_standby()
    elif (FC_state == "FC_STATE_SHUTDOWN"):
        FC_state = FC_shutdown()
    elif (FC_state == "FC_STATE_STARTUP_H2"):
        FC_state = FC_startup_h2()
    elif (FC_state == "FC_STATE_STARTUP_PURGE"):
        FC_state = FC_startup_purge()
    elif (FC_state == "FC_STATE_STARTUP_CHARGE"):
        FC_state = FC_startup_charge()
    elif (FC_state == "FC_STATE_RUN"):
        FC_state = FC_run()
    elif (FC_state == "FC_STATE_REPRESSURIZE"):
        FC_state = FC_repressurize()
    print (pin_value_get_dig_output(H2_VALVE), pin_value_get_dig_output(PURGE_VALVE),
                pin_value_get_dig_output(STARTUP_RELAY), pin_value_get_dig_output(MOTOR_RELAY),
                pin_value_get_dig_output(CAP_RELAY), pin_value_get_dig_output(RESISTOR_RELAY), FC_state)
    print get_FCVOLT(), get_FCCURR(), get_CAPVOLT(), get_CAPCURR(), get_FCTEMP(), calc_opt_temp()
    #change themistor value until current temp = opt temp
    #se if duty cycle goes close to 0, ANSWER: yes it does