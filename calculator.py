from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLineEdit, QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout



class Button(QToolButton):

    def __init__(self, text,callback):#os에서 function 불러내는 게 callback.
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)#사이즈 키우기
        self.setText(text)#버튼이 만들어질 때 생성자의 text를 넣어놓음. 추상화
        self.clicked.connect(callback)


    def sizeHint(self):#버튼 키우기.
        size = super(Button, self).sizeHint()#sizeHint
        size.setHeight(size.height() + 20)#사이즈 바꾸기. derived class size. 부모의 함수는 가상함수, 자녀 쪽은 구체화.
        size.setWidth(max(size.width(), size.height()))#더 큰 값으로 설정.
        return size



class Calculator(QWidget):
    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        try:
            if key == '=':
                result = str(eval(self.display.text()))
                self.display.setText(result)
            elif key == 'C':
                self.display.setText('')
            else:
                self.display.setText(self.display.text() +key)
        except SyntaxError:
            self.display.setText("none")
        except ZeroDivisionError:
            self.display.setText("none")

    def __init__(self, parent=None):
        super().__init__(parent)

        # Display Window
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        self.digitButton = []
        for i in range(10):
            self.digitButton += [Button(str(i),self.buttonClicked)]
        # . and = Buttons
        self.decButton = Button('.',self.buttonClicked)
        self.eqButton = Button('=',self.buttonClicked)

        # Operator Buttons
        self.mulButton = Button('*',self.buttonClicked)
        self.divButton = Button('/',self.buttonClicked)
        self.addButton = Button('+',self.buttonClicked)
        self.subButton = Button('-',self.buttonClicked)

        # Parentheses Buttons
        self.lparButton = Button('(',self.buttonClicked)
        self.rparButton = Button(')',self.buttonClicked)

        # Clear Button
        self.clearButton = Button('C',self.buttonClicked)

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 2)

        numLayout = QGridLayout()

        numLayout.addWidget(self.digitButton[0], 3, 0)

        for j in range(1, 10):
            numLayout.addWidget(self.digitButton[j], 2 - (j - 1) // 3, (j - 1) % 3)

        numLayout.addWidget(self.decButton, 3, 1)
        numLayout.addWidget(self.eqButton, 3, 2)

        mainLayout.addLayout(numLayout, 1, 0)

        opLayout = QGridLayout()

        opLayout.addWidget(self.mulButton, 0, 0)
        opLayout.addWidget(self.divButton, 0, 1)
        opLayout.addWidget(self.addButton, 1, 0)
        opLayout.addWidget(self.subButton, 1, 1)

        opLayout.addWidget(self.lparButton, 2, 0)
        opLayout.addWidget(self.rparButton, 2, 1)

        opLayout.addWidget(self.clearButton, 3, 0)

        mainLayout.addLayout(opLayout, 1, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("My Calculator")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
#button[0].buttonclicked.connect.display.().함수를 부르는 방법 fuction calling user가 하면 call forward(외부 이벤트.) os가 하면 call back(내부 이벤트.)
#button은trigger,publisher. self.display.setText는 subscriber. send함수는 버튼 구별 가능.
#display는 문자열을 받음. eval함수는 문자열로 되어 있는 수식을 숫자로 바꾸고 계산해주고 결과를 숫자로 바꿔줌. display에다 넣으려면 문자여야 하니가 str으로 바꿔줌.
#buttonclicked함수는 os가 수행함. 이거를 call back이라고 함.buttonclicked는 callback함수.
#사람이 버튼 0번째 거를 누르면 버튼이 눌려진 걸 버튼 함수와 센더 함수가 알아서 button[0]이 불려짐. 이게 call forward
