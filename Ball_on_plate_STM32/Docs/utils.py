#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 20:27:46 2021

@author: ord

Transforma el angulo de los 3 motores en una trama apta para mandar por USB
"""

from binascii import hexlify

def angulos2protocolo(angulo_a, angulo_b, angulo_c):
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