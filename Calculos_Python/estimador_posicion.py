import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import settings
import json
import controller
import time
import copy
import pandas as pd

centro_x =0
centro_y =0

def empty(a):
    pass

def set_center(event,x,y,flags,param):
    global centro_x
    global centro_y
    if (event == cv2.EVENT_LBUTTONDBLCLK): 
        centro_x,centro_y = x,y


# Esta funcion lo que hace es buscar las coordenadas de los dos CRQs
# y calcular la distancia en pixeles entre ellos, la idea luego (no esta hecho)
# es tomar la medida en cm y hacer la conversion de pixeles a cm
def calibrar_distancia_en_pixeles(cap):
    #primer while:
    #   hace la calibracion pixeles a cm
    distancia_pixeles=0
    while (True):
        success,img = cap.read()

        #crea una imagen negra para poder dibujar arriba los contornos de los QRs
        mask = np.zeros(img.shape[:2], dtype="uint8")
        # creo rectangulo para utilizar como mascara
        cv2.rectangle(mask, (0, 0), (640, 480), 0, -1)
        #en este punto lo que tenemos es una imagen negra de 640 por 480 donde vamos a dibujar los contornos de los QRs

        #toma los QRs y dibuja los rectangulos sobre la imagen negra
        for code in decode(img):
            pts=np.array([code.polygon],np.int32)
            pts=pts.reshape((-1,1,2))
            cv2.polylines(mask,[pts],True,(255,0,255),5)


        #busco los contornos de los QRs
        contornos, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        largo_contornos=len(contornos)

        if largo_contornos==2:
            i=0
            for cnt in contornos:
                if i==0:
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                    epsilon = 0.001 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    x1, y1, w1, h1 = cv2.boundingRect(approx)
                    cv2.circle(img, (int(x1 + h1 / 2), int(y1 + w1 / 2)), 10, (255, 0, 0), -1)
                    #coordenadas calculadas para debug
                    #coordenadas = np.array([x1 + h1 / 2, y1 + w1 / 2])
                if i==1:
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                    epsilon = 0.001 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    x2, y2, w2, h2 = cv2.boundingRect(approx)
                    cv2.circle(img, (int(x2 + h2 / 2), int(y2 + w2 / 2)), 10, (0, 0, 255), -1)
                    #coordenadas calculadas para debug 
                    #coordenadas = np.array([x2 + h2 / 2, y2 + w2 / 2])

                i=i+1

            diferencia_x=np.absolute(x1-x2)
            diferencia_y=np.absolute(y1-y2)
            distancia_pixeles=np.sqrt(diferencia_y**2+diferencia_x**2)
            print("Distancia en Pixeles")
            print(distancia_pixeles)

        cv2.imshow('result',img)
        #cv2.imshow('result2',mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    return distancia_pixeles


#Funcion que toma las coordenas de los QRs y las promedia para obtener el centro de la plataforma
#Se interrumpe el calculo y se guarda el centro al apretar 'w'
# retorna dos valores centro_x y centro_y

def obtener_centro_en_pixeles(cap):
    centro_x=0
    centro_y=0
    while (True):
        success,img = cap.read()
        mask = np.zeros(img.shape[:2], dtype="uint8")
        # creo rectangulo para utilizar como mascara
        cv2.rectangle(mask, (0, 0), (640, 480), 0, -1)

        for code in decode(img):
            pts=np.array([code.polygon],np.int32)
            pts=pts.reshape((-1,1,2))
            cv2.polylines(mask,[pts],True,(255,0,255),5)


        contornos, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        largo_contornos=len(contornos)

        if largo_contornos==2:
            i=0
            for cnt in contornos:
                if i==0:
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                    epsilon = 0.001 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    x1, y1, w1, h1 = cv2.boundingRect(approx)
                    cv2.circle(img, (int(x1 + h1 / 2), int(y1 + w1 / 2)), 10, (255, 0, 0), -1)
                    coordenadas = np.array([x1 + h1 / 2, y1 + w1 / 2])
                    x1=int(x1 + h1 / 2)
                    y1=int(y1 + w1 / 2)
                    print("P1")
                    print(coordenadas)
                if i==1:
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                    epsilon = 0.001 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    x2, y2, w2, h2 = cv2.boundingRect(approx)
                    cv2.circle(img, (int(x2 + h2 / 2), int(y2 + w2 / 2)), 10, (0, 0, 255), -1)
                    coordenadas = np.array([x2 + h2 / 2, y2 + w2 / 2])
                    x2=int(x2 + h2 / 2)
                    y2=int(y2 + w2 / 2)
                    print("P2")
                    print(coordenadas)
                i=i+1

            centro_x=(x1+x2)/2
            centro_y=(y1+y2)/2
            centro_xy=np.array([centro_x,centro_y])
            print("Centro en Pixeles")
            print(centro_xy)

        cv2.line(img,(int(centro_x),1),(int(centro_x),480-1),(255,0,255),3)
        cv2.line(img,(1,int(centro_y)),(640-1,int(centro_y)),(255,0,255),3)

        cv2.imshow('result',img)
        cv2.imshow('result2',mask)

        if cv2.waitKey(1) & 0xFF == ord('w'):
            cv2.destroyAllWindows()
            break
    #fuera del while, llego aca cuando se apreta w
    return centro_x,centro_y

