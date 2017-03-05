#from GetData import * #import everything from GetData(which is a class from a file)
from TestBench_GPIO_Constants import *
from TestBench_GPIO_Functions import *
import time
from TestBench_Constants import *
from TestBench_ADC import *
from TestBench_PID import *

#start_delay not needed, it is a value in not working fan function
charge_thres = 35 #35 volts
purge_counter = 0
purge_timer = 0
repress_delay = 0
purge_state = "FIRST_PURGE_CYCLE"

# valve close = 0
# relay close = 1
# ignore fan stuff for now, will work on it later, pwm comes in here
# work on math functions(the weird non state functions) after the state functions(includes purge stuff)

def FC_standby():
    if pin_value_get_dig(START):
        FC_state = "FC_STATE_STARTUP_H2"
    else:
        #make sure fuel cell stays off
        #supply valve closed
        pin_value_set_dig(H2_VALVE, 0)
        #purge valve closed,
        pin_value_set_dig(PURGE_VALVE, 0)
        #relays open, set = 0
        pin_value_set_dig(MOTOR_RELAY, 0)
        pin_value_set_dig(RESISTOR_RELAY, 0)
        pin_value_set_dig(CAP_RELAY, 0)

        FANUpdate(0.001)
        FC_state = "FC_STATE_STANDBY"
    return FC_state

def FC_startup_h2():
    #open supply valve
    pin_value_set_dig(H2_VALVE, 1)
    #purge valve closed
    pin_value_set_dig(PURGE_VALVE, 0)
    #relays open
    pin_value_set_dig(STARTUP_RELAY, 0)
    pin_value_set_dig(MOTOR_RELAY, 0)
    pin_value_set_dig(RESISTOR_RELAY, 0)
    pin_value_set_dig(CAP_RELAY, 0)

    #input h2 until voltage reaches 30
    if (get_FCVOLT() < 30):
        #loop back into same state
        FC_state = "FC_STATE_STARTUP_H2"
    else:
        #voltage is 30 then go to start up purge
        FC_state = "FC_STATE_STARTUP_PURGE"
    return FC_state

def FC_startup_purge():
    global delay_timer1
    global repress_delay
    global purge_timer
    #h2 valve still open
    pin_value_set_dig(H2_VALVE, 1)
    #close startup relay
    if (pin_value_get_dig_output(RESISTOR_RELAY) == 0 or pin_value_get_dig_output(CAP_RELAY) == 0):
        pin_value_set_dig(STARTUP_RELAY, 1)
    #motor relay still open
    pin_value_set_dig(MOTOR_RELAY, 0)
    #RES relay open
    pin_value_set_dig(RESISTOR_RELAY, 0)
    #CAP relay still open
    pin_value_set_dig(CAP_RELAY, 0)

    #open purge valve and start timer
    if (pin_value_get_dig_output(PURGE_VALVE) == 0):
        purge_timer = time.clock()

    pin_value_set_dig(PURGE_VALVE, 1)

    #wait 3 seconds before changing state
    if (time.clock() - purge_timer < 3):
        FC_state = "FC_STATE_STARTUP_PURGE"
    else:
        #close purge valve
        pin_value_set_dig(PURGE_VALVE, 0)
        #supply valve still open
        pin_value_set_dig(H2_VALVE, 1)
        #open all relays
        pin_value_set_dig(STARTUP_RELAY, 0)
        pin_value_set_dig(RESISTOR_RELAY, 0)
        pin_value_set_dig(MOTOR_RELAY, 0)
        pin_value_set_dig(CAP_RELAY, 0)

        delay_timer1 = time.clock()

        repress_delay = time.clock()
        #change state to repressurized delay
        FC_state = "FC_STATE_REPRESSURIZE"
    return FC_state

def FC_repressurize():
    global repress_delay
    FC_state = "FC_STATE_REPRESSURIZE"
    if (time.clock() - repress_delay > 1):
        FC_state = "FC_STATE_STARTUP_CHARGE"
    return FC_state

def get_time_between_last_purges():
    return time_between_last_purges

def get_number_of_purges():
    return purge_counter

def get_total_charge_extracted():
    return estimated_total_charge_extracted/1000

