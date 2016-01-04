#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time

from windows import LoginWindow, HallWindow, RoomWindow
from client import Client, ClientThread
from util import Util, GameState, PlayerSide, PlayerState
from util import *
from board import Board, Desk
from service import RoomService


class Room(QWidget):
    def __init__(self,roomID,director):
        QWidget.__init__(self)
        print "A chess room is created!"
        self.initData(roomID,director)
        self.ui = RoomWindow()
        self.ui.ChessBoard = Board()
        self.ui.setupUi(self)
        self.setChessBoard()
        self.connectService()
        self.connectEvent()
        self.sendArriveRoomRequest()
        self.setWindowTitle(unicode(self.director.playerNickname)+u" in #"+unicode(self.ID)+u" room")

    def initData(self,roomID,director):
        self.ID = roomID
        self.director = director
        self.isClosed = False

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
        print message
        if message != "":
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
            self.ui.Score.setText(str(Util.GetScore(winTimes,loseTimes,drawTimes)))
            if self.state == PlayerState.NOT_READY:
                self.ui.ReadyButton.setDisabled(False)
                self.ui.AdmitDefeatButton.setDisabled(True)
                self.ui.UndoButton.setDisabled(True)
            elif self.state == PlayerState.READY:
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
            elif self.state == PlayerState.TAKING_CHESS:
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
            elif self.state == PlayerState.WAITING_FOR_TAKING:
                self.ui.ReadyButton.setDisabled(True)
                self.ui.AdmitDefeatButton.setDisabled(False)
                self.ui.UndoButton.setDisabled(False)
            elif self.state == PlayerState.WAITING_FOR_UNDO:
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
            self.ui.EnemyScore.setText(str(Util.GetScore(winTimes,loseTimes,drawTimes)))
        self.update()

    def addNewEventList(self,eventString):
        self.ui.LiveText.setPlainText(self.ui.LiveText.toPlainText() + '\n' + unicode(eventString))
    def getRequestForUndoHandler(self):
        reply = QMessageBox.question(self,u'want to withdraw?',u"do you let him withdraw?",QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sendAcceptForUndo()
        else:
            self.sendRejectForUndo()

    def getRejectForUndo(self):
        QMessageBox.about(self,u'fail to withdraw',u'fail to withdraw!')

    def getWinInfo(self):
        QMessageBox.about(self,u'you win!',u'congratulations!')

    def getLoseInfo(self):
        QMessageBox.about(self,u'you lose!',u'come on!')

    def getDrawInfo(self):
        QMessageBox.about(self,u'you draw!',u'draw, again?!')

    def __del__(self):
        if self.isClosed == False:
            print "The room is delete Delete!"
            rowNum,colNum = Util.getRowAndColNumber(self.ID)
            self.director.clientThread.client.sendToServer(1002,1005,{"row_num":rowNum,"col_num":colNum})
            self.director.clientThread.client.sendToServer(1003,1003,{'room_id':self.ID})

    def closeEvent(self, QCloseEvent):
        self.isClosed = True
        print "The room is delete Delete!"
        rowNum,colNum = Util.getRowAndColNumber(self.ID)
        self.director.clientThread.client.sendToServer(1002,1005,{"row_num":rowNum,"col_num":colNum})
        self.director.clientThread.client.sendToServer(1003,1003,{'room_id':self.ID})

    def setChessBoard(self):
        self.chessBoard = Board()
        self.chessBoard.setParent(self.ui.ChessBoard)
        self.update()

#if __name__ == '__main__':
#    import sys
#    app = QApplication(sys.argv)
#    room = Room(0,0)
#    room.show()
#    sys.exit(app.exec_())

class Hall(QWidget):
    def __init__(self,tableRowNum=6,tableColNum=5,director = None):
        QWidget.__init__(self)
        self.initData(tableRowNum,tableColNum,director)
        self.ui = HallWindow()
        self.ui.setupUi(self)
        self.setTables()
        self.connectUIEvent()
        self.connectToService()
        self.updateHallWithServer()
        self.setWindowTitle(u"user name: "+director.playerNickname)

    def initData(self,tableRowNum,tableColNum,director):
        self.tableRowNum = tableRowNum
        self.tableColNum = tableColNum
        self.director = director
        self.room = None

    def updateHallWithServer(self):
        self.director.clientThread.client.sendToServer(1002,1001,{})

    def createDesk(self, rowNum, colNum):
        return Desk(rowNum*self.tableColNum + colNum + 1)

    def setDesk(self,desk,rowNum,colNum):
            layout = QHBoxLayout(desk)
            layout.setAlignment(Qt.AlignCenter)
            desk.setLayout(layout)
            self.ui.Tables.setCellWidget(rowNum,colNum,desk)

    def setTables(self):
        self.ui.Tables.setRowCount(self.tableRowNum)
        self.ui.Tables.setColumnCount(self.tableColNum)
        self.ui.Tables.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.Tables.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        for i in xrange(self.tableRowNum):
            #self.ui.Tables.setRowHeight(i,float(self.ui.Tables.height())/self.tableRowNum)
            for j in xrange(self.tableColNum):
                self.ui.Tables.setColumnWidth(j,float(self.ui.Tables.width() - 17)/self.tableColNum)
                desk = self.createDesk(i,j)
                self.setDesk(desk,i,j)
                #print i,",",j," desk setup!"
        self.ui.Tables.resizeRowsToContents()
        self.ui.Tables.verticalHeader().setVisible(False)
        self.ui.Tables.horizontalHeader().setVisible(False)

    def connectUIEvent(self):
        self.connect(self.ui.SendButton,SIGNAL('clicked()'),self.sendMessage)

    def sendMessage(self):
        message = unicode(self.ui.InputText.toPlainText())
        createTime = time.ctime()
        data = {}
        data['message'] = message
        data['create_time'] = createTime
        self.director.clientThread.client.sendToServer(1002,1002,data)
        self.ui.InputText.setPlainText("")

    def connectToService(self):
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL('clearOnlineListHandler()'),self.clearOnlineList)
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL('updateOnlineListHandler(QString,int,int,int)'),self.updateOnlineList)
        
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL('clearRankListHandler()'),self.clearRankList)
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL('updateRankListHandler(QString,int,int,int)'),self.updateRankList)
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL("updateDeskHandler(int,int,int,bool)"),self.updateDesk)
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL("addNewHallChatHandler(QString,QString)"),self.addNewHallChat)
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL("chooseDeskSuccess(int,int,int)"),self.chooseDeskSuccess)
        self.connect(self.director.clientThread.client.dispatcher.services[1002],\
                     SIGNAL("chooseDeskFail(int,int)"),self.chooseDeskFail)

    def chooseDeskSuccess(self,rowNum,colNum,playersNum):
        print "choose desk successfully:",playersNum
        desk = self.createDesk(rowNum,colNum)
        if playersNum>0:
            print "CreateAndShowingRoom"
            roomID = Util.getIDFromRowAndColNum(rowNum,colNum)
            self.room = Room(Util.getIDFromRowAndColNum(rowNum,colNum),self.director)
            QMessageBox.about(self,u"enter room successfully!",u"welcome to #%d room"%roomID)
            self.room.show()

    def chooseDeskFail(self,rowNum,colNum):
        QMessageBox.about(self ,u"fail to enter room",u"this room is full!")

    def clearOnlineList(self):
        print "ClearOnlineList"
        self.ui.OnlineList.clearContents()
        for i in range(self.ui.OnlineList.rowCount(),-1,-1):
            self.ui.OnlineList.removeRow(i)

    def updateOnlineList(self,nickname,winTimes,loseTimes,drawTimes):
        self.ui.OnlineList.insertRow(self.ui.OnlineList.rowCount())
        rowNum = self.ui.OnlineList.rowCount()-1
        score = Util.GetScore(winTimes,loseTimes,drawTimes)
        self.ui.OnlineList.setItem(rowNum,0,QTableWidgetItem(nickname))
        self.ui.OnlineList.setItem(rowNum,1,QTableWidgetItem(str(winTimes)))
        self.ui.OnlineList.setItem(rowNum,2,QTableWidgetItem(str(score)))
        self.ui.OnlineList.setItem(rowNum,3,QTableWidgetItem(str(drawTimes)))
        self.ui.OnlineList.setItem(rowNum,4,QTableWidgetItem(str(loseTimes)))

    def clearRankList(self):
        self.ui.RankList.clearContents()
        for i in range(self.ui.RankList.rowCount(),-1,-1):
            self.ui.RankList.removeRow(i+1)

    def updateRankList(self,nickname,winTimes,loseTimes,drawTimes):
        self.ui.RankList.insertRow(self.ui.RankList.rowCount())
        rowNum = self.ui.RankList.rowCount()-1
        score = Util.GetScore(winTimes,loseTimes,drawTimes)
        self.ui.RankList.setItem(rowNum,0,QTableWidgetItem(nickname))
        self.ui.RankList.setItem(rowNum,1,QTableWidgetItem(str(winTimes)))
        self.ui.RankList.setItem(rowNum,2,QTableWidgetItem(str(score)))
        self.ui.RankList.setItem(rowNum,3,QTableWidgetItem(str(drawTimes)))
        self.ui.RankList.setItem(rowNum,4,QTableWidgetItem(str(loseTimes)))

    def updateDesk(self,rowNum,colNum,playersNum,isPlaying):
        try:
            #print "Updating Desk ",rowNum,",",colNum,":",playersNum,"---",isPlaying
            desk = self.createDesk(rowNum,colNum)

            if(playersNum == 0):
                desk.state = GameState.EMPTY
            elif playersNum == 1:
                desk.state = GameState.ONLY_LEFT_PERSON_WAITING
            elif playersNum == 2:
                if isPlaying :
                    desk.state = GameState.PLAYING
                else:
                    desk.state = GameState.TWO_PERSON_WAITING

            self.setDesk(desk,rowNum,colNum)

        except AttributeError,e:
            print "UpdateDeskError"
            print e
            print rowNum,colNum,playersNum,isPlaying


    def addNewHallChat(self,nickname,message):
        print message
        if message != "":
            self.ui.MessageText.setPlainText(self.ui.MessageText.toPlainText()+"\n"+nickname+":"+message)


