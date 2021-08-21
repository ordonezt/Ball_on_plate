/**
 * @file utiles.c
 * @brief Funciones utiles miscelaneas.
 * @author Tomás Bautista Ordóñez
 * @date 23/07/2021
 */

#include "main.h"

/**
 * @brief Hace un promedio de datos signados de 16 bits
 *
 * @param datos Vector de datos
 * @param longitud Cantidad de elementos
 * @return
 */
int16_t promedio(int16_t datos[], uint8_t longitud)
{
	int32_t acumulador = 0;

	for(uint8_t i = 0; i < longitud; i++)
		acumulador += datos[i];

	return acumulador / longitud;
}
