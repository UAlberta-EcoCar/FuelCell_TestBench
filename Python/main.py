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
#FANStart()

while 1:
    print pin_value_get_dig(START)
#print pin_value_get_ana(TEST)
#pin_value_set_dig(H2_VALVE, 1)