def adjust_settings(cap,image_settings):
    cv2.namedWindow("Ventana")
    cv2.resizeWindow("Ventana", 500, 200)

    #Sliders para ajuste del tamanio del area de trabajo para recortar cosas
    #por fuera del plato. Estos objetos meten ruido en la deteccion
    cv2.createTrackbar("Xmax", "Ventana", 519, 640, empty)
    cv2.createTrackbar("Xmin", "Ventana", 112, 640, empty)
    cv2.createTrackbar("Ymax", "Ventana", 420, 480, empty)
    cv2.createTrackbar("Ymin", "Ventana", 87, 480, empty)

    #Umbrales de deteccion de contorno utilizados en Canny
    cv2.namedWindow("Umbrales")
    cv2.resizeWindow("Umbrales", 500, 150)
    cv2.createTrackbar("Umbral1", "Umbrales", 120, 500, empty)
    cv2.createTrackbar("Umbral2", "Umbrales", 315, 500, empty)

    #Umbral para comparacion de escala de grises
    #la idea es poner en negro todos los pixeles con luminocidad menor 
    #a este umbral
    cv2.createTrackbar("Ugr","Umbrales",245,255,empty)

    #Umbral de area (no esta en uso) buscaba un umbral minimo en un contorno para decir que es la pelota
    cv2.createTrackbar("Area","Umbrales",3000,10000,empty)

    while(True):
        #obtencion de los valores de los sliders
        x_min = cv2.getTrackbarPos("Xmin", "Ventana")
        x_max = cv2.getTrackbarPos("Xmax", "Ventana")
        y_min = cv2.getTrackbarPos("Ymin", "Ventana")
        y_max = cv2.getTrackbarPos("Ymax", "Ventana")
        u_1=cv2.getTrackbarPos("Umbral1", "Umbrales")
        u_2=cv2.getTrackbarPos("Umbral2", "Umbrales")
        u_gris= cv2.getTrackbarPos("Ugr","Umbrales")
        u_area= cv2.getTrackbarPos("Area","Umbrales")
        u_area=2000
        success, img = cap.read()
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

        cv2.imshow("Camara", img)
        cv2.imshow("Canny", canny)
        cv2.imshow("Imagen Recortada", imagen_recortada)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            cv2.destroyAllWindows()
            break
    return x_min,x_max,y_min,y_max,u_1,u_2,u_gris,u_area


def calibracion ():
    image_settings={}
    cap = cv2.VideoCapture(2)
    #setea resolucion
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 100)

    #la funcion es un while true, hasta que se apreta Q
    image_settings["distancia_pixeles"]=calibrar_distancia_en_pixeles(cap)

    #la funcion es un while true, hasta que se apreta W
    #image_settings["centro_x"],image_settings["centro_y"]=obtener_centro_en_pixeles(cap)
    image_settings["centro_x"]=326
    image_settings["centro_y"]=205

    #En este punto ya terminamos con la calibracion

    x_min,x_max,y_min,y_max,u_1,u_2,u_gris,u_area=adjust_settings(cap,image_settings)  
    image_settings["x_min"]=x_min
    image_settings["x_max"]=x_max
    image_settings["y_min"]=y_min
    image_settings["y_max"]=y_max
    image_settings["u_1"]=u_1
    image_settings["u_2"]=u_2
    image_settings["u_gris"]=u_gris
    image_settings["u_area"]=u_area
    save_image_settings(image_settings)

def estimar_posicion(image_settings):
    log={"pos_x":[],"pos_y":[],"exec_time":[],"angle_x":[],"angle_y":[]}
    global centro_x
    global centro_y
    cap = cv2.VideoCapture(2)
    cv2.namedWindow('Camara')
    
    #setea resolucion
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 100)
    #inicializo las posiciones en None para detectar cuando no se encuentra la
    pos_x=None
    pos_y=None
    angle_x=0
    angle_y=0
    distancia_pixeles=image_settings["distancia_pixeles"]
    centro_x=image_settings["centro_x"]
    centro_y=image_settings["centro_y"]

    x_min=image_settings["x_min"]
    x_max=image_settings["x_max"]
    y_min=image_settings["y_min"]
    y_max=image_settings["y_max"]
    u_1=image_settings["u_1"]
    u_2=image_settings["u_2"]
    u_gris=image_settings["u_gris"]
    u_area=image_settings["u_area"]
    ball_pos=settings.ball_t()
    platform_controller=controller.controller_t()
    cv2.setMouseCallback('Camara',set_center)
    while (True):
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
                
                ball_pos.pos_x=coordenadas[0]
                ball_pos.pos_y=-coordenadas[1]
                angle_x,angle_y=platform_controller.control(ball_pos)
                
        cv2.imshow("Camara", img)
        cv2.imshow("Canny", canny)
        cv2.imshow("Imagen Recortada", imagen_recortada)
        log["pos_x"].append(copy.deepcopy(ball_pos.pos_x))
        log["pos_y"].append(copy.deepcopy(ball_pos.pos_y))
        log["angle_x"].append(copy.deepcopy(angle_x))
        log["angle_y"].append(copy.deepcopy(angle_y))
        log["exec_time"].append((time.time()-start_time)*1000)
        print(f"execution time:{(time.time()-start_time)*1000} mSeg")
        if cv2.waitKey(1) & 0xFF == ord('e'):
            cv2.destroyAllWindows()
            df=pd.DataFrame.from_dict(log)
            df.to_excel("logs.xlsx")
            break
    return 


def test():
    platform_controller=controller.controller_t()
    ball_pos=settings.ball_t()
    while (True):
        ball_pos.pos_x=-float(input("x="))
        ball_pos.pos_y=-float(input("y="))
        platform_controller.control(ball_pos)
    return 


def save_image_settings(settings):
    with open('./image_settings.json', "w") as file:
        data=json.dumps(settings)
        file.write(data)
    return

def load_image_settings():
    with open('./image_settings.json', "r") as file:
        data=file.read()
        return json.loads(data)


if __name__ == '__main__':
    settings.init()
    estimar_posicion()


