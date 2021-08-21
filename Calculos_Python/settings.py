
#defino las variables globales que quiero configurar desde la interfaz 


class ball_t:
    def __init__(self):
        self.pos_x=0
        self.pos_y=0

def init():
    global Kp 
    global Ki
    global Kd 
    global ball_pos
    global pos_y
    global pos_x
    Kp=0
    Ki=0
    Kd=0
    pos_x=0
    pos_y=0
    ball_pos=ball_t()



