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
#include "timers.h"
#include "servos.h"

#define LONGITUD_TRAMA_RX		12
#define LONGITUD_BUFFER_RX 		64		//Tiene que ser potencia de dos si o si, entran 5 tramas y pico

#define INICIO_TRAMA_CPU		0x80
#define FIN_TRAMA_CPU			0x90

#define BYTE_MAB0 				0
#define BYTE_MAB1				(BYTE_MAB0 + 1)
#define BYTE_MAB2				(BYTE_MAB1 + 1)

#define BYTE_MBB0 				(BYTE_MAB2 + 1)
#define BYTE_MBB1				(BYTE_MBB0 + 1)
#define BYTE_MBB2				(BYTE_MBB1 + 1)

#define BYTE_MCB0 				(BYTE_MBB2 + 1)
#define BYTE_MCB1				(BYTE_MCB0 + 1)
#define BYTE_MCB2				(BYTE_MCB1 + 1)

#define BYTE_MSB				(BYTE_MCB2 + 1)


//typedef struct{
//	union{
//		uint8_t cruda[LONGITUD_TRAMA_RX];
//	};
//}cpu_trama_rx_t;

RINGBUFF_T cpu_rx_ring_buffer;
uint8_t cpu_rx_buffer[LONGITUD_BUFFER_RX];

uint8_t *buffer_tx = "Hola Mundo!\n";

void cpu_transmitir_basico(char timer_id[])
{
	CDC_Transmit_FS(buffer_tx, strlen(buffer_tx));
	timer_configurar(1000, 0, timer_id, cpu_transmitir_basico);
}

void cpu_transmitir(uint8_t mensaje[], uint32_t longitud)
{
	CDC_Transmit_FS(mensaje, longitud);
}

void cpu_inicializar(void)
{
	RingBuffer_Init(&cpu_rx_ring_buffer, cpu_rx_buffer, sizeof(cpu_rx_buffer[0]),  LONGITUD_BUFFER_RX);
	//cpu_transmitir_basico("hw");
}

uint8_t cpu_recibir(uint8_t mensaje[], uint32_t longitud)
{
	cpu_transmitir(mensaje, longitud);
	return RingBuffer_InsertMult(&cpu_rx_ring_buffer, mensaje, longitud) == longitud;
}

/**
 * Transforma una trama de comunicacion en angulos para los motores
 * @param mensaje Trama recibida
 * @param angulo_a Puntero donde almacenar la posicion del motor A
 * @param angulo_b Puntero donde almacenar la posicion del motor B
 * @param angulo_c Puntero donde almacenar la posicion del motor C
 * @return 0 ok, 1 error
 */
uint8_t trama2angulos(uint8_t mensaje[], uint32_t* angulo_a, uint32_t* angulo_b, uint32_t* angulo_c)
{
	*angulo_a = 		(mensaje[BYTE_MAB2] << (2 * 8)) |
				((((mensaje[BYTE_MSB] & 0x02) << 6) | mensaje[BYTE_MAB1]) << (1 * 8)) |
				((((mensaje[BYTE_MSB] & 0x01) << 7) | mensaje[BYTE_MAB0]) << (0 * 8));

	*angulo_b = 		(mensaje[BYTE_MBB2] << (2 * 8)) |
				((((mensaje[BYTE_MSB] & 0x08) << 4) | mensaje[BYTE_MBB1]) << (1 * 8)) |
				((((mensaje[BYTE_MSB] & 0x04) << 5) | mensaje[BYTE_MBB0]) << (0 * 8));

	*angulo_c = 		(mensaje[BYTE_MCB2] << (2 * 8)) |
				((((mensaje[BYTE_MSB] & 0x20) << 2) | mensaje[BYTE_MCB1]) << (1 * 8)) |
				((((mensaje[BYTE_MSB] & 0x10) << 3) | mensaje[BYTE_MCB0]) << (0 * 8));
	return 0;
}

/**
 * Procesa los datos recibidos de la CPU
 */
void cpu_rx(void)
{
	uint8_t dato;
	static uint8_t indice, mensaje[LONGITUD_TRAMA_RX], estado=0;
	uint32_t num;
	uint32_t angulo_a, angulo_b, angulo_c;

	if(RingBuffer_Pop(&cpu_rx_ring_buffer, &dato))
	{
		switch(estado)
		{
		case 0:
			if(dato == INICIO_TRAMA_CPU)
			{
				estado = 1;
				indice = 0;
				memset(mensaje, '\0', sizeof(mensaje[0]) * LONGITUD_TRAMA_RX);
			}
			break;
		case 1:

			if(dato == FIN_TRAMA_CPU)
			{
				//Validar mensaje
				if(trama2angulos(mensaje, &angulo_a, &angulo_b, &angulo_c) == 0)
				{
					servos_agregar_angulo(SERVO_A, angulo_a);
					servos_agregar_angulo(SERVO_B, angulo_b);
					servos_agregar_angulo(SERVO_C, angulo_c);
				}

				estado = 0;
			}
			else if((dato & 0x80) == 0)
			{
				mensaje[indice++] = dato;
			}
			else
				estado = 0;

			if(indice >= (LONGITUD_TRAMA_RX - 1))
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

