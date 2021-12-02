import pigpio
import time

pi = pigpio.pi()

# Enable pigpio on command line prior to running code using ~~> sudo pigpiod
# Disable after code using ~~> sudo killall pigpiod

# 23 - x Dir            27 - y Dir          5 - z Dir           Orange
# 24 - x Step           22 - y Step         6 - z Step          Blue      
# 10 - x Limit          9 - y limit         11 - z limit        Grey

yzdelay = 0.00025
xdelay = 0.0025
# x Direction
#       0 ~~> Clockwise ~~> towards motor
#       1 ~~> Counter   ~~> away
# yz Direction
#       1 ~~> Clockwise ~~> towards motor
#       0 ~~> Counter   ~~> away

# Precision and Threaded leads
#       12.5 um / step        1 step = 0.0000125 m
#       3.175 um / step       1 step = 0.000003175 m
PreStepConv = 0.0000125
TheStepConv = 0.000003175

def StartUpZero():
    pi.set_mode(10, pigpio.INPUT)           # Set pin 10 as input
    pi.set_pull_up_down(10, pigpio.PUD_UP)  # Set default 10 as up/high/1/True
    pi.set_mode(9, pigpio.INPUT)            #  \
    pi.set_pull_up_down(9, pigpio.PUD_UP)   # -- y axis
    pi.set_mode(11, pigpio.INPUT)           #  \
    pi.set_pull_up_down(11, pigpio.PUD_UP)  # -- z axis
    
    pi.write(23, 0)     # x Dir low ~~> towards motor
    pi.write(27, 1)     # y Dir high ~~> towards motor
    pi.write(5, 0)      # z Dir low ~~> away motor/ up
    
    # Zero X
    input_state_x = True      # Switch not pushed
    while input_state_x == True:  # While switch not pushed
        pi.write(24, 1)         # Set local pi's GPIO BCM 10 high
        time.sleep(xdelay)
        pi.write(24, 0)         # Set local pi's GPIO BCM 10 low
        time.sleep(xdelay)
        input_state_x = pi.read(10)   # reads 1/True/not pushed or 0/False/pushed
    
    # Zero Y
    input_state_y = True
    while input_state_y == True:
        pi.write(22, 1)
        time.sleep(yzdelay)
        pi.write(22, 0)
        time.sleep(yzdelay)
        input_state_y = pi.read(9)
    
    # Zero Z
    input_state_z = True
    while input_state_z == True:
        pi.write(6, 1)
        time.sleep(yzdelay)
        pi.write(6, 0)
        time.sleep(yzdelay)
        input_state_z = pi.read(11)
    
    # Return zeroed position
    if input_state_x == False and input_state_y == False and input_state_z == False:
        return [0, 0, 0]

def MoveToHome(xn, yn, zn, Xc, Yc, Zc):
    # Moves sensor from zero to home to start scan
    # xn, yn, zn are distances in m of the point from zero that we move to
    # Xc, Yc, Zc are the current position of the sensor

    # Calc x move dist & dir
    if xn > Xc:     # Move away from zero/motor
        x = xn - Xc
        pi.write(23, 1)     # x Dir ~~> away zero/motor
    else:           # Move towards zero
        x = Xc - xn
        pi.write(23, 0)
    
    # Calc y move dist & dir
    if yn > Yc:     # Move away from zero/motor
        y = yn - Yc
        pi.write(27, 0)     # y Dir ~~> away motor
    else:           # Move towards zero
        y = Yc - yn
        pi.write(27, 1)
    
    # Calc z move dist & dir
    if zn > Zc:     # Move away from zero and towards motor
        z = zn - Zc
        pi.write(5, 1)      # z Dir ~~> towards motor and away from zero
    else:           # Move towards zero and away from motor
        z = Zc - zn
        pi.write(5, 0)

    xStep = round(x/PreStepConv)
    yStep = round(y/TheStepConv)
    zStep = round(z/TheStepConv)

    # Move to x home
    for x in range(xStep):
        pi.write(24, 1)         # Set local pi's GPIO BCM 10 high
        time.sleep(xdelay)
        pi.write(24, 0)         # Set local pi's GPIO BCM 10 low
        time.sleep(xdelay)
    
    # Move to y home
    for y in range(yStep):
        pi.write(22, 1)
        time.sleep(yzdelay)
        pi.write(22, 0)
        time.sleep(yzdelay)
    
    # Move to z home
    for z in range(zStep):
        pi.write(6, 1)
        time.sleep(yzdelay)
        pi.write(6, 0)
        time.sleep(yzdelay)

def RectScan(xLength, yLength, ScanWidthMeters, speed):
    # All values in m, m, m, m/s

    XScanWidth = int(ScanWidthMeters/PreStepConv)    # - Convert scan width from m to steps
    YScanWidth = int(ScanWidthMeters/TheStepConv)    # /
    
    xStep = round(xLength/PreStepConv)      # Convert x length from m to Steps
    xIndent = int(round(xStep/XScanWidth))       # number of times to indent x for new line of scans
    yStep = round(yLength/TheStepConv)
    yIndent = int(round(yStep/YScanWidth))

    xScandelay = (PreStepConv/speed)/2
    yScandelay = (TheStepConv/speed)/2

    xDir = 1
    pi.write(27, 0)     # y Dir ~~> away motor

    for indent in range(yIndent):
        for y in range(YScanWidth):
            pi.write(22, 1)
            time.sleep(yScandelay)
            pi.write(22, 0)
            time.sleep(yScandelay)

        pi.write(23, xDir)     # x Dir ~~> initial away motor
        for x in range(xIndent):
            for x in range(XScanWidth):
                pi.write(24, 1)
                time.sleep(xScandelay)
                pi.write(24, 0)
                time.sleep(xScandelay)
            time.sleep(1)       # This time would be taken to scan and record value
                                # Insert Scan function here
        if xDir == 0:
            xDir = 1
        else:
            xDir = 0
