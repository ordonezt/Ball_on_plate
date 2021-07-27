

"""
Created on Fri Jun 19:38 2021

@author: Gastón Meghinasso

Toma como parametros los ángulos y altura deseadas en la plataforma y 
Envía los comandos necesarios por USB para realizar el movimiento
"""


from serial_com import send_command_to_platform
import numpy as np
import time

angle_x_space=np.linspace(start=-19,stop=19,num=20)
angle_y_space=np.linspace(start=-19,stop=19,num=20)
h_space=np.linspace(start=10,stop=16,num=20)

for h in h_space:
    for ang_x in angle_x_space:
        for angle_y in angle_y_space:
            send_command_to_platform("/dev/ttyACM0",ang_x,angle_y,h)
            time.sleep(0.05)