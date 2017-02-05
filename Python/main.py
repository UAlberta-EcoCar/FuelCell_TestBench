# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:52:00 2017

@author: Adnan
"""

from TestBench_GPIO_Constants import *
from TestBench_GPIO_Functions import *
from TestBench_Functions import *



digital_configure()
analog_configure()


#print pin_value_get_dig(START)
#print pin_value_get_ana(TEST)
#pin_value_set_dig(H2_VALVE, 1)

while (1):
    print FC_startup_charge()