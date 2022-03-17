import threading
import settings
from serial_com import send_command_to_platform
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as fzctrl
import time
#declaro las variables como globales para que puedan ser accedidas por
# el thread de modificación




class controller_t:
    def __init__(self, tipo, ancho_plataforma_x=None, ancho_plataforma_y=None):
        self.tipo = tipo
        self.prev_pos_x=0 #variable auxiliar para el control derivativo
        self.prev_pos_y=0 #variable auxiliar para el control derivativo

        self.Integral=0 #variable auxiliar para el control integral
        self.T=1/30 #30FPS
        self.delta_max_x = self.delta_max_y = 0
        if tipo == 'Fuzzy':
            
            #Entrada
            error_y = fzctrl.Antecedent(np.linspace(-ancho_plataforma_y / 2, ancho_plataforma_y / 2, 11), 'error_y')
            rango_delta_y = 0.03 * ancho_plataforma_y #20*settings.Escala_y
            delta_y = fzctrl.Antecedent(np.linspace(-rango_delta_y, rango_delta_y, 11), 'delta_y')
            ANGULO_MAXIMO = 20 #Sacar de algun lado, por ahora hardcodeado
            #Salida
            angulo_y = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 11), 'angulo_y', defuzzify_method='centroid')

            #Entrada
            error_x = fzctrl.Antecedent(np.linspace(-ancho_plataforma_x / 2, ancho_plataforma_x / 2, 11), 'error_x')
            rango_delta_x = 0.03 * ancho_plataforma_x #20*settings.Escala_y
            delta_x = fzctrl.Antecedent(np.linspace(-rango_delta_x, rango_delta_x, 11), 'delta_x')
            ANGULO_MAXIMO = 20 #Sacar de algun lado, por ahora hardcodeado
            #Salida
            angulo_x = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 11), 'angulo_x', defuzzify_method='centroid')

            #Creo las funciones de membresia ("categoria" de cada variable)
            #Por simplicidad las genero de forma automatica pero se puede jugar con la forma y ancho de banda de cada categoria.
            nombres = ['ne', 'ng', 'nm', 'np', 'nd', 'ce', 'pd', 'pp', 'pm', 'pg', 'pe'] #Negativo grande, negativo pequeño, cero, positivo pequeño y positivo grande.
            
            error_y.automf(names=nombres)

            delta_y.automf(names=nombres)

            angulo_y.automf(names=nombres)

            error_x.automf(names=nombres)

            delta_x.automf(names=nombres)

            angulo_x.automf(names=nombres)

            # #Version 13
            # #Escribo las reglas
            # regla0 = fzctrl.Rule(antecedent=((error['ne'] & (delta['ne'] | delta['ng'] | delta['nm'] | delta['np']))    |
            #                                  (error['ng'] & (delta['ne'] | delta['ng'] | delta['nm']))                  |
            #                                  (error['nm'] & (delta['ne'] | delta['ng']))                                |
            #                                  (error['np'] & (delta['ne']))),
            #                      consequent=angulo['pe'], label='Regla pe')

            
            # regla1 = fzctrl.Rule(antecedent=((error['ne'] & (delta['nd'] | delta['ce']))    |
            #                                  (error['ng'] & (delta['nd'] | delta['np']))    |
            #                                  (error['nm'] & (delta['np'] | delta['nm']))    |
            #                                  (error['np'] & (delta['nm'] | delta['ng']))    |
            #                                  (error['nd'] & (delta['ng'] | delta['ne']))    |
            #                                  (error['ce'] & (delta['ne']))),
            #                      consequent=angulo['pg'], label='Regla pg')


            # regla2 = fzctrl.Rule(antecedent=((error['pd'] & delta['ne'])    |
            #                                  (error['ce'] & delta['ng'])    |
            #                                  (error['nd'] & delta['nm'])    |
            #                                  (error['np'] & delta['np'])    |
            #                                  (error['nm'] & delta['nd'])    |
            #                                  (error['ng'] & delta['ce'])    |
            #                                  (error['ne'] & delta['pd'])),
            #                      consequent=angulo['pm'], label='Regla pm')


            # regla3 = fzctrl.Rule(antecedent=((error['pp'] & delta['ne'])    |
            #                                  (error['pd'] & delta['ng'])    |
            #                                  (error['ce'] & delta['nm'])    |
            #                                  (error['nd'] & delta['np'])    |
            #                                  (error['np'] & delta['nd'])    |
            #                                  (error['nm'] & delta['ce'])    |
            #                                  (error['ng'] & delta['pd'])    |
            #                                  (error['ne'] & delta['pp'])),
            #                      consequent=angulo['pp'], label='Regla pp')


            # regla4 = fzctrl.Rule(antecedent=((error['pg'] & delta['ne'])    |
            #                                  (error['pm'] & (delta['ng'] | delta['ne']))    |
            #                                  (error['pp'] & (delta['nm'] | delta['ng']))    |
            #                                  (error['pd'] & (delta['np'] | delta['nm']))    |
            #                                  (error['ce'] & (delta['nd'] | delta['np']))    |
            #                                  (error['nd'] & (delta['ce'] | delta['nd']))    |
            #                                  (error['np'] & (delta['pd'] | delta['ce']))    |
            #                                  (error['nm'] & (delta['pp'] | delta['pd']))    |
            #                                  (error['ng'] & (delta['pm'] | delta['pp']))    |
            #                                  (error['ne'] & (delta['pg'] | delta['pm']))),
            #                      consequent=angulo['pd'], label='Regla pd')


            # regla5 = fzctrl.Rule(antecedent=((error['ne'] & delta['pe']) |
            #                                  (error['ng'] & delta['pg']) | 
            #                                  (error['nm'] & delta['pm']) |
            #                                  (error['np'] & delta['pp']) |
            #                                  (error['nd'] & delta['pd']) |
            #                                  (error['ce'] & delta['ce']) |
            #                                  (error['pd'] & delta['nd']) |
            #                                  (error['pp'] & delta['np']) |
            #                                  (error['pm'] & delta['nm']) |
            #                                  (error['pg'] & delta['ng']) |
            #                                  (error['pe'] & delta['ne'])),
            #                     consequent=angulo['ce'], label='Regla ce')


            # regla6 = fzctrl.Rule(antecedent=((error['pe'] & (delta['nm'] | delta['ng']))    |
            #                                  (error['pg'] & (delta['np'] | delta['nm']))    |
            #                                  (error['pm'] & (delta['nd'] | delta['np']))    |
            #                                  (error['pp'] & (delta['ce'] | delta['nd']))    |
            #                                  (error['pd'] & (delta['pd'] | delta['ce']))    |
            #                                  (error['ce'] & (delta['pp'] | delta['pd']))    |
            #                                  (error['nd'] & (delta['pm'] | delta['pp']))    |
            #                                  (error['np'] & (delta['pg'] | delta['pm']))    |
            #                                  (error['nm'] & (delta['pe'] | delta['pg']))    |
            #                                  (error['ng'] & delta['pe'])),
            #                      consequent=angulo['nd'], label='Regla nd')


            # regla7 = fzctrl.Rule(antecedent=((error['pe'] & delta['np'])    |
            #                                  (error['pg'] & delta['nd'])    |
            #                                  (error['pm'] & delta['ce'])    |
            #                                  (error['pp'] & delta['pd'])    |
            #                                  (error['pd'] & delta['pp'])    |
            #                                  (error['ce'] & delta['pm'])    |
            #                                  (error['nd'] & delta['pg'])    |
            #                                  (error['np'] & delta['pe'])),
            #                      consequent=angulo['np'], label='Regla np')
            

            # regla8 = fzctrl.Rule(antecedent=((error['pe'] & delta['nd'])    |
            #                                  (error['pg'] & delta['ce'])    |
            #                                  (error['pm'] & delta['pd'])    |
            #                                  (error['pp'] & delta['pp'])    |
            #                                  (error['pd'] & delta['pm'])    |
            #                                  (error['ce'] & delta['pg'])    |
            #                                  (error['nd'] & delta['pe'])),
            #                      consequent=angulo['nm'], label='Regla nm')

            # regla9 = fzctrl.Rule(antecedent=((error['pe'] & (delta['pd'] | delta['ce']))    |
            #                                  (error['pg'] & (delta['pp'] | delta['pd']))    |
            #                                  (error['pm'] & (delta['pm'] | delta['pp']))    |
            #                                  (error['pp'] & (delta['pg'] | delta['pm']))    |
            #                                  (error['pd'] & (delta['pe'] | delta['pg']))    |
            #                                  (error['ce'] & (delta['pe']))),
            #                      consequent=angulo['ng'], label='Regla ng')


            # regla10 = fzctrl.Rule(antecedent=((error['pe'] & (delta['pe'] | delta['pg'] | delta['pm'] | delta['pp']))    |
            #                                   (error['pg'] & (delta['pe'] | delta['pg'] | delta['pm']))                  |
            #                                   (error['pm'] & (delta['pe'] | delta['pg']))                                |
            #                                   (error['pp'] & (delta['pe']))),
            #                      consequent=angulo['ne'], label='Regla ne')

            # #Version 14
            # #Escribo las reglas
            # regla0 = fzctrl.Rule(antecedent=((error['ne'] & (delta['ne'] | delta['ng']))    |
            #                                  (error['ng'] & delta['ne'])),
            #                      consequent=angulo['pe'], label='Regla pe')

            
            # regla1 = fzctrl.Rule(antecedent=((error['ne'] & delta['nm'])    |
            #                                  (error['ng'] & delta['ng'])    |
            #                                  (error['nm'] & delta['ne'])),
            #                      consequent=angulo['pg'], label='Regla pg')


            # regla2 = fzctrl.Rule(antecedent=((error['nd'] & delta['ne'])                    |
            #                                  (error['np'] & (delta['ng'] | delta['ne']))    |
            #                                  (error['nm'] & (delta['nm'] | delta['ng']))    |
            #                                  (error['ng'] & (delta['np'] | delta['nm']))    |
            #                                  (error['ne'] & (delta['nd'] | delta['np']))),
            #                      consequent=angulo['pm'], label='Regla pm')


            # regla3 = fzctrl.Rule(antecedent=((error['pd'] & delta['ne'])                    |
            #                                  (error['ce'] & (delta['ng'] | delta['ne']))    |
            #                                  (error['nd'] & (delta['nm'] | delta['ng']))    |
            #                                  (error['np'] & (delta['np'] | delta['nm']))    |
            #                                  (error['nm'] & (delta['nd'] | delta['np']))    |
            #                                  (error['ng'] & (delta['ce'] | delta['nd']))    |
            #                                  (error['ne'] & (delta['pd'] | delta['ce']))),
            #                      consequent=angulo['pp'], label='Regla pp')


            # regla4 = fzctrl.Rule(antecedent=((error['pg'] & delta['ne'])                                  |
            #                                  (error['pm'] & (delta['ng'] | delta['ne']))                  |
            #                                  (error['pp'] & (delta['nm'] | delta['ng'] | delta['ne']))    |
            #                                  (error['pd'] & (delta['np'] | delta['nm'] | delta['ng']))    |
            #                                  (error['ce'] & (delta['nd'] | delta['np'] | delta['nm']))    |
            #                                  (error['nd'] & (delta['ce'] | delta['nd'] | delta['np']))    |
            #                                  (error['np'] & (delta['pd'] | delta['ce'] | delta['nd']))    |
            #                                  (error['nm'] & (delta['pp'] | delta['pd'] | delta['ce']))    |
            #                                  (error['ng'] & (delta['pm'] | delta['pp'] | delta['pd']))    |
            #                                  (error['ne'] & (delta['pg'] | delta['pm'] | delta['pp']))),
            #                      consequent=angulo['pd'], label='Regla pd')


            # regla5 = fzctrl.Rule(antecedent=((error['ne'] & delta['pe']) |
            #                                  (error['ng'] & delta['pg']) | 
            #                                  (error['nm'] & delta['pm']) |
            #                                  (error['np'] & delta['pp']) |
            #                                  (error['nd'] & delta['pd']) |
            #                                  (error['ce'] & delta['ce']) |
            #                                  (error['pd'] & delta['nd']) |
            #                                  (error['pp'] & delta['np']) |
            #                                  (error['pm'] & delta['nm']) |
            #                                  (error['pg'] & delta['ng']) |
            #                                  (error['pe'] & delta['ne'])),
            #                     consequent=angulo['ce'], label='Regla ce')


            # regla6 = fzctrl.Rule(antecedent=((error['pe'] & (delta['np'] | delta['nm'] | delta['ng']))    |
            #                                  (error['pg'] & (delta['nd'] | delta['np'] | delta['nm']))    |
            #                                  (error['pm'] & (delta['ce'] | delta['nd'] | delta['np']))    |
            #                                  (error['pp'] & (delta['pd'] | delta['ce'] | delta['nd']))    |
            #                                  (error['pd'] & (delta['pp'] | delta['pd'] | delta['ce']))    |
            #                                  (error['ce'] & (delta['pm'] | delta['pp'] | delta['pd']))    |
            #                                  (error['nd'] & (delta['pg'] | delta['pm'] | delta['pp']))    |
            #                                  (error['np'] & (delta['pe'] | delta['pg'] | delta['pm']))    |
            #                                  (error['nm'] & (delta['pe'] | delta['pg']))                  |
            #                                  (error['ng'] & delta['pe'])),
            #                      consequent=angulo['nd'], label='Regla nd')


            # regla7 = fzctrl.Rule(antecedent=((error['pe'] & (delta['ce'] | delta['nd']))    |
            #                                  (error['pg'] & (delta['pd'] | delta['ce']))    |
            #                                  (error['pm'] & (delta['pp'] | delta['pd']))    |
            #                                  (error['pp'] & (delta['pm'] | delta['pp']))    |
            #                                  (error['pd'] & (delta['pg'] | delta['pm']))    |
            #                                  (error['ce'] & (delta['pe'] | delta['pg']))    |
            #                                  (error['nd'] & delta['pe'])),
            #                      consequent=angulo['np'], label='Regla np')
            

            # regla8 = fzctrl.Rule(antecedent=((error['pe'] & (delta['pp'] | delta['pd']))    |
            #                                  (error['pg'] & (delta['pm'] | delta['pp']))    |
            #                                  (error['pm'] & (delta['pg'] | delta['pm']))    |
            #                                  (error['pp'] & (delta['pe'] | delta['pg']))    |
            #                                  (error['pd'] & delta['pe'])),
            #                      consequent=angulo['nm'], label='Regla nm')

            # regla9 = fzctrl.Rule(antecedent=((error['pe'] & delta['pm'])    |
            #                                  (error['pg'] & delta['pg'])    |
            #                                  (error['pm'] & delta['pe'])),
            #                      consequent=angulo['ng'], label='Regla ng')


            # regla10 = fzctrl.Rule(antecedent=((error['pe'] & (delta['pe'] | delta['pg']))    |
            #                                   (error['pg'] & delta['pe'])),
            #                      consequent=angulo['ne'], label='Regla ne')


            #Version 15
            #Escribo las reglas
            regla0_x = fzctrl.Rule(antecedent=((error_x['ne'] & (delta_x['ne'] | delta_x['ng']))    |
                                             (error_x['ng'] & delta_x['ne'])),
                                 consequent=angulo_x['pe'], label='Regla pe')

            
            regla1_x = fzctrl.Rule(antecedent=((error_x['ne'] & delta_x['nm'])    |
                                             (error_x['ng'] & delta_x['ng'])    |
                                             (error_x['nm'] & delta_x['ne'])),
                                 consequent=angulo_x['pg'], label='Regla pg')


            regla2_x = fzctrl.Rule(antecedent=((error_x['nd'] & delta_x['ne'])                    |
                                             (error_x['np'] & (delta_x['ng'] | delta_x['ne']))    |
                                             (error_x['nm'] & (delta_x['nm'] | delta_x['ng']))    |
                                             (error_x['ng'] & (delta_x['np'] | delta_x['nm']))    |
                                             (error_x['ne'] & (delta_x['nd'] | delta_x['np']))),
                                 consequent=angulo_x['pm'], label='Regla pm')


            regla3_x = fzctrl.Rule(antecedent=((error_x['pd'] & delta_x['ne'])                    |
                                             (error_x['ce'] & (delta_x['ng'] | delta_x['ne']))    |
                                             (error_x['nd'] & (delta_x['nm'] | delta_x['ng']))    |
                                             (error_x['np'] & (delta_x['np'] | delta_x['nm']))    |
                                             (error_x['nm'] & (delta_x['nd'] | delta_x['np']))    |
                                             (error_x['ng'] & (delta_x['ce'] | delta_x['nd']))    |
                                             (error_x['ne'] & (delta_x['pd'] | delta_x['ce']))),
                                 consequent=angulo_x['pp'], label='Regla pp')


            regla4_x = fzctrl.Rule(antecedent=((error_x['pg'] & delta_x['ne'])                                  |
                                             (error_x['pm'] & (delta_x['ng'] | delta_x['ne']))                  |
                                             (error_x['pp'] & (delta_x['nm'] | delta_x['ng'] | delta_x['ne']))    |
                                             (error_x['pd'] & (delta_x['np'] | delta_x['nm'] | delta_x['ng']))    |
                                             (error_x['ce'] & (delta_x['nd'] | delta_x['np'] | delta_x['nm']))    |
                                             (error_x['nd'] & (delta_x['ce'] | delta_x['nd'] | delta_x['np']))    |
                                             (error_x['np'] & (delta_x['pd'] | delta_x['ce'] | delta_x['nd']))    |
                                             (error_x['nm'] & (delta_x['pp'] | delta_x['pd'] | delta_x['ce']))    |
                                             (error_x['ng'] & (delta_x['pm'] | delta_x['pp'] | delta_x['pd']))    |
                                             (error_x['ne'] & (delta_x['pg'] | delta_x['pm'] | delta_x['pp']))),
                                 consequent=angulo_x['pd'], label='Regla pd')


            regla5_x = fzctrl.Rule(antecedent=((error_x['ne'] & delta_x['pe']) |
                                             (error_x['ng'] & delta_x['pg']) | 
                                             (error_x['nm'] & delta_x['pm']) |
                                             (error_x['np'] & delta_x['pp']) |
                                             (error_x['nd'] & delta_x['pd']) |
                                             (error_x['ce'] & delta_x['ce']) |
                                             (error_x['pd'] & delta_x['nd']) |
                                             (error_x['pp'] & delta_x['np']) |
                                             (error_x['pm'] & delta_x['nm']) |
                                             (error_x['pg'] & delta_x['ng']) |
                                             (error_x['pe'] & delta_x['ne'])),
                                consequent=angulo_x['ce'], label='Regla ce')


            regla6_x = fzctrl.Rule(antecedent=((error_x['pe'] & (delta_x['np'] | delta_x['nm'] | delta_x['ng']))    |
                                             (error_x['pg'] & (delta_x['nd'] | delta_x['np'] | delta_x['nm']))    |
                                             (error_x['pm'] & (delta_x['ce'] | delta_x['nd'] | delta_x['np']))    |
                                             (error_x['pp'] & (delta_x['pd'] | delta_x['ce'] | delta_x['nd']))    |
                                             (error_x['pd'] & (delta_x['pp'] | delta_x['pd'] | delta_x['ce']))    |
                                             (error_x['ce'] & (delta_x['pm'] | delta_x['pp'] | delta_x['pd']))    |
                                             (error_x['nd'] & (delta_x['pg'] | delta_x['pm'] | delta_x['pp']))    |
                                             (error_x['np'] & (delta_x['pe'] | delta_x['pg'] | delta_x['pm']))    |
                                             (error_x['nm'] & (delta_x['pe'] | delta_x['pg']))                  |
                                             (error_x['ng'] & delta_x['pe'])),
                                 consequent=angulo_x['nd'], label='Regla nd')


            regla7_x = fzctrl.Rule(antecedent=((error_x['pe'] & (delta_x['ce'] | delta_x['nd']))    |
                                             (error_x['pg'] & (delta_x['pd'] | delta_x['ce']))    |
                                             (error_x['pm'] & (delta_x['pp'] | delta_x['pd']))    |
                                             (error_x['pp'] & (delta_x['pm'] | delta_x['pp']))    |
                                             (error_x['pd'] & (delta_x['pg'] | delta_x['pm']))    |
                                             (error_x['ce'] & (delta_x['pe'] | delta_x['pg']))    |
                                             (error_x['nd'] & delta_x['pe'])),
                                 consequent=angulo_x['np'], label='Regla np')
            

            regla8_x = fzctrl.Rule(antecedent=((error_x['pe'] & (delta_x['pp'] | delta_x['pd']))    |
                                             (error_x['pg'] & (delta_x['pm'] | delta_x['pp']))    |
                                             (error_x['pm'] & (delta_x['pg'] | delta_x['pm']))    |
                                             (error_x['pp'] & (delta_x['pe'] | delta_x['pg']))    |
                                             (error_x['pd'] & delta_x['pe'])),
                                 consequent=angulo_x['nm'], label='Regla nm')

            regla9_x = fzctrl.Rule(antecedent=((error_x['pe'] & delta_x['pm'])    |
                                             (error_x['pg'] & delta_x['pg'])    |
                                             (error_x['pm'] & delta_x['pe'])),
                                 consequent=angulo_x['ng'], label='Regla ng')


            regla10_x = fzctrl.Rule(antecedent=((error_x['pe'] & (delta_x['pe'] | delta_x['pg']))    |
                                              (error_x['pg'] & delta_x['pe'])),
                                 consequent=angulo_x['ne'], label='Regla ne')

            #Version 15
            #Escribo las reglas
            regla0_y = fzctrl.Rule(antecedent=((error_y['ne'] & (delta_y['ne'] | delta_y['ng']))    |
                                             (error_y['ng'] & delta_y['ne'])),
                                 consequent=angulo_y['pe'], label='Regla pe')

            
            regla1_y = fzctrl.Rule(antecedent=((error_y['ne'] & delta_y['nm'])    |
                                             (error_y['ng'] & delta_y['ng'])    |
                                             (error_y['nm'] & delta_y['ne'])),
                                 consequent=angulo_y['pg'], label='Regla pg')


            regla2_y = fzctrl.Rule(antecedent=((error_y['nd'] & delta_y['ne'])                    |
                                             (error_y['np'] & (delta_y['ng'] | delta_y['ne']))    |
                                             (error_y['nm'] & (delta_y['nm'] | delta_y['ng']))    |
                                             (error_y['ng'] & (delta_y['np'] | delta_y['nm']))    |
                                             (error_y['ne'] & (delta_y['nd'] | delta_y['np']))),
                                 consequent=angulo_y['pm'], label='Regla pm')


            regla3_y = fzctrl.Rule(antecedent=((error_y['pd'] & delta_y['ne'])                    |
                                             (error_y['ce'] & (delta_y['ng'] | delta_y['ne']))    |
                                             (error_y['nd'] & (delta_y['nm'] | delta_y['ng']))    |
                                             (error_y['np'] & (delta_y['np'] | delta_y['nm']))    |
                                             (error_y['nm'] & (delta_y['nd'] | delta_y['np']))    |
                                             (error_y['ng'] & (delta_y['ce'] | delta_y['nd']))    |
                                             (error_y['ne'] & (delta_y['pd'] | delta_y['ce']))),
                                 consequent=angulo_y['pp'], label='Regla pp')


            regla4_y = fzctrl.Rule(antecedent=((error_y['pg'] & delta_y['ne'])                                  |
                                             (error_y['pm'] & (delta_y['ng'] | delta_y['ne']))                  |
                                             (error_y['pp'] & (delta_y['nm'] | delta_y['ng'] | delta_y['ne']))    |
                                             (error_y['pd'] & (delta_y['np'] | delta_y['nm'] | delta_y['ng']))    |
                                             (error_y['ce'] & (delta_y['nd'] | delta_y['np'] | delta_y['nm']))    |
                                             (error_y['nd'] & (delta_y['ce'] | delta_y['nd'] | delta_y['np']))    |
                                             (error_y['np'] & (delta_y['pd'] | delta_y['ce'] | delta_y['nd']))    |
                                             (error_y['nm'] & (delta_y['pp'] | delta_y['pd'] | delta_y['ce']))    |
                                             (error_y['ng'] & (delta_y['pm'] | delta_y['pp'] | delta_y['pd']))    |
                                             (error_y['ne'] & (delta_y['pg'] | delta_y['pm'] | delta_y['pp']))),
                                 consequent=angulo_y['pd'], label='Regla pd')


            regla5_y = fzctrl.Rule(antecedent=((error_y['ne'] & delta_y['pe']) |
                                             (error_y['ng'] & delta_y['pg']) | 
                                             (error_y['nm'] & delta_y['pm']) |
                                             (error_y['np'] & delta_y['pp']) |
                                             (error_y['nd'] & delta_y['pd']) |
                                             (error_y['ce'] & delta_y['ce']) |
                                             (error_y['pd'] & delta_y['nd']) |
                                             (error_y['pp'] & delta_y['np']) |
                                             (error_y['pm'] & delta_y['nm']) |
                                             (error_y['pg'] & delta_y['ng']) |
                                             (error_y['pe'] & delta_y['ne'])),
                                consequent=angulo_y['ce'], label='Regla ce')


            regla6_y = fzctrl.Rule(antecedent=((error_y['pe'] & (delta_y['np'] | delta_y['nm'] | delta_y['ng']))    |
                                             (error_y['pg'] & (delta_y['nd'] | delta_y['np'] | delta_y['nm']))    |
                                             (error_y['pm'] & (delta_y['ce'] | delta_y['nd'] | delta_y['np']))    |
                                             (error_y['pp'] & (delta_y['pd'] | delta_y['ce'] | delta_y['nd']))    |
                                             (error_y['pd'] & (delta_y['pp'] | delta_y['pd'] | delta_y['ce']))    |
                                             (error_y['ce'] & (delta_y['pm'] | delta_y['pp'] | delta_y['pd']))    |
                                             (error_y['nd'] & (delta_y['pg'] | delta_y['pm'] | delta_y['pp']))    |
                                             (error_y['np'] & (delta_y['pe'] | delta_y['pg'] | delta_y['pm']))    |
                                             (error_y['nm'] & (delta_y['pe'] | delta_y['pg']))                  |
                                             (error_y['ng'] & delta_y['pe'])),
                                 consequent=angulo_y['nd'], label='Regla nd')


            regla7_y = fzctrl.Rule(antecedent=((error_y['pe'] & (delta_y['ce'] | delta_y['nd']))    |
                                             (error_y['pg'] & (delta_y['pd'] | delta_y['ce']))    |
                                             (error_y['pm'] & (delta_y['pp'] | delta_y['pd']))    |
                                             (error_y['pp'] & (delta_y['pm'] | delta_y['pp']))    |
                                             (error_y['pd'] & (delta_y['pg'] | delta_y['pm']))    |
                                             (error_y['ce'] & (delta_y['pe'] | delta_y['pg']))    |
                                             (error_y['nd'] & delta_y['pe'])),
                                 consequent=angulo_y['np'], label='Regla np')
            

            regla8_y = fzctrl.Rule(antecedent=((error_y['pe'] & (delta_y['pp'] | delta_y['pd']))    |
                                             (error_y['pg'] & (delta_y['pm'] | delta_y['pp']))    |
                                             (error_y['pm'] & (delta_y['pg'] | delta_y['pm']))    |
                                             (error_y['pp'] & (delta_y['pe'] | delta_y['pg']))    |
                                             (error_y['pd'] & delta_y['pe'])),
                                 consequent=angulo_y['nm'], label='Regla nm')

            regla9_y = fzctrl.Rule(antecedent=((error_y['pe'] & delta_y['pm'])    |
                                             (error_y['pg'] & delta_y['pg'])    |
                                             (error_y['pm'] & delta_y['pe'])),
                                 consequent=angulo_y['ng'], label='Regla ng')


            regla10_y = fzctrl.Rule(antecedent=((error_y['pe'] & (delta_y['pe'] | delta_y['pg']))    |
                                              (error_y['pg'] & delta_y['pe'])),
                                 consequent=angulo_y['ne'], label='Regla ne')

            #Creo el sistema y arranco la simulacion
            self.sistema_x = fzctrl.ControlSystem([regla0_x, regla1_x, regla2_x, regla3_x, regla4_x, regla5_x, regla6_x, regla7_x, regla8_x, regla9_x, regla10_x])
            self.simulacion_x = fzctrl.ControlSystemSimulation(self.sistema_x)

            self.sistema_y = fzctrl.ControlSystem([regla0_y, regla1_y, regla2_y, regla3_y, regla4_y, regla5_y, regla6_y, regla7_y, regla8_y, regla9_y, regla10_y])
            self.simulacion_y = fzctrl.ControlSystemSimulation(self.sistema_y)

    def control(self,ball_pos):
        #Para debug, se puede borrar
        delta_x = ball_pos.pos_x - self.prev_pos_x
        delta_y = ball_pos.pos_y - self.prev_pos_y
        if delta_x > self.delta_max_x:
            self.delta_max_x = delta_x
        if delta_y > self.delta_max_y:
            self.delta_max_y = delta_y
        print("deltas max {}, {}".format(self.delta_max_x, self.delta_max_y))

        tiempo_inicial = time.time()
        angle_x=self.controller_1d(ball_pos.pos_x,self.prev_pos_x, 'x')
        angle_y=self.controller_1d(ball_pos.pos_y,self.prev_pos_y, 'y')
        tiempo_final = time.time()

        self.prev_pos_x=ball_pos.pos_x
        self.prev_pos_y=ball_pos.pos_y
    
        print('angle_x={0}\n'.format(angle_x))
        print('angle_y={0}\n'.format(angle_y))
        #print("Envio de comando a la plataforma comentado!!")
        send_command_to_platform("/dev/ttyACM0",angle_x,angle_y,13)
        print('Demora = {}'.format(tiempo_final - tiempo_inicial))
        return {"angle_x": angle_x, "angle_y": angle_y, "vel_x": delta_x, "vel_y": delta_y}

    def controller_1d(self,pos,prev_pos, coord):
        if self.tipo == 'PID':
            #estos valores se actualizan desde la GUI
            Ki=settings.Ki
            Kp=settings.Kp
            Kd=settings.Kd
            pos=-pos
            #parte integral
            self.Integral=self.Integral + pos * Ki * self.T
            #parte proporcional
            Propocional=pos * Kp
            #parte derivativa
            print(f"pos={pos}")
            print(f"prev_pos={prev_pos}")
            
            Derivativa=-(-pos-prev_pos) * Kd /self.T

            control_angle=self.Integral+Propocional+Derivativa
        
        elif self.tipo == 'Fuzzy':
            delta = pos - prev_pos
            
            print('Delta: {}'.format(delta))

            if(coord == 'x'):
                self.simulacion_x.input['error_x'] = pos
                self.simulacion_x.input['delta_x'] = delta
                self.simulacion_x.compute()
                control_angle = self.simulacion_x.output['angulo_x']
            else:
                self.simulacion_y.input['error_y'] = pos
                self.simulacion_y.input['delta_y'] = delta
                self.simulacion_y.compute()
                control_angle = self.simulacion_y.output['angulo_y']
        
        return control_angle

    

