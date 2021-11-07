import pigpio
import time

# Enable pigpio on command line prior to running code using ~~> sudo pigpiod
# Disable after code using ~~> sudo killall pigpiod

# 23 - x Dir            27 - y Dir          5 - z Dir           Orange
# 24 - x Step           22 - y Step         6 - z Step          Blue      
# 10 - x Limit          9 - y limit         11 - z limit        Grey


pi = pigpio.pi()

delay = 0.00025
steps = 1600
Dir = 0
        # 0 ~~> Clockwise ~~> towards motor
        # 1 ~~> Counter   ~~> away

def StartUpZero():
    pi.set_mode(10, pigpio.INPUT)           # Set pin 10 as input
    pi.set_pull_up_down(10, pigpio.PUD_UP)  # Set default 10 as up/high/1/True
    pi.set_mode(9, pigpio.INPUT)            #  \
    pi.set_pull_up_down(9, pigpio.PUD_UP)   # -- y axis
    pi.set_mode(11, pigpio.INPUT)           #  \
    pi.set_pull_up_down(11, pigpio.PUD_UP)  # -- z axis
    
    pi.write(23, 0)     # x Dir low ~~> towards motor
    pi.write(27, 1)     # y Dir high ~~> towards motor
    pi.write(5, 0)      # z Dir low ~~> away motor
    
    # Zero X
    input_state_x = True      # Switch not pushed
    while input_state_x == True:  # While switch not pushed
        pi.write(24, 1)         # Set local pi's GPIO BCM 10 high
        time.sleep(0.0025)
        pi.write(24, 0)         # Set local pi's GPIO BCM 10 low
        time.sleep(0.0025)
        input_state_x = pi.read(10)   # reads 1/True/not pushed or 0/False/pushed
    
    # Zero Y
    input_state_y = True
    while input_state_y == True:
        pi.write(22, 1)
        time.sleep(delay)
        pi.write(22, 0)
        time.sleep(delay)
        input_state_y = pi.read(9)
    
    # Zero z
    input_state_z = True
    while input_state_z == True:
        pi.write(6, 1)
        time.sleep(delay)
        pi.write(6, 0)
        time.sleep(delay)
        input_state_z = pi.read(11)
