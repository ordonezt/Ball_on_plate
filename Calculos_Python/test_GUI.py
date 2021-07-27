import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from Ui_MainWindow import Ui_MainWindow

import settings
import time


def show_params():
    while (True):
        time.sleep(1)
        print(f'Kp={settings.Kp}\n')
        print(f'Ki={settings.Ki}\n')
        print(f'Kd={settings.Kd}\n')

class MainWindow:
    def __init__(self):
        self.main_win=QMainWindow()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.init_slider(self.ui.Kp_slider,self.ui.Kp_value)
        self.init_slider(self.ui.Ki_slider,self.ui.Ki_value)
        self.init_slider(self.ui.Kd_slider,self.ui.Kd_value)
        

    def update_slider_label(self,slider,label):
        new_value=slider.value()
        label.setText(str(new_value))

        if (slider==self.ui.Kp_slider):
            settings.Kp=new_value
        if (slider==self.ui.Ki_slider):
            settings.Ki=new_value
        if (slider==self.ui.Kd_slider):
            settings.Kd=new_value

    def show(self):
        self.main_win.show()

    def init_slider(self,slider,label):
        slider.valueChanged.connect(lambda:self.update_slider_label(slider,label) )


def run_gui():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    app.exec_()
    return



