/**
 * @file servos.h
 * @brief En este archivo se encuentran las cabeceras de las funciones de manejo de los servo motores.
 * @author Tomás Bautista Ordóñez
 * @date 14/04/2021
 */

#ifndef INC_USR_SERVOS_H_
#define INC_USR_SERVOS_H_

#include "stm32f1xx.h"

typedef enum{
	SERVO_A,
	SERVO_B,
	SERVO_C
}servo_num_t;

#define CUENTA_MAXIMA					60000

#define LIMITE_SUPERIOR_CUENTAS			7800.0
#define LIMITE_INFERIOR_CUENTAS 		1100.0

#define LIMITE_SUPERIOR_MILIGRADOS		200000.0
#define LIMITE_INFERIOR_MILIGRADOS		0.0

#define LIMITE_SUPERIOR_SEGURO_CUENTAS	7500
#define LIMITE_INFERIOR_SEGURO_CUENTAS	1400

#define M_SERVOS						((LIMITE_SUPERIOR_MILIGRADOS - LIMITE_INFERIOR_MILIGRADOS) / (LIMITE_SUPERIOR_CUENTAS - LIMITE_INFERIOR_CUENTAS))
#define B_SERVOS						LIMITE_INFERIOR_SEGURO_CUENTAS

#define MILIGRADOS_MAXIMO				((LIMITE_SUPERIOR_SEGURO_CUENTAS - LIMITE_INFERIOR_SEGURO_CUENTAS) * M_SERVOS)

typedef struct{
	GPIO_TypeDef * puerto_gpio;
	uint16_t pin_gpio;
	uint32_t canal;
	TIM_HandleTypeDef *handler;
	uint32_t miligrados;
}servo_t;

/**
 * Inicializa los servos y los enciende a 0 grados.
 */
void servos_inicializar(void);

/**
 * Mueve el servo a la posicion especificada
 * @param servo Puntero al servo a modificar.
 * @param miligrados Angulo final al que se quiere llegar
 */
void servos_set_posicion(servo_t *servo, uint32_t miligrados);

/**
 * Tarea periodica que controla el movimiento de los servos
 */
void servos_tarea(void);

/**
 * Agrega un angulo a la lista de movimientos de un motor
 * @param servo Motor que se quiere mover
 * @param miligrados Angulo al que se quiere posicionar el motor
 * @return 0 Ok, 1 error
 */
uint8_t servos_agregar_angulo(servo_num_t servo, uint32_t miligrados);

#endif /* INC_USR_SERVOS_H_ */
