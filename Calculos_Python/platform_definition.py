import numpy as np
import cmath
import pyperclip
import geogebra
import limb
import movement_assignment
import checks
import basis
import design_utils

class platform:
    def __init__(self,d,D,l1,l2,max_limb_error,max_limb_try_count,max_joint_angle):
        "d: distancia de cada junta universal en la plataforma al centro"
        
        "D: distancia del eje de cada motor al centro de la base"
        
        "la altura del eje del motor es conciderada el plano z=0"
        
        "l1: long del antebrazo"
        
        "l2: long del brazo"
        
        "max_limb_error: máximo error (en las mismas unidades de l1 y l2) que es permitido para posicionar el brazo"
        
        "max_limb_try_count: máxima cantidad de iteraciones para calcular el ángulo de un motor, si la cantidad"
        "Si la cantidad requerida de iteraciones es mayor, genera un error llamado 'Point unreachable' "
        
        "max_joint_angle:angulo máximo que puede tener la junta universal, una posición que lo exceda genera un error"
        "llamado 'Joint angle exceeded'"
        
        self.c1=np.array([0,-d,0])
        self.c2=np.array([-d*np.sin(np.pi/3),d*np.cos(np.pi/3),0])
        self.c3=np.array([d*np.sin(np.pi/3),d*np.cos(np.pi/3),0])
        
        self.d=d
        self.D=D

        self.l1=l1
        self.l2=l2
        
        self.max_limb_error=max_limb_error
        self.max_limb_try_count=max_limb_try_count
        
        #defino los angulos de los motores
        self.ang1=0
        self.ang2=0
        self.ang3=0
        #defino los angulos máximos que se les permite rotar a los motores
        self.angle_max=90
        self.angle_min=-90
        #defino el ángulo máximo permitido en las juntas universales
        self.max_joint_angle=max_joint_angle        

    def reset_platform (self):
        #función que vuelve a la plataforma a su estado sin actuar
        self.c1=self.d*np.array([0,-1,0])
        self.c2=self.d*np.array([-1*np.sin(np.pi/3),np.cos(np.pi/3),0])
        self.c3=self.d*np.array([np.sin(np.pi/3),np.cos(np.pi/3),0])
        #defino los angulos de los motores
        self.ang1=0
        self.ang2=0
        self.ang3=0
        
    def rotate(self,movement,joint,angle):
        #Cambio la base de referencia a la de la junta en la cual se realiza el movimiento
        if joint=="C1":
            self.c1=basis.base_change_cannon_to_m1(self.c1)
            self.c2=basis.base_change_cannon_to_m1(self.c2)
            self.c3=basis.base_change_cannon_to_m1(self.c3)              
        if joint=="C2":
            self.c1=basis.base_change_cannon_to_m2(self.c1)
            self.c2=basis.base_change_cannon_to_m2(self.c2)
            self.c3=basis.base_change_cannon_to_m2(self.c3)                 
        if joint=="C3":
            self.c1=basis.base_change_cannon_to_m3(self.c1)
            self.c2=basis.base_change_cannon_to_m3(self.c2)
            self.c3=basis.base_change_cannon_to_m3(self.c3)
        #Realizo la rotación
        if movement=="pitch":
            self.c1=basis.rotate_in_x_axis(self.c1,angle)
            self.c2=basis.rotate_in_x_axis(self.c2,angle)
            self.c3=basis.rotate_in_x_axis(self.c3,angle)    
        if movement=="roll":
            self.c1=basis.rotate_in_y_axis(self.c1,angle)
            self.c2=basis.rotate_in_y_axis(self.c2,angle)
            self.c3=basis.rotate_in_y_axis(self.c3,angle)
            
        #Corrijo el offset de la plataforma
        ##Siempre tomo la junta de la izquiera como referencia en cada caso
        if joint=="C1":
            self.apply_offset(self.c2)
        if joint=="C2":
            self.apply_offset(self.c3)
        if joint=="C3":
            self.apply_offset(self.c1)
        #Cambiamos a la base orginal
        if joint=="C1":
            self.c1=basis.base_change_m1_to_cannon(self.c1)
            self.c2=basis.base_change_m1_to_cannon(self.c2)
            self.c3=basis.base_change_m1_to_cannon(self.c3)              
        if joint=="C2":
            self.c1=basis.base_change_m2_to_cannon(self.c1)
            self.c2=basis.base_change_m2_to_cannon(self.c2)
            self.c3=basis.base_change_m2_to_cannon(self.c3)                 
        if joint=="C3":
            self.c1=basis.base_change_m3_to_cannon(self.c1)
            self.c2=basis.base_change_m3_to_cannon(self.c2)
            self.c3=basis.base_change_m3_to_cannon(self.c3)           
        
    def apply_offset (self,pos):
        "la función desplaza la plataforma el offset correspondiente para compenzar el introducido por la rotación"
        allowed_pos=-pos[0]*np.tan(np.pi/6)
        offset=np.array([0,allowed_pos-pos[1],0])
        self.c1=self.c1+offset
        self.c2=self.c2+offset
        self.c3=self.c3+offset
        
        
    def calculate_P(self):
        #Función que obtiene las coordenadas de las juntas c1,c2,c3 en las bases de los motores m1,m2 y m3
        #respectivamente. Se le suma el vector (0,D,0) para establecer el punto de origen en el rotor del motor
        P1=basis.base_change_cannon_to_m1(self.c1)+np.array([0,self.D,0])
        P2=basis.base_change_cannon_to_m2(self.c2)+np.array([0,self.D,0])
        P3=basis.base_change_cannon_to_m3(self.c3)+np.array([0,self.D,0])
        #elimino la coordenana en x. Dado que las juntas se desplazan por el plano y-z de cada motor la coordenada en x es siempre cero
        P1=np.array([P1[1],P1[2]])
        P2=np.array([P2[1],P2[2]])
        P3=np.array([P3[1],P3[2]])
        return P1,P2,P3
    

        
    def correct_height(self,h):
        #Función que dada la posición de las 3 juntas en el espacio cálcula la altura del centro de la plataforma
        #y desplaza las juntas verticalmente para cumplir con la altura solicitada
        
        #Obtengo las componentes x,y,z de las juntas
        c1x=self.c1[0]
        c2x=self.c2[0]
        c3x=self.c3[0]
        
        c1y=self.c1[1]
        c2y=self.c2[1]
        c3y=self.c3[1]
        
        c1z=self.c1[2]
        c2z=self.c2[2]
        c3z=self.c3[2]
        #Dada la ecuación del plano Z= q1 * x + q2 * y + q3, donde q1,2,3 son los parametros que definen el plano
        #Es posible encontrar el valor de los 3 parametros si se poseen 3 puntos que definan el plano 
        #Particularmente el parametro q3 nos da la altura del plano en el centro de la plataforma q3=Z(x=0,y=0)
        #A continuación lo que se hace es resolver el sistema matricial con los 3 puntos siendo las juntas 
        #y los parametros del plano siendo la variable params. El parametro q3 es params[2]
        A=np.array([[c1x,c1y,1],[c2x,c2y,1],[c3x,c3y,1]])
        B=np.array([c1z,c2z,c3z]).transpose()
        params=np.linalg.solve(A,B)
        #Obtengo un vector de offset que sumado a las juntas las desplace a la posición deseada
        offset=np.array([0,0,h-params[2]])
        #corrijo la altura
        self.c1=self.c1+offset
        self.c2=self.c2+offset
        self.c3=self.c3+offset
        

    def solve_platform(self,r_x,r_y,h):
        #Función que dados los ángulos en x e y y la altura deseada, obtiene los ángulos de los motores para
        #alcanzarlo
        
        self.reset_platform() #pongo las juntas en la posición inicial para empezar el analisis
        if r_x==0 and r_y==0:
            #Este if se utiliza para no calcular rotaciones cuando los ángulos de ambos ejes son cero
            self.correct_height(h)
        else:
            joint,movement,angle=movement_assignment.assign_movement(r_x,r_y)
            #assign_movement calcula la junta, el movimiento y el ángulo necesario para realizar de forma
            #aproximada los angulos requeridos en x y en y
            self.rotate(movement,joint,angle)
            self.correct_height(h) #llevo la plataforma a la altura indicada
        
        P1,P2,P3=self.calculate_P() #referencio las 3 juntas C1,C2,C3 a los planos de referencia de su respectivo
                                    #motor, tomando el rotor del motor como punto (0,0). El analisis se realiza en 
                                    #dos dimensiones dado que las juntas se mueven sobre un plano. Las juntas referenciadas
                                    #pasan a llamarse P1,P2 y P3 respectivamente
                    
        limb_i=limb.limb(self.l1,self.l2) #defino el objeto que representa cada brazo de la plataforma
        #Calculo los angulos necesarios en cada motor dado un error máximo en cm de la posición del punto P1,2,3
        #Y un número máximo de iteraciones posibles para llegar al resultado
        self.ang1=limb_i.calculate_motor_angle(P1,self.max_limb_error,self.max_limb_try_count)
        self.ang2=limb_i.calculate_motor_angle(P2,self.max_limb_error,self.max_limb_try_count)
        self.ang3=limb_i.calculate_motor_angle(P3,self.max_limb_error,self.max_limb_try_count)
        #Chekeo que el ángulo en las juntas universales no supere el máximo que permiten
        for joint in ["C1","C2","C3"]:
            angle=checks.get_joint_angle(self.c1,self.c2,self.c3,joint)
            if np.abs(angle)> self.max_joint_angle:
                raise ValueError('Joint angle exceeded\n {}.angle={}º >{}º'.format(joint,angle*180/np.pi,self.max_joint_angle*180/np.pi))
                print('Joint angle exceeded\n {}.angle={}º >{}º'.format(joint,angle*180/np.pi,self.max_joint_angle*180/np.pi))
                return -1
            else:
                return 0       