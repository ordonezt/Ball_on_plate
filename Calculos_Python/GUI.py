from tkinter import *
import settings
import threading
import estimador_posicion
from serial_com import send_command_to_platform
import main

def update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text):
    settings.Kd=float(Kd_slider.get())
    Kd_text.set("Kd="+str(settings.Kd))

    settings.Ki=float(Ki_slider.get())
    Ki_text.set("Ki="+str(settings.Ki))

    settings.Kp=float(Kp_slider.get())
    Kp_text.set("Kp="+str(settings.Kp))
    
def comenzar_calibracion():
    thread=threading.Thread(target=estimador_posicion.calibracion)
    thread.start()
    return
def comenzar_control():
    image_settings=estimador_posicion.load_image_settings()
    t2=threading.Thread(target=lambda: estimador_posicion.estimar_posicion(image_settings))
    #t2=threading.Thread(target= estimador_posicion.test)
    t2.start()
    return

def reset_platform():
    send_command_to_platform("/dev/ttyACM0",0,0,13)
    return

def start_GUI():
    root= Tk()
    
    root.title("Adjuts parameters")
    root.geometry('800x800')
    #Kd setting
    Kd_text=StringVar()
    Kd_label=Label(root,textvariable=Kd_text)
    Kd_label.pack()
    Kd_slider=Scale(root, from_=0, to=0.03,orient = HORIZONTAL,label="Kd",resolution=0.0001)
    Kd_slider.pack(anchor='w')
    #Kp setting
    Kp_text=StringVar()
    Kp_label=Label(root,textvariable=Kp_text)
    Kp_label.pack()
    Kp_slider=Scale(root, from_=0, to=0.1,orient = HORIZONTAL,label="Kp",resolution=0.001)
    Kp_slider.pack(anchor='w')
    #Ki setting
    Ki_text=StringVar()
    Ki_label=Label(root,textvariable=Ki_text)
    Ki_label.pack()
    Ki_slider=Scale(root, from_=0, to=0.1,orient = HORIZONTAL,label="Ki",resolution=0.01)
    Ki_slider.pack(anchor='w')
  

    #boton de confirmación de parametros
    confirm_button= Button(root,text="confirmar parametros",command=lambda: update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text))
    confirm_button.pack()

    #boton para inicio de calibracion
    cal_button= Button(root,text="Calibracion",command=comenzar_calibracion)
    cal_button.pack(anchor='w')
    #boton para comenzar
    cal_button= Button(root,text="Comenzar",command=comenzar_control)
    cal_button.pack(anchor='w')
    #boton para resetear la plataforma
    cal_button= Button(root,text="Resetear plataforma",command=reset_platform)
    cal_button.pack(anchor='w')
    #arranco la GUI
    root.mainloop()


if __name__=="__main__":
    start_GUI()
