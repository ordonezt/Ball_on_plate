/*
 * adxl345.c
 *
 *  Created on: 21 jul. 2021
 *      Author: ord
 */

/**
 * IMPORTANTE No zarparse con la velocidad de SPI, el maximo segun la hoja de datos es 4MHz, pero ya si superas
 * 1,6MHz tenes que empezar a poner delays entre datos de la trama los cuales son un quilombo y no es practico.
 * O sea, no pongas una velocidad mayor de 1,6MHz si no queres sufrir como sufri yo.
 */

#include "main.h"
#include "adxl.h"
#include "utiles.h"
#include <string.h>
#include <math.h>

extern SPI_HandleTypeDef hspi1;

adxl_t adxl;

void adxl_escribir_registro(uint8_t registro, uint8_t valor)
{
	uint8_t datos[2];

	datos[0] = registro & 0x3F;  //Escritura de un solo registro
	datos[1] = valor;

	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_RESET);
	HAL_SPI_Transmit(&hspi1, datos, 2, ADXL_SPI_TIMEOUT);
	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_SET);
}

uint8_t adxl_leer_registro(uint8_t registro)
{
	uint8_t valor = 0;

	registro |= 0x80 & 0xBF;  //Lectura de un solo registro

	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_RESET);
	HAL_SPI_Transmit(&hspi1, &registro, 1, ADXL_SPI_TIMEOUT);
	HAL_SPI_Receive(&hspi1, &valor, 1, ADXL_SPI_TIMEOUT);
	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_SET);

	return valor;
}

void adxl_recibir_trama(void)
{
	uint8_t registro = REG_DATAX0;

	registro |= 0x80 | 0x40; //Lectura de multiples registros
	memset(adxl.buffer_rx, 0, sizeof(adxl.buffer_rx[0]) * 2 * CANTIDAD_EJES);

	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_RESET);
	HAL_SPI_Transmit(&hspi1, &registro, 1, ADXL_SPI_TIMEOUT);
	HAL_SPI_Receive_IT(&hspi1, adxl.buffer_rx, 2 * CANTIDAD_EJES);
//	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_SET);
}

void adxl_alarma_calculo(char timer_id[])
{
	adxl.calculo_pendiente = true;

	timer_configurar(PERIODO_CALCULO_ANGULO, false, timer_id, adxl_alarma_calculo);
}

float cuentas2g(int16_t cuentas)
{
	//Configure el dipositivo en +-2g, entonces tenemos 256LSB/g segun la hoja de datos
	return (float)cuentas / LSB_POR_G;
}

void adxl_inicializar()
{
	uint8_t id;

	//Controlar que el ID este bien
	id = adxl_leer_registro(REG_DEVID);
	if(id != 0345) while(1);

	//Configurar frecuencia de muestreo
	adxl_escribir_registro(REG_BW_RATE, 0b0000 << 4 | FS_100Hz); //Bajo consumo apagado, frecuencia de muestreo 100 Hz

	//Configurar resolucion
	adxl_escribir_registro(REG_DATA_FORMAT, 0); //Resolucion 10 bits, rango +-2g

	//Comenzar la medicion
	adxl_escribir_registro(REG_POWER_CTL, 0x08); //Modos de bajo consumo ignorados, arranco la medicion

	//Configurar interrupciones
	adxl_escribir_registro(REG_INT_ENABLE, 0); //Deshabilito las interrupciones
	adxl_escribir_registro(REG_INT_MAP, 0); //La interrupcion de datos listos se genera en INT1
	adxl_escribir_registro(REG_INT_ENABLE, 0x80); //Habilito la interrupcion por dato listo

	adxl.inicializado = true;

	//Si llego una interrupcion antes la tengo que leer
	if(HAL_GPIO_ReadPin(ADXL_INT) == GPIO_PIN_SET)
		adxl_recibir_trama();

	timer_agregar(PERIODO_CALCULO_ANGULO, false, "ang", adxl_alarma_calculo);

//	//Controlo lo que configure
//	bw_rate = adxl_leer_registro(REG_BW_RATE);
//	data_format = adxl_leer_registro(REG_DATA_FORMAT);
//	power_ctl = adxl_leer_registro(REG_POWER_CTL);
//	int_map = adxl_leer_registro(REG_INT_MAP);
//	int_enable = adxl_leer_registro(REG_INT_ENABLE);
}

