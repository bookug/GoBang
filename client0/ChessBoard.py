#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

from PyQt4 import QtGui,QtCore
import sys

class ChessBoardCellState:
    White = 0
    Black = 1
    Empty = 2
    StateDict = {\
        0   :   u"白棋",\
        1   :   u"黑棋",\
        2   :   u"无棋"\

        }
class PlayerSide:
    White = 0
    Black = 1
    StateDict = {\
        0:u"白方",\
        1:u"黑方"\
        }

class PlayerState:
    NotReady = 0
    Ready = 1
    TakingChess = 2
    WaitingForTaking = 3
    WaitingForUndo = 4
    MakingDecisionForUndo = 5
    StateDict = {\
        0:u'还没准备好',
        1:u'我准备好了啦',
        2:u'思考中Zzz',
        3:u'等待下棋',
        4:u'请求悔棋ing',
        5:u'要不要悔棋'
        }

class ChessBoardDirection:
    Left = 0
    Right = 1
    Down = 2
    Up = 3
    UpLeft = 4
    DownRight = 5
    UpRight = 6
    DownLeft = 7

class ChessBoard(QtGui.QWidget):
    padding = 20
    cellWidth = 32
    cellHeight = 32
    rowSize = 15
    colSize = 15
    chessBoardBackgroundPixmap = None
    blackChessPixmap = None
    whiteChessPixmap = None

    currentSide = ChessBoardCellState.White

    def initChessBoardCellsState(self):
        self.chessBoardCells = []
        for m in xrange(self.rowSize):
            chessBoardRow = []
            for n in xrange(self.colSize):
                chessBoardRow.append(ChessBoardCellState.Empty)
            self.chessBoardCells.append(chessBoardRow)

    def init(self):
        self.initChessBoardCellsState()
        self.chessBoardBackgroundPixmap = QtGui.QPixmap(r'./ChessBoard.png')
        self.blackChessPixmap = QtGui.QPixmap(r'./BlackChess1.png')
        self.whiteChessPixmap = QtGui.QPixmap(r'./WhiteChess1.png')

        self.setFixedSize(self.padding * 2 + (self.colSize - 1) * self.cellWidth,self.padding * 2 + (self.rowSize - 1) * self.cellHeight)
    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.init()
    @staticmethod
    def getChessBoardCellLeftTopPosition(rowNum,colNum):
        '''
        number start from zero
        '''
        xPosition = ChessBoard.padding + colNum * ChessBoard.cellWidth - 0.5 * ChessBoard.cellWidth
        yPosition = ChessBoard.padding + rowNum * ChessBoard.cellHeight - 0.5 * ChessBoard.cellHeight
        return xPosition,yPosition
    @staticmethod
    def getCellNumberFromPosition(x,y):
        colNum,rowNum = int((x-ChessBoard.padding + 0.5 * ChessBoard.cellWidth )/ChessBoard.cellWidth),int((y-ChessBoard.padding + 0.5 * ChessBoard.cellHeight)/ChessBoard.cellHeight)
        if colNum >= 0 and colNum < ChessBoard.colSize and rowNum >= 0 and rowNum < ChessBoard.rowSize :
            return rowNum,colNum
        else:
            return -1,-1

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0,0,self.padding * 2 + (self.colSize - 1) * self.cellWidth,self.padding * 2 + (self.rowSize - 1) * self.cellHeight,self.chessBoardBackgroundPixmap)
        for m in xrange(self.rowSize):
            for n in xrange(self.colSize):
                if self.chessBoardCells[m][n] == ChessBoardCellState.White:
                    print "Add White Chess"
                    x,y = self.getChessBoardCellLeftTopPosition(m,n)
                    painter.drawPixmap(x,y,self.cellWidth,self.cellHeight,self.whiteChessPixmap)
                elif self.chessBoardCells[m][n] == ChessBoardCellState.Black:
                    print "Add Black Chess"
                    x,y = self.getChessBoardCellLeftTopPosition(m,n)
                    painter.drawPixmap(x,y,self.cellWidth,self.cellHeight,self.blackChessPixmap)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            x, y = QMouseEvent.x(),QMouseEvent.y()
            print x,",",y,":Clicked!"
            m, n = ChessBoard.getCellNumberFromPosition(x,y)
            if m != -1 and n != -1:
                print "GetChessBoardMouseEvent"
                self.emit(QtCore.SIGNAL('takeAChess(int,int)'),m,n)

    def isWonSinceLastStep(self,rowNum,colNum):
        for i in xrange(8):
            if self.getSameSideChessNumber(i,rowNum,colNum,self.chessBoardCells[rowNum][colNum])>=4:
                return True
        return False

    @staticmethod
    def isRowNumAvailable(m):
        if m<ChessBoard.rowSize and m>=0:
            return True
        else:
            return False

    def changeCellState(self,state,rowNum,colNum):
        try:
            self.chessBoardCells[rowNum][colNum] = state
        except BaseException,e:
            print "Error in change cell state"
            print e
            print rowNum,colNum,state
    def takeAStep(self,side,rowNum,colNum):
        self.chessBoardCells[rowNum][colNum] = side

    @staticmethod
    def isColNumAvailable(n):
        if n<ChessBoard.colSize and n>=0:
            return True
        else:
            return False

    def getSameSideChessNumber(self,direction,rowNum,colNum,side):
        sum = 0
        currentSide = self.chessBoardCells[rowNum][colNum]
        m,n = rowNum,colNum
        if direction == ChessBoardDirection.Down:
            for i in range(1,4):
                m = m + 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.Up:
            for i in range(1,4):
                m = m - 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.Left:
            for i in range(1,4):
                n = n - 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.Right:
            for i in range(1,4):
                n = n + 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.UpLeft:
            for i in range(1,4):
                m = m - 1
                n = n - 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.UpRight:
            for i in range(1,4):
                m = m - 1
                n = n + 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.DownLeft:
            for i in range(1,4):
                m = m + 1
                n = n + 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        elif direction == ChessBoardDirection.DownRight:
            for i in range(1,4):
                m = m + 1
                n = n - 1
                if ChessBoard.isRowNumAvailable(m) and ChessBoard.isColNumAvailable(n):
                    if side == self.chessBoardCells[m][n]:
                        sum = sum + 1
                    else:
                        break;
                else:
                    break
        return sum

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    chessBoard= ChessBoard()
    chessBoard.show()

    sys.exit(app.exec_())


