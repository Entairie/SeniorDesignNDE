import pigpio
import time
from NDE_Stage_Utility import * # my custom stage library

StartUpZero()


# x, y, z are dist of home in m

# start point
x = 0.075
y = 0.04
z = 0.3

MoveToHome(x, y, z)

# length of specimim
# rectangle
length = 0.145
width = 0.075

RectScan(length, width)

