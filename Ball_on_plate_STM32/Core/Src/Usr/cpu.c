/*
 * cpu.c
 *
 *  Created on: Apr 16, 2021
 *      Author: ord
 */


#include "cpu.h"
#include "string.h"	//ToDo: Borrar?
#include "usbd_cdc_if.h"

uint8_t *buffer_tx = "Hola Mundo!\n";

void cpu_transmitir_basico(void)
{
	CDC_Transmit_FS(buffer_tx, strlen(buffer_tx));
}
