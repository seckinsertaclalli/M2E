# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 01:24:35 2020

@author: Seçkin Sertaç LALLI
"""


from PyQt5 import QtWidgets
from Arayuz import Ui_MainWindow
import sys

class ApplicationWindow():
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        # self.setFixedSize(640, 480)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
def main():
    
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
  
    
if __name__ == '__main__':
  main()