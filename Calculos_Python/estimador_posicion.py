import cv2
import numpy as np
import os
import settings
import json
import controller
import time
import copy
import pandas as pd
import matplotlib.pyplot as plt

def empty(a):
    pass


def estimar_posicion(image_settings):
    

    cap = cv2.VideoCapture(settings.selected_camera)
    #setea resolucion
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 100)
    #inicializo las posiciones en None para detectar cuando no se encuentra la
    pos_x=None
    pos_y=None
    angle_x=0
    angle_y=0
    salidas_controlador = {"angle_x": 0, "angle_y":0, "vel_x":0, "vel_y":0}
    fps = 0
    Escala_x=image_settings["Escala_x"]
    Escala_y=image_settings["Escala_y"]
    centro_x=image_settings["centro_x"]
    centro_y=image_settings["centro_y"]

    settings.Escala_x=image_settings["Escala_x"]
    settings.Escala_y=image_settings["Escala_y"]
    

    x_min=image_settings["x_min"]
    x_max=image_settings["x_max"]
    y_min=image_settings["y_min"]
    y_max=image_settings["y_max"]
    u_1=image_settings["u_1"]
    u_2=image_settings["u_2"]
    u_gris=image_settings["u_gris"]
    u_area=image_settings["u_area"]
    ball_pos=settings.ball_t()

    platform_controller=controller.controller_t(tipo=settings.controller, ancho_plataforma_x=abs(x_max-x_min)*Escala_x, ancho_plataforma_y=abs(y_max-y_min)*Escala_y )#ancho_plataforma=300)
    print("Utilizando controlador "+settings.controller)
    settings.log={"pos_x":[],"pos_y":[],"angle_x":[],"angle_y":[], "vel_x":[], "vel_y":[], "fps":[]}
    while (settings.control_state!="Stoped"):
        while(settings.control_state=="Paused"): #Si pausan el control, hago un poll de la variable de estado cada medio segundo para salir
            time.sleep(0.5)
        success, img = cap.read()
        start_time=time.time()
        #creo mascara llena de 0 para recortar imagen
        mask = np.zeros(img.shape[:2], dtype="uint8")
        #creo rectangulo para utilizar como mascara
        #esta mascara esta parametrizada con los slider para poder dejar afuera obstalucos
        cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), 255, -1)
        #enmascaramos la imagen de video
        masked = cv2.bitwise_and(img, img, mask=mask)
        imagen_recortada=masked
        #invierto color a escala de grises
        invert=cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

        # Lo que hace es normalizar la imagen en brillo para aprovechar todo el rango dinamico
        #no esta en uso, no aportaba mejoras significativas
        #aplico histograma
        #equ = cv2.equalizeHist(invert)
        #cv2.imshow('Ecualizadas', equ)
        #invert=equ

        #agrego mascara para detectar los blancos
        _,binarizada=cv2.threshold(invert,u_gris,255,cv2.THRESH_BINARY)
        #detecto contornos
        canny=cv2.Canny(binarizada, u_1, u_2)
        #dilato los contornos
        canny=cv2.dilate(canny,None,iterations=1)
        #supresion de sombras
        #_,sombra=cv2.threshold(canny,254,255,cv2.THRESH_BINARY)

        #obtengo los contornos
        #podemos probar otros algoritmos de deteccion de contornos
        contornos, _= cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        #detecto circulos en los contornos
        #La idea de este for es detectar los contornos y aproximarlos con poli lineas
        #figuras simples van a tener muchas poli lineas entonces si tiene mas de 40 
        #poli lineas es un circulo
        for cnt in contornos:
            area=cv2.contourArea(cnt)
            epsilon=0.001*cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,epsilon,True)
            x,y,w,h=cv2.boundingRect(approx)
            if len(approx)>40:
                #cv2.drawContours(img,[cnt],-1, (0, 255, 0), 3)
                cv2.circle(img, (int(x+h/2), int(y+w/2)), 10, (255, 0, 0),-1)
                cv2.circle(img, (int(centro_x),int(centro_y)), 10, (0,255, 0),-1)
                coordenadas=np.array([x+h/2-centro_x,y+w/2-centro_y])
                #Aca obtengo las coordenadas
                print("Las coordenadas son")
                print(coordenadas)
                print(np.array([x+h/2,y+w/2]))
                
                ball_pos.pos_x=-coordenadas[0] *Escala_x
                ball_pos.pos_y=-coordenadas[1] *Escala_y
                # angle_x,angle_y=platform_controller.control(ball_pos)
                tiempo_actual = time.time()
                try:
                    periodo = tiempo_actual - tiempo_anterior
                    fps = 1 / periodo
                except:
                    fps = 0
                    pass
                tiempo_anterior = tiempo_actual
                

                salidas_controlador=platform_controller.control(ball_pos)
                
                
        cv2.imshow("Camara", img)
        cv2.imshow("Canny", canny)
        cv2.imshow("Imagen Recortada", imagen_recortada)


        settings.log["pos_x"].append(copy.deepcopy(ball_pos.pos_x))
        settings.log["pos_y"].append(copy.deepcopy(ball_pos.pos_y))
        # settings.log["angle_x"].append(copy.deepcopy(angle_x))
        # settings.log["angle_y"].append(copy.deepcopy(angle_y))
        if "angle_x" in salidas_controlador:
            angle_x = salidas_controlador["angle_x"]
            settings.log["angle_x"].append(copy.deepcopy(angle_x))
        if "angle_y" in salidas_controlador:
            angle_y = salidas_controlador["angle_y"]
            settings.log["angle_y"].append(copy.deepcopy(angle_y))
        if "vel_x" in salidas_controlador:
            vel_x = salidas_controlador["vel_x"]
            settings.log["vel_x"].append(copy.deepcopy(vel_x))
        if "vel_y" in salidas_controlador:
            vel_y = salidas_controlador["vel_y"]
            settings.log["vel_y"].append(copy.deepcopy(vel_y))

        settings.log["fps"].append(copy.deepcopy(fps))
        
        if cv2.waitKey(1) & 0xFF == ord('e'):
            cv2.destroyAllWindows()
            df=pd.DataFrame.from_dict(settings.log)
            df.to_excel("logs.xlsx") #Genero excel con la información guardada
            break
    #Si el control debe detenerse:
    cv2.destroyAllWindows()

    df=pd.DataFrame.from_dict(settings.log)
    df.to_excel("logs.xlsx") #Genero excel con la información guardada
    if (settings.excel_enabled==True):
        print("Guardando excel")
        df.to_excel("resultado.xlsx") #Genero excel con la información guardada
        
    return 




def test():
    platform_controller=controller.controller_t(tipo='Fuzzy', ancho_plataforma=30)
    ball_pos=settings.ball_t()
    while (True):
        ball_pos.pos_x=-float(input("x="))
        ball_pos.pos_y=-float(input("y="))
        platform_controller.control(ball_pos)
    return 




if __name__ == '__main__':
    settings.init()
    estimar_posicion()


