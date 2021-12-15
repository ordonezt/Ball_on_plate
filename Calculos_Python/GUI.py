from tkinter import *
import settings
import threading
from time import sleep
import estimador_posicion
from serial_com import send_command_to_platform
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import calibracion
import os
import pandas as pd

def update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text):
    settings.Kd=float(Kd_slider.get())
    Kd_text.set("Kd="+str(settings.Kd))

    settings.Ki=float(Ki_slider.get())
    Ki_text.set("Ki="+str(settings.Ki))

    settings.Kp=float(Kp_slider.get())
    Kp_text.set("Kp="+str(settings.Kp))

def update_slider(value,slider):
    #Valores del PID
    if(slider=="Kd"):
        settings.Kd=float(value)
    if(slider=="Kp"):
        settings.Kp=float(value)
    if(slider=="Ki"):
        settings.Ki=float(value)
    #Valores controlador de variables de estado
    if(slider=="VDE_K1"):
        settings.VDE_K1=float(value)
    if(slider=="VDE_K2"):
        settings.VDE_K2=float(value)

    print(slider+":"+value)

def comenzar_calibracion():
    thread=threading.Thread(target=calibracion.calibracion)
    thread.start()
    return


def comenzar_pausar_control(start_button_text,controller_drop,stop_controller_button):
    stop_controller_button["state"]="normal" #habilito el boton para terminar el controlador
    if(settings.control_state=="Stoped"): #Primera vez que se ejecuta, hay que cargar las configuraciones globales y ejecutar el thread
        settings.control_state="Running" #Variable global que permite al controlador comenzar
        start_button_text.set("Pausar")
        image_settings=settings.load_image_settings()
        t2=threading.Thread(target=lambda: estimador_posicion.estimar_posicion(image_settings))
        t2.start()
        controller_drop["state"]="disabled" #Deshabilito el dropdown
    elif(settings.control_state=="Running"):    
        start_button_text.set("Reanudar")
        settings.control_state="Paused" #Pauso al controlador de la plataforma
    elif (settings.control_state=="Paused"):
        settings.control_state="Running" #Vuelvo a arrancar el controlador
        start_button_text.set("Pausar")

    print(settings.control_state)
   
    return

def terminal_control(start_button_text,controller_drop,stop_controller_button):
    settings.control_state="Stoped" #Pauso al controlador de la plataforma
    start_button_text.set("Comenzar")
    controller_drop["state"]="normal" #habilito el dropdown
    stop_controller_button["state"]="disabled" #deshabilito el boton para terminar el controlador
    print(settings.control_state)
    if (settings.plotting_enabled==True):
        print("Generando graficos...")
        os.system("python3 plot_results.py")
    return


def reset_platform():
    send_command_to_platform("/dev/ttyACM0",0,0,13)
    return

def configurar_controlador(root,conf_controller_button,controller_drop):
    conf_controller_button["state"]="disabled"
    controller_drop["state"]="disabled"
    conf_controller_window= Toplevel(root)
    conf_controller_window.title("Configuración controlador "+settings.controller)
    conf_controller_window.geometry('300x200')

    #uso una funcion para que habilite el volver a configurar el controlador después de cerrado
    conf_controller_window.protocol("WM_DELETE_WINDOW", lambda:conf_param_closing(conf_controller_window,conf_controller_button,controller_drop))

    if (settings.controller=="PID"):
        configurar_PID(conf_controller_window)
    elif(settings.controller=="Variables de Estado"):
        configurar_VDE(conf_controller_window)
    elif(settings.controller=="Fuzzy"):
        configurar_fuzzy(conf_controller_window)
    return

def test_data_gen():
    t=0
    time=[]
    while (True):
        sleep(33/1000)
        t=t+33/1000
        settings.log["pos_x"].append(np.sin(2*np.pi*t) *np.exp(-t/10))
        settings.log["pos_x"].append(-np.sin(2*np.pi*t)*np.exp(-t/10))
        settings.log["time"].append(t)


    
def configurar_PID(window):
    settings.Ki=0
    settings.Kd=0
    settings.Kp=0
    
    #Kd setting
    Kd_slider=Scale(window,label="Kd [°m/seg]", from_=0, to=150,orient = HORIZONTAL,resolution=0.5,command= lambda value :update_slider(value,slider="Kd"))
    Kd_slider.pack(fill=X)
    
    
    #Kp setting
    Kp_slider=Scale(window,label="Kp [°/m]", from_=0, to=150,orient = HORIZONTAL,resolution=0.5,command= lambda value :update_slider(value,slider="Kp"))
    Kp_slider.pack(fill=X)
    
    
    #Ki setting
    Ki_slider=Scale(window,label="Ki [°/ m seg]", from_=0, to=150,orient = HORIZONTAL,resolution=1,command= lambda value :update_slider(value,slider="Ki"))
    Ki_slider.pack(fill=X)

