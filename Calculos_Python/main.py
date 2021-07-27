from serial_com import send_command_to_platform
import numpy as np
import time
import settings
import controller
import test_GUI
import threading
class ball_t:
    def __init__(self):
        self.pos_x=0
        self.pos_y=0



def nicos_magic_opencv_function():
    ball_pos=ball_t()
    ball_pos.pos_x=1
    ball_pos.pos_y=0
    return ball_pos

def main():
    settings.init()
    t1=threading.Thread(target=control_loop)
    t1.start()
    test_GUI.run_gui()



def control_loop():
    ball_pos = ball_t()
    c=controller.controller_t()
    while(True):
        time.sleep(1)
        ball_pos = nicos_magic_opencv_function()
        angle_x,angle_y=c.control(ball_pos)
        print(f'angle_x={angle_x}\n')
        print(f'angle_y={angle_y}\n')
        #send_command_to_platform("/dev/ttyACM0",angle_x,angle_y,14)


if __name__ == '__main__':
    main()