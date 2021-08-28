#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 20:27:46 2021

@author: ord

Funciones utiles.
"""

from binascii import hexlify

def angulos2protocolo(angulo_a, angulo_b, angulo_c):
    """
    Transforma el angulo de los 3 motores en una trama apta para mandar por USB.
    Parametros
    ----------
    angulo_a
        Angulo motor A.
    angulo_b
        Angulo motor B.
    angulo_c
        Angulo motor C.
    Retorno
    ----------
    Trama lista para transmitir.
    """

    trama = []
    trama.append(0x80)
    
    byte0_a = angulo_a            & 0x00_00_00_FF
    byte1_a = (angulo_a >> 8)     & 0x00_00_00_FF
    byte2_a = (angulo_a >> (8*2)) & 0x00_00_00_FF
    
    byte0_b = angulo_b            & 0x00_00_00_FF
    byte1_b = (angulo_b >> 8)     & 0x00_00_00_FF
    byte2_b = (angulo_b >> (8*2)) & 0x00_00_00_FF
    
    byte0_c = angulo_c            & 0x00_00_00_FF
    byte1_c = (angulo_c >> 8)     & 0x00_00_00_FF
    byte2_c = (angulo_c >> (8*2)) & 0x00_00_00_FF
    
    MSB =   ((byte1_c & 0x80) >> (7 - 5)) | \
            ((byte0_c & 0x80) >> (7 - 4)) | \
            ((byte1_b & 0x80) >> (7 - 3)) | \
            ((byte0_b & 0x80) >> (7 - 2)) | \
            ((byte1_a & 0x80) >> (7 - 1)) | \
            ((byte0_a & 0x80) >> (7 - 0))
    
    trama.append(ord('A'))

    trama.append(byte0_a & 0x7F)
    trama.append(byte1_a & 0x7F)
    trama.append(byte2_a & 0x7F)
    
    trama.append(byte0_b & 0x7F)
    trama.append(byte1_b & 0x7F)
    trama.append(byte2_b & 0x7F)
    
    trama.append(byte0_c & 0x7F)
    trama.append(byte1_c & 0x7F)
    trama.append(byte2_c & 0x7F)
    
    trama.append(MSB)
    
    trama.append(0x90)
    
    print(hexlify(bytearray(trama)))
    
    return trama

def protocolo2inclinaciones(trama):
    """
    Transforma la trama recibida en inclinaciones.
    Para pedir las inclinaciones hay que enviar el comando [0x80, 0x41('A'), 0x90].
    
    Parametros
    ----------
    trama
        Cadena que contiene el mensaje recibido.
    Retorno
    ----------
    Inclinacion roll, pitch.
    """
    roll = pitch = -1

    if len(trama) != 10 or trama[0] != 0x80 or trama[1] != 0x41 or trama[9] != 0x90:
        print("Error")
    else:
        roll =                             (trama[4]  << 16) | \
                ((((trama[8] & 0x2) << 6) | trama[3]) << 8) | \
                ((((trama[8] & 0x1) << 7) | trama[2]) << 0)
        
        pitch =                            (trama[7]  << 16) | \
                ((((trama[8] & 0x8) << 4) | trama[6]) << 8) | \
                ((((trama[8] & 0x4) << 5) | trama[5]) << 0)

    return roll, pitch