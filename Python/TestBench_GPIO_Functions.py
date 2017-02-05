from MultiChannelAnalogInput import *
from TestBench_GPIO_Constants import *
from PyDAQmx import *
import numpy

def analog_configure():
    global analog_input_object
      
def pin_value_get_ana(pin_name):
    analog_input_object = MultiChannelAnalogInput(["Dev1/ai" + pin_name])
    analog_input_object.configure()
    return analog_input_object.read()

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
    #digital_port_line[0][0].CreateDIChan("Dev1/port0/line0", "", DAQmx_Val_ChanForAllLines)
    #digital_port_line[0][1].CreateDIChan("Dev1/port0/line1", "", DAQmx_Val_ChanForAllLines)
    #digital_port_line[0][2].CreateDIChan("Dev1/port0/line2", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][3].CreateDIChan("Dev1/port0/line3", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][4].CreateDIChan("Dev1/port0/line4", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][5].CreateDIChan("Dev1/port0/line5", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][6].CreateDIChan("Dev1/port0/line6", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][7].CreateDIChan("Dev1/port0/line7", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][6].CreateDIChan("Dev1/port1/line6", "", DAQmx_Val_ChanForAllLines)

    #creating output channels
    digital_port_line[1][0].CreateDOChan("Dev1/port1/line0", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][1].CreateDOChan("Dev1/port1/line1", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][2].CreateDOChan("Dev1/port1/line2", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][3].CreateDOChan("Dev1/port1/line3", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][4].CreateDOChan("Dev1/port1/line4", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][5].CreateDOChan("Dev1/port1/line5", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[1][7].CreateDOChan("Dev1/port1/line7", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][0].CreateDOChan("Dev1/port2/line0", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][1].CreateDOChan("Dev1/port2/line1", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][2].CreateDOChan("Dev1/port2/line2", "", DAQmx_Val_ChanForAllLines)

    #test output channels
    digital_port_line[0][0].CreateDOChan("Dev1/port0/line0", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][1].CreateDOChan("Dev1/port0/line1", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[0][2].CreateDOChan("Dev1/port0/line2", "", DAQmx_Val_ChanForAllLines)
    digital_port_line[2][3].CreateDOChan("Dev1/port2/line3", "", DAQmx_Val_ChanForAllLines)

    #DAQmx start code
#    digital_port_line[0][0].StartTask()
#    digital_port_line[0][1].StartTask()
#    digital_port_line[0][2].StartTask()
#    digital_port_line[0][3].StartTask()
#    digital_port_line[0][4].StartTask()
#    digital_port_line[0][5].StartTask()
#    digital_port_line[0][6].StartTask()
#    digital_port_line[0][7].StartTask()
#    digital_port_line[1][0].StartTask()
#    digital_port_line[1][1].StartTask()
#    digital_port_line[1][2].StartTask()
#    digital_port_line[1][3].StartTask()
#    digital_port_line[1][4].StartTask()
#    digital_port_line[1][5].StartTask()
#    digital_port_line[1][6].StartTask()
#    digital_port_line[1][7].StartTask()
#    digital_port_line[2][0].StartTask()
#    digital_port_line[2][1].StartTask()
#    digital_port_line[2][2].StartTask()

    global read 
    read = int32()

def pin_value_get_dig(pin_name):
    data = numpy.array(numpy.zeros(1, dtype=numpy.uint32))
    digital_port_line[pin_name[0]][pin_name[1]].StartTask()
    digital_port_line[pin_name[0]][pin_name[1]].ReadDigitalU32(-1, 1, DAQmx_Val_GroupByChannel, data, 1000, byref(read), None)
    digital_port_line[pin_name[0]][pin_name[1]].StopTask()

    return data

def pin_value_set_dig(pin_name, on_or_off):
    data = numpy.array([on_or_off], dtype = numpy.uint8) #this is to set the voltage to high or low
    digital_port_line[pin_name[0]][pin_name[1]].StartTask()
    digital_port_line[pin_name[0]][pin_name[1]].WriteDigitalLines(1,1,10.0,DAQmx_Val_GroupByChannel,data,None,None)
    digital_port_line[pin_name[0]][pin_name[1]].StopTask()
    digital_port_line_output_readings[pin_name[0]][pin_name[1]] = on_or_off
    return digital_port_line_output_readings[pin_name[0]][pin_name[1]]

def pin_value_get_dig_output(pin_name):
    return digital_port_line_output_readings[pin_name[0]][pin_name[1]]