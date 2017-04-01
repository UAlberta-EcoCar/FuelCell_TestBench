# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:57:31 2017

@author: Adnan
"""
from TestBench_GPIO_Constants import *
from TestBench_ADC import *
from TestBench_GPIO_Functions import *
from TestBench_CheckAlarms_Constants import *

error_msg = "None"

def FC_check_alarms(FC_state):
  global error_msg
  
  error_msg = "None"
  if(pin_value_get_dig_output(H20K) == 0.0):
		error_msg = "FC_ERR_H2OK_LOW"
	#check temp H L and pressure H always
  if(get_FCTEMP() > HIGH_TEMP_THRES):
		error_msg = "FC_ERR_TEMP_H"
  if(get_FCTEMP() < LOW_TEMP_THRES):
		error_msg = "FC_ERR_TEMP_L"
  if(get_FCPRES() > FC_HIGH_PRES_THRES):
		error_msg = "FC_ERR_PRES_H"
  if FC_state == "FC_state_STARTUP_PURGE":
		if(get_FCPRES() > FC_HIGH_PRES_THRES):
			error_msg = "FC_ERR_PRES_H"
		if(get_FCCURR() > OVER_CUR_THRES):
			error_msg = "FC_ERR_OVER_CUR"
		if(get_FCVOLT() > OVER_VOLT_THRES):
			error_msg = "FC_ERR_OVER_VOLT"
		if(get_FCPRES() < PURGE_PRESS_LOW_THRES):
			error_msg = "FC_ERR_PURGE_PRESS_LOW"
  if FC_state == "FC_state_STARTUP_CHARGE":
		if(get_FCPRES() < FC_LOW_PRES_THRES):
			error_msg = "FC_ERR_PRES_L"
		if (get_FCPRES() > FC_HIGH_PRES_THRES):
			error_msg = "FC_ERR_PRES_H"
		if(get_FCCURR() > OVER_CUR_THRES):
			error_msg = "FC_ERR_OVER_CUR"
		if(get_FCVOLT() > OVER_VOLT_THRES):
			error_msg = "FC_ERR_OVER_VOLT"
  if FC_state == "FC_state_RUN":
		if(get_FCPRES() < FC_LOW_PRES_THRES):
			error_msg = "FC_ERR_PRES_L"
		if(get_FCPRES() > FC_HIGH_PRES_THRES):
			error_msg = "FC_ERR_PRES_H"
		if(get_FCCURR() > OVER_CUR_THRES):
			error_msg = "FC_ERR_OVER_CUR"
		if(get_FCVOLT() > OVER_VOLT_THRES):
			error_msg = "FC_ERR_OVER_VOLT"
		if(get_FCVOLT() < LOW_VOLT_THRES):
			error_msg = "FC_ERR_VOLT_LOW"
  if FC_state == "FC_state_ALARM":
		if(get_FCCURR() > OVER_CUR_THRES):
			error_msg = "FC_ERR_OVER_CUR"
  return(error_msg)
  
def get_error_msg():
    return(error_msg)