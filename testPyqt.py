from SceneLayer import *
import time
import ThreadManager as th
from Button import *
from SoundManager import *
from omok import *
from Network.NetworkManager import *


class GameController(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setWindowTitle('Omok Game!!')

        self.main_layer = QGridLayout()
        self.setLayout(self.main_layer)

    def mousePressEvent(self, event):
        print(event.x(), event.y())
        dol_x = 55 + ((event.x() - 55)//45)*44
        dol_y = 57 + ((event.y() - 57)//45)*44
        print(dol_x, dol_y)
        self.omokdol = Button('BlackDol.png',(dol_x,dol_y),(42,42),None, self)
        app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Game = GameController()
    Game.show()
    sys.exit(app.exec_())
