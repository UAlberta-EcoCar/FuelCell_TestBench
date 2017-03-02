# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 16:40:54 2017

@author: Adnan
"""
# For both current sensors, the calculation is I = Volt_reading/(Gain * R_shunt)
# Resistance of shunt resistor, R_shunt is 0.001 ohms
FCCURRCoefficient = 10 # Gain is 100.
CAPCURRCoefficient = 10.60603 # Gain is 94.286.
CAPVOLTCoefficient = 11 # 10k and 1k Voltage Divider
FCVOLTCoefficient = 11 # 10k and 1k Voltage Divider
FCPRESCoefficient = 24
FCPRESConst = 24648
TANKPRESCoefficient = 0
TANKPRESConst = 0
TEMPCoefficient_x3 = -1.9553
TEMPCoefficient_x2 = 16.15
TEMPCoefficient_x = -59.671
TEMPConst = 103.39

# Using the equation y = -1.9553x3 + 16.15x2 - 59.671x + 103.39
# Check Gdrive for Excel document showing curve fit data
# Excluded temperatures from -25 to -40 deg C and 85 to 125 deg C
# to make calculation easier on Python code. More temperatures would mean
# a higher order polynomial to correctly fit the data