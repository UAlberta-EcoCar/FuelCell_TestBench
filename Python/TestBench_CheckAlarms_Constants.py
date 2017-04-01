# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:55:22 2017

@author: Adnan
"""

LOW_TEMP_THRES = 0 #0C. 
HIGH_TEMP_THRES = 75 # 75C
FC_HIGH_PRES_THRES = 10 #10 PSI
FC_LOW_PRES_THRES = 2 #2.0 PSI
OVER_CUR_THRES = 75 #75A
UNDER_CUR_THRES = 0 #only possible if sensor is disconnected if in start purge 
OVER_VOLT_THRES = 50.6 #50.6V
LOW_VOLT_THRES = 15 #capacitors are drained too much 15V
PURGE_PRESS_LOW_THRES = 1 # 1 PSI