from MultiChannelAnalogInput import *
from TestBench_GPIO_Constants import *
from TestBench_Constants import *
from PyDAQmx import *
import numpy

def analog_configure():
    global analog_input_object

def pin_value_get_ana(pin_name):
    analog_input_object = MultiChannelAnalogInput([DAQ_dev_name + "/ai" + pin_name])
    analog_input_object.configure()
    analog_value = analog_input_object.read()
    return analog_value[0]

#def analog_configure2():
#    if type(physicalChannel) == type(""):
#            self.physicalChannel = [physicalChannel]
#        else:
#            self.physicalChannel  =physicalChannel
#        self.numberOfChannel = physicalChannel.__len__()
#        if limit is None:
#            self.limit = dict([(name, (-10.0,10.0)) for name in self.physicalChannel])
#        elif type(limit) == tuple:
#            self.limit = dict([(name, limit) for name in self.physicalChannel])
#        else:
#            self.limit = dict([(name, limit[i]) for  i,name in enumerate(self.physicalChannel)])
#        if reset:
#            DAQmxResetDevice(physicalChannel[0].split('/')[0] )
#
#
#    taskHandles = dict([(name,TaskHandle(0)) for name in self.physicalChannel])
#        for name in self.physicalChannel:
#            DAQmxCreateTask("",byref(taskHandles[name]))
#            DAQmxCreateAIVoltageChan(taskHandles[name],name,"",DAQmx_Val_RSE,
#                                     self.limit[name][0],self.limit[name][1],
#                                     DAQmx_Val_Volts,None)
#        self.taskHandles = taskHandles



def pin_value_get_ana2(pin_name):
    analog_input_object = MultiChannelAnalogInput([DAQ_dev_name + "/ai" + pin_name])
    analog_input_object.configure()
    analog_value = analog_input_object.read()
    return (analog_value[0])

def digital_configure():
    global digital_port_line
    global digital_port_line_output_readings

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
    digital_port_line = [[my00,my01,my02,my03,my04,my05,my06,my07],[my10,my11,my12,my13,my14,my15,my16,my17],[my20,my21,my22,my23,my24,my25,my26,my27]]

    digital_port_line_output_readings = numpy.zeros(shape=(3, 8))

    #creating input channels
    digital_port_line[0][0].CreateDIChan(DAQ_dev_name + "/port0/line0", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][1].CreateDIChan(DAQ_dev_name + "/port0/line1", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][2].CreateDIChan(DAQ_dev_name + "/port0/line2", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][3].CreateDIChan(DAQ_dev_name + "/port0/line3", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][4].CreateDIChan(DAQ_dev_name + "/port0/line4", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][5].CreateDIChan(DAQ_dev_name + "/port0/line5", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][6].CreateDIChan(DAQ_dev_name + "/port0/line6", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][7].CreateDIChan(DAQ_dev_name + "/port0/line7", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][6].CreateDIChan(DAQ_dev_name + "/port1/line6", "", DAQmx_Val_ChanForAllLines)

    #creating output channels
    digital_port_line[1][0].CreateDOChan(DAQ_dev_name + "/port1/line0", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][1].CreateDOChan(DAQ_dev_name + "/port1/line1", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][2].CreateDOChan(DAQ_dev_name + "/port1/line2", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][3].CreateDOChan(DAQ_dev_name + "/port1/line3", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][4].CreateDOChan(DAQ_dev_name + "/port1/line4", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][5].CreateDOChan(DAQ_dev_name + "/port1/line5", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][7].CreateDOChan(DAQ_dev_name + "/port1/line7", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][0].CreateDOChan(DAQ_dev_name + "/port2/line0", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][1].CreateDOChan(DAQ_dev_name + "/port2/line1", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][2].CreateDOChan(DAQ_dev_name + "/port2/line2", "", DAQmx_Val_ChanForAllLines)

    global read
    read = int32()

def pin_value_get_dig(pin_name):
    data = numpy.array(numpy.zeros(1, dtype=numpy.uint32))
    digital_port_line[pin_name[0]][pin_name[1]].StartTask()
    digital_port_line[pin_name[0]][pin_name[1]].ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data, 1000, byref(read), None)
    digital_port_line[pin_name[0]][pin_name[1]].StopTask()

    return data[0]

def pin_value_set_dig(pin_name, on_or_off):
    data = numpy.array([on_or_off], dtype = numpy.uint8) #this is to set the voltage to high or low
    digital_port_line[pin_name[0]][pin_name[1]].StartTask()
    digital_port_line[pin_name[0]][pin_name[1]].WriteDigitalLines(1,1,10.0,DAQmx_Val_GroupByChannel,data,None,None)
    digital_port_line[pin_name[0]][pin_name[1]].StopTask()
    digital_port_line_output_readings[pin_name[0]][pin_name[1]] = on_or_off
    return digital_port_line_output_readings[pin_name[0]][pin_name[1]]

def pin_value_get_dig_output(pin_name):
    return digital_port_line_output_readings[pin_name[0]][pin_name[1]]

#0.001 is off and 0.999 is max
def FANStart():
    global fanTaskHandle
    fanTaskHandle = TaskHandle(0)
    DAQmxCreateTask("", byref(fanTaskHandle))
    DAQmxCreateCOPulseChanFreq(fanTaskHandle, DAQ_dev_name + "/ctr0", "", DAQmx_Val_Hz, DAQmx_Val_Low,
                               0.0, 1 / float(0.00004), 0.001)
    DAQmxCfgImplicitTiming(fanTaskHandle, DAQmx_Val_ContSamps, 1000)
    DAQmxStartTask(fanTaskHandle)

def FANUpdate(duty_cycle):
    global fanTaskHandle
    global prev_duty_cycle
    global g_duty_cycle
    if (prev_duty_cycle != duty_cycle):
        g_duty_cycle = duty_cycle
        prev_duty_cycle = duty_cycle
        DAQmxStopTask(fanTaskHandle)
        DAQmxClearTask(fanTaskHandle)
        DAQmxCreateTask("", byref(fanTaskHandle))
        DAQmxCreateCOPulseChanFreq(fanTaskHandle, DAQ_dev_name + "/ctr0", "", DAQmx_Val_Hz, DAQmx_Val_Low,
                               0.0, 1 / float(0.00004), duty_cycle)
        DAQmxCfgImplicitTiming(fanTaskHandle, DAQmx_Val_ContSamps, 1000)
        DAQmxStartTask(fanTaskHandle)
