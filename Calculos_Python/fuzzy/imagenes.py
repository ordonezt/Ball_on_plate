import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as fzctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

#Constantes
ANCHO_PLATAFORMA = 1#m
ANGULO_MAXIMO = 20#º
VELOCIDAD_MAXIMA = 1#m/s

#Creo las variables difusas. 1 entrada, 1 salida

#Entrada
rango_error = ANCHO_PLATAFORMA/2
error = fzctrl.Antecedent(np.linspace(-rango_error, rango_error, 11), 'Error')
#Entrada 2
velocidad = fzctrl.Antecedent(np.linspace(-VELOCIDAD_MAXIMA, VELOCIDAD_MAXIMA, 11), 'Variable')

#Salida
angulo = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 11), 'Angulo')

#Creo las funciones de membresia ("categoria" de cada variable)
#Por simplicidad las genero de forma automatica pero se puede jugar con la forma y ancho de banda de cada categoria.
nombres = ['ne', 'ng', 'nm', 'np', 'nd', 'ce', 'pd', 'pp', 'pm', 'pg', 'pe']
error.automf(names=nombres)
angulo.automf(names=nombres)
velocidad.automf(names=nombres)

fig_e = error.view()
plt.show()

fig_v = velocidad.view()
plt.show()

fig_a = angulo.view()
plt.show()