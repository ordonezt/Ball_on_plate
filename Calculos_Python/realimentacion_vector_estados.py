import time  
import threading
import settings
from serial_com import send_command_to_platform
#declaro las variables como globales para que puedan ser accedidas por
# el thread de modificación

class controller_fsf:
    def __init__(self):
        self.prev_pos_x=0 
        self.prev_pos_y=0 

        self.Integral=0 
        #self.T=1/30 #30FPS
        self.T_prev=time.time()
        self.T_actual=0

    def control(self,ball_pos):
        self.T_actual=time.time()
        angle_x=self.controller_fsf(ball_pos.pos_x,self.prev_pos_x,self.T_actual,self.T_prev)
        angle_y=self.controller_fsf(ball_pos.pos_y,self.prev_pos_y,self.T_actual,self.T_prev)

        self.prev_pos_x=ball_pos.pos_x
        self.prev_pos_y=ball_pos.pos_y
        self.T_prev=self.T_actual

        send_command_to_platform("/dev/ttyACM0",angle_x,angle_y,13)
        return angle_x,angle_x

    def controller_fsf(self,pos,prev_pos,T_actual,T_previo):
        #estos valores se actualizan desde la GUI
        Kv=settings.VDE_K1
        Kp=settings.VDE_K2
        pos=-pos
        
        self.Velocidad=(pos-prev_pos)/(T_previo-T_actual)
        self.Posicion=pos

        print(f"pos={pos}")
        print(f"velocidad={self.Velocidad}}")

        control_angle=Kv*self.Velocidad+Kp*self.Posicion

        return control_angle