def get_J_since_last_purge():
    return uJ_since_last_purge/1000000

def get_total_E():
    return estimated_total_E/1000

def FC_startup_charge():
    global repress_delay
    global delay_timer1
    global delay_timer2
    global purge_timer
    global purge_integration_timer
    global purge_state
    global time_since_last_purge
    global charge_thres
    global delta_purge_timer
    global total_charge_energy_integration_timer
    global time_between_last_purges
    global purge_counter
    global estimated_total_charge_extracted
    global uJ_since_last_purge
    global estimated_total_E
    global mAms_since_last_purge
    global fan_update_timer
    #will keep charging until state exits
    FC_state = "FC_STATE_STARTUP_CHARGE"
    if (time.clock() - delay_timer1 < 1):
        return FC_state

    if (purge_state == "FIRST_PURGE_CYCLE"):
        purge_integration_timer = time.clock()
        purge_state = "PURGE_VALVE_CLOSED"

    delta_purge_time = time.clock() - purge_integration_timer
    if (delta_purge_time > PURGE_INTEGRATION_INTERVAL):
        mAms_since_last_purge = mAms_since_last_purge + delta_purge_time * get_FCCURR()
        time_since_last_purge = time_since_last_purge + delta_purge_time
        uJ_since_last_purge = uJ_since_last_purge + delta_purge_time * get_FCCURR() * get_FCVOLT()
        purge_integration_timer = time.clock()

    if (mAms_since_last_purge > PURGE_THRESHOLD):
        #open purge valve
        pin_value_set_dig(PURGE_VALVE, 1)
        #increase number of purges
        purge_counter = purge_counter + 1
        #we restart counting mAms as soon as valve opens
        #reset mAms sum
        mAms_since_last_purge = 0
        #reset energy
        uJ_since_last_purge = 0
        #record time
        time_between_last_purges = time_since_last_purge
        time_since_last_purge = 0 #reset timer
        #reset timer
        purge_integration_timer = time.clock()

        #start purge timer to time purge
        purge_timer = time.clock()
        #change purge state to open
        purge_state = "PURGE_VALVE_OPEN"

    if (purge_state == "PURGE_VALVE_OPEN"): #if purge valve is open
        if (time.clock() - purge_timer > PURGE_TIME): #if it has completed purge
            #close purge valve
            pin_value_set_dig(PURGE_VALVE, 0)
            #change purge state to closed
            purge_state = "PURGE_VALVE_CLOSED"

    if (time.clock() - fan_update_timer > FANUPDATE_INTERVAL):
        print PID(get_FCTEMP(), calc_opt_temp()), "duty cycle"
        FANUpdate(PID(get_FCTEMP(), calc_opt_temp()))
        fan_update_timer = time.clock()

    delta_t = time.clock() - total_charge_energy_integration_timer
    if (delta_t > TOTAL_CHARGE_ENERGY_INTEGRATION_INTERVAL):
        estimated_total_E = estimated_total_E + get_FCVOLT() * get_FCCURR() * delta_t
        estimated_total_charge_extracted = estimated_total_charge_extracted + get_FCCURR() * delta_t
        total_charge_energy_integration_timer = time.clock()

    if (get_CAPVOLT() < charge_thres):
        #close resistor relay
        pin_value_set_dig(RESISTOR_RELAY, 1)
        #other relays still open
        pin_value_set_dig(STARTUP_RELAY, 0)
        pin_value_set_dig(MOTOR_RELAY, 0)
        pin_value_set_dig(CAP_RELAY, 0)
        #h2 valve open
        pin_value_set_dig(H2_VALVE, 1)

        #purge valve still closed?

        delay_timer2 = time.clock()
    else:#caps are charged
        charge_thres = 33 #33 volts

        if (time.clock() - delay_timer2 < 4):
            return "FC_STATE_STARTUP_CHARGE"

        #close motor relay
        pin_value_set_dig(MOTOR_RELAY, 1)
        #go to main run state
        FC_state = "FC_STATE_RUN"

    return FC_state

#MAN5100319 - FCgen 1020ACS Product Manual, section 4.3.2, page 55
def calc_opt_temp():
    return (0.53 * get_FCCURR()) + 26.01

