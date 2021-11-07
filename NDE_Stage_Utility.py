import pyfirmata as fir
import time

# Change on PC to see on Pi

a = fir.Arduino('COM3')         # Set up Firmata on COM3
a.digital[2].mode = fir.OUTPUT  # X Direction pin
a.digital[3].mode = fir.OUTPUT  # X Step pin
a.digital[4].mode = fir.OUTPUT  # Y Direction pin
a.digital[5].mode = fir.OUTPUT  # Y Step pin
a.digital[6].mode = fir.OUTPUT  # Z Direction pin
a.digital[7].mode = fir.OUTPUT  # Z Step pin

def StartUpZero():
    a.digital[2].write(0)       # Clockwise, towards motors
    #while a.digital[xLimitPin].read() == 0
    n = 0;
    while n < 800:
        a.digital[3].write(1)
        time.sleep(0.00005)
        a.digital[3].write(0)
        time.sleep(0.00005)
        n += 1
        print(n)
    
    a.digital[4].write(1)       # Clockwise, towards motors
    #while a.digital[yLimitPin].read() == 0
    n = 0;
    while n < 800:
        a.digital[5].write(1)
        time.sleep(0.00005)
        a.digital[5].write(0)
        time.sleep(0.00005)
        n += 1
        print(n)
    
    a.digital[6].write(1)       # Clockwise, towards motors
    #while a.digital[yLimitPin].read() == 0
    n = 0;
    while n < 800:
        a.digital[7].write(1)
        time.sleep(0.00005)
        a.digital[7].write(0)
        time.sleep(0.00005)
        n += 1
        print(n)




