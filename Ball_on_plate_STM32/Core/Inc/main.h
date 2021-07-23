/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define LED_ESTADO_Pin GPIO_PIN_13
#define LED_ESTADO_GPIO_Port GPIOC
#define SERVO_A_Pin GPIO_PIN_0
#define SERVO_A_GPIO_Port GPIOA
#define SERVO_B_Pin GPIO_PIN_1
#define SERVO_B_GPIO_Port GPIOA
#define SERVO_C_Pin GPIO_PIN_2
#define SERVO_C_GPIO_Port GPIOA
#define SERVO_D_Pin GPIO_PIN_3
#define SERVO_D_GPIO_Port GPIOA
#define ADXL_SCK_Pin GPIO_PIN_5
#define ADXL_SCK_GPIO_Port GPIOA
#define ADXL_MISO_Pin GPIO_PIN_6
#define ADXL_MISO_GPIO_Port GPIOA
#define ADXL_MOSI_Pin GPIO_PIN_7
#define ADXL_MOSI_GPIO_Port GPIOA
#define ADXL_CS_Pin GPIO_PIN_0
#define ADXL_CS_GPIO_Port GPIOB
#define ADXL_INT_Pin GPIO_PIN_1
#define ADXL_INT_GPIO_Port GPIOB
#define ADXL_INT_EXTI_IRQn EXTI1_IRQn
/* USER CODE BEGIN Private defines */
#define LED_PIN 	LED_ESTADO_GPIO_Port, LED_ESTADO_Pin
#define ADXL_CS 	ADXL_CS_GPIO_Port, ADXL_CS_Pin
#define ADXL_INT 	ADXL_INT_GPIO_Port, ADXL_INT_Pin
/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
