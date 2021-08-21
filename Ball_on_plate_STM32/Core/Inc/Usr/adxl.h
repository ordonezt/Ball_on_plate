/**
 * @file adxl.h
 * @brief En este archivo se encuentran las cabeceras de las funciones de manejo del acelerometro.
 * @author Tomás Bautista Ordóñez
 * @date 21/07/2021
 */

#ifndef INC_USR_ADXL_H_
#define INC_USR_ADXL_H_

#include "timers.h"
#include <stdbool.h>

//Registros del adxl
#define REG_DEVID				0x00
#define REG_THRESH_TAP          0x1D
#define REG_OFSX                0x1E
#define REG_OFSY                0x1F
#define REG_OFSZ                0x20
#define REG_DUR                 0x21
#define REG_Latent              0x22
#define REG_Window              0x23
#define REG_THRESH_ACT          0x24
#define REG_THRESH_INACT        0x25
#define REG_TIME_INACT          0x26
#define REG_ACT_INACT_CTL       0x27
#define REG_THRESH_FF           0x28
#define REG_TIME_FF             0x29
#define REG_TAP_AXES            0x2A
#define REG_ACT_TAP_STATUS      0x2B
#define REG_BW_RATE             0x2C
#define REG_POWER_CTL           0x2D
#define REG_INT_ENABLE          0x2E
#define REG_INT_MAP             0x2F
#define REG_INT_SOURCE          0x30
#define REG_DATA_FORMAT         0x31
#define REG_DATAX0              0x32
#define REG_DATAX1              0x33
#define REG_DATAY0              0x34
#define REG_DATAY1              0x35
#define REG_DATAZ0              0x36
#define REG_DATAZ1              0x37
#define REG_FIFO_CTL            0x38
#define REG_FIFO_STATUS         0x39

///ms de timeout de comunicacion con el acelerometro
#define ADXL_SPI_TIMEOUT		2

///Cantidad de promedios sobre la señal cruda
#define CANTIDAD_PROMEDIOS_ACELERACION 		10
///Cantidad de ejes del acelerometro
#define CANTIDAD_EJES 						3

///Velocidad de calculo y transmision de rotaciones
#define PERIODO_CALCULO_ANGULO	COUNT_100ms

///Escala de aceleraciones
#define LSB_POR_G				256

/**
 * @brief Variable de estado de un eje de aceleracion.
 *
 */
typedef struct{
	int16_t buffer[CANTIDAD_PROMEDIOS_ACELERACION];/**< Buffer de aceleraciones para filtrar */
	int16_t promedio;/**< Promedio del buffer */
	float 	aceleracion;/**< Aceleracion actual */
	int16_t indice;/**< Posicion actual dentro del buffer */
}adxl_eje_t;

/**
 * @brief Variable de estado del acelerometro.
 *
 */
typedef struct{
	bool inicializado;/**< Flag de dispositivo inicializado */
	bool calculo_pendiente;/**< Flag de calculo de rotaciones pendientes */
	uint8_t buffer_rx[2 * CANTIDAD_EJES];/**< Buffer de recepcion de tramas */
	adxl_eje_t ejes[CANTIDAD_EJES];/**< Ejes de aceleracion */
	uint32_t roll;/**< Roll actual */
	uint32_t pitch;/**< Pitch actual */
	uint32_t tramas_recibidas;/**< Cantidad actual de tramas recibidas */
}adxl_t;

/**
 * @brief Nombre de cada eje.
 *
 */
typedef enum{
	EJE_X,/**< EJE_X */
	EJE_Y,/**< EJE_Y */
	EJE_Z /**< EJE_Z */
}ejes_t;

/**
 * @brief Enumeracion de las distintas frecuencias de muestreo permitidas por el acelerometro.
 *
 */
typedef enum{
	FS_0_10Hz,/**< FS_0_10Hz */
	FS_0_20Hz,/**< FS_0_20Hz */
	FS_0_39Hz,/**< FS_0_39Hz */
	FS_0_78Hz,/**< FS_0_78Hz */
	FS_1_56Hz,/**< FS_1_56Hz */
	FS_3_13Hz,/**< FS_3_13Hz */
	FS_6_25Hz,/**< FS_6_25Hz */
	FS_12_5Hz,/**< FS_12_5Hz */
	FS_25Hz,  /**< FS_25Hz */
	FS_50Hz,  /**< FS_50Hz */
	FS_100Hz, /**< FS_100Hz */
	FS_200Hz, /**< FS_200Hz */
	FS_400Hz, /**< FS_400Hz */
	FS_800Hz, /**< FS_800Hz */
	FS_1600Hz,/**< FS_1600Hz */
	FS_3200Hz /**< FS_3200Hz */
}adxl_frec_muestreo_t;

/**
 * @brief Inicializa el acelerometro
 *
 */
void adxl_inicializar();

/**
 * @brief Maneja la interrupcion por dato listo del acelerometro. Dispara una lectura de trama.
 *
 */
void adxl_interrupcion_callback(void);

/**
 * @brief Calcula y envia a la cpu las rotaciones cuando corresponde.
 *
 */
void adxl_tarea(void);

#endif /* INC_USR_ADXL_H_ */
