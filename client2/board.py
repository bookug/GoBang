#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import sys, math
from PyQt4 import QtGui,QtCore

from util import BoardCell, BoardDirection, PlayerSide, PlayerState

class Board(QtGui.QWidget):
    padding = 40
    cellWidth = 64
    cellHeight = 64
    rowSize = 15
    colSize = 15
    boardBackgroundPixmap = None
    blackChessPixmap = None
    whiteChessPixmap = None

    currentSide = BoardCell.White

    def initBoardCells(self):
        self.boardCells = []
        for m in xrange(self.rowSize):
            boardRow = []
            for n in xrange(self.colSize):
                boardRow.append(BoardCell.Empty)
            self.boardCells.append(boardRow)

    def init(self):
        self.initBoardCells()
        self.boardBackgroundPixmap = QtGui.QPixmap(r'./img/ChessBoard.png')
        self.blackChessPixmap = QtGui.QPixmap(r'./img/BlackChess1.png')
        self.whiteChessPixmap = QtGui.QPixmap(r'./img/WhiteChess1.png')

        #self.setFixedSize(self.padding * 2 + (self.colSize - 1) * self.cellWidth,self.padding * 2 + (self.rowSize - 1) * self.cellHeight)

    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.init()

    @staticmethod
    def getBoardCellLeftTopPosition(rowNum,colNum):
        '''
        number start from zero
        '''
        x = Board.padding + colNum * Board.cellWidth - 0.5 * Board.cellWidth
        y = Board.padding + rowNum * Board.cellHeight - 0.5 * Board.cellHeight
        return x, y

    @staticmethod
    def getCellNumberFromPosition(x,y):
        colNum, rowNum = int((x - Board.padding + 0.5 * Board.cellWidth )/Board.cellWidth), int((y - Board.padding + 0.5 * Board.cellHeight)/Board.cellHeight)
        if colNum >= 0 and colNum < Board.colSize and rowNum >= 0 and rowNum < Board.rowSize :
            return rowNum,colNum
        else:
            return -1,-1  #error

    #each time when moving, flush and rearrange
    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.padding * 2 + (self.colSize - 1) * self.cellWidth, self.padding * 2 + (self.rowSize - 1) * self.cellHeight, self.boardBackgroundPixmap)
        for m in xrange(self.rowSize):
            for n in xrange(self.colSize):
                if self.boardCells[m][n] == BoardCell.White:
                    print "Add White Chess"
                    x, y = self.getBoardCellLeftTopPosition(m, n)
                    painter.drawPixmap(x, y, self.cellWidth, self.cellHeight, self.whiteChessPixmap)
                elif self.boardCells[m][n] == BoardCell.Black:
                    print "Add Black Chess"
                    x, y = self.getChessBoardCellLeftTopPosition(m, n)
                    painter.drawPixmap(x, y, self.cellWidth, self.cellHeight, self.blackChessPixmap)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            x, y = QMouseEvent.x(),QMouseEvent.y()
            print x,",",y,":Clicked!"
            m, n = Board.getCellNumberFromPosition(x,y)
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

    def takeAStep(self, side, rowNum, colNum):
        self.boardCells[rowNum][colNum] = side

    @staticmethod
    def isRowNumValid(m):
        if m < Board.rowSize and m >= 0:
            return True
        else:
            return False

    @staticmethod
    def isColNumValid(n):
        if n < Board.colSize and n >= 0:
            return True
        else:
            return False

    def getSameSideCount(self, direction, rowNum, colNum, side):
        sum = 0
        m,n = rowNum,colNum
        if direction == BoardDirection.Down:
            for i in range(1,4):
                m = m + 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.Up:
            for i in range(1,4):
                m = m - 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.Left:
            for i in range(1,4):
                n = n - 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.Right:
            for i in range(1,4):
                n = n + 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.UpLeft:
            for i in range(1,4):
                m = m - 1
                n = n - 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.UpRight:
            for i in range(1,4):
                m = m - 1
                n = n + 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.DownLeft:
            for i in range(1,4):
                m = m + 1
                n = n - 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
                    if side == self.boardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == BoardDirection.DownRight:
            for i in range(1,4):
                m = m + 1
                n = n + 1
                if Board.isRowNumAvailable(m) and Board.isColNumAvailable(n):
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


