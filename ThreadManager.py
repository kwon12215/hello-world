from PyQt5.QtCore import *


class ThreadManager(QThread):
    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.animations = []
        self.start()

    def add_animation(self, function, repeat=1):
        temp = ThreadClass(function,repeat)
        self.animations.append(temp)

    def run(self):
        while True:
            for i in self.animations:
                if i.isStop:
                    self.animations.remove(i)
                    del i

class ThreadClass(QThread):
    def __init__(self,function,repeat=1, parent=None):
        super(ThreadClass, self).__init__(parent)

        self.function = function
        self.repeat = repeat
        self.isStop = False
        self.start()

    def __del__(self):
        print(".... end thread.....")
        self.wait()

    def run(self):
        for i in range(self.repeat):
            self.function()
        self.isStop = True




