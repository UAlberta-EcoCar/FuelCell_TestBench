# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 20:52:00 2017

@author: Adnan
"""

from TestBench_GPIO_Constants import *
from TestBench_GPIO_Functions import *

DigitalConfigure()
AnalogConfigure()

while(1):     
    print PinValueGetDig()
    print PinValueGetAna()