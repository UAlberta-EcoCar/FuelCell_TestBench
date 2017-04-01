# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 21:09:55 2017

@author: Adnan
"""

import serial
import datetime
from TestBench_CheckAlarms import *
from TestBench_Functions import *
from TestbenchFCC_GUI import *
from TestBench_ADC import *
from TestBench_GPIO_Functions import *
from TestBench_GPIO_Constants import *


def init_datalogging():
    filename = datetime.datetime.now().strftime("%Y-%m-%d--%Hh %Mm %Ss %fms")
    file_handle = open('%s.csv' %filename, 'w') # opens the csv file
    return file_handle

def datalogging(file_handle,FC_state):
    global gui
    
    file_handle.write('Time(s),FC_ERROR,FC_STATE,FC_PURGE_COUNT, \
                        FC_TIME_BETWEEN_LAST_PURGES, \
                        FC_ENERGY_SINCE_LAST_PURGE,FC_TOTAL_ENERGY, \
                        FC_CHARGE_SINCE_LAST_PURGE,FC_TOTAL_CHARGE,FC_VOLT, \
                        FC_CURR,FC_CAPVOLT,FC_TEMP,FC_OPTTEMP,FC_PRES, \
                        FC_FAN_SPEED,FC_START_RELAY,FC_RES_RELAY, \
                        FC_CAP_RELAY,FC_MOTOR_RELAY,FC_PURGE_VALVE, \
                        FC_H2_VALVE\n')
    data_line = "%s,%s,%s,%s, \
                    %s, \
                    %s,%s, \
                    %s,%s,%s, \
                    %s,%s,%s,%s,%s, \
                    %s,%s,%s, \
                    %s,%s,%s, \
                    %s" \
                    % (time.time(), get_error_msg(), FC_state, get_number_of_purges(), \
                    get_time_between_last_purges(), \
                    get_J_since_last_purge(), get_total_E(), \
                    time.time(), get_total_charge_extracted(), get_FCVOLT(), \
                    get_FCCURR(), get_CAPVOLT(), get_FCTEMP(), calc_opt_temp(), get_FCPRES(), \
                    get_duty_cycle, pin_value_get_dig_output(STARTUP_RELAY), pin_value_get_dig_output(RESISTOR_RELAY), \
                    pin_value_get_dig_output(CAP_RELAY), pin_value_get_dig_output(MOTOR_RELAY), pin_value_get_dig_output(PURGE_VALVE), \
                    pin_value_get_dig_output(H2_VALVE))
    file_handle.write(data_line)