from serial_com import send_command_to_platform
import time
import numpy as np
inc=2*np.pi/180
h=14
i=0
pause=0.3

while (True):
    angle_y=15*np.sin(i*inc)
    angle_x=15*np.cos(i*inc)
    send_command_to_platform("/dev/ttyACM0",angle_x,angle_y,h)
    time.sleep(pause)
    i=i+1
