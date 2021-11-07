import pigpio
import time

# Enable pigpio on command line prior to running code using ~~> sudo pigpiod
# Disable after code using ~~> sudo killall pigpiod
# Connect driver DIR to BCM 23
# Connect driver STEP to BCM 22

pi = pigpio.pi()

pi.set_mode(10, pigpio.INPUT)           # Set pin 10 as input
pi.set_pull_up_down(10, pigpio.PUD_UP)  # Set default 10 as up/high/1/True

delay = 0.0025
steps = 1600
Dir = 0
        # 0 ~~> Clockwise ~~> towards motor
        # 1 ~~> Counter   ~~> away
                        
pi.write(23, Dir)       # Set local pi's GPIO BCM 23 high/low

input_state = True      # Switch not pushed

while input_state == True:  # While switch not pushed
    pi.write(22, 1)         # Set local pi's GPIO BCM 22 high
    time.sleep(delay)
    pi.write(22, 0)         # Set local pi's GPIO BCM 22 low
    time.sleep(delay)
    input_state = pi.read(10)   # reads 1/True/not pushed or 0/False/pushed
