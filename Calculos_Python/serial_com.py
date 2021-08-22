from serial_frame import angulos2protocolo
import platform_definition
import serial
import numpy as np

"""
Created on Fri Jun 19:38 2021

@author: Gaston Meghinasso

Toma como parametros los angulos y altura deseadas en la plataforma y 
Envia los comandos necesarios por USB para realizar el movimiento
"""

def send_command_to_platform(port,x_ang,y_ang,altura):
    p=platform_definition.platform(d=6,D=10,l1=6,l2=13,max_limb_error=0.00001,max_limb_try_count=30,max_joint_angle=23*np.pi/180)
    try:
        rad_x_ang=x_ang*np.pi/180
        rad_y_ang=y_ang*np.pi/180
        p.solve_platform(rad_x_ang,rad_y_ang,altura)

    except:
        print("Point unreachable")
    else:
        print(f'motor 1:{p.ang1*180/np.pi}')
        print(f'motor 2:{p.ang2*180/np.pi}')
        print(f'motor 3:{p.ang3*180/np.pi}')
        ang_motor_1= int( (p.ang1*180/np.pi +80) *1000   ) # Multiplico por mil porque el frame es en milesimas de grado
        ang_motor_2= int( (p.ang2*180/np.pi +88) *1000   )
        ang_motor_3= int( (p.ang3*180/np.pi +86) *1000   )
        ser = serial.Serial(port,baudrate = 9600,timeout=1)
        trama = angulos2protocolo(ang_motor_1,ang_motor_2,ang_motor_3)


        ser.write(bytes(trama))