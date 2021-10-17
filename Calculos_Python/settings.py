
#defino las variables globales que quiero configurar desde la interfaz 


class ball_t:
    def __init__(self):
        self.pos_x=0
        self.pos_y=0

def init():
    global Kp 
    global Ki
    global Kd

    global VDE_K1
    global VDE_K2
    global VDE_K3
    


    
    global ball_pos
    global pos_y
    global pos_x
    global control_state
    global controller
    controller="PID"
    #setting controlador lineal
    Kp=0
    Ki=0
    Kd=0
    #settings controlador VDE
    VDE_K1=0
    VDE_K2=0
    VDE_K3=0

    pos_x=0
    pos_y=0
    control_state="Running"
    ball_pos=ball_t()



