import threading
import settings
from serial_com import send_command_to_platform
import numpy as np
import skfuzzy.control as fzctrl
#declaro las variables como globales para que puedan ser accedidas por
# el thread de modificación




class controller_t:
    def __init__(self, tipo, ancho_plataforma=None):
        self.tipo = tipo
        #if tipo == 'pid':
        self.prev_pos_x=0 #variable auxiliar para el control derivativo
        self.prev_pos_y=0 #variable auxiliar para el control derivativo

        self.Integral=0 #variable auxiliar para el control integral
        self.T=1/30 #30FPS
        if tipo == 'fuzzy1':
            #Creo las variables difusas. 1 entrada, 1 salida
            #Entrada
            error = fzctrl.Antecedent(np.linspace(-ancho_plataforma / 2, ancho_plataforma / 2, 5), 'error')
            ANGULO_MAXIMO = 10 #Sacar de algun lado, por ahora hardcodeado
            #Salida
            angulo = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 5), 'angulo')

            #Creo las funciones de membresia ("categoria" de cada variable)
            #Por simplicidad las genero de forma automatica pero se puede jugar con la forma y ancho de banda de cada categoria.
            nombres = ['ng', 'np', 'ce', 'pp', 'pg'] #Negativo grande, negativo pequeño, cero, positivo pequeño y positivo grande.
            error.automf(names=nombres)
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

        elif tipo == 'fuzzy2':
            #Entrada
            error = fzctrl.Antecedent(np.linspace(-ancho_plataforma / 2, ancho_plataforma / 2, 5), 'error')
            DELTA_MAXIMO = 0.8 * ancho_plataforma
            delta = fzctrl.Antecedent(np.linspace(-DELTA_MAXIMO, DELTA_MAXIMO, 5), 'delta')
            ANGULO_MAXIMO = 20 #Sacar de algun lado, por ahora hardcodeado
            #Salida
            angulo = fzctrl.Consequent(np.linspace(-ANGULO_MAXIMO, ANGULO_MAXIMO, 5), 'angulo')

            #Creo las funciones de membresia ("categoria" de cada variable)
            #Por simplicidad las genero de forma automatica pero se puede jugar con la forma y ancho de banda de cada categoria.
            nombres = ['ng', 'np', 'ce', 'pp', 'pg'] #Negativo grande, negativo pequeño, cero, positivo pequeño y positivo grande.
            error.automf(names=nombres)
            delta.automf(names=nombres)
            angulo.automf(names=nombres)

            #Escribo las reglas
            regla0 = fzctrl.Rule(antecedent=((error['ng'] & delta['pg']) | 
                                 (error['ng'] & delta['pp']) | 
                                 (error['np'] & delta['pg'])),
                                 consequent=angulo['pg'], label='Regla pg')


            regla1 = fzctrl.Rule(antecedent=((error['ng'] & delta['ce']) | 
                                            (error['ng'] & delta['np']) | 
                                            (error['np'] & delta['pp']) | 
                                            (error['np'] & delta['ce']) | 
                                            (error['ce'] & delta['pp']) | 
                                            (error['ce'] & delta['pg']) | 
                                            (error['pp'] & delta['pg'])),
                                            consequent=angulo['pp'], label='Regla pp')


            regla2 = fzctrl.Rule(antecedent=((error['ng'] & delta['ng']) | 
                                            (error['np'] & delta['np']) | 
                                            (error['ce'] & delta['ce']) | 
                                            (error['pp'] & delta['pp']) | 
                                            (error['pg'] & delta['pg']) | 
                                            (error['pp'] & delta['pg'])),
                                            consequent=angulo['ce'], label='Regla ce')


            regla3 = fzctrl.Rule(antecedent=((error['pg'] & delta['ce']) | 
                                            (error['pg'] & delta['pp']) | 
                                            (error['pp'] & delta['np']) | 
                                            (error['pp'] & delta['ce']) | 
                                            (error['ce'] & delta['np']) | 
                                            (error['ce'] & delta['ng']) | 
                                            (error['np'] & delta['ng'])),
                                            consequent=angulo['np'], label='Regla np')


            regla4 = fzctrl.Rule(antecedent=((error['pg'] & delta['ng']) | 
                                            (error['pg'] & delta['np']) | 
                                            (error['pp'] & delta['ng'])),
                                            consequent=angulo['ng'], label='Regla ng')

            #Creo el sistema y arranco la simulacion
            self.sistema = fzctrl.ControlSystem([regla0, regla1, regla2, regla3, regla4])
            self.simulacion = fzctrl.ControlSystemSimulation(self.sistema)

    def control(self,ball_pos):
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
        if self.tipo == 'pid':
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
        
        elif self.tipo == 'fuzzy2':
            delta = pos - prev_pos
            print('Delta: {}'.format(delta))
            self.simulacion.input['error'] = pos
            self.simulacion.input['delta'] = delta
            self.simulacion.compute()
            control_angle = self.simulacion.output['angulo']
        
        return control_angle

    

