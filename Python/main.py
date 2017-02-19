# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:52:00 2017

@author: Adnan
"""

from TestBench_GPIO_Constants import *
from TestBench_GPIO_Functions import *
from TestBench_Functions import *
import DAQmxFunctions

digital_configure()
analog_configure()
FANStart()

initial_time = time.clock()
#print pin_value_get_dig(START)
#print pin_value_get_ana(TEST)
#pin_value_set_dig(H2_VALVE, 1)

while 1:
    #time1 = time.clock()
    #FANUpdate(0.999)
    #time2 = time.clock()
    #print time2 - time1
    if time.clock() - initial_time > 5:
        FANUpdate(0.5)
        initial_time = time.clock()
    elif time.clock() - initial_time > 3:
        FANUpdate(0.999)