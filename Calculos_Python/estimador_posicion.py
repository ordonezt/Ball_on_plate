import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import settings
def empty(a):
    pass


def estimar_posicion():
    cap = cv2.VideoCapture(2)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 100)

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
                if i==1:
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                    epsilon = 0.001 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    x2, y2, w2, h2 = cv2.boundingRect(approx)
                    cv2.circle(img, (int(x2 + h2 / 2), int(y2 + w2 / 2)), 10, (0, 0, 255), -1)
                    coordenadas = np.array([x2 + h2 / 2, y2 + w2 / 2])

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
            break

    cv2.namedWindow("Ventana")
    cv2.resizeWindow("Ventana", 500, 200)
    cv2.createTrackbar("Xmax", "Ventana", 519, 640, empty)
    cv2.createTrackbar("Xmin", "Ventana", 112, 640, empty)
    cv2.createTrackbar("Ymax", "Ventana", 420, 480, empty)
    cv2.createTrackbar("Ymin", "Ventana", 87, 480, empty)

    cv2.namedWindow("Umbrales")
    cv2.resizeWindow("Umbrales", 500, 150)
    cv2.createTrackbar("Umbral1", "Umbrales", 120, 500, empty)
    cv2.createTrackbar("Umbral2", "Umbrales", 315, 500, empty)
    cv2.createTrackbar("Ugr","Umbrales",245,255,empty)
    cv2.createTrackbar("Area","Umbrales",3000,10000,empty)

    while(True):
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
        cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), 255, -1)
        masked = cv2.bitwise_and(img, img, mask=mask)
        imagen_recortada=masked
        #invierto color a escala de grises
        invert=cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

        #aplico histograma
        #equ = cv2.equalizeHist(invert)
        #cv2.imshow('Ecualizadas', equ)
        #invert=equ

        #agrego máscara para detectar los blancos
        _,binarizada=cv2.threshold(invert,u_gris,255,cv2.THRESH_BINARY)
        #detecto contornos
        canny=cv2.Canny(binarizada, u_1, u_2)
        #dilato los contornos
        canny=cv2.dilate(canny,None,iterations=1)
        #supresion de sombras
        #_,sombra=cv2.threshold(canny,254,255,cv2.THRESH_BINARY)
        #obtengo los contornos
        contornos, _= cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        #detecto circulos en los contornos
        for cnt in contornos:
            area=cv2.contourArea(cnt)
            epsilon=0.001*cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,epsilon,True)
            x,y,w,h=cv2.boundingRect(approx)
            if len(approx)>40:
                #cv2.drawContours(img,[cnt],-1, (0, 255, 0), 3)
                cv2.circle(img, (int(x+h/2), int(y+w/2)), 10, (255, 0, 0),-1)
                coordenadas=np.array([x+h/2-centro_x,y+w/2-centro_y])
                #Aca obtengo las coordenadas
                print("Las coordenadas son")
                settings.ball_pos.pos_x=coordenadas[0]
                settings.ball_pos.pos_y=coordenadas[1]
                print(coordenadas)

        cv2.imshow("Camara", img)
        cv2.imshow("Canny", canny)
        cv2.imshow("Imagen Recortada", imagen_recortada)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            break


if __name__ == '__main__':
    settings.init()
    estimar_posicion()
