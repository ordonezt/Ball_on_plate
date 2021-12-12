from serial_com import send_command_to_platform
import numpy as np
import time
import settings
import controller
import GUI
import threading
import cv2
import numpy as np
from pyzbar.pyzbar import decode

import estimador_posicion



def main():
    settings.init()   
    GUI.start_GUI()



if __name__ == '__main__':
    main()
