# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 21:22:45 2017

@author: Adnan
"""
import time

P_control = 1000
I_control = 0
D_control = 0

accumulated_error = 0
past_temperature = 0
time_passed = 0

def PID(currentTemp, setPoint):
  global P_control
  global I_control
  global D_control
  global time_passed
  global accumulated_error
  global past_temperature
  currentTemp = currentTemp
  setPoint = setPoint
  
  #proportional part
  p_value = 0
  p_value = (currentTemp - setPoint) * P_control

  time_passed = time.clock() - time_passed #calculate time difference since last update

  #integral part
  accumulated_error = (currentTemp - setPoint)*(time_passed) + \
      accumulated_error
  i_value = accumulated_error * I_control
  
  d_value = 0
  d_value = (currentTemp - past_temperature) / (time_passed)
  d_value = d_value * D_control

  time_passed = time.clock() #record past run time
  past_temperature = currentTemp
  setPoint = ((p_value + i_value + d_value)/1023) #scale value down
  
  #precaution against possible negative numbers
  if(setPoint < 0.001):
	  setPoint = 0.001
  elif(setPoint > 0.999):
      setPoint = 0.999
  return(setPoint)

def initialize_pid():
  #initialize variables
  time_passed = time.clock()