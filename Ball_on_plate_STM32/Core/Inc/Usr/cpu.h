/*
 * cpu.h
 *
 *  Created on: Apr 16, 2021
 *      Author: ord
 */

#include "stm32f1xx.h"

void cpu_transmitir_basico(char timer_id[]);
void cpu_transmitir(uint8_t mensaje[], uint32_t longitud);

uint8_t cpu_recibir(uint8_t mensaje[], uint32_t longitud);

/**
 * Procesa los datos recibidos de la CPU
 */
void cpu_rx(void);

void cpu_inicializar(void);
