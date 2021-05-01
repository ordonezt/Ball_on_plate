import numpy as np
 
def check_angles(platform):
       for joint in ["C1","C2","C3"]:
           angle=get_joint_angle(platform,joint)
           if np.abs(angle)> self.max_joint_angle:
               #raise ValueError('Joint angle exceeded\n {}.angle={}º >{}º'.format(joint,angle*180/np.pi,self.max_joint_angle*180/np.pi))
               print('Joint angle exceeded\n {}.angle={}º >{}º'.format(joint,angle*180/np.pi,self.max_joint_angle*180/np.pi))
               return -1
           else:
               return 0


def get_joint_angle(platform,joint):
        "Función que obtiene el ángulo que se le exige a cada junta universal"
        "Lo que hace es tomar las distancias relativas entre cada una de las juntas"
        "y cambiar la base de los punto a una donde el eje Y atravieza el plato desde la junta analizada"
        "el eje Z permanece siendo el mismo de la base y el eje X es perpendicular a Y y Z"
        "Con las coordenadas relativas transformadas en X y Z calcula el ángulo que debe rotar la junta universal"
        "Si el plato se encuentra horizontal al piso, la función retorna 0"
        #vectores entre las juntas
        c13=platform.c3-platform.c1 
        c12=platform.c2-platform.c1
        c23=platform.c3-platform.c2
        c21=platform.c1-platform.c2
        c31=platform.c1-platform.c3
        c32=platform.c2-platform.c3
        
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
        c1_t=np.linalg.solve(W,platform.c1)
        c2_t=np.linalg.solve(W,platform.c2)
        c3_t=np.linalg.solve(W,platform.c3)
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