#potential thing to do in the future, use polynomial fit instead of piece-wise function
def calc_min_temp():
    return (0.53 * get_FCCURR()) + 6.098

def calc_max_temp():
    #if get_FCCURR() >= 64.8: #future improvement
    #    return 75
    #else:
    return (0.355 * get_FCCURR()) + 52
#--

def FC_run():
    global repress_delay
    global delay_timer1
    global delay_timer2
    global purge_timer
    global purge_integration_timer
    global purge_state
    global time_since_last_purge
    global charge_thres
    global delta_purge_timer
    global total_charge_energy_integration_timer
    global time_between_last_purges
    global purge_counter
    global estimated_total_charge_extracted
    global uJ_since_last_purge
    global estimated_total_E
    global mAms_since_last_purge
    global fan_update_timer

    if (time.clock() - fan_update_timer > FANUPDATE_INTERVAL):
        print PID(get_FCTEMP(), calc_opt_temp()), "duty_cycle"
        FANUpdate(PID(get_FCTEMP(), calc_opt_temp()))
        fan_update_timer = time.clock()

    delta_purge_timer = time.clock() - purge_integration_timer
    if (delta_purge_timer > PURGE_INTEGRATION_INTERVAL):
        mAms_since_last_purge = mAms_since_last_purge + delta_purge_time * get_FCCURR()
        uJ_since_last_purge = uJ_since_last_purge + delta_purge_time * get_FCCURR() * get_FCVOLT()
        purge_integration_timer = time.clock()
        time_since_last_purge = time_since_last_purge + delta_purge_time

    if (mAms_since_last_purge > PURGE_THRESHOLD):
        #open purge valve
        pin_value_set_dig(PURGE_VALVE, 1)
        #increase number of purges
        purge_counter = purge_counter + 1
        #reset mAms sum
        mAms_since_last_purge = 0
        #reset energy
        uJ_since_last_purge = 0
        #record time
        time_between_last_purges = time_since_last_purge
        time_since_last_purge = 0
        #reset timer
        purge_integration_timer = time.clock()

        #start purge timer to time purge
        purge_timer = time.clock()
        #change purge state to open
        purge_state = "PURGE_VALVE_OPEN"

    if (purge_state == "PURGE_VALVE_OPEN"):
        if (time.clock() - purge_timer > PURGE_TIME):
            #close purge valve
            pin_value_set_dig(PURGE_VALVE, 0)
            #change purge state eto close
            purge_state = "PURGE_VALVE_CLOSED"

    delta_t = time.clock() - total_charge_energy_integration_timer
    if (delta_t > TOTAL_CHARGE_ENERGY_INTEGRATION_INTERVAL):
        estimated_total_E = estimated_total_E + get_FCVOLT() * get_FCCURR() * delta_t
        estimated_total_charge_extracted = estimated_total_charge_extracted + get_FCCURR() * delta_t
        total_charge_energy_integration_timer = time.clock()

    FC_state = "FC_STATE_RUN"
    return FC_state

def FC_shutdown():
    #close valves
    pin_value_set_dig(H2_VALVE, 0)
    pin_value_set_dig(PURGE_VALVE, 0)
    #close relays
    pin_value_set_dig(MOTOR_RELAY, 1)
    pin_value_set_dig(STARTUP_RELAY, 1)
    pin_value_set_dig(RESISTOR_RELAY, 1)
    pin_value_set_dig(CAP_RELAY, 1)

    FANUpdate(0.999)

    FC_state = "FC_STATE_SHUTDOWN"

    return FC_state

def FC_alarm():
    #close valves
    pin_value_set_dig(H2_VALVE, 0)
    pin_value_set_dig(PURGE_VALVE, 0)
    #close relays
    pin_value_set_dig(MOTOR_RELAY, 1)
    pin_value_set_dig(STARTUP_RELAY, 1)
    pin_value_set_dig(RESISTOR_RELAY, 1)
    pin_value_set_dig(CAP_RELAY, 1)

    FANUpdate(0.999)
    FC_state = "FC_STATE_ALARM"
    return FC_state

def get_duty_cycle():
    global g_duty_cycle
    return g_duty_cycle
