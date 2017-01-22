from MultiChannelAnalogInput import *
from TestBench_GPIO_Constants import *
from PyDAQmx import *
import numpy

def AnalogConfigure():
      global analogInputObject
      
def PinValueGetAna(pinName):
    analogInputObject = MultiChannelAnalogInput(["Dev1/ai" + pinName])
    analogInputObject.configure()
    return analogInputObject.read()

def DigitalConfigure():
    global digitalPortLine

    #initialize a 2D array of size 3 rows X 8 columns with an instance of Task() as each element
    #each index corresponds to the port number and line number, ex: [2][1] means port 2 line 1
    #the list of Task() objects has to be done #these will NOT be referenced in the future
    my00 = Task()
    my01 = Task()
    my02 = Task()
    my03 = Task()
    my04 = Task()
    my05 = Task()
    my06 = Task()
    my07 = Task()
    my10 = Task()
    my11 = Task()
    my12 = Task()
    my13 = Task()
    my14 = Task()
    my15 = Task()
    my16 = Task()
    my17 = Task()
    my20 = Task()
    my21 = Task()
    my22 = Task()
    my23 = Task()
    my24 = Task()
    my25 = Task()
    my26 = Task()
    my27 = Task()
    digitalPortLine = [[my00,my01,my02,my03,my04,my05,my06,my07],[my10,my11,my12,my13,my14,my15,my16,my17],[my20,my21,my22,my23,my24,my25,my26,my27]]

    #creating input channels
    digitalPortLine[0][0].CreateDIChan("Dev1/port0/line0", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][1].CreateDIChan("Dev1/port0/line1", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][2].CreateDIChan("Dev1/port0/line2", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][3].CreateDIChan("Dev1/port0/line3", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][4].CreateDIChan("Dev1/port0/line4", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][5].CreateDIChan("Dev1/port0/line5", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][6].CreateDIChan("Dev1/port0/line6", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[0][7].CreateDIChan("Dev1/port0/line7", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][6].CreateDIChan("Dev1/port1/line6", "", DAQmx_Val_ChanForAllLines)

    #creating output channels
    digitalPortLine[1][0].CreateDOChan("Dev1/port1/line0", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][1].CreateDOChan("Dev1/port1/line1", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][2].CreateDOChan("Dev1/port1/line2", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][3].CreateDOChan("Dev1/port1/line3", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][4].CreateDOChan("Dev1/port1/line4", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][5].CreateDOChan("Dev1/port1/line5", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[1][7].CreateDOChan("Dev1/port1/line7", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[2][0].CreateDOChan("Dev1/port2/line0", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[2][1].CreateDOChan("Dev1/port2/line1", "", DAQmx_Val_ChanForAllLines)
    digitalPortLine[2][2].CreateDOChan("Dev1/port2/line2", "", DAQmx_Val_ChanForAllLines)

    #DAQmx start code
#    digitalPortLine[0][0].StartTask()
#    digitalPortLine[0][1].StartTask()
#    digitalPortLine[0][2].StartTask()
#    digitalPortLine[0][3].StartTask()
#    digitalPortLine[0][4].StartTask()
#    digitalPortLine[0][5].StartTask()
#    digitalPortLine[0][6].StartTask()
#    digitalPortLine[0][7].StartTask()
#    digitalPortLine[1][0].StartTask()
#    digitalPortLine[1][1].StartTask()
#    digitalPortLine[1][2].StartTask()
#    digitalPortLine[1][3].StartTask()
#    digitalPortLine[1][4].StartTask()
#    digitalPortLine[1][5].StartTask()
#    digitalPortLine[1][6].StartTask()
#    digitalPortLine[1][7].StartTask()
#    digitalPortLine[2][0].StartTask()
#    digitalPortLine[2][1].StartTask()
#    digitalPortLine[2][2].StartTask()

    global read 
    read = int32()
    
def PinValueGetDig(pinName):
    data = numpy.array(numpy.zeros(1, dtype=numpy.uint32))
    digitalPortLine[pinName[0]][pinName[1]].StartTask()
    digitalPortLine[pinName[0]][pinName[1]].ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data, 1000, byref(read), None)
    digitalPortLine[pinName[0]][pinName[1]].StopTask()

    return data

def PinValueSetDig(pinName, onOrOff):
    data = numpy.array([onOrOff], dtype = numpy.uint8) #this is to set the voltage to high or low
    digitalPortLine[pinName[0]][pinName[1]].StartTask()
    digitalPortLine[pinName[0]][pinName[1]].WriteDigitalLines(1,1,10.0,DAQmx_Val_GroupByChannel,data,None,None)
    digitalPortLine[pinName[0]][pinName[1]].StopTask()
