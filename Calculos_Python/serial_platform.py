import argparse
from serial_frame import angulos2protocolo
import platform_definition
import serial
import numpy as np

# este comando setea los angulos x e y de la plataforma y la altura

parser = argparse.ArgumentParser()

parser.add_argument("port", type=str,
                    help="Puerto utilizado para la comunicación")

parser.add_argument("x_ang", type=int,
                    help="Ángulo del eje x")

parser.add_argument("y_ang", type=int,
                    help="Ángulo del eje y")

parser.add_argument("altura", type=int,
                    help="Altura requerida para la plataforma")

args = parser.parse_args()

#Defino los parametros de la plataforma
p=platform_definition.platform(d=6,D=10,l1=6,l2=12,max_limb_error=0.00001,max_limb_try_count=30,max_joint_angle=23*np.pi/180)



try:
    rad_x_ang=args.x_ang*np.pi/180
    rad_y_ang=args.y_ang*np.pi/180
    p.solve_platform(rad_x_ang,rad_y_ang,args.altura)

except:
    print("Point unreachable")
else:
    ang_motor_1= int( (p.ang1*180/np.pi) *1000   ) # Multiplico por mil porque el frame es en milesimas de grado
    ang_motor_2= int( (p.ang2*180/np.pi) *1000   )
    ang_motor_3= int( (p.ang3*180/np.pi) *1000   )
    ser = serial.Serial(args.port,baudrate = 9600,timeout=1)
    trama = angulos2protocolo(ang_motor_1,ang_motor_2,ang_motor_3)


    ser.write(bytes(trama))

	

