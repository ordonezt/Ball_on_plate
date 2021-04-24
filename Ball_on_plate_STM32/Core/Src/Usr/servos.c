/**
 * @file servos.c
 * @brief En este archivo se encuentran las funciones de manejo de los servo motores.
 * @author Tomás Bautista Ordóñez
 * @date 14/04/2021
 */

#include "main.h"
#include "servos.h"

extern TIM_HandleTypeDef htim2;

servo_t servo_A, servo_B, servo_C, servo_D;

/**
 * Inicializa los servos y los enciende a 0 grados.
 */
void servos_inicializar(void)
{
	servo_A.handler = &htim2;
	servo_A.puerto_gpio = SERVO_A_GPIO_Port;
	servo_A.pin_gpio = SERVO_A_Pin;
	servo_A.canal = TIM_CHANNEL_1;

	servo_B.handler = &htim2;
	servo_B.puerto_gpio = SERVO_B_GPIO_Port;
	servo_B.pin_gpio = SERVO_B_Pin;
	servo_B.canal = TIM_CHANNEL_2;

	servo_C.handler = &htim2;
	servo_C.puerto_gpio = SERVO_C_GPIO_Port;
	servo_C.pin_gpio = SERVO_C_Pin;
	servo_C.canal = TIM_CHANNEL_3;

	servo_D.handler = &htim2;
	servo_D.puerto_gpio = SERVO_D_GPIO_Port;
	servo_D.pin_gpio = SERVO_D_Pin;
	servo_D.canal = TIM_CHANNEL_4;

	servos_set_posicion(&servo_A, 0);
	servos_set_posicion(&servo_B, 45000);
	servos_set_posicion(&servo_C, 90000);
	servos_set_posicion(&servo_D, 135000);

	HAL_TIM_PWM_Start(servo_A.handler, servo_A.canal);
	HAL_TIM_PWM_Start(servo_B.handler, servo_B.canal);
	HAL_TIM_PWM_Start(servo_C.handler, servo_C.canal);
	HAL_TIM_PWM_Start(servo_D.handler, servo_D.canal);
}

uint32_t servos_miligrados2cuentas(uint32_t miligrados)
{
	/*
	60000 cuentas ---> 20mS
	1 cuenta	  ---> 333.333nS

	Limites reales:
	1100 cuentas ----> 0.366mS ----> 0º
	7800 cuentas ----> 2.600mS ----> 200º

	y[mº] = 29.850746268657 mº/cuentas * x[cuentas] - 32835.8208955224 mº
	x[cuentas] = (y[mº] + 32835.8208955224 mº) / 29.850746268657 mº/cuentas

	**********************************************************************
	**********************************************************************

	Limites de seguridad:
	1400 cuentas ----> 0.466mS ----> 0º
	7500 cuentas ----> 2,500mS ----> 182089 mº

	y[mº] = 29.850746268657 mº/cuentas * x[cuentas] - 41791.0447761194 mº
	x[cuentas] = (y[mº] + 41791.0447761194 mº) / 29.850746268657 mº/cuentas
	*/

	return miligrados / M_SERVOS + B_SERVOS;
}

uint32_t servos_cuentas2miligrados(uint32_t cuentas)
{
	return (cuentas - LIMITE_INFERIOR_SEGURO_CUENTAS) * M_SERVOS;
}

void servos_set_ancho_de_pulso(servo_t servo, uint32_t cuentas)
{
	__HAL_TIM_SET_COMPARE(servo.handler, servo.canal, cuentas);
}

/**
 * Mueve el servo a la posicion especificada
 * @param servo Puntero al servo a modificar.
 * @param miligrados Angulo final al que se quiere llegar
 */
void servos_set_posicion(servo_t *servo, uint32_t miligrados)
{
	if(miligrados <= MILIGRADOS_MAXIMO)
	{
		servo->miligrados = miligrados;
		servos_set_ancho_de_pulso(*servo, servos_miligrados2cuentas(miligrados));
	}
}
