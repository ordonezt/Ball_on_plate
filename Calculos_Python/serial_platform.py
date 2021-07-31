import argparse
from serial_com import send_command_to_platform


# este comando setea los angulos x e y de la plataforma y la altura

parser = argparse.ArgumentParser()

parser.add_argument("port", type=str,
                    help="Puerto utilizado para la comunicación")

parser.add_argument("x_ang", type=float,
                    help="Ángulo del eje x")

parser.add_argument("y_ang", type=float,
                    help="Ángulo del eje y")

parser.add_argument("altura", type=float,
                    help="Altura requerida para la plataforma")

args = parser.parse_args()



send_command_to_platform(args.port,args.x_ang,args.y_ang,args.altura)