import pigpio
import time
from NDE_Stage_Utility import * # my custom stage library

StartUpZero()


# x, y, z are dist of home in m

x = 0.1
y = 0.1
z = 0.15
MoveToHome(x, y, z)