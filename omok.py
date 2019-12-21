class Omok:
    def __init__(self):
        self.omok_board = []
        self.clear_board()
        pass

    def xy_check_board(self, x, y):
        if self.omok_board[x][y] != 0:
            return True
        else:
            return False

    def set_omokdol(self, x, y,dol):
        print('{},{},{}'.format(x,y,dol))
        self.omok_board[x][y] = dol

    def clear_board(self):
        self.omok_board = [[0 for j in range(15)] for i in range(15)]

    def check_board(self, CheckList):
        for k in range(15):
            for l in range(15):
                if CheckList[k][l] == 1:
                    if k <= 10:
                        if CheckList[k][l] == 1 and CheckList[k + 1][l] == 1 and CheckList[k + 2][l] == 1 and\
                                CheckList[k + 3][l] == 1 and CheckList[k + 4][l] == 1:
                            print('흑돌 승리')
                            return 1
                    if l <= 10:
                        if CheckList[k][l] == 1 and CheckList[k][l + 1] == 1 and CheckList[k][l + 2] == 1 and\
                                CheckList[k][l + 3] == 1 and CheckList[k][l + 4] == 1:
                            print('흑돌 승리')
                            return 1
                    if k <= 10 and l <= 10:
                        if CheckList[k][l] == 1 and CheckList[k + 1][l + 1] == 1 and CheckList[k + 2][l + 2] == 1 and\
                                CheckList[k + 3][l + 3] == 1 and CheckList[k + 4][l + 4] == 1:
                            print('흑돌 승리')
                            return 1
                    if k <= 10 and l >= 4:
                        if CheckList[k][l] == 1 and CheckList[k + 1][l - 1] == 1 and CheckList[k + 2][l - 2] == 1 and\
                                CheckList[k + 3][l - 3] == 1 and CheckList[k + 4][l - 4] == 1:
                            print('흑돌 승리')
                            return 1
                elif CheckList[k][l] == 2:
                    if k <= 10:
                        if CheckList[k][l] == 2 and CheckList[k + 1][l] == 2 and CheckList[k + 2][l] == 2 and\
                                CheckList[k + 3][l] == 2 and CheckList[k + 4][l] == 2:
                            print('백돌 승리')
                            return 2
                    if l <= 10:
                        if CheckList[k][l] == 2 and CheckList[k][l + 1] == 2 and CheckList[k][l + 2] == 2 and\
                                CheckList[k][l + 3] == 2 and CheckList[k][l + 4] == 2:
                            print('백돌 승리')
                            return 2
                    if k <= 10 and l <= 10:
                        if CheckList[k][l] == 2 and CheckList[k + 1][l + 1] == 2 and CheckList[k + 2][l + 2] == 2 and\
                                CheckList[k + 3][l + 3] == 2 and CheckList[k + 4][l + 4] == 2:
                            print('백돌 승리')
                            return 2
                    if k <= 10 and l >= 4:
                        if CheckList[k][l] == 2 and CheckList[k + 1][l - 1] == 2 and CheckList[k + 2][l - 2] == 2 and\
                                CheckList[k + 3][l - 3] == 2 and CheckList[k + 4][l - 4] == 2:
                            print('백돌 승리')
                            return 2
        return 0


if __name__ == '__main__':
    omok = Omok()
    CheckList = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
    omok.check_board(CheckList)