from util import BoardDeskState

class BoardDesk(QtGui.QWidget):
    PlayingTablePixmap = None
    NotPlayingTablePixmap = None
    PlayerPixelMap = None
    PlayingTableButtonPixmap = None
    NotPlayingTableButtonPixmap = None
    backgroundWidth = 121
    backgroundHeight = 119
    playerWidth = 32
    playerHeight = 32

    def __init__(self,ID):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(self.backgroundWidth,self.backgroundHeight)
        self.initPixmap()
        self.initDataMember(ID)

    def initDataMember(self,ID):
        self.leftMemberID = -1
        self.rightMemberID = -1
        self.state = BoardDeskState.Empty
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

    def getRowAndColumnNum(self):
        row = math.floor((self.ID-1)/5)
        col = (self.ID-1)%5
        return row,col

    def mouseReleaseEvent(self, QMouseEvent):
        if self.isMousePressed == True:
            self.isMousePressed = False
            self.update()
            director = self.parent().parent().parent().director
            print "Mouse Release Event:",type(director)
            row,col = self.getRowAndColumnNum()
            director.clientThread.client.sendToServer(1002,1004,{"row_num":row,"col_num":col})

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        if  self.state == BoardDeskState.Empty\
        or self.state == BoardDeskState.OnlyLeftPersonWaiting \
        or self.state == BoardDeskState.OnlyRightPersonWaiting \
        or self.state == BoardDeskState.TwoPersonWaiting:
            painter.drawPixmap(0, 0, self.backgroundWidth, self.backgroundHeight,self.NotPlayingTablePixmap)
            if self.state == BoardDeskState.OnlyLeftPersonWaiting:
                painter.drawPixmap(0,\
                                   self.backgroundHeight/2.0 - self.playerHeight/2.0,\
                                   self.playerWidth,\
                                   self.playerHeight,\
                                   self.PlayerPixelMap\
                                    )

            elif self.state == BoardDeskState.OnlyRightPersonWaiting:
                painter.drawPixmap(\
                    self.backgroundWidth - self.playerWidth,\
                    self.backgroundHeight/2.0 - self.playerHeight/2.0,\
                    self.playerWidth,\
                    self.playerHeight,\
                    self.PlayerPixelMap)

            elif self.state == BoardDeskState.TwoPersonWaiting:
                painter.drawPixmap(0,\
                                   self.backgroundHeight/2.0 - self.playerHeight/2.0,\
                                   self.playerWidth,\
                                   self.playerHeight,\
                                   self.PlayerPixelMap\
                                    )
                painter.drawPixmap(\
                    self.backgroundWidth-self.playerWidth,\
                    self.backgroundHeight/2.0 - self.playerHeight/2.0,\
                    self.playerWidth,\
                    self.playerHeight,\
                    self.PlayerPixelMap)

            if self.isMouseHover:
                if not self.isMousePressed:
                    painter.drawPixmap(0, 0, self.backgroundWidth, self.backgroundHeight, self.NotPlayingTableButtonPixmap)
        else:
            painter.drawPixmap(0, 0, self.backgroundWidth, self.backgroundHeight, self.PlayingTablePixmap)
            painter.drawPixmap(0,\
                               self.backgroundHeight/2.0 - self.playerHeight/2.0,\
                               self.playerWidth,\
                               self.playerHeight,\
                               self.PlayerPixelMap\
                                )
            painter.drawPixmap(\
                self.backgroundWidth-self.playerWidth,\
                self.backgroundHeight/2.0 - self.playerHeight/2.0,\
                self.playerWidth,\
                self.playerHeight,\
                self.PlayerPixelMap)

            if self.isMouseHover:
                if not self.isMousePressed:
                    painter.drawPixmap(0, 0, self.backgroundWidth, self.backgroundHeight, self.PlayingTableButtonPixmap)

        painter.setFont(QtGui.QFont("default",9))
        painter.drawText(0, self.backgroundHeight/10, self.backgroundWidth, self.backgroundHeight/10, QtCore.Qt.AlignCenter, str(self.ID))

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
    widget = BoardDesk()
    widget.show()
    sys.exit(app.exec_())

#if __name__ == '__main__':
#    test()

