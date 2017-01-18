""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""

from PyDAQmx import *
import numpy as np


data = np.array([1], dtype=np.uint8)

task = Task()
task.CreateDOChan("/Dev1/port0/line0","",DAQmx_Val_ChanForAllLines) #this defines the screw terminal
task.StartTask()
while (1):
    task.WriteDigitalLines(1,1,10.0,DAQmx_Val_GroupByChannel,data,None,None) #turns on a screw terminal on the DAQ device
#task.StopTask()

#do this, analog imput, digital input, digital output, pwm output

#from PyDAQmx import Task
#import numpy as np


#data = np.array([0,1,1,0,1,0,1,0], dtype=np.uint8)

#task = Task()
#task.CreateDOChan("/TestDevice/port" + X.ToString() + "/line0:7","",PyDAQmx.DAQmx_Val_ChanForAllLines) #change to python
#task.StartTask()
#task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
#task.StopTask()

#create function that passes port number X