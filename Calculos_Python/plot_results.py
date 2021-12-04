import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("logs.xlsx")
fig,ax= plt.subplots(2,2)
ax[0,0].plot(df["pos_x"])
ax[0,0].set_title("Posición en X")
ax[0,1].plot(df["angle_x"])
ax[0,1].set_title("Ángulo de actuación en X")
ax[1,0].plot(df["pos_y"])
ax[1,0].set_title("Posición en Y")
ax[1,1].plot(df["angle_y"])
ax[1,1].set_title("Ángulo de actuación en Y")

plt.show()

