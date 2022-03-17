import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("logs.xlsx")
fig,ax= plt.subplots(2,3)
ax[0,0].plot(df["pos_x"])
ax[0,0].set_title("Posición en X")
ax[0,1].plot(df["angle_x"])
ax[0,1].set_title("Ángulo de actuación en X")
ax[1,0].plot(df["pos_y"])
ax[1,0].set_title("Posición en Y")
ax[1,1].plot(df["angle_y"])
ax[1,1].set_title("Ángulo de actuación en Y")
ax[0,2].plot(df["vel_x"])
ax[0,2].set_title("Velocidad en X")
ax[1,2].plot(df["vel_y"])
ax[1,2].set_title("Velocidad en Y")

fig2,ax2= plt.subplots()
ax2.plot(df["fps"])
ax2.set_title("FPS")

plt.show()