class Login(QWidget):
    def __init__(self,director):
        QWidget.__init__(self)
        self.director = director
        self.ui = LoginWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.loginButton,SIGNAL('clicked()'),self.onLoginButtonClickedEvent)

    def onLoginButtonClickedEvent(self):
        if self.director.clientThread == None:
            self.director.clientThread = ClientThread(self.director)
            client = Client(8,str(self.ui.ServerIPText.text()),self.ui.PortNumberText.text().toInt()[0],0.1,self.director.clientThread)
            self.director.clientThread.begin(client)
            self.connectWithService()
        else:
            self.director.clientThread.client.close()
            self.director.clientThread.client.isAlive = False
            self.director.clientThread = ClientThread(self.director)
            client = Client(8,str(self.ui.ServerIPText.text()),self.ui.PortNumberText.text().toInt()[0],0.1,self.director.clientThread)
            self.director.clientThread.begin(client)
            print "get another client"
            self.connectWithService()
        data = {}
        data['nickname'] = unicode(self.ui.NicknameText.text())
        data['password'] = unicode(self.ui.PasswordText.text())
        self.director.clientThread.client.sendToServer(1001,1001,data)
        self.director.playerNickname = data['nickname']

    def connectWithService(self):
        self.disconnect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('goToHallFromLoginWindow(bool,int,int)'),self.goToHallFromLoginWindow)
        self.disconnect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('loginFailed(QString)'),self.loginFailed)
        self.connect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('goToHallFromLoginWindow(bool,int,int)'),self.goToHallFromLoginWindow)
        self.connect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('loginFailed(QString)'),self.loginFailed)

    def goToHallFromLoginWindow(self,isFirstLogin,tableColNum,tableRowNum):
        print "Go To Hall From Login Window"
        if isFirstLogin:
            QMessageBox.about(None,u"welcome",u"welcome to login first")
        else:
            QMessageBox.about(None,u'welcome',u"welcome to login again")
        self.close()
        print "Type self director:",self.director
        self.hall = Hall(tableRowNum,tableColNum,self.director )
        self.hall.show()

    def loginFailed(self,errorString):
        QMessageBox.about(None,u"fail to login!",errorString)

