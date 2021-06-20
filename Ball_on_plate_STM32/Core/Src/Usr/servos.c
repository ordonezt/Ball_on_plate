/**
 * @file servos.c
 * @brief En este archivo se encuentran las funciones de manejo de los servo motores.
 * @author Tomás Bautista Ordóñez
 * @date 14/04/2021
 */

#include "main.h"
#include "servos.h"
#include "my_ring_buffer.h"

#define CANTIDAD_SERVOS				3
#define LONGITUD_BUFFER_ANGULOS		4
extern TIM_HandleTypeDef htim2;

servo_t servos[CANTIDAD_SERVOS];

RINGBUFF_T 	servo_ring_buffer[CANTIDAD_SERVOS];
uint32_t 	servo_angulos_buffer[LONGITUD_BUFFER_ANGULOS][CANTIDAD_SERVOS];
uint8_t flag_inicializado[3];
/**
 * Inicializa los servos y los enciende a 0 grados.
 */
void servos_inicializar(void)
{
	for(uint8_t i = 0; i < CANTIDAD_SERVOS; i++)
		RingBuffer_Init(&servo_ring_buffer[i], servo_angulos_buffer[i], sizeof(servo_angulos_buffer[i][0]), LONGITUD_BUFFER_ANGULOS);

	servos[SERVO_A].handler = &htim2;
	servos[SERVO_A].puerto_gpio = SERVO_A_GPIO_Port;
	servos[SERVO_A].pin_gpio = SERVO_A_Pin;
	servos[SERVO_A].canal = TIM_CHANNEL_1;

	servos[SERVO_B].handler = &htim2;
	servos[SERVO_B].puerto_gpio = SERVO_B_GPIO_Port;
	servos[SERVO_B].pin_gpio = SERVO_B_Pin;
	servos[SERVO_B].canal = TIM_CHANNEL_2;

	servos[SERVO_C].handler = &htim2;
	servos[SERVO_C].puerto_gpio = SERVO_C_GPIO_Port;
	servos[SERVO_C].pin_gpio = SERVO_C_Pin;
	servos[SERVO_C].canal = TIM_CHANNEL_3;
}

/**
 * Transforma miligrados en cuentas de PWM
 * @param miligrados Angulo a transformar
 * @return cuentas de PWM correspondientes a ese angulo
 */
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

/**
 * Transforma cuentas de PWM en miligrados
 * @param cuentas Cuentas de PWM
 * @return Angulo en miligrados correspondientes a esa cantidad de cuentas
 */
uint32_t servos_cuentas2miligrados(uint32_t cuentas)
{
	return (cuentas - LIMITE_INFERIOR_SEGURO_CUENTAS) * M_SERVOS;
}

/**
 * Escribe en el perisferico PWM el ancho de pulso requerido
 * @param servo Estructura al servo que se quiere mover
 * @param cuentas a escribir
 */
void servos_set_ancho_de_pulso(servo_t servo, uint32_t cuentas)
{
	__HAL_TIM_SET_COMPARE(servo.handler, servo.canal, cuentas);

	if(HAL_TIM_GetChannelState(servo.handler, servo.canal) != HAL_TIM_CHANNEL_STATE_BUSY)
		HAL_TIM_PWM_Start(servo.handler, servo.canal);
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

/**
 * Tarea periodica que controla el movimiento de los servos
 */
void servos_tarea(void)
{
	uint32_t angulo;

	for(uint8_t i = 0; i < CANTIDAD_SERVOS; i++)
	{
		if(RingBuffer_Pop(&servo_ring_buffer[i], &angulo))
			servos_set_posicion(&servos[i], angulo);
	}
}

/**
 * Agrega un angulo a la lista de movimientos de un motor
 * @param servo Motor que se quiere mover
 * @param miligrados Angulo al que se quiere posicionar el motor
 * @return 0 Ok, 1 error
 */
uint8_t servos_agregar_angulo(servo_num_t servo, uint32_t miligrados)
{
	return !RingBuffer_Insert(&servo_ring_buffer[servo], &miligrados);
}
