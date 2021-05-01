import numpy as np

def get_joint_angle(c1,c2,c3,joint):
    "Función que obtiene el ángulo que se le exige a cada junta universal"
    "Lo que hace es tomar las distancias relativas entre cada una de las juntas"
    "y cambiar la base de los punto a una donde el eje Y atravieza el plato desde la junta analizada"
    "el eje Z permanece siendo el mismo de la base y el eje X es perpendicular a Y y Z"
    "Con las coordenadas relativas transformadas en X y Z calcula el ángulo que debe rotar la junta universal"
    "Si el plato se encuentra horizontal al piso, la función retorna 0"
    #vectores entre las juntas
    c13=c3-c1 
    c12=c2-c1
    c23=c3-c2
    c21=c1-c2
    c31=c1-c3
    c32=c2-c3
    
    #Obtengo la base de la junta en cada caso
    if joint=="C1":
        #El eje Y es la suma de las distancia C13 y C12 (vector sobre el plato que apunta hacia adelante)
        y=c13+c12
        y=y/np.linalg.norm(y)
        #El eje Z no cambia
        z=np.array([0,0,1])
        #El eje x es el producto vectorial entre el el vector "y" y el eje Z 
        x=np.cross(y,z)
        
    if joint=="C2":
        y=c23+c21
        y=y/np.linalg.norm(y)
        #El eje Z no cambia
        z=np.array([0,0,1])
        #El eje x es el producto vectorial entre el el vector "y" y el eje Z 
        x=np.cross(y,z)
    if joint=="C3":
        y=c32+c31
        y=y/np.linalg.norm(y)
        #El eje Z no cambia
        z=np.array([0,0,1])
        #El eje x es el producto vectorial entre el el vector "y" y el eje Z 
        x=np.cross(y,z)
    
    W=np.array([x,y,z]).transpose()

    
    #cambio de base los puntos
    c1_t=np.linalg.solve(W,c1)
    c2_t=np.linalg.solve(W,c2)
    c3_t=np.linalg.solve(W,c3)
    c13_t=c3_t-c1_t 
    c12_t=c2_t-c1_t
    c23_t=c3_t-c2_t
    c21_t=c1_t-c2_t
    c31_t=c1_t-c3_t
    c32_t=c2_t-c3_t
    if joint=="C1":
        angle=np.arctan(c13_t[2]/c13_t[0])
    if joint=="C2":
        angle=np.arctan(c23_t[2]/c23_t[0])
    if joint=="C3":
        angle=np.arctan(c32_t[2]/c32_t[0])
    return angle



def check_motor_height (c1,c2,c3,D):
    h=2.5
    largo=2
    ancho=5
    
    c1x=c1[0]
    c2x=c2[0]
    c3x=c3[0]
        
    c1y=c1[1]
    c2y=c2[1]
    c3y=c3[1]
        
    c1z=c1[2]
    c2z=c2[2]
    c3z=c3[2]
        
    A=np.array([[c1x,c1y,1],[c2x,c2y,1],[c3x,c3y,1]])
    B=np.array([c1z,c2z,c3z]).transpose()
    params=np.linalg.solve(A,B)
    for x in np.linspace(start=0,stop=ancho,num=50):
        point=np.array([[x],[-D-largo],[1]])
        height_plato=np.dot(params,point)
        if height_plato<h:
            return -1