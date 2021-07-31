from tkinter import *
import settings

def update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text,posy_slider,posx_slider,posx_text,posy_text):
    settings.Kd=float(Kd_slider.get())
    Kd_text.set("Kd="+str(settings.Kd))

    settings.Ki=float(Ki_slider.get())
    Ki_text.set("Ki="+str(settings.Ki))

    settings.Kp=float(Kp_slider.get())
    Kp_text.set("Kp="+str(settings.Kp))
    
    print("slider:")
    print(posy_slider.get())
    settings.pos_y=float(posy_slider.get())
    posy_text.set("Kp="+str(settings.pos_y))

    settings.pos_x=float(posx_slider.get())
    posx_text.set("Kp="+str(settings.pos_x))

def start_GUI():
    root= Tk()
    
    root.title("Adjuts parameters")
    root.geometry('800x800')
    #Kd setting
    Kd_text=StringVar()
    Kd_label=Label(root,textvariable=Kd_text)
    Kd_label.pack()
    Kd_slider=Scale(root, from_=0, to=0.1,orient = HORIZONTAL,label="Kd",resolution=0.001)
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
    #x pos setting
    posx_text=StringVar()
    posx_label=Label(root,textvariable=posx_text)
    posx_label.pack()
    posx_slider=Scale(root, from_=-250, to=250,orient = HORIZONTAL,label="posx",resolution=1)
    posx_slider.pack(anchor='w')  
    #y pos setting
    posy_text=StringVar()
    posy_label=Label(root,textvariable=posy_text)
    posy_label.pack()
    posy_slider=Scale(root, from_=-250, to=250,orient = HORIZONTAL,label="posy",resolution=1)
    posy_slider.pack(anchor='w')      

    #boton de confirmación de parametros
    confirm_button= Button(root,text="confirmar parametros",command=lambda: update_parameters(Kd_slider,Ki_slider,Kp_slider,Kd_text,Ki_text,Kp_text,posy_slider,posx_slider,posx_text,posy_text))
    confirm_button.pack()
    #arranco la GUI
    root.mainloop()


if __name__=="__main__":
    start_GUI()
