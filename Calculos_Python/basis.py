import numpy as np

####################################### Funciones de rotación de puntos ################################################
def x_rotation_matrix(r_x):
    return np.array([[1,0,0],[0,np.cos(r_x),np.sin(r_x)],[0,-np.sin(r_x),np.cos(r_x)]]) 
    
def y_rotation_matrix(r_y):
    return np.array([[np.cos(r_y),0,-np.sin(r_y)],[0,1,0],[np.sin(r_y),0,np.cos(r_y)]])

def rotate_in_y_axis(point,r_y):
    W=y_rotation_matrix(r_y)
    return np.dot(W,point)

def rotate_in_x_axis(point,r_x):
    W=x_rotation_matrix(r_x)
    return np.dot(W,point)

####################################### Funciones de cambio de base ################################################
def get_m2_basis():
    #Función que retorna la matriz de cambio de base desde la canónica a la base del motor2
    # La base se genera de la misma forma que el motor 3
    Wm2=np.array([[-np.cos(np.pi/3),np.cos(np.pi/6),0],[-np.sin(np.pi/3),-np.sin(np.pi/6),0],[0,0,1]])
    return Wm2

def get_m3_basis():
    #Función que retorna la matriz de cambio de base desde la canónica a la base del motor3
    #El sistema de referencia del motor 3 se define de la siguiente forma:
    ## El eje y positivo es paralelo al plano x-y canónico y su dirección y sentido está determinada por el vector
    ## que va desde el eje del motor 3 al centro de la plaforma
    ## el eje x positivo es paralelo al plano x-y canónico y se encuentra perpendicular al eje 'y' y a la derecha del mismo
    ## El eje z es el mismo que el de la base canónica
    Wm3=np.array([[-np.cos(np.pi/3),-np.cos(np.pi/6),0],[np.sin(np.pi/3),-np.sin(np.pi/6),0],[0,0,1]])
    return Wm3
def get_m1_basis():
    #Función que retorna la matriz de cambio de base desde la canónica a la base del motor1
    # La base del motor 1 corresponde a la base canónica
    Wm1=np.identity(3)
    return Wm1


def base_change_cannon_to_m1(point):
    return point


def base_change_cannon_to_m2(point):
    Wm2=get_m2_basis()
    return np.linalg.solve(Wm2,point)

def base_change_cannon_to_m3(point):
    Wm3=get_m3_basis()
    return np.linalg.solve(Wm3,point)

def base_change_m3_to_cannon(point):
    Wm3=get_m3_basis()
    return np.dot(Wm3,point)

def base_change_m2_to_cannon(point):
    Wm2=get_m2_basis()
    return np.dot(Wm2,point)

def base_change_m1_to_cannon(point):
    return point