import json
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

    global ball_pos
    global pos_y
    global pos_x
    global control_state
    global controller
    global selected_camera
    global plotting_enabled
    global excel_enabled

    global Escala_y
    global Escala_x
    global log
    controller="PID"
    #setting controlador lineal
    Kp=0
    Ki=0
    Kd=0
    #settings controlador VDE
    VDE_K1=0
    VDE_K2=0

    Escala_y=0
    Escala_x=0

    #Variable global que habilita el ploteo en tiempo real
    plotting_enabled=False
    excel_enabled=False
    #diccionario con los valores obtenidos
    log={"pos_x":[],"pos_y":[],"angle_x":[],"angle_y":[]}
    pos_x=0
    pos_y=0
    control_state="Running"
    ball_pos=ball_t()

    selected_camera=2

def save_image_settings(settings):
    with open('./image_settings.json', "w") as file:
        data=json.dumps(settings)
        file.write(data)
    return

def load_image_settings():
    with open('./image_settings.json', "r") as file:
        data=file.read()
        return json.loads(data)


