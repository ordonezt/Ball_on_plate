import cv2
import numpy as np

def empty(a):
    pass

def estimar_posicion():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 100)

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

    while True:
        x_min = cv2.getTrackbarPos("Xmin", "Ventana")
        x_max = cv2.getTrackbarPos("Xmax", "Ventana")
        y_min = cv2.getTrackbarPos("Ymin", "Ventana")
        y_max = cv2.getTrackbarPos("Ymax", "Ventana")

        u_1=cv2.getTrackbarPos("Umbral1", "Umbrales")
        u_2=cv2.getTrackbarPos("Umbral2", "Umbrales")
        u_gris= cv2.getTrackbarPos("Ugr","Umbrales")
        u_area= cv2.getTrackbarPos("Area","Umbrales")

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
                coordenadas=np.array([x+h/2,y+w/2])
                if area < u_area:
                    #Aca obtengo las coordenadas
                    print("Las coordenadas son")
                    print(coordenadas)

        cv2.imshow("Camara", img)
        cv2.imshow("Canny", canny)
        cv2.imshow("Imagen Recortada", imagen_recortada)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    estimar_posicion()