/*
 * utiles.c
 *
 *  Created on: Jul 23, 2021
 *      Author: ord
 */

#include "main.h"

int16_t promedio(int16_t datos[], uint8_t longitud)
{
	int32_t acumulador = 0;

	for(uint8_t i = 0; i < longitud; i++)
		acumulador += datos[i];

	return acumulador / longitud;
}
