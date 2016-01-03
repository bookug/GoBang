# -*- coding: utf-8 -*-
__author__ = 'gzs2478'

from hall_window import Ui_HallWindow
from ChessBoardDesk import ChessBoardDesk,ChessBoardDeskState

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import GoBang
import time
import ChessRoom
class Hall(QWidget):
    def __init__(self,tableRowNum=6,tableColNum=5,director = None):
        QWidget.__init__(self)
        self.initData(tableRowNum,tableColNum,director)
        self.ui = Ui_HallWindow()
        self.ui.setupUi(self)
        self.setTables()
        self.connectUIEvent()
        self.connectToService()
        self.updateHallWithServer()
        self.setWindowTitle(u"用户名："+director.playerNickname)

    def initData(self,tableRowNum,tableColNum,director):
        self.tableRowNum = tableRowNum
        self.tableColNum = tableColNum
        self.director      = director
        self.room = None

    def updateHallWithServer(self):
        self.director.clientThread.client.sendToServer(1002,1001,{})

    def createDesk(self,rowNum,colNum):
        return ChessBoardDesk(rowNum*self.tableColNum+colNum+1)
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

    @staticmethod
    def getIDFromRowAndColNum(rowNum,colNum):
        return rowNum*5 + colNum + 1
    @staticmethod
    def getRowAndColNumber(roomID):
        rowNum = (roomID-1)/5
        colNum = (roomID-1)%5
        return rowNum,colNum
    def chooseDeskSuccess(self,rowNum,colNum,playersNum):

        print "Choose Desk successfully:",playersNum
        desk = self.createDesk(rowNum,colNum)

        if playersNum>0:
            print "CreateAndShowingRoom"
            roomID = Hall.getIDFromRowAndColNum(rowNum,colNum)
            self.room = ChessRoom.ChessRoom(Hall.getIDFromRowAndColNum(rowNum,colNum),self.director)
            QMessageBox.about(self,u"进入房间成功",u"欢迎进入%d号房间"%roomID)
            self.room.show()
    def chooseDeskFail(self,rowNum,colNum):
        QMessageBox.about(self ,u"进房失败",u"房间已满！")


    def clearOnlineList(self):
        print "ClearOnlineList"
        self.ui.OnlineList.clearContents()
        for i in range(self.ui.OnlineList.rowCount(),-1,-1):
            self.ui.OnlineList.removeRow(i)

    def updateOnlineList(self,nickname,winTimes,loseTimes,drawTimes):
        self.ui.OnlineList.insertRow(self.ui.OnlineList.rowCount())
        rowNum = self.ui.OnlineList.rowCount()-1
        score = GoBang.GoBang.GetScore(winTimes,loseTimes,drawTimes)
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
        score = GoBang.GoBang.GetScore(winTimes,loseTimes,drawTimes)
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
                desk.state = ChessBoardDeskState.Empty
            elif playersNum == 1:
                desk.state = ChessBoardDeskState.OnlyLeftPersonWaiting
            elif playersNum == 2:
                if isPlaying :
                    desk.state = ChessBoardDeskState.Playing
                else:
                    desk.state = ChessBoardDeskState.TwoPersonWaiting

            self.setDesk(desk,rowNum,colNum)

        except AttributeError,e:
            print "UpdateDeskError"
            print e
            print rowNum,colNum,playersNum,isPlaying


    def addNewHallChat(self,nickname,message):
        self.ui.MessageText.setPlainText(self.ui.MessageText.toPlainText()+"\n"+nickname+":"+message)






