/**
 * @file leds.c
 * @brief En este archivo se encuentran las funciones de manejo de los leds.
 * @author Tomás Bautista Ordóñez
 * @date 15/04/2021
 */

#include "main.h"
#include "timers.h"
#include "leds.h"

/**
 * @brief Togglea el led periodicamente
 *
 * @param timer_id Identificador del timer utilizado
 */
void led_accion(char timer_id[])
{
	HAL_GPIO_TogglePin(LED_PIN);
	timer_configurar(LED_COUNT, false, timer_id, led_accion);
}

/**
 * @brief Inicializa la secuencia del led.
 *
 */
void leds_inicializar(void)
{
	timer_agregar(LED_COUNT, false, "led", led_accion);
}
