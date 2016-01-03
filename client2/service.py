#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Service(QObject):
    def __init__(self,sid,parent = None):
        QObject.__init__(self,None)
        self.service_id = sid
        self.commands = {}
        self.parent = parent

    def setParent(self,dispatcher):
        self.parent = dispatcher

    def handle(self,msg,owner):
        commandID = msg['command_id']
        if not commandID in self.commands:
            raise Exception('Wrong Command %s'%commandID)
        function = self.commands[commandID]
        return function(msg,owner)
    def register(self,commandID,function):
        self.commands[commandID] = function

    def registers(self,CommandDict):
        for commandID in CommandDict:
            self.register(commandID,CommandDict[commandID])
        return 0

from board import PlayerState, PlayerSide

class RoomService(Service):
    serviceID = 1003

    def __init__(self,parent):
        Service.__init__(self,self.serviceID,parent)
        self.initData()

    def initData(self):
        self.registers({\
            1001 : self.getLastChatHandler,\
            1002 : self.getChessCellsHandler,\
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

    def getChessCellsHandler(self,msg,owner):
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
            player['nickname'] = u'nobody comes'
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

class LoginService(Service):
    serviceID = 1001

    def __init__(self,parent):
        Service.__init__(self,self.serviceID,parent)
        self.initData()

    def initData(self):
        self.registers({\
            1001 : self.loginSuccessHandler,\
            1002 : self.loginFailedHandler\
        })
        self.director = self.parent.parent.parent.parent
        print "Director is"
        print type(self.director)

    def loginSuccessHandler(self,msg,owner):
        print "LoginSuccessHandler"
        data = msg['data']
        self.emit(\
            SIGNAL('goToHallFromLoginWindow(bool,int,int)'),\
            data['is_first_login'],data['table_col_num'],\
            data['table_row_num'])
    def loginFailedHandler(self,msg,owner):
        print "LoginFailedHandler"
        self.emit(SIGNAL('loginFailed(QString)'),u"wrong password, or login already!")

class HallService(Service):
    serviceID = 1002

    def __init__(self,parent):
        Service.__init__(self,self.serviceID,parent)
        self.initData()

    def initData(self):
        self.registers({\
            1001 : self.getOnlineListHandler,\
            1002 : self.getRankListHandler,\
            1003 : self.getDeskListHandler,\
            1004 : self.getNewChatHandler,\
            1005 : self.chooseDeskHandler\
        })
        self.director = self.parent.parent.parent.parent
        print "Director is"
        print type(self.director)

    def getOnlineListHandler(self,msg,owner):
        print "GetOnlineList"
        data = msg['data']
        players = data['players']
        self.emit(SIGNAL('clearOnlineListHandler()'))
        for player in players:
            self.emit(SIGNAL('updateOnlineListHandler(QString,int,int,int)'),\
                      player['nickname'],\
                      player['win_times'],\
                      player['lose_times'],\
                      player['draw_times']
                      )

    def getRankListHandler(self,msg,owner):
        print "GetOnlineList"
        data = msg['data']
        players = data['players']
        self.emit(SIGNAL('clearRankListHandler()'))
        for player in players:
            self.emit(SIGNAL('updateRankListHandler(QString,int,int,int)'),\
                      player['nickname'],\
                      player['win_times'],\
                      player['lose_times'],\
                      player['draw_times']
                      )

    def getDeskListHandler(self,msg,owner):
        try:
            print "GetDeskListHandler"
            data = msg['data']
            deskInfos = data['desk_infos']
            for deskInfo in deskInfos:
                self.emit(SIGNAL("updateDeskHandler(int,int,int,bool)"),\
                          deskInfo['row_num'],\
                          deskInfo['col_num'],\
                          len(deskInfo['players']),\
                          deskInfo['is_playing']
                          )
        except BaseException,e:
            print "GetDeskListError"
            print e
            print msg

    def getNewChatHandler(self,msg,owner):
        print "GetNEwChat"
        data = msg['data']
        newChatMessage = data['message']
        for nickname in newChatMessage:
            self.emit(SIGNAL("addNewHallChatHandler(QString,QString)"),nickname,newChatMessage[nickname])

    def chooseDeskHandler(self,msg,owner):
        print "Choose Desk Event"
        data = msg['data']
        isChooseDeskSuccess = data['is_choose_desk_success']
        rowNum = data['row_num']
        colNum = data['col_num']
        if isChooseDeskSuccess == True:
            playersNum = data['player_num']
            self.emit(SIGNAL("chooseDeskSuccess(int,int,int)"),rowNum,colNum,playersNum)
        else:
            self.emit(SIGNAL("chooseDeskFail(int,int)"),rowNum,colNum)

