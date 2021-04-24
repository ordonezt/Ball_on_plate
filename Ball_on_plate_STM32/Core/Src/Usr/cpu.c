/*
 * cpu.c
 *
 *  Created on: Apr 16, 2021
 *      Author: ord
 */


#include "cpu.h"
#include "string.h"	//ToDo: Borrar?
#include "usbd_cdc_if.h"
#include "my_ring_buffer.h"

//ToDo: Borrar
#include "servos.h"
extern servo_t servo_A;
void servos_set_ancho_de_pulso(servo_t servo, uint32_t cuentas);

#define LONGITUD_TRAMA_RX		8
#define LONGITUD_BUFFER_RX 		16		//Tiene que ser potencia de dos si o si

//typedef struct{
//	union{
//		uint8_t cruda[LONGITUD_TRAMA_RX];
//	};
//}cpu_trama_rx_t;

RINGBUFF_T cpu_rx_ring_buffer;
uint8_t cpu_rx_buffer[LONGITUD_BUFFER_RX];

uint8_t *buffer_tx = "Hola Mundo!\n";

void cpu_transmitir_basico(void)
{
	CDC_Transmit_FS(buffer_tx, strlen(buffer_tx));
}

void cpu_transmitir(uint8_t mensaje[], uint32_t longitud)
{
	CDC_Transmit_FS(mensaje, longitud);
}

void cpu_inicializar(void)
{
	RingBuffer_Init(&cpu_rx_ring_buffer, cpu_rx_buffer, sizeof(cpu_rx_buffer[0]),  LONGITUD_BUFFER_RX);
}

uint8_t cpu_recibir(uint8_t mensaje[], uint32_t longitud)
{
	cpu_transmitir(mensaje, longitud);
	return RingBuffer_InsertMult(&cpu_rx_ring_buffer, mensaje, longitud) == longitud;
}

void cpu_rx(void)
{
	uint8_t dato;
	static uint8_t indice, mensaje[LONGITUD_TRAMA_RX], estado=0;
	uint32_t num;

	if(RingBuffer_Pop(&cpu_rx_ring_buffer, &dato))
	{
		switch(estado)
		{
		case 0:
			if(dato == '<')
			{
				estado = 1;
				indice = 0;
				memset(mensaje, '\0', sizeof(mensaje[0]) * LONGITUD_TRAMA_RX);
			}
			break;
		case 1:

			if(dato >= '0' && dato <= '9')
				mensaje[indice++] = dato;
			else if(dato == '>')
			{
				//Validar mensaje
				num = atoi(mensaje);
				servos_set_ancho_de_pulso(servo_A, num);

				estado = 0;
			}
			else
				estado = 0;

			if(indice >= LONGITUD_TRAMA_RX)
				estado = 0;
			break;
		default:
			estado = 0;
			break;
		}
	}
}

void cpu_tx_rx(void)
{
	cpu_rx();
}
