from MultiChannelAnalogInput import *
from TestBench_GPIO_Constants import *
from PyDAQmx import *
import numpy

def AnalogConfigure():
      global multipleAI
      multipleAI = MultiChannelAnalogInput(["Dev1/ai13","Dev1/ai14"])
      multipleAI.configure()
      
def PinValueGetAna():
    return multipleAI.read("test")

def DigitalConfigure():
    global digital_input1
    global digital_input2
    #global digital_input3
    global digital_output1

    digital_input1 = Task()
    digital_input2 = Task()
    #digital_input3 = Task()
    digital_output1 = Task()

    digital_input1.CreateDIChan("Dev1/port0/line0:7", "", DAQmx_Val_ChanForAllLines)
    digital_input2.CreateDIChan("Dev1/port1/line0:7", "", DAQmx_Val_ChanForAllLines)
    #digital_input3.CreateDIChan("Dev1/port2/line0:7", "", DAQmx_Val_ChanForAllLines)
    digital_output1.CreateDOChan("/Dev1/port2/line0","",DAQmx_Val_ChanForAllLines)
    # DAQmx Start Code
    digital_input1.StartTask()
    digital_input2.StartTask()
    #digital_input3.StartTask()
    digital_output1.StartTask()
    global read 
    read = int32()
    
def PinValueGetDig():
    data1 = numpy.array(numpy.zeros(16, dtype=numpy.uint32))
    data2 = numpy.array(numpy.zeros(16, dtype=numpy.uint32))
    data3 = numpy.array(numpy.zeros(16, dtype=numpy.uint32))
    digital_input1.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data1, 1000, byref(read), None)
    digital_input2.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data2, 1000, byref(read), None)
    digital_input3.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data3, 1000, byref(read), None)
    dataAll = numpy.concatenate((data1,data2,data3))
    digital_input1.StopTask()
    digital_input2.StopTask()
    digital_input3.StopTask()
    return dataAll

def PinValueSetDig():
    data = numpy.array([1], dtype = numpy.uint8)
    digital_output1.WriteDigitalLines(1,1,10.0,DAQmx_Val_GroupByChannel,data,None,None)
    digital_output1.StopTask()