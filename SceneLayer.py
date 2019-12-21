import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SceneLayer(QGridLayout):
    def __init__(self,parent):
        super().__init__()
        self.widgets = []
        self.parent_ = parent

    def add_widget(self, widget):
        # widget을 SceneLayer에서 쓸수있게 등록 해줌
        try:
            if widget is not None:
                self.widgets.append(widget)
        except:
            print('Error : SceneLayer function add_widget')
    def set_active(self, isbool):
        # 해당 Scene 의 모든 위젯들을 isbool 인자 값에따라 끄거나 킴
        try:
            if not isbool:
                for i in self.widgets:
                    i.hide()
            else:
                for i in self.widgets:
                    i.show()
        except:
            pass

''' 
        opacity_effect = QGraphicsOpacityEffect()
        if isbool:
            opacity_effect.setOpacity(1)
        else:
            opacity_effect.setOpacity(0)
        for i in self.widgets:
            i.setGraphicsEffect(opacity_effect)
'''


if "__main__" == __name__:
    '''
    테스트 코드
    '''
    app = QApplication(sys.argv)
    screen = QWidget()
    screen.setGeometry(200, 100, 640, 480)
    screen.setWindowTitle('test SceneLayer Class')
    screen.show()

    main_layout = QVBoxLayout()
    test_scene_layer = SceneLayer()
    test_scene_text = QPushButton('Text Test')
    test_scene_layer.add_widget(test_scene_text)

    test_button_on = QPushButton('on')
    test_button_on.clicked.connect(lambda x: test_scene_layer.set_active(True))
    test_button_off = QPushButton('off')
    test_button_off.clicked.connect(lambda x: test_scene_layer.set_active(False))

    main_layout.addLayout(test_scene_layer)
    main_layout.addWidget(test_button_on)
    main_layout.addWidget(test_button_off)

    screen.setLayout(main_layout)
    sys.exit(app.exec_())
