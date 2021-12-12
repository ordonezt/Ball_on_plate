import cv2
import settings
import numpy as np


numClicks=0 #contador con la cantidad de esquinas seleccionadas
coordenadas=[] #lista de coordenadas seleccionadas

def empty(a):
    pass


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

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    return x_min,x_max,y_min,y_max,u_1,u_2,u_gris,u_area




#función del callback del mouse para capturar la coordenada del click
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       print("mouse event!")
       global numClicks
       global coordenadas
       numClicks=numClicks+1
       coordenadas.append({'x':x,'y':y})


def calibracion_centro_escala(cap):
	global numClicks
	global coordenadas

	centro={'x':0,'y':0}
	Esq_sup_izq={'x':0,'y':0}
	Esq_sup_der={'x':0,'y':0}
	Esq_inf_izq={'x':0,'y':0}
	Esq_inf_der={'x':0,'y':0}
	coordenadas=[]
	while (True):
		success,img = cap.read()
		cv2.setMouseCallback('video', onMouse) #podria ir afuera del loop
		for coordenada in coordenadas:
			cv2.circle(img, (coordenada['x'],coordenada['y']), 5, (255, 0, 255), 8)
		cv2.imshow('video', img)
		if cv2.waitKey(1) == ord('q'):
			break		
	for coordenada in coordenadas:
		centro['x']=centro['x']+coordenada['x']
		centro['y']=centro['y']+coordenada['y']
		
	centro['x']=centro['x']/4
	centro['y']=centro['y']/4
	
	for coordenada in coordenadas:
		if (coordenada['x']>centro['x'] and coordenada['y']>centro['y']):
			Esq_sup_der=coordenada
		if (coordenada['x']<centro['x'] and coordenada['y']<centro['y']):
			Esq_inf_izq=coordenada		
		if (coordenada['x']<centro['x'] and coordenada['y']>centro['y']):
			Esq_sup_izq=coordenada		
		if (coordenada['x']>centro['x'] and coordenada['y']<centro['y']):
			Esq_inf_der=coordenada

	Escala_x= Esq_sup_der['x']-Esq_inf_izq['x']
	Escala_x = 0.30 / Escala_x #30cm de esquina a esquina dividio la distancia en pixeles
	Escala_y= Esq_sup_der['y']-Esq_inf_izq['y']
	Escala_y = 0.30 / Escala_y #30cm de esquina a esquina dividio la distancia en pixeles		
	print(Escala_x)
	print(Escala_y)
	return centro['x'],centro['y'],Escala_x,Escala_y
	

def calibracion ():
    image_settings={}
    cap = cv2.VideoCapture(settings.selected_camera)
    print(settings.selected_camera)
    #setea resolucion
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 100)

    #la funcion es un while true, hasta que se apreta W
    image_settings["centro_x"],image_settings["centro_y"],image_settings["Escala_x"],image_settings["Escala_y"]=calibracion_centro_escala(cap)


    x_min,x_max,y_min,y_max,u_1,u_2,u_gris,u_area=adjust_settings(cap,image_settings)  
    image_settings["x_min"]=x_min
    image_settings["x_max"]=x_max
    image_settings["y_min"]=y_min
    image_settings["y_max"]=y_max
    image_settings["u_1"]=u_1
    image_settings["u_2"]=u_2
    image_settings["u_gris"]=u_gris
    image_settings["u_area"]=u_area
    settings.save_image_settings(image_settings)   
	
if __name__=="__main__":
	calibracion()


