from SceneLayer import *
import time
import ThreadManager as th
from Button import *
from SoundManager import *
from omok import *
from Network.NetworkManager import *
import PlayerInfo
import AImanager as oai


class GameController(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setWindowTitle('Omok Game!!')
        self.main_layer = QGridLayout()
        self.setLayout(self.main_layer)
        self.isMouseEvent = False
        self.isSingle = False
        self.isGameEnd = False
        self.playerinfomanager = PlayerInfo.PlayerInfo(self,self.InitGameController,self.set_network_nickname)

        self.MainMenuScene = SceneLayer(self)
        self.playerinfomanager.name_layer_create(self.MainMenuScene)
        self.InitGameController()

    def GameExit(self):
        QApplication.closeAllWindows()

    def InitGameController(self):
        self.omokmanager = Omok()
        self.soundmanager = SoundManager()
        self.NetworkSetting()

        self.LogoSceneCreate()
        self.MainSceneCreate()
        self.MatchingSceneCreate()

        self.InGameSceneCreate()

        self.ThreadManager = th.ThreadManager(self)
        self.ThreadManager.add_animation(self.logo_play)

        self.my_turn = True
        self.my_dol = 0
        self.omokdol = []

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.run)
        self.timer.start()

        self.select_x = -1
        self.select_y = -1

    def run(self):
        if self.networkmanager.q.qsize() > 0:
            temp = self.networkmanager.q.get()
            temp[0](int(temp[1]),int(temp[2]))

    def set_network_nickname(self):
        self.networkmanager.set_nickname(self.playerinfomanager.player_name)

    def SelectImageMove(self, x,y):
        self.SelectImage.move(34+x*43.4,36+y*43.2)

        self.select_x = x
        self.select_y = y

    def mousePressEvent(self, event):

        if not self.isMouseEvent:
            return

        x = (event.x() - 34) // 43
        y = (event.y() - 36) // 43
        if x >= 15 or y >= 15:
            return

        self.SelectImageMove(x,y)

    def Single_SetSton(self):
        if self.my_turn and not self.isSingle:
            print(self.my_turn)
            self.SetSton(self.select_x, self.select_y, self.my_dol)
            self.networkmanager.send_ston(str(self.select_x), str(self.select_y))
        if self.my_turn and self.isSingle:
            print(self.my_turn)
            self.SetSton(self.select_x, self.select_y, self.my_dol)

            print('ㄴㄹㄷ2 {}'.format(
                self.omokmanager.omok_board
            ))
            ai_dol = '11'
            if self.my_dol == '1':
                ai_dol = '2'
            elif self.my_dol == '2':
                ai_dol = '1'

            ai_xy = oai.ai_play(self.omokmanager.omok_board.copy(), int(ai_dol))

            self.omokmanager.omok_board[ai_xy[0]][ai_xy[1]] = 0

            print('!!컴퓨터는 {} , {} 에둔다 {}'.format(ai_xy[0],ai_xy[1],ai_dol))
            self.SetSton(ai_xy[0], ai_xy[1], ai_dol)

    def NetworkSetting(self):
        qsrand(int(time.time()))
        nickname = 'imsi' + str(qrand()%100000)

        self.networkmanager = NetworkManager(nickname)
        self.networkmanager.add_msg_function('SETSTON', self.SetSton)
        self.networkmanager.add_msg_function('GAMESTART', self.SetMultiStart)
        print('네트워크')

    def SetLastDolImage(self,x,y):
        self.InGameScene.widgets.remove(self.LastDolImage)
        self.LastDolImage.deleteLater()


        self.LastDolImage = QLabel(self)
        self.LastDolImage.setGeometry(34+x*43.4,36+y*43.2, 42, 42)
        pixmap = QPixmap('Images/LastDol.png')
        self.LastDolImage.setPixmap(pixmap)

        self.InGameScene.add_widget(self.LastDolImage)
        self.LastDolImage.show()

    def SetSton(self, posX, posY, dol=-1):
        if self.isGameEnd:
            return

        print(posX, ',', posY)
        for i in self.omokdol:
            i.show()
        dol_image = ''
        if dol == '1':
            dol_image = 'BlackDol.png'
        elif dol == '2':
            dol_image = 'WhiteDol.png'
        elif dol == -1:
            print('join')
            if self.my_dol == '1':
                dol_image = 'WhiteDol.png'
                dol = '2'
            else:
                dol_image = 'BlackDol.png'
                dol = '1'

        check_in_dol = self.omokmanager.xy_check_board(posX, posY)
        print(check_in_dol)
        if check_in_dol:
            return
        self.soundmanager.SetStonSound()
        self.my_turn = not self.my_turn
        self.TurnChangeImage()
        self.omokmanager.set_omokdol(posX,posY,int(dol))
        omokdol = Button(dol_image, (34+posX*43.4,36 + posY*43.2), (42, 42), None, self)
        omokdol.show()
        self.SetLastDolImage(posX,posY)
        print(omokdol)
        self.omokdol.append(omokdol)

        print(self.omokdol[-1].pos())
        print(self.omokdol[-1].size())
        self.samsam_check()
        winlose_check = self.omokmanager.check_board(self.omokmanager.omok_board)
        self.win_lose_check(winlose_check)

    def samsam_check(self):
        board = self.omokmanager.omok_board

        if board[7][7] != 0 or board[8][7] == 0 or board[9][7] == 0 or board[7][8] == 0 or board[7][9] == 0:
            self.SamSamImage.move(1000,1000)
            return

        posX = 7
        posY = 7
        self.SamSamImage.move(34+posX*43.4,36 + posY*43.2)

    def win_lose_check(self, check_num):
        print('start' , self.isGameEnd)
        print('음악에 심취한다....')
        if check_num != 0 and not self.isGameEnd:
            print(self.isGameEnd)
            self.isGameEnd = True
            print(self.isGameEnd)
            self.WinLoseSceneCreate()
            if check_num == int(self.my_dol):
                self.YouWinLose.setText('You Win!!')
                self.ThreadManager.add_animation(self.soundmanager.WinSound)
                self.playerinfomanager.game_end(True)

            else:
                self.YouWinLose.setText('You Lose...')
                self.ThreadManager.add_animation(self.soundmanager.LoseSound)
                self.playerinfomanager.game_end(False)
            self.ThreadManager.add_animation(self.WinLose_play)

    def TurnChangeImage(self):
        if self.my_turn:
            self.TurnBlackImage.move(720, 195)
        else:
            self.TurnBlackImage.move(720,35)

    def MainSceneCreate(self):
        self.GameStartButton = Button('GameStartButton.png',(274,480-62),(172,62),self.SetSingleStart,self)
        self.main_layer.addLayout(self.MainMenuScene,0,0)


        self.lbl1 = QLabel(self)
        self.lbl1.resize(1280, 720)
        pixmap1 = QPixmap("Images/panja1.jpg")
        self.lbl1.setPixmap(QPixmap(pixmap1))

        self.lbl2 = QLabel(self)
        self.lbl2.move(335, 0)
        self.lbl2.resize(720, 360)
        pixmap2 = QPixmap("Images/eggss.png")
        self.lbl2.setPixmap(QPixmap(pixmap2))

        self.lbl3 = Button("MultiButton.png",(470,360),(350,80),self.GameStartButtonClicked,self)
        self.lbl4 = Button('SingleButton.png',(470,470),(350,80),self.SetSingleStart,self)
        self.lbl5 = Button('ExitButton.png',(500,600),(297,87),self.GameExit,self)

        self.MainMyIcon = QLabel(self)
        self.MainMyIcon.setGeometry(55, 40, 150, 150)
        pixmap = QPixmap('Images/Circle.png')
        self.MainMyIcon.setPixmap(pixmap)

        self.MainMyTextNickName = QLabel(self)
        self.MainMyTextNickName.setGeometry(215, 15, 200, 200)
        self.MainMyTextNickName.setText('hyunseo\n0전 0승 0패')
        font = QFont("Arial")
        font.setPointSize(25)
        font.setWeight(200)
        self.MainMyTextNickName.setFont(font)

        self.MainMenuScene.add_widget(self.lbl1)
        self.MainMenuScene.add_widget(self.lbl2)
        self.MainMenuScene.add_widget(self.lbl3)
        self.MainMenuScene.add_widget(self.lbl4)
        self.MainMenuScene.add_widget(self.lbl5)
        self.MainMenuScene.add_widget(self.GameStartButton)
        self.MainMenuScene.add_widget(self.MainMyIcon)
        self.MainMenuScene.add_widget(self.MainMyTextNickName)
        self.MainMenuScene.set_active(False)

    def SetSingleStart(self):
        self.isSingle = True
        self.isMouseEvent = True
        self.InfoTextUpdate("Computer", "0", '0')
        print('플레이어 정보 바꾸는거 끝남')
        self.InGameScene.set_active(True)
        qsrand((time.time()))#int권장
        turn = str(int(qrand()%2+1))
        self.my_dol = turn
        print(turn)
        if turn == '1':
            print('너는 흑돌')
            self.my_turn = True
        elif turn == '2':
            print('너는 흰돌')
            self.my_turn = False
        self.SetMyYouDolImage(turn)
        self.TurnChangeImage()
        self.InGameScene.set_active(True)
        if turn == '2':
            print('너는 흰돌')
            self.SetSton(7, 7, '1')

    def SetMultiStart(self, turn,you_name,you_count,you_win_count):
        self.matching_timer.stop()
        self.MatchingScene.set_active(False)
        self.isMouseEvent = True
        self.InfoTextUpdate(you_name, you_count, you_win_count)
        print('플레이어 정보 바꾸는거 끝남')
        self.InGameScene.set_active(True)
        self.my_dol = turn
        print(turn)
        if turn == '1':
            print('너는 흑돌')
            self.my_turn = True
        elif turn == '2':
            print('너는 흰돌')
            self.my_turn = False

        self.SetMyYouDolImage(turn)
        self.TurnChangeImage()

    def MatchingSceneCreate(self):
        self.MatchingScene = SceneLayer(self)

        self.MatchingImage = QLabel(self)
        self.MatchingImage.resize(1280, 720)
        pixmap = QPixmap('Images/matching1.png')
        self.MatchingImage.setPixmap(pixmap)

        self.MatchingScene.add_widget(self.MatchingImage)
        self.MatchingScene.set_active(False)

        self.MatchingImage_time = 0
        self.matching_timer = QTimer()
        self.matching_timer.setInterval(300)
        self.matching_timer.timeout.connect(self.MatchingAnimation)

    def MatchingAnimation(self):
        time = self.MatchingImage_time
        self.MatchingImage_time += 1
        pixmap = QPixmap('Images/matching2.png')
        if  time  == 1:
            pixmap = QPixmap('Images/matching2.png')
        elif time == 2:
            pixmap = QPixmap('Images/matching3.png')
        elif time == 3:
            pixmap = QPixmap('Images/matching4.png')
        elif time == 4:
            pixmap = QPixmap('Images/matching5.png')
        elif time == 5:
            pixmap = QPixmap('Images/matching1.png')
            self.MatchingImage_time = 0

        self.MatchingImage.setPixmap(pixmap)

    def GameStartButtonClicked(self):
        print('게임스타트 버튼 클릭')
        self.MainMenuScene.set_active(False)
        self.ThreadManager.add_animation(self.soundmanager.ButtonClickSound)
        self.MatchingScene.set_active(True)
        self.matching_timer.start()
        # 멀티 ㄱㄱ
        print('게임스타트 보냈는데')
        self.networkmanager.GameStart(self.playerinfomanager.game_count,
                                      self.playerinfomanager.game_win_count)
        pass

    def LogoSceneCreate(self):
        self.LogoScene = SceneLayer(self)
        self.LogoImageLabel = QLabel(self)
        self.LogoImageLabel.resize(1280,720)
        pixmap = QPixmap('Images/logo_image.png')
        self.LogoImageLabel.setPixmap(pixmap)

        self.LogoScene.add_widget(self.LogoImageLabel)
        self.main_layer.addLayout(self.LogoScene,0,0)

    def gameInit(self):
        self.omokmanager.clear_board()
        for i in self.omokdol:
            print('지움')
            i.hide()
            del i

        self.omokdol = []
        self.isGameEnd = False
        self.WinLoseScene.set_active(False)
        del self.WinLoseScene
        self.SamSamImage.move(1000,1000)
        self.LastDolImage.setGeometry(1000,1000,42,42)
        self.InGameScene.set_active(False)
        self.MainMenuScene.set_active(True)

    def WinLose_play(self):
        time.sleep(1)
        print('이겼다 졌다 앺냐')
        self.WinLoseScene.set_active(True)
        size = 50
        font = QFont("Arial")
        font.setWeight(200)
        for i in range(20):
            time.sleep(0.005)
            size += 1
            font.setPointSize(size)
            self.YouWinLose.setFont(font)
        for i in range(20):
            time.sleep(0.005)
            size -= 1
            font.setPointSize(size)
            self.YouWinLose.setFont(font)

        time.sleep(2)
        self.gameInit()

    def logo_play(self):
        self.LogoScene.set_active(True)
        time.sleep(1)
        opacity = 1
        for i in range(100):
            time.sleep(0.01)
            opacity -= 0.01
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(opacity)
            self.LogoImageLabel.setGraphicsEffect(opacity_effect)

        if not self.playerinfomanager.valid_name_check():
            self.playerinfomanager.NameEditScene.set_active(True)
        else:
            self.MainMenuScene.set_active(True)

        self.LogoScene.set_active(False)

    def WinLoseSceneCreate(self):
        self.WinLoseScene = SceneLayer(self)

        self.WinLoseBackground = QLabel(self)
        self.WinLoseBackground.resize(1280, 400)
        self.WinLoseBackground.move(0, 160)
        pixmap = QPixmap('Images/WinLoseBackground.png')
        self.WinLoseBackground.setPixmap(pixmap)


        self.YouWinLose = QLabel(self)
        self.YouWinLose.setGeometry(0, 0, 1280, 720)
        self.YouWinLose.setText('You Win')
        self.YouWinLose.setStyleSheet('Color:white')
        self.YouWinLose.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(50)
        font.setWeight(200)
        self.YouWinLose.setFont(font)

        self.WinLoseScene.add_widget(self.YouWinLose)
        self.WinLoseScene.add_widget(self.WinLoseBackground)
        self.WinLoseScene.set_active(False)

    def InfoTextUpdate(self, you_name=0, you_count=0, you_win_count=0):
        mytext = '{}\n{}전 {}승 {}패'.format(
            self.playerinfomanager.player_name,
            self.playerinfomanager.game_count,
            self.playerinfomanager.game_win_count,
            int(self.playerinfomanager.game_count) -
            int(self.playerinfomanager.game_win_count)
        )
        self.MyTextNickName.setText(mytext)
        self.MainMyTextNickName.setText(mytext)
        youtext = '{}\n{}전 {}승 {}패'.format(
            you_name,
            you_count,
            you_win_count,
            int(you_count) - int(you_win_count)
        )
        self.YouTextNickName.setText(youtext)

    def SetMyYouDolImage(self, turn):
        if turn == '1':
            pixmap = QPixmap('Images/BlackDol.png')
            you_pixmap = QPixmap('Images/WhiteDol.png')
        elif turn == '2':
            pixmap = QPixmap('Images/WhiteDol.png')
            you_pixmap = QPixmap('Images/BlackDol.png')

        self.YouIconDol.setPixmap(you_pixmap)
        self.MyIconDol.setPixmap(pixmap)

    def InGameSceneCreate(self):
        self.InGameScene = SceneLayer(self)

        self.InGameImageLabel = QLabel(self)
        self.InGameImageLabel.resize(1280, 720)
        pixmap = QPixmap('Images/InGameBackground.jpg')
        self.InGameImageLabel.setPixmap(pixmap)

       # self.goButton = Button('omok_board2.png',(35,35),(650,650),None,self)
        self.InGameBoard = QLabel(self)
        self.InGameBoard.setGeometry(35,35,650,650)
        pixmap = QPixmap('Images/omok_board2.png')
        self.InGameBoard.setPixmap(pixmap)

        self.InGameBoard2 = QLabel(self)
        self.InGameBoard2.setGeometry(720,35,525,320)
        pixmap = QPixmap('Images/Tree.jpeg')
        self.InGameBoard2.setPixmap(pixmap)

        self.MyIcon = QLabel(self)
        self.MyIcon.setGeometry(725, 40, 150, 150)
        pixmap = QPixmap('Images/Circle.png')
        self.MyIcon.setPixmap(pixmap)

        self.YouIcon = QLabel(self)
        self.YouIcon.setGeometry(725, 200, 150, 150)
        pixmap = QPixmap('Images/Circle.png')
        self.YouIcon.setPixmap(pixmap)

        self.MyIconDol = QLabel(self)
        self.MyIconDol.setGeometry(725, 40, 42, 42)
        pixmap = QPixmap('Images/BlackDol.png')
        self.MyIconDol.setPixmap(pixmap)
        self.YouIconDol = QLabel(self)
        self.YouIconDol.setGeometry(725, 200, 42, 42)
        pixmap = QPixmap('Images/BlackDol.png')
        self.YouIconDol.setPixmap(pixmap)

        self.MyTextNickName = QLabel(self)
        self.MyTextNickName.setGeometry(885,15,200,200)
        self.MyTextNickName.setText('hyunseo\n0전 0승 0패')
        font = QFont("Arial")
        font.setPointSize(16)
        font.setWeight(200)
        self.MyTextNickName.setFont(font)

        self.YouTextNickName = QLabel(self)
        self.YouTextNickName.setGeometry(885, 175, 200, 200)
        self.YouTextNickName.setText('onwoo\n0전 0승 0패')
        self.YouTextNickName.setFont(font)

        self.ChakSuButton = Button('ChaksuButton.png',(850,720-35-122),(300,122),self.Single_SetSton,self)

        self.SelectImage = QLabel(self)
        self.SelectImage.setGeometry(1000,1000,42,42)
        pixmap = QPixmap('Images/Select.png')
        self.SelectImage.setPixmap(pixmap)

        self.LastDolImage = QLabel(self)
        self.LastDolImage.setGeometry(1000,1000,42,42)
        pixmap = QPixmap('Images/LastDol.png')
        self.LastDolImage.setPixmap(pixmap)

        self.SamSamImage = QLabel(self)
        self.SamSamImage.setGeometry(1000, 1000, 42, 42)
        pixmap = QPixmap('Images/SamSam.png')
        self.SamSamImage.setPixmap(pixmap)

        self.TurnBlackImage = QLabel(self)
        self.TurnBlackImage.setGeometry(720,35,525,160)
        pixmap = QPixmap('Images/TurnBlackImage.png')
        self.TurnBlackImage.setPixmap(pixmap)

        self.InGameScene.add_widget(self.InGameImageLabel)
        self.InGameScene.add_widget(self.InGameBoard)
        self.InGameScene.add_widget(self.InGameBoard2)
        self.InGameScene.add_widget(self.MyIcon)
        self.InGameScene.add_widget(self.YouIcon)
        self.InGameScene.add_widget(self.MyTextNickName)
        self.InGameScene.add_widget(self.YouTextNickName)
        self.InGameScene.add_widget(self.ChakSuButton)
        self.InGameScene.add_widget(self.SelectImage)
        self.InGameScene.add_widget(self.LastDolImage)
        self.InGameScene.add_widget(self.TurnBlackImage)
        self.InGameScene.add_widget(self.MyIconDol)
        self.InGameScene.add_widget(self.YouIconDol)
        self.InGameScene.add_widget(self.SamSamImage)
        # self.InGameScene.add_widget(self.goButton)

        self.InGameScene.set_active(False)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Game = GameController()
    Game.show()
    sys.exit(app.exec_())
