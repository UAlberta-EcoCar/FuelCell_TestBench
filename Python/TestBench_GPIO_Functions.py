from MultiChannelAnalogInput import *
from TestBench_GPIO_Constants import *
from PyDAQmx import *
import numpy

#get analong input of pin
#def PinValueGetAnalog(pinName):
#    obj = GetData([currDev + "/ai" + pinName])
#    obj.configure()
#   return obj.read()

def AnalogConfigure():
#    global physicalChannel
#    global taskHandles
#    physicalChannel = ["Dev1/ai2","Dev1/ai1"]
#    limit = None
#    reset = False
#    global taskhandle     
#    numberOfChannel = physicalChannel.__len__()
#    limit = dict([(name, (-10.0,10.0)) for name in physicalChannel])
#    if reset:
#        DAQmxResetDevice(physicalChannel[0].split('/')[0] )
#
#    # Create one task handle per Channel
#    taskHandles = dict([(name,TaskHandle(0)) for name in physicalChannel])
#    for name in physicalChannel:
#        DAQmxCreateTask("",byref(taskHandles[name]))
#        DAQmxCreateAIVoltageChan(taskHandles[name],name,"",DAQmx_Val_RSE,
#                                 limit[name][0],limit[name][1],
#                                 DAQmx_Val_Volts,None)
#        taskHandle = taskHandles[name]
#        DAQmxStartTask(taskHandle)
#    global read_analog    
#    read_analog = int32() 
      global multipleAI
      multipleAI = MultiChannelAnalogInput(["Dev1/ai13","Dev1/ai14"])
      multipleAI.configure()
      
def PinValueGetAna():
#    data_analog = numpy.zeros((1,), dtype=numpy.float64)
#    appended_analog_data = numpy.zeros((1,), dtype=numpy.float64)
##        data = AI_data_type()
#    for name in physicalChannel:
#        DAQmxReadAnalogF64(taskHandles[name],1,10.0,DAQmx_Val_GroupByChannel,data_analog,1,byref(read_analog),None)
#        appended_analog_data.append(data_analog)
##    DAQmxStopTask(taskHandle)
#    return appended_analog_data     
    return multipleAI.read("test")

def DigitalConfigure():
    global digital_input1
    global digital_input2
    
    digital_input1 = Task()
    digital_input2 = Task()
    # DAQ Configuration Code
#    digital_input.CreateDIChan(currDev + "/port" + portLine[0] + "/line" + portLine[1], "", DAQmx_Val_ChanForAllLines)    
    digital_input1.CreateDIChan("Dev1/port0/line0:7", "", DAQmx_Val_ChanForAllLines)    
    digital_input2.CreateDIChan("Dev1/port2/line0:7", "", DAQmx_Val_ChanForAllLines)    
    # DAQmx Start Code
    digital_input1.StartTask()
    digital_input2.StartTask()    
    global read 
    read = int32()
    
def PinValueGetDig():
    data1 = numpy.array(numpy.zeros(16, dtype=numpy.uint32))
    data2 = numpy.array(numpy.zeros(16, dtype=numpy.uint32))    
    digital_input1.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data1, 1000, byref(read), None)
    digital_input2.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data2, 1000, byref(read), None)
#    data2=data[0]
#    digital_input.StopTask()
    data3 = numpy.concatenate((data1,data2))
    digital_input1.StopTask()
    digital_input2.StopTask()    
    return data3