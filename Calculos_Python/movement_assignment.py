import numpy as np
import cmath
import basis 
def assign_movement(r_x,r_y):
    "Segunda versión de la función para asignar el movimiento"
    "toma como parametros los dos ángulos en el eje x y en el eje y"
    "y devuelve la junta a actuar, el movimiento y el ángulo"
        
    #obtengo el gradiente del plano que pasa por (0,0,0)
    #y cumple con los ángulos r_x y r_y
    grad_plane=np.array([np.tan(r_x),np.tan(r_y)]) 
    ball_dir=-grad_plane #La dirección en la cual se desplaza la pelota es la del -grad(plano)
                         #Este es el caso ideal sin las restricciones de la plataforma   
    #Aproximo la dirección deseada a algunas de las posibles dadas las restricciones de la plataforma
    ##Convertimos ball_dir a coordenadas polares y nos quedamos con el ángulo para compararlo con las direcciones
    ##posibles
    angle=cmath.polar(ball_dir[0]+1j*ball_dir[1])[1]*(180/np.pi)
    ##Dividimos los 360 grados en las direcciones posible y asignamos el movimiento
    sentido=1 #uso esta variable para invertir el sentido del vector dado que trabajo con cuadrantes 1 y 2
    if angle<0:
        angle+=180 #Cómo todavía no calculo el sentido sino la dirección sumo 180 para solo trabajar con los 1er y 2do cuadrantes
        sentido=-1 #Cómo esto corresponde a cuadrantes 3 y 4 invierto el sentido del vector calculado a continuación
    if angle > 165:
        movement= "roll"
        joint="C1"
        roll_vector=pol2rect(1,180 * np.pi/180) #vector que indica la dirección y sentido en la cual se mueve la pelota                                      #es la mejor aproximación del -grad(plano) que permite la plataforma
    if angle > 135 and angle <= 165:
        movement= "pitch"
        joint="C2"
        roll_vector=pol2rect(1,150 * np.pi/180)
    if angle > 105 and angle <= 135:
        movement= "roll"
        joint="C3"
        roll_vector=pol2rect(1,120 * np.pi/180)
    if angle > 75 and angle <= 105:
        movement= "pitch"
        joint="C1"
        roll_vector=pol2rect(1,90 * np.pi/180)
    if angle <= 75 and angle >45:
        movement= "roll"
        joint="C2"
        roll_vector=pol2rect(1,60 * np.pi/180)
    if angle <= 45 and angle >15:
        movement= "pitch"
        joint="C3"
        roll_vector=pol2rect(1,30 * np.pi/180)
    if angle <= 15:
        movement= "roll"
        joint="C1"
        roll_vector=pol2rect(1,0 * np.pi/180)

    roll_vector=roll_vector*sentido #corrijo el sentido si es necesario
    #Calculo el ángulo que se debe realizar en el movimiento
    movement_angle=calculate_angle(ball_dir,roll_vector,joint,movement)
    return joint,movement,movement_angle


def pol2rect(mod,ang):
    #Función que realiza la conversión de polar a cartesiana
    dir=cmath.exp(1j*ang)
    return np.array([dir.real,dir.imag,0])

def calculate_angle(ball_dir,roll_vector,joint,movement):
    #Función que obtiene el ángulo de inclinación que se le va a dar a la junta actuada
    #Usa el mismo ángulo que el del grandiente original
    angle=np.arctan(np.linalg.norm(ball_dir))
    ##determino el sentido de movimiento para determinar si el ángulo es positivo o negativo
    #Cambio el sistema de referencia al de la junta que debe actuarse
    if joint=="C1":
        roll_vector=basis.base_change_cannon_to_m1(roll_vector)
    if joint=="C2":
        roll_vector=basis.base_change_cannon_to_m2(roll_vector)
    if joint=="C3":
        roll_vector=basis.base_change_cannon_to_m3(roll_vector)
    if movement=="roll" and roll_vector[0]<0:
        #Si el movimiento es de roll y la dirección del roll en el marco de referencia del motor/junta
        # indicado es en la dirección de las x's negativas, entonces el ángulo debe ser negativo
        angle=angle*(-1)

    if movement=="pitch" and roll_vector[1]<0:
        #Si el movimiento es de pitch y la dirección del pitch en el marco de referencia del motor/junta
        # indicado es en la dirección de las y's negativas, entonces el ángulo debe ser negativo
        angle=angle*(-1)

    return angle