void adxl_tarea(void)
{
	if(adxl.calculo_pendiente == true)
	{
		adxl.calculo_pendiente = false;

		for(ejes_t eje = EJE_X; eje <= EJE_Z; eje++)
		{
			adxl.ejes[eje].promedio = promedio(adxl.ejes[eje].buffer, CANTIDAD_PROMEDIOS_ACELERACION);
			adxl.ejes[eje].aceleracion = cuentas2g(adxl.ejes[eje].promedio);
		}

		adxl.pitch 	= (int32_t)(1000 * (180 / M_PI) * atan2f(adxl.ejes[EJE_Y].aceleracion, sqrtf(powf(adxl.ejes[EJE_X].aceleracion, 2) + powf(adxl.ejes[EJE_Z].aceleracion, 2))));
		adxl.roll 	= (int32_t)(1000 * (180 / M_PI) * atan2f(-adxl.ejes[EJE_X].aceleracion, adxl.ejes[EJE_Z].aceleracion));
//		adxl.roll 	= (uint32_t)(1000 * (180 / M_PI) * atan2f(-adxl.ejes[EJE_X].aceleracion, sqrtf(powf(adxl.ejes[EJE_Y].aceleracion, 2) + powf(adxl.ejes[EJE_Z].aceleracion, 2))));

//		adxl.pitch 	= (int32_t)(1000 * (180 / M_PI) * atanf(-adxl.ejes[EJE_X].aceleracion / sqrtf(powf(adxl.ejes[EJE_Y].aceleracion, 2) + powf(adxl.ejes[EJE_Z].aceleracion, 2))));
//		//adxl.roll 	= (int32_t)(1000 * (180 / M_PI) * atan2f(-adxl.ejes[EJE_X].aceleracion, adxl.ejes[EJE_Z].aceleracion));
//		adxl.roll 	= (int32_t)(1000 * (180 / M_PI) * atanf(adxl.ejes[EJE_Y].aceleracion / sqrtf(powf(adxl.ejes[EJE_X].aceleracion, 2) + powf(adxl.ejes[EJE_Z].aceleracion, 2))));
	}
}
///*Aplicacion que lee el acelerometro promedia y calcula los angulos en °*/
//void lectura_acelerometro()
//{
//
//		adxl_read(0x32);
//		x_new=((data_rec[1]<<8)|data_rec[0]);
//		y_new=((data_rec[3]<<8)|data_rec[2]);
//		z_new=((data_rec[5]<<8)|data_rec[4]);
//
//		promedio_angulos();
//
//
//		xg=x*0.0078;
//		yg=y*0.0078;
//		zg=z*0.0078;
//
//		alpha=atan2(xg,zg)*(180/pi);
//		beta=atan2(yg,zg)*(180/pi);
//
//		alpha_entero=truncf(alpha);
//		beta_entero=truncf(beta);
//
//		alpha_decimal=(uint16_t)(100*fabs(alpha)-100*fabs(alpha_entero));
//		beta_decimal=(uint16_t)(100*fabs(beta)-100*fabs(beta_entero));
//
//		itoa(alpha_entero,buff_ae,10);
//		itoa(alpha_decimal,buff_ad,10);
//		itoa(beta_entero,buff_be,10);
//		itoa(beta_decimal,buff_bd,10);
//
//
//		if(beta_decimal<9)
//		{
//		 buff_bd[1]=buff_bd[0];
//		 buff_bd[0]='0';
//		}
//
//		if(alpha_decimal<9)
//		{
//		 buff_ad[1]=buff_ad[0];
//		 buff_ad[0]='0';
//		}
//
//
//
//
//}

void adxl_interrupcion_callback(void)
{
	if(adxl.inicializado == true)
		adxl_recibir_trama();
}

/**
  * @brief  Rx Transfer completed callback.
  * @param  hspi pointer to a SPI_HandleTypeDef structure that contains
  *               the configuration information for SPI module.
  * @retval None
  */
void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi)
{
	ejes_t eje;

	HAL_GPIO_WritePin(ADXL_CS, GPIO_PIN_SET);

	adxl.tramas_recibidas++;

	for(eje = EJE_X; eje < CANTIDAD_EJES; eje++)
	{
		adxl.ejes[eje].buffer[adxl.ejes[eje].indice++] = (adxl.buffer_rx[eje * 2 + 1] << 8) | adxl.buffer_rx[eje * 2];
		adxl.ejes[eje].indice %= CANTIDAD_PROMEDIOS_ACELERACION;
	}
}
