from serial_frame import angulos2protocolo
import platform_definition
import serial
import numpy as np
import limb
import basis
"""
Created on Fri Jun 19:38 2021

@author: Gaston Meghinasso

Toma como parametros los angulos y altura deseadas en la plataforma y 
Envia los comandos necesarios por USB para realizar el movimiento
"""

#Function that performs the rotation
def rotate_vector(ang_x,ang_y,p):
    Mx=np.array([[1,0,0],[0,np.cos(ang_x),-np.sin(ang_x)],[0,np.sin(ang_x),np.cos(ang_x)]])
    My=np.array([[np.cos(ang_y),0,np.sin(ang_y)],[0,1,0],[-np.sin(ang_y),0,np.cos(ang_y)]])
    Mxy=np.dot(Mx,My)
    p_rot=np.dot(Mxy,p)
    return p_rot

def send_command_to_platform(port,x_ang,y_ang,altura):

    if(x_ang>20):
        x_ang=20

    if(y_ang>20):
        y_ang=20

    if(x_ang<-20):
        x_ang=-20

    if(y_ang<-20):
        y_ang=-20
    #positions of the ball joins when they are unactuated
    dist=6
    C1=dist*np.array([0,-1,0])
    C2=dist*np.array([-np.cos(np.pi*30/180),np.sin(np.pi*30/180),0])
    C3=dist*np.array([np.cos(np.pi*30/180),np.sin(np.pi*30/180),0])
    #making the rotation of the joints

    
    x_ang=x_ang*np.pi/180
    y_ang=y_ang*np.pi/180
    print(x_ang)
    print(y_ang)


    C1r=rotate_vector(y_ang,x_ang,C1)
    C2r=rotate_vector(y_ang,x_ang,C2)
    C3r=rotate_vector(y_ang,x_ang,C3)
    #calculo el angulo de los motores
    print(C1r)
    print(C2r)
    print(C3r)
    
    P1=basis.base_change_cannon_to_m1(C1r)+np.array([0,10,altura])
    P2=basis.base_change_cannon_to_m2(C2r)+np.array([0,10,altura])
    P3=basis.base_change_cannon_to_m3(C3r)+np.array([0,10,altura])

    limb_1=limb.limb(l1=6,l2=13)
    limb_2=limb.limb(l1=6,l2=12.5)
    limb_3=limb.limb(l1=6,l2=13)
    try:
        ang1=limb_1.calculate_motor_angle(P1,0.01,30)
        ang2=limb_2.calculate_motor_angle(P2,0.01,30)
        ang3=limb_3.calculate_motor_angle(P3,0.01,30)
    except:
        pass
    else:
        print(f'motor 1:{ang1*180/np.pi}')
        print(f'motor 2:{ang2*180/np.pi}')
        print(f'motor 3:{ang3*180/np.pi}')
        ang_motor_1= int( (ang1*180/np.pi +80) *1000   ) # Multiplico por mil porque el frame es en milesimas de grado
        ang_motor_2= int( (ang2*180/np.pi +86) *1000   )
        ang_motor_3= int( (ang3*180/np.pi +86) *1000   )
        ser = serial.Serial(port,baudrate = 9600,timeout=1)
        trama = angulos2protocolo(ang_motor_1,ang_motor_2,ang_motor_3)
        ser.write(bytes(trama))