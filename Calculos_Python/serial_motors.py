import argparse
from serial_frame import angulos2protocolo
import platform_definition
import serial
import time

# este comando setea los angulos de cada motor en grados

parser = argparse.ArgumentParser()

parser.add_argument("port", type=str,
                    help="Puerto utilizado para la comunicación")

parser.add_argument("ang_motor_1", type=int,
                    help="Ángulo del motor 1")

parser.add_argument("ang_motor_2", type=int,
                    help="Ángulo del motor 2")

parser.add_argument("ang_motor_3", type=int,
                    help="Ángulo del motor 3")

args = parser.parse_args()


ser = serial.Serial(args.port,baudrate = 9600,timeout=1)

args.ang_motor_1+=80
args.ang_motor_2+=84
args.ang_motor_3+=86

trama = angulos2protocolo(args.ang_motor_1*1000,args.ang_motor_2*1000,args.ang_motor_3*1000)
ser.write(bytes(trama))


	

