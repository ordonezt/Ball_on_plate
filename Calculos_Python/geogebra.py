import numpy as np
import basis

class geogebra_script:
    def __init__(self):
        self.script=""
        self.first_item=1
        
    def add_point(self,point,name):
        if self.first_item==0:
            self.script+=","
        self.first_item=0
        self.script+="\"{0}=({1:.3f},{2:.3f},{3:.3f})\"\n".format(name,point[0],point[1],point[2])

    def add_2D_point(self,point,name):
        if self.first_item==0:
            self.script+=","
        self.first_item=0
        self.script+="\"{0}=({1:.3f},{2:.3f})\"\n".format(name,point[0],point[1])
        
    def define_polygon(self,point1,point2,point3):
        if self.first_item==0:
            self.script+=","
        self.first_item=0
        self.script+="\""
        self.script+="Polygon({},{}, {})".format(point1,point2,point3)
        self.script+="\""
        self.script+="\n"

    def define_plane(self,point1,point2,point3):
        if self.first_item==0:
            self.script+=","
        self.first_item=0
        self.script+="\""
        self.script+="Plane({},{}, {})".format(point1,point2,point3)
        self.script+="\""
        self.script+="\n"
    def define_segment(self,point1,point2):
        if self.first_item==0:
            self.script+=","
        self.first_item=0
        self.script+="\""
        self.script+="Segment({},{})".format(point1,point2)
        self.script+="\""
        self.script+="\n"   
    def print_script(self):
        print("Execute[{\n"+self.script+"}]")
        return "Execute[{\n"+self.script+"}]"  
    
    def generate_geogebra (self,platform):
        s1=geogebra_script()
        #Imprimo el plato
        s1.add_point(platform.c1,"C1")
        s1.add_point(platform.c2,"C2")
        s1.add_point(platform.c3,"C3")
        s1.define_polygon("C1","C2","C3")

        #imprimo los ejes de los motores
        D1=platform.D*np.array([0,-1,0])
        D2=platform.D*np.array([-1*np.sin(np.pi/3),np.cos(np.pi/3),0])
        D3=platform.D*np.array([np.sin(np.pi/3),np.cos(np.pi/3),0])
        s1.add_point(D1,"M1")
        s1.add_point(D2,"M2")
        s1.add_point(D3,"M3")
        #Imprimo los planos de acción de los motores
        s1.add_point(np.array([0,0,0]),"AUX0") 
        s1.add_point(np.array([0,0,1]),"AUX4")
        s1.define_plane("M1","AUX0","AUX4")
        s1.define_plane("M2","AUX0","AUX4")
        s1.define_plane("M3","AUX0","AUX4")
        #imprimo el brazo l1
        a1=np.array([0,np.cos(platform.ang1),np.sin(platform.ang1)])*platform.l1 #esto es visto desde el plano de referencia del motor
        a1=a1-np.array([0,platform.D,0])#muevo el cero al centro de la plataforma
        s1.add_point(a1,"A1")
        s1.define_segment("M1","A1")
        s1.define_segment("A1","C1")

        #imprimo el brazo l2
        a2=np.array([0,np.cos(platform.ang2),np.sin(platform.ang2)])*platform.l1  #esto es visto desde el plano de referencia del motor
        a2=a2-np.array([0,platform.D,0])#muevo el cero al centro de la plataforma
        a2=basis.base_change_m2_to_cannon(a2)
        s1.add_point(a2,"A2")
        s1.define_segment("M2","A2")
        s1.define_segment("A2","C2")
        #imprimo el brazo l3
        a3=np.array([0,np.cos(platform.ang3),np.sin(platform.ang3)])*platform.l1  #esto es visto desde el plano de referencia del motor
        a3=a3-np.array([0,platform.D,0])#muevo el cero al centro de la plataforma
        a3=basis.base_change_m3_to_cannon(a3)
        s1.add_point(a3,"A3")
        s1.define_segment("M3","A3")
        s1.define_segment("A3","C3")        
        #imprimo los limites del motor
        aux1=np.array([0,-platform.D-2,2.5])
        s1.add_point(aux1,"AUX1")
        aux2=np.array([5,-platform.D-2,2.5])
        s1.add_point(aux2,"AUX2")
        s1.define_segment("AUX1","AUX2")
        return s1.print_script()