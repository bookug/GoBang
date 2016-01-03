#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

from chess_room_window import Ui_ChessRoomWindow
from ChessBoard import ChessBoard,ChessBoardCellState,PlayerSide,PlayerState
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Hall
import time
import GoBang
import RoomService

class ChessRoom(QWidget):
    def __init__(self,roomID,director):
        QWidget.__init__(self)
        print "A chess room is create!"
        self.initData(roomID,director)
        self.ui = Ui_ChessRoomWindow()
        self.ui.ChessBoard = ChessBoard()
        self.ui.setupUi(self)
        self.setChessBoard()
        self.connectService()
        self.connectEvent()
        self.sendArriveRoomRequest()

        self.setWindowTitle(unicode(self.director.playerNickname)+u" 在"+unicode(self.ID)+u"号房间")

    def connectService(self):
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('addNewRoomChat(QString,QString)'),\
            self.addNewRoomChat)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('updateChessCell(int,int,int)'),\
            self.updateChessCell)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('updatePlayerInfo(QString,int,int,int,int,int)'),\
            self.updatePlayerInfo)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('addNewEventList(QString)'),\
            self.addNewEventList)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('getRequestForUndoHandler()'),\
            self.getRequestForUndoHandler)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('getRejectForUndoHandler()'),\
            self.getRejectForUndo)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('getWinInfo()'),\
            self.getWinInfo)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('getLoseInfo()'),\
            self.getLoseInfo)
        self.connect(\
            self.director.clientThread.client.dispatcher.services[1003],\
            SIGNAL('getDrawInfo()'),\
            self.getDrawInfo)

    def connectEvent(self):
        self.connect(self.ui.SendButton,SIGNAL('clicked()'),self.sendChat)
        self.connect(self.ui.UndoButton,SIGNAL('clicked()'),self.sendUndoRequest)
        self.connect(self.ui.ReadyButton,SIGNAL('clicked()'),self.sendReady)
        self.connect(self.ui.AdmitDefeatButton,SIGNAL('clicked()'),self.sendCommitLose)
        self.connect(self.chessBoard,SIGNAL('takeAChess(int,int)'),self.sendTakeAChess)
    def sendArriveRoomRequest(self):
        self.director.clientThread.client.sendToServer(1003,1001,{'room_id':self.ID})

    def sendChat(self):
        message = unicode(self.ui.InputText.toPlainText())
        curTime = time.ctime()
        self.director.clientThread.client.sendToServer(1003,1002,{'room_id':self.ID,'message':message,'create_time':curTime})
        self.ui.InputText.setPlainText("")

    def sendUndoRequest(self):
        print "I send undo request!"
        self.director.clientThread.client.sendToServer(1003,1007,{'room_id':self.ID})

    def sendTakeAChess(self,rowNum,colNum):
        side = self.side
        self.director.clientThread.client.sendToServer(1003,1004,{'room_id':self.ID,'side':side,'row_num':rowNum,'col_num':colNum})

    def sendReady(self):
        self.director.clientThread.client.sendToServer(1003,1005,{'room_id':self.ID})

    def sendDisready(self):
        self.director.clientThread.client.sendToServer(1003,1006,{'room_id':self.ID})

    def sendCommitLose(self):
        self.director.clientThread.client.sendToServer(1003,1010,{'room_id':self.ID})

    def sendRequestForUndo(self):
        self.director.clientThread.client.sendToServer(1003,1007,{'room_id':self.ID})
    def sendAcceptForUndo(self):
        self.director.clientThread.client.sendToServer(1003,1008,{'room_id':self.ID})
    def sendRejectForUndo(self):
        self.director.clientThread.client.sendToServer(1003,1009,{'room_id':self.ID})

    def addNewRoomChat(self,nickname,message):
        self.ui.MessageText.setPlainText(self.ui.MessageText.toPlainText()+"\n"+nickname+":"+message)

    def updateChessCell(self,rowNum,colNum,chessCellState):
        try:
            self.chessBoard.changeCellState(chessCellState,rowNum,colNum)
        except BaseException,e:
            print "Error in update chess cell"
            print e
            print rowNum,colNum,chessCellState

    def updatePlayerInfo(self,nickname,winTimes,loseTimes,drawTimes,state,side):
        print "UpdatePlayerInfo is Emitted!",self.director.playerNickname

        if unicode(self.director.playerNickname) == unicode(nickname):
            print "Update My info",unicode(nickname)
            self.ui.NickName.setText(unicode(nickname))
            self.ui.WinTime.setText(str(winTimes))
            self.ui.LoseTime.setText(str(loseTimes))
            self.ui.Draw.setText(str(drawTimes))
            self.ui.State.setText(unicode(PlayerState.StateDict[state]))
            self.ui.Side.setText(unicode(PlayerSide.StateDict[side]))
            self.side = side
            self.state = state
            self.ui.Score.setText(str(GoBang.GoBang.GetScore(winTimes,loseTimes,drawTimes)))
            if self.state == PlayerState.NotReady:
                self.ui.ReadyButton.setDisabled(False)
                self.ui.AdmitDefeatButton.setDisabled(True)
                self.ui.UndoButton.setDisabled(True)
            elif self.state == PlayerState.Ready:
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
            elif self.state == PlayerState.TakingChess:#todo
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
            elif self.state == PlayerState.WaitingForTaking:
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
            elif self.state == PlayerState.WaitingForUndo:
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(True)
            else:
                self.ui.ReadyButton.setDisabled(False)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
        else:
            print "Update Enemy Info",unicode(nickname)
            self.ui.EnemyNickName.setText(unicode(nickname))
            self.ui.EnemyWinTime.setText(str(winTimes))
            self.ui.EnemyLoseTime.setText(str(loseTimes))
            self.ui.EnemyDrawTime.setText(str(drawTimes))
            self.ui.EnemyState.setText(unicode(PlayerState.StateDict[state]))
            self.ui.EnemySide.setText(unicode(PlayerSide.StateDict[side]))
            self.ui.EnemyScore.setText(str(GoBang.GoBang.GetScore(winTimes,loseTimes,drawTimes)))
        self.update()

    def addNewEventList(self,eventString):
        self.ui.LiveText.setPlainText(self.ui.LiveText.toPlainText() + '\n' + unicode(eventString))
    def getRequestForUndoHandler(self):
        reply = QMessageBox.question(self,u'居然要悔棋',u"难道你能让他悔棋么？",QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sendAcceptForUndo()
        else:
            self.sendRejectForUndo()

    def getRejectForUndo(self):
        QMessageBox.about(self,u'悔棋被拒',u'悔棋被拒！')
    def getWinInfo(self):
        QMessageBox.about(self,u'你赢了！',u'认真你就赢了！')
    def getLoseInfo(self):

        QMessageBox.about(self,u'你输了！',u'认真你就输了！')
    def getDrawInfo(self):
        QMessageBox.about(self,u'平局！',u'居然是平局！')

    def __del__(self):
        if self.isClosed == False:
            print "The room is delete Delete!"
            rowNum,colNum = Hall.Hall.getRowAndColNumber(self.ID)
            self.director.clientThread.client.sendToServer(1002,1005,{"row_num":rowNum,"col_num":colNum})
            self.director.clientThread.client.sendToServer(1003,1003,{'room_id':self.ID})
    def closeEvent(self, QCloseEvent):
        self.isClosed = True
        print "The room is delete Delete!"
        rowNum,colNum = Hall.Hall.getRowAndColNumber(self.ID)
        self.director.clientThread.client.sendToServer(1002,1005,{"row_num":rowNum,"col_num":colNum})
        self.director.clientThread.client.sendToServer(1003,1003,{'room_id':self.ID})

    def initData(self,roomID,director):
        self.ID = roomID
        self.director = director
        self.isClosed = False

    def setChessBoard(self):
        self.chessBoard = ChessBoard()
        self.chessBoard.setParent(self.ui.ChessBoard)
        self.update()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    room = ChessRoom(0,0,1)
    room.show()
    sys.exit(app.exec_())