#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Service import Service
from ChessBoard import PlayerState,PlayerSide
class RoomService(Service):
    serviceID = 1003
    def __init__(self,parent):
        Service.__init__(self,self.serviceID,parent)
        self.initData()
    def initData(self):
        self.registers({\
            1001 : self.getLastChatHandler,\
            1002 : self.getChessCellsHanlder,\
            1003 : self.getPlayerHandler,\
            1004 : self.getNewMessage,\
            1005 : self.getRequestForUndo,\
            1006 : self.getRejectForUndo,\
            1007 : self.getWinInfo,\
            1008 : self.getLoseInfo,\
            1009 : self.getDrawInfo\
        })
        self.director = self.parent.parent.parent.parent
        print "Director is"
        print type(self.director)

    def getLastChatHandler(self,msg,owner):
        data = msg['data']
        nickname,message = data['nickname'],data['message']
        self.emit(SIGNAL('addNewRoomChat(QString,QString)'),nickname,message)

    def getChessCellsHanlder(self,msg,owner):
        try:
            data = msg['data']
            chessCells = data['chess_cells']
            for rowNum in xrange(len(chessCells)):
                row = chessCells[rowNum]
                for colNum in xrange(len(row)):
                    chessCell = chessCells[rowNum][colNum]

                    self.emit(SIGNAL('updateChessCell(int,int,int)'),rowNum,colNum,chessCell)
        except BaseException,e:
            print "Error in Chess Cells handler"
            print e
            print msg
    def getPlayerHandler(self,msg,owner):
        print "GetPlayerHandler"
        data = msg['data']
        players = data['players']
        if len(players) == 1:
            player = {}
            player['nickname'] = u'还没人来'
            player['win_times'] = 0
            player['lose_times'] = 0
            player['draw_times'] = 0
            player['state'] = PlayerState.NotReady
            otherSide = players[players.keys()[0]]['side']
            if otherSide == PlayerSide.Black:
                player['side'] = PlayerSide.White
            else:
                player['side'] = PlayerSide.Black
            players[-1] = player

        for connectID in players:
            player = players[connectID]
            self.emit(SIGNAL('updatePlayerInfo(QString,int,int,int,int,int)'),\
                      player['nickname'],\
                      player['win_times'],\
                      player['lose_times'],\
                      player['draw_times'],\
                      player['state'],\
                      player['side']\
                      )
    def getNewMessage(self,msg,owner):
        data = msg['data']
        eventString = data['event']
        self.emit(SIGNAL('addNewEventList(QString)'),eventString)

    #1005
    def getRequestForUndo(self,msg,owner):
        data = msg['data']
        self.emit(SIGNAL('getRequestForUndoHandler()'))

    def getRejectForUndo(self,msg,owner):
        data = msg['data']
        self.emit(SIGNAL('getRejectForUndoHandler()'))

    def getWinInfo(self,msg,owner):
        data = msg['data']
        self.emit(SIGNAL('getWinInfo()'))

    def getLoseInfo(self,msg,owner):
        data = msg['data']
        self.emit(SIGNAL('getLoseInfo()'))

    def getDrawInfo(self,msg,owner):
        data = msg['data']
        self.emit(SIGNAL('getDrawInfo()'))
