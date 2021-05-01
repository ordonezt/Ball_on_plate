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
    def x_rotation_matrix(self,r_x):
        return np.array([[1,0,0],[0,np.cos(r_x),-np.sin(r_x)],[0,np.sin(r_x),np.cos(r_x)]]) 
    
    def y_rotation_matrix(self,r_y):
        return np.array([[np.cos(r_y),0,np.sin(r_y)],[0,1,0],[-np.sin(r_y),0,np.cos(r_y)]])
          
    def rotate(self,movement,joint,angle):
        if movement=="pitch":
            M_r=self.x_rotation_matrix(angle)
        if movement=="roll":
            M_r=self.y_rotation_matrix(angle)
            
        if joint=="C1":
            wm=np.identity(3)
        if joint=="C2":
            wm=self.get_m2_basis()
        if joint=="C3":
            wm=self.get_m3_basis()
        #transformamos los puntos a la base conveniente
        self.c1=np.linalg.solve(wm,self.c1)
        self.c2=np.linalg.solve(wm,self.c2)
        self.c3=np.linalg.solve(wm,self.c3)
        #realizamos la rotación de los mismos
        self.c1=M_r.dot(self.c1)
        self.c2=M_r.dot(self.c2)
        self.c3=M_r.dot(self.c3)
        #corregimos el offset de la plataforma
        if joint=="C1":
            self.apply_offset(self.c2)
        if joint=="C2":
            self.apply_offset(self.c3)
        if joint=="C3":
            self.apply_offset(self.c1)
        #obtengo los puntos en la base original
        self.c1=wm.dot(self.c1)
        self.c2=wm.dot(self.c2)  
        self.c3=wm.dot(self.c3)
        
    def apply_offset (self,pos):
        "la función desplaza la plataforma el offset correspondiente para compenzar el introducido por la rotación"
        allowed_pos=-pos[0]*np.tan(np.pi/6)
        offset=np.array([0,allowed_pos-pos[1],0])
        self.c1=self.c1+offset
        self.c2=self.c2+offset
        self.c3=self.c3+offset
        
    def get_m2_basis(self):
        Wm2=np.array([[-np.cos(np.pi/3),np.cos(np.pi/6),0],[-np.sin(np.pi/3),-np.sin(np.pi/6),0],[0,0,1]])
        return Wm2

    def get_m3_basis(self):
        Wm3=np.array([[-np.cos(np.pi/3),-np.cos(np.pi/6),0],[np.sin(np.pi/3),-np.sin(np.pi/6),0],[0,0,1]])
        return Wm3
    
        
    def calculate_P(self):
            wm2=self.get_m2_basis()
            wm3=self.get_m3_basis()
            P1=self.c1+np.array([0,self.D,0])
            P2=np.linalg.solve(wm2,self.c2)+np.array([0,self.D,0])
            P3=np.linalg.solve(wm3,self.c3)+np.array([0,self.D,0])
            #elimino la coordenana en x
            P1=np.array([P1[1],P1[2]])
            P2=np.array([P2[1],P2[2]])
            P3=np.array([P3[1],P3[2]])
            return P1,P2,P3
    

        
    def correct_height(self,h):
        c1x=self.c1[0]
        c2x=self.c2[0]
        c3x=self.c3[0]
        
        c1y=self.c1[1]
        c2y=self.c2[1]
        c3y=self.c3[1]
        
        c1z=self.c1[2]
        c2z=self.c2[2]
        c3z=self.c3[2]
        
        A=np.array([[c1x,c1y,1],[c2x,c2y,1],[c3x,c3y,1]])
        B=np.array([c1z,c2z,c3z]).transpose()
        params=np.linalg.solve(A,B)
        offset=np.array([0,0,h-params[2]])
        #corrijo la altura
        self.c1=self.c1+offset
        self.c2=self.c2+offset
        self.c3=self.c3+offset
        

    def solve_platform(self,r_x,r_y,h):
        if r_x==0 and r_y==0:
            #Este if se utiliza para no calcular rotaciones cuando los ángulos de ambos ejes son cero
            self.correct_height(h)
        else:
            joint,movement,angle=movement_assignment.assign_movement(r_x,r_y)
            self.rotate(movement,joint,angle)
            self.correct_height(h)
        
        P1,P2,P3=self.calculate_P()
        limb_i=limb(self.l1,self.l2)
        self.ang1=limb_i.calculate_motor_angle(P1,self.max_limb_error,self.max_limb_try_count)
        self.ang2=limb_i.calculate_motor_angle(P2,self.max_limb_error,self.max_limb_try_count)
        self.ang3=limb_i.calculate_motor_angle(P3,self.max_limb_error,self.max_limb_try_count)
        #Chekeo el ángulo necesario en las juntas universales
        return universal_joint_angles.check_angles(self)


    

        
    
    
    def get_gradient(self):
        c1x=self.c1[0]
        c2x=self.c2[0]
        c3x=self.c3[0]
        
        c1y=self.c1[1]
        c2y=self.c2[1]
        c3y=self.c3[1]
        
        c1z=self.c1[2]
        c2z=self.c2[2]
        c3z=self.c3[2]
        
        A=np.array([[c1x,c1y,1],[c2x,c2y,1],[c3x,c3y,1]])
        B=np.array([c1z,c2z,c3z]).transpose()
        params=np.linalg.solve(A,B)
        return params
        