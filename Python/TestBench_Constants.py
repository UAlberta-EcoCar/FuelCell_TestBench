global repress_delay
global delay_timer1
global delay_timer2
global purge_timer
global purge_integration_timer
global purge_state
global time_since_last_purge
global charge_thres
global delta_purge_time
global total_charge_energy_integration_timer
global time_between_last_purges
global purge_counter
global estimated_total_charge_extracted
global uJ_since_last_purge
global estimated_total_E
global mAms_since_last_purge
global fan_update_timer

FANUPDATE_INTERVAL = 100
PURGE_INTEGRATION_INTERVAL = 5
PURGE_THRESHOLD = 2300000000
PURGE_TIME = 200
TOTAL_CHARGE_ENERGY_INTEGRATION_INTERVAL = 5

purge_state = "FIRST_PURGE_CYCLE"

delay_timer1 = 0
delay_timer2 = 0
purge_timer = 0
purge_counter = 0
time_between_last_purges = 0
mAms_since_last_purge = 0
total_charge_energy_integration_timer = 0
time_since_last_purge = 0
uJ_since_last_purge = 0
estimated_total_E = 0
estimated_total_charge_extracted = 0
fan_update_timer = 0
purge_integration_timer = 0
delta_purge_time = 0