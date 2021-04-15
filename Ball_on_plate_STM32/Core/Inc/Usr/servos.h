/**
 * @file servos.h
 * @brief En este archivo se encuentran las cabeceras de las funciones de manejo de los servo motores.
 * @author Tomás Bautista Ordóñez
 * @date 14/04/2021
 */

#ifndef INC_USR_SERVOS_H_
#define INC_USR_SERVOS_H_

#include "stm32f1xx.h"


#define CUENTA_MAXIMA			60000
#define ANGULO_MAXIMO			180
#define MILIGRADOS_POR_CUENTA	60
#define CUENTAS_180		6000
#define CUENTAS_0		3000
#define MILIGRADOS_MAXIMO		180000

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

#endif /* INC_USR_SERVOS_H_ */
