

def move_platform (platform):






def rotate(platform,movement,joint,angle):
  
    if joint=="C1":
        platform.c1=base_change_cannon_to_m1(platform.c1)
        platform.c2=base_change_cannon_to_m1(platform.c2)
        platform.c3=base_change_cannon_to_m1(platform.c3)

    if joint=="C2":
        platform.c1=base_change_cannon_to_m2(platform.c1)
        platform.c2=base_change_cannon_to_m2(platform.c2)
        platform.c3=base_change_cannon_to_m2(platform.c3)
    if joint=="C3":
        platform.c1=base_change_cannon_to_m3(platform.c1)
        platform.c2=base_change_cannon_to_m3(platform.c2)
        platform.c3=base_change_cannon_to_m3(platform.c3)
    if movement=="pitch":
        platform.c1=rotate_in_y_axis(platform.c1,angle)
        platform.c2=rotate_in_y_axis(platform.c2,angle)
        platform.c3=rotate_in_y_axis(platform.c3,angle)
    if movement=="roll":
        platform.c1=rotate_in_x_axis(platform.c1,angle)
        platform.c2=rotate_in_x_axis(platform.c2,angle)
        platform.c3=rotate_in_x_axis(platform.c3,angle)

            
    #corregimos el offset de la plataforma
    if joint=="C1":
        platform=apply_offset(platform,platform.c2)
    if joint=="C2":
        platform=apply_offset(platform,platform.c3)
    if joint=="C3":
        platform=apply_offset(platform,platform.c1)
    #obtengo los puntos en la base original
    if joint=="C1":
        platform.c1=base_change_m1_to_cannon(platform.c1)
        platform.c2=base_change_m1_to_cannon(platform.c2)
        platform.c3=base_change_m1_to_cannon(platform.c3)
    if joint=="C2":
        platform.c1=base_change_m2_to_cannon(platform.c1)
        platform.c2=base_change_m2_to_cannon(platform.c2)
        platform.c3=base_change_m2_to_cannon(platform.c3)
    if joint=="C3":
        platform.c1=base_change_m3_to_cannon(platform.c1)
        platform.c2=base_change_m3_to_cannon(platform.c2)
        platform.c3=base_change_m3_to_cannon(platform.c3)
    return platform

def apply_offset (platform,pos):
    "la función desplaza la plataforma el offset correspondiente para compenzar el introducido por la rotación"
    allowed_pos=-pos[0]*np.tan(np.pi/6)
    offset=np.array([0,allowed_pos-pos[1],0])
    platform.c1=platform.c1+offset
    platform.c2=platform.c2+offset
    platform.c3=platform.c3+offset
    return platform