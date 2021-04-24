/*
 * cpu.h
 *
 *  Created on: Apr 16, 2021
 *      Author: ord
 */

#include "stm32f1xx.h"

void cpu_transmitir_basico(void);

uint8_t cpu_recibir(uint8_t mensaje[], uint32_t longitud);

void cpu_rx(void);

void cpu_inicializar(void);
