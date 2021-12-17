import threading
import settings
from serial_com import send_command_to_platform
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as fzctrl
#declaro las variables como globales para que puedan ser accedidas por
# el thread de modificación




class controller_t:
    def __init__(self, tipo, ancho_plataforma=None):
        self.tipo = tipo
        self.prev_pos_x=0 #variable auxiliar para el control derivativo
        self.prev_pos_y=0 #variable auxiliar para el control derivativo

        self.Integral=0 #variable auxiliar para el control integral
        self.T=1/30 #30FPS
        self.delta_max_x = self.delta_max_y = 0
        if tipo == 'fuzzy1':
            self.angulo_anterior = 0
            #Creo las variables difusas. 1 entrada, 1 salida
            #Entrada
            error = fzctrl.Antecedent(np.linspace(-ancho_plataforma / 2, ancho_plataforma / 2, 5), 'error')
            ANGULO_MAXIMO = 20 #Sacar de algun lado, por ahora hardcodeado
            #Salida
            angulo = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 5), 'angulo')

            #Creo las funciones de membresia ("categoria" de cada variable)
            #Por simplicidad las genero de forma automatica pero se puede jugar con la forma y ancho de banda de cada categoria.
            nombres = ['ng', 'np', 'ce', 'pp', 'pg'] #Negativo grande, negativo pequeño, cero, positivo pequeño y positivo grande.
            #error.automf(names=nombres)
            error['ng'] = fuzz.trimf(error.universe, [-ancho_plataforma/2, -ancho_plataforma/2, -(2/3) * (ancho_plataforma/2)])
            error['np'] = fuzz.trapmf(error.universe, [-ancho_plataforma/2, -(2/3) * (ancho_plataforma/2), -(1/3) * (ancho_plataforma/2), 0])
            error['ce'] = fuzz.trapmf(error.universe, [-(1/3) * (ancho_plataforma/2), -0.1 * (ancho_plataforma/2), 0.1 * (ancho_plataforma/2), (1/3) * (ancho_plataforma/2)])
            error['pp'] = fuzz.trapmf(error.universe, [0, (1/3) * (ancho_plataforma/2), (2/3) * (ancho_plataforma/2), ancho_plataforma/2])
            error['pg'] = fuzz.trimf(error.universe, [(2/3) * (ancho_plataforma/2), ancho_plataforma/2, ancho_plataforma/2])
            angulo.automf(names=nombres)

            #Escribo las reglas
            #Si el error es negativo grande entonces el angulo es positivo grande
            regla0 = fzctrl.Rule(antecedent=error['ng'], consequent=angulo['pg'], label='Regla pg')
            #Si el error es negativo pequeño entonces el angulo es positivo pequeño
            regla1 = fzctrl.Rule(antecedent=error['np'], consequent=angulo['pp'], label='Regla pp')
            #Si el error es cero entonces el angulo es cero
            regla2 = fzctrl.Rule(antecedent=error['ce'], consequent=angulo['ce'], label='Regla ce')
            #Si el error es positivo pequeño entonces el angulo es negativo pequeño
            regla3 = fzctrl.Rule(antecedent=error['pp'], consequent=angulo['np'], label='Regla np')
            #Si el error es positivo grande entonces el angulo es negativo grande
            regla4 = fzctrl.Rule(antecedent=error['pg'], consequent=angulo['ng'], label='Regla ng')

            #Creo el sistema y arranco la simulacion
            self.sistema = fzctrl.ControlSystem([regla0, regla1, regla2, regla3, regla4])
            self.simulacion = fzctrl.ControlSystemSimulation(self.sistema)

        elif tipo == 'Fuzzy':
            
            #Entrada
            error = fzctrl.Antecedent(np.linspace(-ancho_plataforma / 2, ancho_plataforma / 2, 5), 'error')
            rango_delta = DELTA_MAXIMO = 20*settings.Escala_y #0.5 * ancho_plataforma
            delta = fzctrl.Antecedent(np.linspace(-DELTA_MAXIMO, DELTA_MAXIMO, 5), 'delta')
            ANGULO_MAXIMO = 15 #Sacar de algun lado, por ahora hardcodeado
            #Salida
            angulo = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 5), 'angulo')

            #Creo las funciones de membresia ("categoria" de cada variable)
            #Por simplicidad las genero de forma automatica pero se puede jugar con la forma y ancho de banda de cada categoria.
            nombres = ['ng', 'np', 'ce', 'pp', 'pg'] #Negativo grande, negativo pequeño, cero, positivo pequeño y positivo grande.
            
            error.automf(names=nombres)
            # error['ng'] = fuzz.trimf(error.universe, [-ancho_plataforma/2, -ancho_plataforma/2, -(2/3) * (ancho_plataforma/2)])
            # error['np'] = fuzz.trapmf(error.universe, [-ancho_plataforma/2, -(2/3) * (ancho_plataforma/2), -(1/3) * (ancho_plataforma/2), 0])
            # #error['ce'] = fuzz.trimf(error.universe, [-(1/3) * (ancho_plataforma/2), 0, (1/3) * (ancho_plataforma/2)])
            # error['ce'] = fuzz.trapmf(error.universe, [-(1/3) * (ancho_plataforma/2), -0.1 * (ancho_plataforma/2), 0.1 * (ancho_plataforma/2), (1/3) * (ancho_plataforma/2)])
            # error['pp'] = fuzz.trapmf(error.universe, [0, (1/3) * (ancho_plataforma/2), (2/3) * (ancho_plataforma/2), ancho_plataforma/2])
            # error['pg'] = fuzz.trimf(error.universe, [(2/3) * (ancho_plataforma/2), ancho_plataforma/2, ancho_plataforma/2])

            delta.automf(names=nombres)
            # delta['ng'] = fuzz.trimf(delta.universe, [-rango_delta, -rango_delta, -(2/3) * rango_delta])
            # delta['np'] = fuzz.trapmf(delta.universe, [-rango_delta, -(2/3) * rango_delta, -(1/3) * rango_delta, 0])
            # delta['ce'] = fuzz.trapmf(delta.universe, [-(1/3) * rango_delta, -0.1 * rango_delta, 0.1 * rango_delta, (1/3) * rango_delta])
            # delta['pp'] = fuzz.trapmf(delta.universe, [0, (1/3) * rango_delta, (2/3) * rango_delta, rango_delta])
            # delta['pg'] = fuzz.trimf(delta.universe, [(2/3) * rango_delta, rango_delta, rango_delta])

            angulo.automf(names=nombres)

            # #Originales
            # #Escribo las reglas
            # regla0 = fzctrl.Rule(antecedent=((error['ng'] & delta['ng']) | 
            #                      (error['ng'] & delta['np']) | 
            #                      (error['np'] & delta['ng'])),
            #                      consequent=angulo['pg'], label='Regla pg')


            # regla1 = fzctrl.Rule(antecedent=((error['ng'] & delta['ce']) | 
            #                                 (error['ng'] & delta['pp']) | 
            #                                 (error['np'] & delta['np']) | 
            #                                 (error['np'] & delta['ce']) | 
            #                                 (error['ce'] & delta['np']) | 
            #                                 (error['ce'] & delta['ng']) | 
            #                                 (error['pp'] & delta['ng'])),
            #                                 consequent=angulo['pp'], label='Regla pp')


            # regla2 = fzctrl.Rule(antecedent=((error['ng'] & delta['pg']) | 
            #                                 (error['np'] & delta['pp']) | 
            #                                 (error['ce'] & delta['ce']) | 
            #                                 (error['pp'] & delta['np']) | 
            #                                 (error['pg'] & delta['ng']) | 
            #                                 (error['pp'] & delta['ng'])),
            #                                 consequent=angulo['ce'], label='Regla ce')


            # regla3 = fzctrl.Rule(antecedent=((error['pg'] & delta['ce']) | 
            #                                 (error['pg'] & delta['np']) | 
            #                                 (error['pp'] & delta['pp']) | 
            #                                 (error['pp'] & delta['ce']) | 
            #                                 (error['ce'] & delta['pp']) | 
            #                                 (error['ce'] & delta['pg']) | 
            #                                 (error['np'] & delta['pg'])),
            #                                 consequent=angulo['np'], label='Regla np')


            # regla4 = fzctrl.Rule(antecedent=((error['pg'] & delta['pg']) | 
            #                                 (error['pg'] & delta['pp']) | 
            #                                 (error['pp'] & delta['pg'])),
            #                                 consequent=angulo['ng'], label='Regla ng')

            # #Version 4 estabiliza en el centro a velocidades chicas
            # #Escribo las reglas
            # regla0 = fzctrl.Rule(antecedent=((error['pg']) 
            #                                 |(error['pp'] & delta['pg'])),
            #                      consequent=angulo['ng'], label='Regla ng')


            # regla1 = fzctrl.Rule(antecedent=(((delta['pg'] | delta['pp'])       & (error['ce']))    | 
            #                                  (error['pp']  & (delta['ce'] | delta['pp']))),
            #                     consequent=angulo['np'], label='Regla np')


            # regla2 = fzctrl.Rule(antecedent=((error['np'] &  (delta['pp'] | delta['pg']))              |
            #                                  (error['ce'] & (delta['ce']))  |
            #                                  (error['pp'] &  (delta['ng'] | delta['np']))),
            #                     consequent=angulo['ce'], label='Regla ce')


            # regla3 = fzctrl.Rule(antecedent=((error['np'] & (delta['np'] | delta['ce']))                |
            #                                  ((delta['ng'] | delta['np']) & (error['ce']))),
            #                      consequent=angulo['pp'], label='Regla pp')


            # regla4 = fzctrl.Rule(antecedent=((error['ng']) |
            #                                  (error['np'] & delta['ng'])),
            #                      consequent=angulo['pg'], label='Regla pg')

            #Version 7
            #Escribo las reglas
            regla0 = fzctrl.Rule(antecedent=((error['pg'] & (delta['pp'] | delta['pg'])) |
                                             (error['pp'] & delta['pg']) |
                                             (error['ce'] & delta['pg'])),
                                 consequent=angulo['ng'], label='Regla ng')


            regla1 = fzctrl.Rule(antecedent=((error['pg'] & delta['ce'])                 | 
                                             (error['pp'] & (delta['pp'] | delta['ce'])) |
                                             (error['ce'] & delta['pp']) |
                                             (error['ng'] & delta['pg'])),
                                consequent=angulo['np'], label='Regla np')


            regla2 = fzctrl.Rule(antecedent=((error['ng'] & delta['pp'])                  |
                                             (error['np'] & (delta['pp'] | delta['pg']))  |
                                             (error['ce'] & (delta['ce']))                |
                                             (error['pp'] & (delta['ng'] | delta['np']))  |
                                             (error['pg'] & delta['np'])),
                                consequent=angulo['ce'], label='Regla ce')


            regla3 = fzctrl.Rule(antecedent=((error['ng'] & delta['ce']) | 
                                             (error['np'] & (delta['np'] | delta['ce'])) | 
                                             (error['ce'] & delta['np']) |
                                             (error['pg'] & delta['ng'])),
                                 consequent=angulo['pp'], label='Regla pp')


            regla4 = fzctrl.Rule(antecedent=((error['ng'] & (delta['np'] | delta['ng'])) | 
                                             (error['np'] & delta['ng']) |
                                             (error['ce'] & delta['ng'])),
                                 consequent=angulo['pg'], label='Regla pg')

            #Creo el sistema y arranco la simulacion
            self.sistema = fzctrl.ControlSystem([regla0, regla1, regla2, regla3, regla4])
            self.simulacion = fzctrl.ControlSystemSimulation(self.sistema)

    def control(self,ball_pos):
        #Para debug, se puede borrar
        if (ball_pos.pos_x - self.prev_pos_x) > self.delta_max_x:
            self.delta_max_x = ball_pos.pos_x - self.prev_pos_x
        if (ball_pos.pos_y - self.prev_pos_y) > self.delta_max_y:
            self.delta_max_y = ball_pos.pos_y - self.prev_pos_y
        print("deltas max {}, {}".format(self.delta_max_x, self.delta_max_y))

        angle_x=self.controller_1d(ball_pos.pos_x,self.prev_pos_x)
        angle_y=self.controller_1d(ball_pos.pos_y,self.prev_pos_y)

        self.prev_pos_x=ball_pos.pos_x
        self.prev_pos_y=ball_pos.pos_y
    
        print('angle_x={0}\n'.format(angle_x))
        print('angle_y={0}\n'.format(angle_y))
        #print("Envio de comando a la plataforma comentado!!")
        send_command_to_platform("/dev/ttyACM0",angle_x,angle_y,13)
        return angle_x,angle_x

    def controller_1d(self,pos,prev_pos):
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

        elif self.tipo == 'fuzzy1':
            print('Delta: {}'.format(pos - prev_pos))
            self.simulacion.input['error'] = pos
            self.simulacion.compute()
            control_angle = self.simulacion.output['angulo']
        
        elif self.tipo == 'Fuzzy':
            delta = pos - prev_pos
            
            print('Delta: {}'.format(delta))
            self.simulacion.input['error'] = pos
            self.simulacion.input['delta'] = delta
            self.simulacion.compute()
            control_angle = self.simulacion.output['angulo']
        
        return control_angle

    

