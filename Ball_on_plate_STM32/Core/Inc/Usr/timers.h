/**
* @file timers.h
* @brief  Maquinaria de timers por software.
* Timers de 1 ms hasta 49 dias y 17 horas.
*
* @author Tomás Bautista Ordóñez
* @date 01/09/2020
*/

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef TIMERS_H
#define TIMERS_H

#include "stm32f1xx.h"
#include "stdbool.h"
#include "string.h"

///Cantidad maxima de timers
#define 	TIMER_LEN 		10
///Longitud maxima del id del timer
#define 	TIMER_LEN_ID 	6

//Cuentas en ticks
#define 	COUNT_1ms		1
#define 	COUNT_10ms		10
#define 	COUNT_20ms		20
#define 	COUNT_25ms		25
#define 	COUNT_50ms		50
#define 	COUNT_100ms		100
#define 	COUNT_200ms		200
#define 	COUNT_300ms		300
#define 	COUNT_400ms		400
#define 	COUNT_500ms		500
#define 	COUNT_600ms		600
#define 	COUNT_700ms		700
#define 	COUNT_800ms		800
#define 	COUNT_900ms		900
#define		COUNT_1s		1000
#define 	COUNT_2s		2000
#define 	COUNT_3s		3000
#define 	COUNT_8s		8000

///Convierte segundos en cuentas de timer
#define 	SEC2TIMER_COUNT(x)		((x) * COUNT_1s)
///Convierte cuentas de timer en segundos
#define 	TIMER_COUNT2SEC(x)		(float)(x) / COUNT_1s)


/**
 * @brief Estructura de timer
 *
 */
typedef struct{
	uint32_t cuenta;		/**< Tiempo restante en ticks */
	bool pausado;			/**< Estado de ejecucion */
	char id[TIMER_LEN_ID];	/**< Identificador */
	void (*accion) (char[]);/**< Accion que realiza al completarse */
}timer_soft_t;

/**
 * Retorna el valor del tick actual
 * @return tick actual.
 */
uint32_t timer_get_tick(void);

/**
 * Agrega un timer a la lista con la configuracion espeificadada.
 * @param ms Cantidad de ms de timeout.
 * @param pausado true o false.
 * @param id Identificador del timer.
 * @param accion Accion a ejecutar cuando expire el timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_agregar(uint32_t ms, bool pausado, char id[], void (*accion) (char[]));

/**
 * Cambia el estado del timer (pausdo o no).
 * @param pausado true o false.
 * @param id Identificador del timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_cambiar_estado(char id[], bool pausado);

/**
 * Borra el timer.
 * @param id Identificador del timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_borrar(char id[]);

/**
 * Borra todos los timers.
 */
void timer_borrar_todos(void);

/**
 * Configura y transmite la configuracion del canal y los latiguillos del mismo.
 */
void timer_tarea(void);

/**
 * Configura o agrega un timer.
 * @param ms Cantidad de ms de timeout.
 * @param pausado true o false.
 * @param id Identificador del timer.
 * @param accion Accion a ejecutar cuando expire el timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_configurar(uint32_t ms, bool pausado, char id[], void (*accion) (char[]));

/**
 * Checkea si el timer esta o no corriendo.
 * @param id Identificador del timer.
 * @return true esta corriendo, false esta pausado.
 */
bool timer_esta_corriendo(char id[]);

/**
 * Retorna la cuenta restante del timer.
 * @param id Identificador del timer.
 * @return cuenta restante.
 */
uint32_t timer_get_cuenta(char id[]);

#endif /* TIMERS_H */
