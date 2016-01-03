#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

from PyQt4 import QtGui,QtCore
import sys
import math

class ChessBoardDeskState(QtGui.QWidget):
    Empty = 0
    OnlyLeftPersonWaiting = 1;
    OnlyRightPersonWaiting = 2
    TwoPersonWaiting = 3;
    Playing = 4;

class ChessBoardDesk(QtGui.QWidget):
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
        self.state = ChessBoardDeskState.Empty
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
        if  self.state == ChessBoardDeskState.Empty\
        or self.state == ChessBoardDeskState.OnlyLeftPersonWaiting \
        or self.state == ChessBoardDeskState.OnlyRightPersonWaiting \
        or self.state == ChessBoardDeskState.TwoPersonWaiting:
            painter.drawPixmap(0,0,self.backgroundWidth,self.backgroundHeight,self.NotPlayingTablePixmap)
            if self.state == ChessBoardDeskState.OnlyLeftPersonWaiting:
                painter.drawPixmap(0,\
                                   self.backgroundHeight/2.0-self.playerHeight/2.0,\
                                   self.playerWidth,\
                                   self.playerHeight,\
                                   self.PlayerPixelMap\
                                    )

            elif self.state == ChessBoardDeskState.OnlyRightPersonWaiting:
                painter.drawPixmap(\
                    self.backgroundWidth-self.playerWidth,\
                    self.backgroundHeight/2.0-self.playerHeight/2.0,\
                    self.playerWidth,\
                    self.playerHeight,\
                    self.PlayerPixelMap)

            elif self.state == ChessBoardDeskState.TwoPersonWaiting:
                painter.drawPixmap(0,\
                                   self.backgroundHeight/2.0-self.playerHeight/2.0,\
                                   self.playerWidth,\
                                   self.playerHeight,\
                                   self.PlayerPixelMap\
                                    )
                painter.drawPixmap(\
                    self.backgroundWidth-self.playerWidth,\
                    self.backgroundHeight/2.0-self.playerHeight/2.0,\
                    self.playerWidth,\
                    self.playerHeight,\
                    self.PlayerPixelMap)

            if self.isMouseHover:
                if not self.isMousePressed:
                    painter.drawPixmap(0,0,self.backgroundWidth,self.backgroundHeight,self.NotPlayingTableButtonPixmap)
        else:
            painter.drawPixmap(0,0,self.backgroundWidth,self.backgroundHeight,self.PlayingTablePixmap)
            painter.drawPixmap(0,\
                               self.backgroundHeight/2.0-self.playerHeight/2.0,\
                               self.playerWidth,\
                               self.playerHeight,\
                               self.PlayerPixelMap\
                                )
            painter.drawPixmap(\
                self.backgroundWidth-self.playerWidth,\
                self.backgroundHeight/2.0-self.playerHeight/2.0,\
                self.playerWidth,\
                self.playerHeight,\
                self.PlayerPixelMap)

            if self.isMouseHover:
                if not self.isMousePressed:
                    painter.drawPixmap(0,0,self.backgroundWidth,self.backgroundHeight,self.PlayingTableButtonPixmap)

        painter.setFont(QtGui.QFont("default",9))
        painter.drawText(0,self.backgroundHeight/10,self.backgroundWidth,self.backgroundHeight/10,QtCore.Qt.AlignCenter,str(self.ID))
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
    widget = ChessBoardDesk()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test()