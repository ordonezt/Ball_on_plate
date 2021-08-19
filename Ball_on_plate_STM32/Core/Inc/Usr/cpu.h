/**
 * @file cpu.c
 * @brief En este archivo se encuentran las cabeceras de las funciones de manejo de la comunicacion con la CPU.
 * @author Tomás Bautista Ordóñez
 * @date 16/04/2021
 */

#include "stm32f1xx.h"

/**
 * @brief Transmite periodicamente un mensaje basico a la CPU
 *
 * @param timer_id Identificador del timer relacionado
 */
void cpu_transmitir_basico(char timer_id[]);

/**
 * @brief Transmite una trama a la CPU
 *
 * @param mensaje Trama a enviar
 * @param longitud Cantidad de caracteres del mensaje
 */
void cpu_transmitir(uint8_t mensaje[], uint32_t longitud);

/**
 * @brief Recibe una trama de comunicacion.
 * Recibe una trama de comunicacion de la CPU y la inserta en una cola para ser procesada
 *
 * @param mensaje trama recibida
 * @param longitud cantidad de caracteres
 * @return
 */
uint8_t cpu_recibir(uint8_t mensaje[], uint32_t longitud);

/**
 * Procesa los datos recibidos de la CPU
 */
void cpu_rx(void);

/**
 * @brief Inicializa la interfaz de comunicacion con la CPU
 *
 */
void cpu_inicializar(void);
