import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import numpy as np
from time import sleep
time=[]
x_samples=[]
y_samples=[]


def plot_variables(i):
    plt.cla()
    plt.plot(time[-50:],x_samples[-50:],label='x axis')
    plt.plot(time[-50:],y_samples[-50:],label='y axis')
    plt.legend(loc='upper left')
    plt.tight_layout()  

def live_plotting():
    ani=FuncAnimation(plt.gcf(), plot_variables, interval=1)
    plt.tight_layout()
    plt.show()
    print("Died!!")

def generar_datos():
    t=0
    while (True):
        sleep(33/1000)
        t=t+33/1000
        x_samples.append(np.sin(2*np.pi*t) *np.exp(-t/10))
        y_samples.append(-np.sin(2*np.pi*t)*np.exp(-t/10))
        time.append(t)



t1=threading.Thread(target=generar_datos)
t1.start()
live_plotting()
