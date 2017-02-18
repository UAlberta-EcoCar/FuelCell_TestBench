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


#print pin_value_get_dig(START)
#print pin_value_get_ana(TEST)
#pin_value_set_dig(H2_VALVE, 1)

#while (1):
#taskHandle2 = TaskHandle(1)
#DAQmxStopTask(taskHandle1)
#DAQmxClearTask(taskHandle1)
FANUpdate(0.9)
a = raw_input("Generating pulse train. Press Enter to interrupt\n")
FANUpdate(0.999)
a = raw_input("Generating pulse train. Press Enter to interrupt\n")
FANUpdate(0.001)
a = raw_input("Generating pulse train. Press Enter to interrupt\n")

