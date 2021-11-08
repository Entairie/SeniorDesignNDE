import pigpio
import time
from NDE_Stage_Utility import * # my custom stage library

# x, y, z are dist of home from zero in m
x = 0.095;      y = 0.065;      z = 0.16

# length and width of rectangle specimin in m
length = 0.145;     width = 0.075

# Steps between scans
ScanWidth = 20



StartUpZero()

MoveToHome(x, y, z)

RectScan(length, width, ScanWidth)
