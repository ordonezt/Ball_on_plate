import threading
import settings
from serial_com import send_command_to_platform
#declaro las variables como globales para que puedan ser accedidas por
# el thread de modificación




class controller_t:
    def __init__(self):
        self.prev_pos_x=0 #variable auxiliar para el control derivativo
        self.prev_pos_y=0 #variable auxiliar para el control derivativo

        self.Integral=0 #variable auxiliar para el control integral
        self.T=1/30 #30FPS



    def control(self,ball_pos):
        angle_x=self.controller_1d(ball_pos.pos_x,self.prev_pos_x)
        angle_y=self.controller_1d(ball_pos.pos_y,self.prev_pos_y)

        self.prev_pos_x=ball_pos.pos_x
        self.prev_pos_y=ball_pos.pos_y
    
        print('angle_x={0}\n'.format(angle_x))
        print('angle_y={0}\n'.format(angle_y))
        #print("Envio de comando a la plataforma comentado!!")
        send_command_to_platform("/dev/ttyACM0",angle_x,angle_y,13)
        return angle_x,angle_x

    def controller_1d(self,pos,prev_pos):
        #estos valores se actualizan desde la GUI
        Ki=settings.Ki
        Kp=settings.Kp
        Kd=settings.Kd
        pos=-pos
        #parte integral
        self.Integral=self.Integral + pos * Ki * self.T
        #parte proporcional
        Propocional=pos * Kp
        #parte derivativa
        print(f"pos={pos}")
        print(f"prev_pos={prev_pos}")
        
        Derivativa=-(-pos-prev_pos) * Kd /self.T

        control_angle=self.Integral+Propocional+Derivativa

        return control_angle

    

