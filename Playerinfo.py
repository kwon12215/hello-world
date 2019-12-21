from SceneLayer import *
from Button import *

#omok

class PlayerInfo:
    def __init__(self, mainLayer, controllerInit, set_network_nickname):
        self.player_name = ""
        self.game_count = int(0)
        self.game_win_count = int(0)
        self.filename = 'playerinfo.txt'

        self.mainLayer = mainLayer
        self.init = controllerInit
        self.set_network_nickname = set_network_nickname

    def name_layer_create(self, main_menu_scene):
        self.NameEditScene = SceneLayer(self.mainLayer)
        self.NickNameImage = QLabel(self.mainLayer)
        self.NickNameImage.resize(1280, 720)
        pixmap = QPixmap('Images/InGameBackground.jpg')
        self.NickNameImage.setPixmap(pixmap)

        self.NickNameImage_Black = QLabel(self.mainLayer)
        self.NickNameImage_Black.resize(1280, 720)
        pixmap = QPixmap('Images/NickNameBackground.jpg')
        self.NickNameImage_Black.setPixmap(pixmap)

        self.MyTextNickName = QLabel(self.mainLayer)
        self.MyTextNickName.setGeometry(140, 310, 500, 200)
        self.MyTextNickName.setStyleSheet('Color:white')
        self.MyTextNickName.setText('닉네임을 입력하세요 : ')
        self.MyTextNickName.setAlignment(Qt.AlignRight)
        font = QFont()
        font.setPointSize(25)
        font.setWeight(200)
        self.MyTextNickName.setFont(font)

        self.nameEdit = QLineEdit(self.mainLayer)
        self.nameEdit.setGeometry(650, 310, 200, 50)
        font = QFont()
        font.setPointSize(20)
        font.setWeight(200)
        self.nameEdit.setFont(font)

        self.NickNameCreateButton = Button('NickNameCreate.png',(860,285),(100,100),self.name_button_clicked,self.mainLayer)

        self.NameEditScene.add_widget(self.NickNameImage)
        self.NameEditScene.add_widget(self.MyTextNickName)
        self.NameEditScene.add_widget(self.nameEdit)
        self.NameEditScene.add_widget(self.NickNameCreateButton)
        self.NameEditScene.set_active(False)
        self.main_menu_scene = main_menu_scene

    def game_end(self, isWin):
        if isWin:
            self.game_win_count += 1
            self.game_count += 1
        else:
            self.game_count += 1

        self.player_info_save()

    def player_info_save(self):
        f = open(self.filename, 'w')
        data = '{}:{}:{}'.format(self.player_name,self.game_count,self.game_win_count)
        f.write(data)
        f.close()

    def name_button_clicked(self):
        self.player_name = self.nameEdit.text()
        print(self.player_name)
        self.player_info_save()
        self.NameEditScene.set_active(False)
        for i in self.NameEditScene.widgets:
            del i

        del self.NameEditScene

        self.main_menu_scene.set_active(True)
        self.set_network_nickname()

    def valid_name_check(self):
        try:
            with open(self.filename, 'r') as f:
                data = f.readline()
                data = data.split(':')

                self.player_name = data[0]
                self.game_count = int(data[1])
                self.game_win_count = int(data[2])
                print(self.game_count)
                print(self.player_name)
                return True

        except FileNotFoundError:
            return False
