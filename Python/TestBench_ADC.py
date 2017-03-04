# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 16:39:54 2017

@author: Adnan
"""
from TestBench_ADC_Constants import *
from TestBench_GPIO_Functions import *
from TestBench_AnalogDefs import *

def convert_temp(temp_reading_raw):
    # Third order polynomial. Check Systems Drive for calculations
    temp_reading = ((TEMPCoefficient_x3 * temp_reading_raw**3) +
        (TEMPCoefficient_x2 * temp_reading_raw**2) +
        (TEMPCoefficient_x * temp_reading_raw) +
        TEMPConst)
    return temp_reading

def get_FCTEMP1():
    return convert_temp(pin_value_get_ana(FCTEMP1))

def get_FCTEMP2():
    return convert_temp(pin_value_get_ana(FCTEMP2))

def get_FCTEMP():
    return (convert_temp((pin_value_get_ana(FCTEMP1) +
                pin_value_get_ana(FCTEMP2))/2))

def get_FCPRES():
	return (pin_value_get_ana(FCPRES) * FCPRESCoefficient - FCPRESConst)

def get_CAPCURR():
	return (pin_value_get_ana(CAPCURR) * CAPCURRCoefficient)

def get_FCCURR():
	val = pin_value_get_ana(FCCURR) * FCCURRCoefficient
	if val < 0: #filter out negative numbers b/c they mess with the current integration algorithm
		return (0)
	else:
		return (val)

def get_CAPVOLT():
	return (pin_value_get_ana(CAPVOLT) * CAPVOLTCoefficient)
	#10k and 1k voltage divider
	#CAPVOLT = DAQReading * (10k + 1k) / 1k

def get_FCVOLT():
	return(pin_value_get_ana(FCVOLT) * FCVOLTCoefficient)
	#10k and 1k voltage divider
	#FCVolt = DAQReading * (10k + 1k) / 1k
