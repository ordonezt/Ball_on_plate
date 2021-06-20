import geogebra
import checks
def test_movements(platform,h_range,r_x_range,r_y_range):
    #Función que realiza el testeo de la plataforma.
    #Resuelve la plataforma en cada una de las combinaciones de h_range,r_x_range e r_y_range
    #Donde:
    #   h_range: lista de alturas a resolver
    #   r_x_range: lista con angulos en eje x a resolver
    #   r_y_range: lista con angulos en eje y a resolver
    #Se imprimen mensajes si:
    #    las combinaciones de l1,l2 y ángulos min y máx del motor hacen imposible alcanzar la junta.
    #    En este caso la función imprime el error 'point unreachable'
    #    La impresión del error se genera dentro del objeto limb
    # 
    #    Si el ángulo requerido en alguna de las juntas universales supera el ángulo máximo seteado 
    #    como parametro. 
    #
    #Devuelve: un objecto geogebra_script con una nube de puntos de las posiciones de P1 (C1 en el marco de referencia del motor1)


    s1=geogebra.geogebra_script()
    point=0 #variable para generar el nombre de cada punto en el point cloud generado por geogebra
    for height in h_range:
        for angle_x in r_x_range:
            for angle_y in r_y_range:
                result=platform.solve_platform(r_x=angle_x,r_y=angle_y,h=height) 
                if result==-1: #ángulo de junta universal excedido
                    print("angle exceeded")
                    print("angle_x={}".format(angle_x*180/np.pi))
                    print("angle_y={}".format(angle_y*180/np.pi))
                else:
                    check_h=checks.check_motor_height (platform.c1,platform.c2,platform.c3,platform.D)
                    #check_motor_height checkea que la inclinación del plato no provoque que el mismo choque con 
                    #alguno de los motores. Se realizaron los checkeos con uno solo dado que como se barren todas 
                    #las combinaciones posibles el resultado con los demás motores es identico
                    if check_h==-1:
                        print("Motor choca con el plato:\n")
                        "[BUG]:si el motor choca contra el plato y al mismo tiempo el punto es unreachable no se puede generar el"
                        "Script de geogebra, porque no hay angulos para armar los limbs"
                        #p1.generate_geogebra()
                    #A continuación guardo el punto P1 en un script de geogebra para generar una nube de puntos
                    P1,P2,P3=platform.calculate_P()
                    name="P"+str(point)
                    s1.add_2D_point(P1,name)
                    point=point+1
    return s1