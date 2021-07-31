from tkinter import *
import settings

def update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text):
    settings.Kd=float(Kd_slider.get())
    Kd_text.set("Kd="+str(settings.Kd))

    settings.Ki=float(Ki_slider.get())
    Ki_text.set("Ki="+str(settings.Ki))

    settings.Kp=float(Kp_slider.get())
    Kp_text.set("Kp="+str(settings.Kp))


def start_GUI():
    root= Tk()
    
    root.title("Adjuts parameters")
    root.geometry('800x800')
    #Kd setting
    Kd_text=StringVar()
    Kd_label=Label(root,textvariable=Kd_text)
    Kd_label.pack()
    Kd_slider=Scale(root, from_=0, to=250,orient = HORIZONTAL,label="Kd",resolution=0.1)
    Kd_slider.pack(anchor='w')
    #Kp setting
    Kp_text=StringVar()
    Kp_label=Label(root,textvariable=Kp_text)
    Kp_label.pack()
    Kp_slider=Scale(root, from_=0, to=250,orient = HORIZONTAL,label="Kp",resolution=0.1)
    Kp_slider.pack(anchor='w')
    #Ki setting
    Ki_text=StringVar()
    Ki_label=Label(root,textvariable=Ki_text)
    Ki_label.pack()
    Ki_slider=Scale(root, from_=0, to=250,orient = HORIZONTAL,label="Ki",resolution=0.1)
    Ki_slider.pack(anchor='w')
    #boton de confirmación de parametros
    confirm_button= Button(root,text="confirmar parametros",command=lambda: update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text))
    confirm_button.pack()
    #arranco la GUI
    root.mainloop()


if __name__=="__main__":
    start_GUI()