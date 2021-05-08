import platform_definition
import numpy as np

p=platform_definition.platform(d=6,D=10,l1=6,l2=12,max_limb_error=0.00001,max_limb_try_count=30,max_joint_angle=23*np.pi/180)

while True:
    r_x=float(input("Ingrese ángulo (en grados) en x:"))*np.pi/180
    r_y=float(input("Ingrese ángulo (en grados) en y:"))*np.pi/180
    h=float(input("Ingrese altura en centimetros:"))
    try:
        p.solve_platform(r_x,r_y,h)
    except:
        print("Point unreachable")
    else:
        print("Ángulo 1: {:.2f}º".format(p.ang1*180/np.pi))
        print("Ángulo 2: {:.2f}º".format(p.ang2*180/np.pi))
        print("Ángulo 3: {:.2f}º".format(p.ang3*180/np.pi))
    