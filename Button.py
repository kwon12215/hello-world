from PyQt5.QtWidgets import *

#omok button.py
class Button(QPushButton):
    ''' PyQt QToolButton
        Custom Button Class hyunseo jjangjjang'''
    def __init__(self, image,pos,size, callback=None,parent=None):
        super().__init__(parent)
        self.resize(size[0], size[1])
        self.move(pos[0],pos[1])
        img_url = 'background-image:url(Images/{});border:0px;'.format(image)
        self.setStyleSheet(img_url)
        if callback is not None:
            self.clicked.connect(callback)

