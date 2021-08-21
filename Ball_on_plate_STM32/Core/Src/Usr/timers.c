/**
* @file timers.c
* @brief  Maquinaria de timers por software.
* Timers de 1 ms hasta 49 dias y 17 horas.
*
* @author Tomás Bautista Ordóñez
* @date 01/09/2020
*/

#include "timers.h"

///Buffer de timers
timer_soft_t buffer_timers[TIMER_LEN];

/**
 * Retorna el valor del tick actual
 * @return tick actual.
 */
uint32_t timer_get_tick(void)
{
	return HAL_GetTick();
}

/**
 * Agrega un timer a la lista con la configuracion espeificadada.
 * @param ms Cantidad de ms de timeout.
 * @param pausado true o false.
 * @param id Identificador del timer.
 * @param accion Accion a ejecutar cuando expire el timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_agregar(uint32_t ms, bool pausado, char id[], void (*accion) (char[]))
{
	for(uint8_t i=0; i < TIMER_LEN; i++)
	{
		if(buffer_timers[i].accion == NULL)
		{
			buffer_timers[i].cuenta = ms;
			buffer_timers[i].pausado = pausado;
			strcpy(buffer_timers[i].id, id);
			buffer_timers[i].accion = accion;
			return 0;
		}
	}
	return 1;
}

/**
 * Cambia el estado del timer (pausdo o no).
 * @param pausado true o false.
 * @param id Identificador del timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_cambiar_estado(char id[], bool pausado)
{
	for(uint8_t i=0; i < TIMER_LEN; i++)
	{
		if(strcmp(id, buffer_timers[i].id) == 0)
		{
			buffer_timers[i].pausado = pausado;
			return 0;
		}
	}
	return 1;
}

/**
 * Borra el timer.
 * @param id Identificador del timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_borrar(char id[])
{
	for(uint8_t i=0; i < TIMER_LEN; i++)
	{
		if(strcmp(id, buffer_timers[i].id) == 0)
		{
			memset(buffer_timers + i, 0, sizeof(buffer_timers[i]));
			return 0;
		}
	}
	return 1;
}

/**
 * Borra todos los timers.
 */
void timer_borrar_todos(void)
{
	memset(buffer_timers, 0, sizeof(buffer_timers) * TIMER_LEN);
}

/**
 * Configura y transmite la configuracion del canal y los latiguillos del mismo.
 */
void timer_tarea(void)
{
	static uint32_t tick_anterior = 0;
	
	if(timer_get_tick() - tick_anterior)
	{
		tick_anterior = timer_get_tick();
		//Si transcurrio un tick... recorro toda la lista de timers
		for(uint8_t i=0; i < TIMER_LEN; i++)
		{
			if(buffer_timers[i].pausado == false)
			{
				//Si el timer no esta pausado me fijo si hay que decrementar la cuenta
				if(buffer_timers[i].cuenta != 0)
					buffer_timers[i].cuenta--;
				else
				{
					//Si el timer caduco lo pauso y ejecuto su accion en caso de que sea valida
					buffer_timers[i].pausado = true;
					if(buffer_timers[i].accion != NULL)
						buffer_timers[i].accion(buffer_timers[i].id);
				}
			}
		}
	}
}

/**
 * Configura o agrega un timer.
 * @param ms Cantidad de ms de timeout.
 * @param pausado true o false.
 * @param id Identificador del timer.
 * @param accion Accion a ejecutar cuando expire el timer.
 * @return 1 error, 0 ok.
 */
uint8_t timer_configurar(uint32_t ms, bool pausado, char id[], void (*accion) (char[]))
{
	for(uint8_t i=0; i < TIMER_LEN; i++)
	{
		if(strcmp(id, buffer_timers[i].id) == 0)
		{
			buffer_timers[i].cuenta = ms;
			buffer_timers[i].pausado = pausado;
			buffer_timers[i].accion = accion;
			return 0;
		}
	}
	
	return timer_agregar(ms, pausado, id,accion);
}

/**
 * Checkea si el timer esta o no corriendo.
 * @param id Identificador del timer.
 * @return true esta corriendo, false esta pausado.
 */
bool timer_esta_corriendo(char id[])
{
	for(uint8_t i=0; i < TIMER_LEN; i++)
	{
		if(strcmp(id, buffer_timers[i].id) == 0)
		{
			return !(buffer_timers[i].pausado);
		}
	}
	return false;
}

/**
 * Retorna la cuenta restante del timer.
 * @param id Identificador del timer.
 * @return cuenta restante.
 */
uint32_t timer_get_cuenta(char id[])
{
	for(uint8_t i=0; i < TIMER_LEN; i++)
	{
		if(strcmp(id, buffer_timers[i].id) == 0)
		{
			return buffer_timers[i].cuenta;
		}
	}
	return 0;
}
