import cmath
import numpy as np

class limb:
    def __init__(self,l1,l2):
        self.l1=l1
        self.l2=l2
    def evaluate_angle(self,P,angle):
        a=self.l1*np.array([np.cos(angle),np.sin(angle)])
        b=((P-a)/(np.linalg.norm(P-a)))*self.l2
        return np.linalg.norm(P-a)-self.l2
     
    def calculate_motor_angle(self,P,max_error,tries):
        P_angle=cmath.polar(P[0]+1j*P[1])[1]
        angle_min=-90*np.pi/180
        angle_max=P_angle
        try_count=0
        while(try_count<tries):
            angle=0.5*(angle_max+angle_min)
            e=self.evaluate_angle(P,angle)
            if np.abs(e)<max_error:
                break
            if e>0:
                angle_min=angle
            if e<0:
                angle_max=angle
            try_count+=1
        if try_count==tries:
            raise ValueError('Point unreachable\nP=({},{})'.format(P[0],P[1]))
            #print('Point unreachable\nP=({},{})'.format(P[0],P[1]))
        else:
            return angle