def configurar_VDE(window):
    settings.VDE_K1=0
    settings.VDE_K2=0
    settings.VDE_K3=0
    
    #VDE K1 setting
    K1_slider=Scale(window,label="VDE K1 (Realimentación de posición)", from_=0, to=0.03,orient = HORIZONTAL,resolution=0.0001,command= lambda value:update_slider(value,slider="VDE K1"))
    K1_slider.pack(fill=X)
    
    
    #VDE K2 setting
    K2_slider=Scale(window,label="VDE K2 (Realimentación de velocidad)", from_=0, to=0.1,orient = HORIZONTAL,resolution=0.001,command= lambda value :update_slider(value, slider="VDE K2"))
    K2_slider.pack(fill=X)




def configurar_fuzzy(window):
    settings.Fuzzy_K1=0
    settings.Fuzzy_K2=0
    settings.Fuzzy_K3=0
    fuzzy_label=Label(window,text="El controlador difuso no admite configuración")
    fuzzy_label.pack()



#Función que vuelve a habilitar los selectores del controlador y la configuración del controlador cuando se cierra la ventana
#de configurar_controlador (función llamante)
def conf_param_closing(window,conf_controller_button,controller_drop):
    conf_controller_button["state"]="normal"
    controller_drop["state"]="normal"
    window.destroy()
    return

def controller_update(controller_drop_text):
    settings.controller=controller_drop_text

def update_graph_checkbox(graphs_enabled):
    if (graphs_enabled==1):
        settings.plotting_enabled=True
        print("graficos habilitados")
    else:
        settings.plotting_enabled=False
    return

def update_excel_checkbox(excel_enabled):
    if (excel_enabled==1):
        settings.excel_enabled=True
    else:
        settings.excel_enabled=False
    return

def select_camera(selected_camera):
    settings.selected_camera=selected_camera
    print("selected_camera="+str(selected_camera))

def start_GUI():
    root= Tk()
    
    root.title("Ball & plate system")
    root.geometry('375x225')
    root.resizable(False, False)


    ###################################################
    ##########frame de opciones del controlador########
    ###################################################
    controller_frame = LabelFrame(root, text="Opciones de control", labelanchor='n',padx=5,pady=5)
    controller_frame.grid(row=0,column=0)

    #boton para inicio de calibracion
    cal_button= Button(controller_frame,text="Calibracion",command=comenzar_calibracion)
    cal_button.pack(fill=X)
    #Dropdown list para elegir el controlador
    controller_drop_text=StringVar()
    controller_drop_text.set("PID")
    controller_drop=OptionMenu(controller_frame,controller_drop_text,"PID","Fuzzy","Variables de Estado",command=controller_update)
    controller_drop.pack(fill=X)
    #boton para configurar controlador
    conf_controller_button= Button(controller_frame,text="Configurar controlador",command= lambda: configurar_controlador(root,conf_controller_button,controller_drop))
    conf_controller_button.pack(fill=X)
    #boton para comenzar/Pausar
    start_button_text=StringVar()
    start_button_text.set("Comenzar")
    settings.control_state="Stoped"
    start_button= Button(controller_frame,textvariable=start_button_text,command= lambda:comenzar_pausar_control(start_button_text,controller_drop,stop_controller_button))
    start_button.pack(fill=X)
    #Boton para finalizar el controlador
    stop_controller_button= Button(controller_frame,text="Finalizar controlador",command=lambda:terminal_control(start_button_text,controller_drop,stop_controller_button))
    stop_controller_button.pack(fill=X)
    stop_controller_button["state"]="disabled"
    #boton para resetear la plataforma
    reset_platform_button= Button(controller_frame,text="Nivelar plataforma",command=reset_platform)
    reset_platform_button.pack(fill=X)
    ###################################################
    ##########frame de Datos y gráficos################
    ###################################################
    data_frame = LabelFrame(root, text="Graficos y datos", labelanchor='n',padx=5,pady=5)
    data_frame.grid(row=0,column=1,sticky="NSEW")
    #excel checkbox
    excel_enabled=IntVar()
    excel_checkbox=Checkbutton(data_frame,text="Generar excel",variable=excel_enabled,command=lambda:update_excel_checkbox(excel_enabled.get()))
    #excel_checkbox.pack(anchor="w")
    excel_checkbox.grid(row=0,column=0,sticky="W")
    #graphs checkbox
    graphs_enabled=IntVar()
    graphs_checkbox=Checkbutton(data_frame,text="Generar graficos",variable=graphs_enabled,command=lambda:update_graph_checkbox(graphs_enabled.get()))
   # graphs_checkbox.pack(anchor="w")
    graphs_checkbox.grid(row=1,column=0,sticky="W")
    #seleccion de camara
    sel_camera_label=Label(data_frame, text="Selcción de cámara")
    #sel_camera_label.pack()
    sel_camera_label.grid(row=3,column=0,sticky="W")
    spin_camera=Spinbox(data_frame,from_=0,to=10,width=2,command=lambda:select_camera(spin_camera.get()))
    #spin_camera.pack(anchor="w")
    spin_camera.grid(row=3,column=1,sticky="W")
    #arranco la GUI
    root.mainloop()




if __name__=="__main__":
    settings.init()
    start_GUI()
