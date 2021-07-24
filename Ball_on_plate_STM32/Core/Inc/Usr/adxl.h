/*
 * adxl345.h
 *
 *  Created on: 21 jul. 2021
 *      Author: ord
 */

#ifndef INC_USR_ADXL_H_
#define INC_USR_ADXL_H_

#include "timers.h"
#include <stdbool.h>

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

#define ADXL_SPI_TIMEOUT		2

#define CANTIDAD_PROMEDIOS_ACELERACION 		10
#define CANTIDAD_EJES 						3

#define PERIODO_CALCULO_ANGULO	COUNT_100ms

#define LSB_POR_G				256

typedef struct{
	int16_t buffer[CANTIDAD_PROMEDIOS_ACELERACION];
	int16_t promedio;
	float 	aceleracion;
	int16_t indice;
}adxl_eje_t;

typedef struct{
	bool inicializado;
	bool calculo_pendiente;
	uint8_t buffer_rx[2 * CANTIDAD_EJES];
	adxl_eje_t ejes[CANTIDAD_EJES];
	int32_t roll;
	int32_t pitch;
	uint32_t tramas_recibidas;
}adxl_t;

typedef enum{
	EJE_X,
	EJE_Y,
	EJE_Z
}ejes_t;

typedef enum{
	FS_0_10Hz,
	FS_0_20Hz,
	FS_0_39Hz,
	FS_0_78Hz,
	FS_1_56Hz,
	FS_3_13Hz,
	FS_6_25Hz,
	FS_12_5Hz,
	FS_25Hz,
	FS_50Hz,
	FS_100Hz,
	FS_200Hz,
	FS_400Hz,
	FS_800Hz,
	FS_1600Hz,
	FS_3200Hz
}adxl_frec_muestreo_t;

void adxl_inicializar();
void adxl_interrupcion_callback(void);
void adxl_tarea(void);

#endif /* INC_USR_ADXL_H_ */
