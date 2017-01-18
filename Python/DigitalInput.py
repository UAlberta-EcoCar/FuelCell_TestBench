from PyDAQmx import *
import numpy

class DigitalInput():
    # Declaration of variable passed by reference
    def __init__(self, devPortLine):
        self.devPortLine = devPortLine
#        self.digital_input = Task()
#
#        # DAQ Configuration Code
#        self.digital_input.CreateDIChan(devPortLine, "", DAQmx_Val_ChanForAllLines)
#        # DAQmx Start Code
#        self.digital_input.StartTask()
#
#    # DAQmx Start Code
    def Read(self):
        digital_input = Task()

        # DAQ Configuration Code
        digital_input.CreateDIChan(self.devPortLine, "", DAQmx_Val_ChanForAllLines)
        # DAQmx Start Code
        digital_input.StartTask()
        
        read = int32()
        data = numpy.zeros(1, dtype=numpy.uint32)
        digital_input.ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data, 1000, byref(read), None)
        data2=data[0]
        print data        
        #digital_input.StopTask()
        return data2