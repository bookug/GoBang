#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import sys, math
from PyQt4 import QtGui,QtCore

from util import CellState, Direction, Configure
from util import PlayerSide, PlayerState
from util import *

class Board(QtGui.QWidget):
    boardBackgroundPixmap = None
    blackChessPixmap = None
    whiteChessPixmap = None

    currentSide = CellState.WHITE

    def initCellStates(self):
        self.boardCells = []
        for m in xrange(Configure.ROW_SIZE):
            boardRow = []
            for n in xrange(Configure.COL_SIZE):
                boardRow.append(CellState.EMPTY)
            self.boardCells.append(boardRow)

    def init(self):
        self.initCellStates()
        self.boardBackgroundPixmap = QtGui.QPixmap(r'./img/ChessBoard.png')
        self.blackChessPixmap = QtGui.QPixmap(r'./img/BlackChess1.png')
        self.whiteChessPixmap = QtGui.QPixmap(r'./img/WhiteChess1.png')

        #self.setFixedSize(Configure.padding * 2 + (Configure.colSize - 1) * Configure.cellWidth,Configure.padding * 2 + (Configure.rowSize - 1) * Configure.cellHeight)

    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.init()

    #each time when moving, flush and rearrange
    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, Configure.PADDING * 2 + (Configure.COL_SIZE - 1) * Configure.CELL_WIDTH, Configure.PADDING * 2 + (Configure.ROW_SIZE - 1) * Configure.CELL_HEIGHT, self.boardBackgroundPixmap)
        for m in xrange(Configure.ROW_SIZE):
            for n in xrange(Configure.COL_SIZE):
                if self.boardCells[m][n] == CellState.WHITE:
                    print "Add White Chess"
                    x, y = getCellLeftTopPosition(m, n)
                    painter.drawPixmap(x, y, Configure.CELL_WIDTH, Configure.CELL_HEIGHT, self.whiteChessPixmap)
                elif self.boardCells[m][n] == CellState.BLACK:
                    print "Add Black Chess"
                    x, y = getCellLeftTopPosition(m, n)
                    painter.drawPixmap(x, y, Configure.CELL_WIDTH, Configure.CELL_HEIGHT, self.blackChessPixmap)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            x, y = QMouseEvent.x(),QMouseEvent.y()
            print x,",",y,":Clicked!"
            m, n = getCellNumberFromPosition(x,y)
            if m != -1 and n != -1:
                print "get chess board mouse event!"
                self.emit(QtCore.SIGNAL('takeAChess(int,int)'),m,n)

    def wonSinceLastStep(self, rowNum, colNum):
        for i in xrange(8):
            if self.getSameSideCount(i, rowNum, colNum, self.boardCells[rowNum][colNum])>=4:
                return True
        return False

    def changeCellState(self, state, rowNum, colNum):
        try:
            self.boardCells[rowNum][colNum] = state
        except BaseException,e:
            print "Error in change cell state"
            print e
            print rowNum, colNum, state

    def getSameSideCount(self, direction, rowNum, colNum, side):
        sum = 0
        m,n = rowNum,colNum
        if direction == Direction.DOWN:
            for i in range(1,4):
                m = m + 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.UP:
            for i in range(1,4):
                m = m - 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.LEFT:
            for i in range(1,4):
                n = n - 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.RIGHT:
            for i in range(1,4):
                n = n + 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.UP_LEFT:
            for i in range(1,4):
                m = m - 1
                n = n - 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.UP_RIGHT:
            for i in range(1,4):
                m = m - 1
                n = n + 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.DOWN_LEFT:
            for i in range(1,4):
                m = m + 1
                n = n - 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == Direction.DOWN_RIGHT:
            for i in range(1,4):
                m = m + 1
                n = n + 1
                if isRowNumValid(m) and isColNumValid(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        return sum

#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    board = Board()
#    board.show()
#    sys.exit(app.exec_())


from util import GameState

class Desk(QtGui.QWidget):
    PlayingTablePixmap = None
    NotPlayingTablePixmap = None
    PlayerPixelMap = None
    PlayingTableButtonPixmap = None
    NotPlayingTableButtonPixmap = None

    def __init__(self,ID):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(Configure.BACKGROUND_WIDTH, Configure.BACKGROUND_HEIGHT)
        self.initPixmap()
        self.initDataMember(ID)

    def initDataMember(self,ID):
        self.leftMemberID = -1
        self.rightMemberID = -1
        self.state = GameState.EMPTY
        self.isMousePressed = False
        self.isMouseHover = False
        self.ID = ID

    def initPixmap(self):
        self.PlayerPixelMap = QtGui.QPixmap(r'./img/17-1.png')
        self.NotPlayingTablePixmap = QtGui.QPixmap(r'./img/tablen.bmp')
        self.PlayingTablePixmap = QtGui.QPixmap(r'./img/tables.bmp')
        self.NotPlayingTableButtonPixmap = QtGui.QPixmap(r'./img/tableh.png')
        self.PlayingTableButtonPixmap = QtGui.QPixmap(r'./img/tables.png')

        if self.PlayerPixelMap == None \
        or self.NotPlayingTableButtonPixmap == None \
        or self.PlayingTablePixmap == None\
        or self.NotPlayingTableButtonPixmap == None\
        or self.PlayingTableButtonPixmap == None:
            print "Error!"

    def mousePressEvent(self, QMouseEvent):
        if self.isMousePressed == False:
            self.isMousePressed = True
            self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.isMousePressed == True:
            self.isMousePressed = False
            self.update()
            director = self.parent().parent().parent().director
            print "Mouse Release Event:",type(director)
            row,col = Util.getRowAndColumnNum(self.ID)
            director.clientThread.client.sendToServer(1002,1004,{"row_num":row,"col_num":col})

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        if  self.state == GameState.EMPTY\
        or self.state == GameState.ONLY_LEFT_PERSON_WAITING \
        or self.state == GameState.ONLY_RIGHT_PERSON_WAITING \
        or self.state == GameState.TWO_PERSON_WAITING:
            painter.drawPixmap(0, 0, Configure.BACKGROUND_WIDTH, Configure.BACKGROUND_HEIGHT, self.NotPlayingTablePixmap)
            if self.state == GameState.ONLY_LEFT_PERSON_WAITING:
                painter.drawPixmap(0,\
                                   Configure.BACKGROUND_HEIGHT / 2.0 - Configure.PLAYER_HEIGHT / 2.0,\
                                   Configure.PLAYER_WIDTH,\
                                   Configure.PLAYER_HEIGHT,\
                                   self.PlayerPixelMap\
                                    )

            elif self.state == GameState.ONLY_RIGHT_PERSON_WAITING:
                painter.drawPixmap(\
                    Configure.BACKGROUND_WIDTH - Configure.PLAYER_WIDTH,\
                    Configure.BACKGROUND_HEIGHT / 2.0 - Configure.PLAYER_HEIGHT / 2.0,\
                    Configure.PLAYER_WIDTH,\
                    Configure.PLAYER_HEIGHT,\
                    self.PlayerPixelMap)

            elif self.state == GameState.TWO_PERSON_WAITING:
                painter.drawPixmap(0,\
                                   Configure.BACKGROUND_HEIGHT / 2.0 - Configure.PLAYER_HEIGHT / 2.0,\
                                   Configure.PLAYER_WIDTH,\
                                   Configure.PLAYER_HEIGHT,\
                                   self.PlayerPixelMap\
                                    )
                painter.drawPixmap(\
                    Configure.BACKGROUND_WIDTH - Configure.PLAYER_WIDTH,\
                    Configure.BACKGROUND_HEIGHT / 2.0 - Configure.PLAYER_HEIGHT / 2.0,\
                    Configure.PLAYER_WIDTH,\
                    Configure.PLAYER_HEIGHT,\
                    self.PlayerPixelMap)

            if self.isMouseHover:
                if not self.isMousePressed:
                    painter.drawPixmap(0, 0, Configure.BACKGROUND_WIDTH, Configure.BACKGROUND_HEIGHT, self.NotPlayingTableButtonPixmap)
        else:
            painter.drawPixmap(0, 0, Configure.BACKGROUND_WIDTH, Configure.BACKGROUND_HEIGHT, self.PlayingTablePixmap)
            painter.drawPixmap(0,\
                               Configure.BACKGROUND_HEIGHT / 2.0 - Configure.PLAYER_HEIGHT / 2.0,\
                               Configure.PLAYER_WIDTH,\
                               Configure.PLAYER_HEIGHT,\
                               self.PlayerPixelMap\
                                )
            painter.drawPixmap(\
                Configure.BACKGROUND_WIDTH - Configure.PLAYER_WIDTH,\
                Configure.BACKGROUND_HEIGHT / 2.0 - Configure.PLAYER_HEIGHT / 2.0,\
                Configure.PLAYER_WIDTH,\
                Configure.PLAYER_HEIGHT,\
                self.PlayerPixelMap)

            if self.isMouseHover:
                if not self.isMousePressed:
                    painter.drawPixmap(0, 0, Configure.BACKGROUND_WIDTH, Configure.BACKGROUND_HEIGHT, self.PlayingTableButtonPixmap)

        painter.setFont(QtGui.QFont("default",9))
        painter.drawText(0, Configure.BACKGROUND_HEIGHT / 10, Configure.BACKGROUND_WIDTH, Configure.BACKGROUND_HEIGHT / 10, QtCore.Qt.AlignCenter, str(self.ID))

    def enterEvent(self, QEvent):
        self.isMouseHover = True
        #print "Enter Event"
        self.update()

    def leaveEvent(self, QEvent):
        self.isMouseHover = False
        #print "Leave Event"
        self.update()

def test():
    app = QtGui.QApplication(sys.argv)
    widget = Desk()
    widget.show()
    sys.exit(app.exec_())

#if __name__ == '__main__':
#    test()

