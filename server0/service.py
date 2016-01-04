#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from util import Direction, DBState, PlayerSide, PlayerState  
from util import *
from game import Desk, Room

class Service(QObject):
    def __init__(self, sid, parent = None):
        QObject.__init__(self)
        self.service_id = sid
        self.commands = {}
        self.parent = parent
        if self.parent!=None:
            self.server = self.parent.parent

    def setParent(self,dispatcher):
        self.parent = dispatcher

    def Server(self):
        return self.parent.parent

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


class LoginService(Service):
    serviceID = 1001

    def __init__(self,parent = None):
        Service.__init__(self, self.serviceID, parent)
        self.initData()

    def initData(self):
        self.registers({\
                        1001 : self.loginHandler\
                        })

    def loginHandler(self, msg, player):
        try:
            print "Login Handler!!"
            print msg, player
            server = self.parent.parent
            data = msg['data']
            if self.server.hasNicknameInConnectedClients(data['nickname']):
                server.sendToClient(player.connectID, 1001, 1002, {})
                return
            player.nickname = data['nickname']

            password = player.getPasswordByNickname(player.nickname, server)
            if password == False:
                self.signUpPlayer(data, player)
                server.sendToClient(player.connectID, 1001, 1001, {'is_first_login':True,'table_col_num':5,'table_row_num':6})
            else:
                if password == data['password']:
                    player.updatePlayerInfoWithNicknameFromDatabase()
                    server.sendToClient(player.connectID, 1001, 1001, {'is_first_login':False,'table_col_num':5,'table_row_num':6})
                else:
                    server.sendToClient(player.connectID, 1001, 1002, {})
        except BaseException,e:
            print "LoginHandler Error"
            print e
            print data

    def signUpPlayer(self, playerInfo, player):
        try:
            #print "SignUpPlayer!!",playerInfo['nickname'],playerInfo['password']

            server = self.parent.parent
            sql = 'INSERT INTO user(nickname,password) VALUES("%s","%s")'%(playerInfo['nickname'],playerInfo['password'])
            server.database.runSQL(sql, DBState.FETCH_NONE)
            player.updatePlayerInfoWithNicknameFromDatabase()
        except BaseException,e:
            log("Error while signup Player!")
            print e
            print playerInfo


class HallService(Service):
    serviceID = 1002

    def __init__(self, parent = None):
        Service.__init__(self, self.serviceID, parent)
        self.initData()

    def initData(self):
        self.registers({\
                        1001 : self.arriveHallHandler,\
                        1002 : self.sendMessageHandler,\
                        1003 : self.leaveHallHandler,\
                        1004 : self.chooseDeskHandler,\
                        1005 : self.leaveDeskHandler,\
                        1006 : self.startGameHandler,\
                        1007 : self.endGameHandler\
                        })
        self.playersInHall = {}
        self.chatMessage = []
        self.desks = []
        for rowNum in xrange(6):
            row = []
            for colNum in xrange(5):
                row.append(Desk())
            self.desks.append(row)
        self.server = self.parent.parent

    def leaveHall(self, connectID):
        if self.playersInHall.has_key(connectID):
            del self.playersInHall[connectID]
            for rowNum in xrange(len(self.desks)):
                row = self.desks[rowNum]
                for colNum in xrange(len(row)):
                    self.desks[rowNum][colNum].leave(connectID)
            self.broadcastOnlineList()
            self.broadcastDeskInfo()

    def arriveHallHandler(self, msg, player):
        self.playersInHall[player.connectID] = player
        self.broadcastOnlineList()
        deskInfos = self.getCurrentDeskInfos()
        players = self.getCurrentRankList()
        self.server.sendToClient(player.connectID, 1002, 1003, {"desk_infos":deskInfos})
        self.server.sendToClient(player.connectID, 1002, 1002, {"players":players})

    def sendMessageHandler(self, msg, player):
        data = msg['data']
        chatMessage = data['message']
        createTime = data['create_time']
        self.chatMessage.append({player.nickname:chatMessage})
        self.broadcastNewChat()

    def leaveHallHandler(self, msg, player):
        self.leaveHall(player.connectID)

    def startGameHandler(self, msg, player):
        data = msg["data"]
        deskRowNum = data['row_num']%6
        deskColNum = data['col_num']%5
        if self.desks[deskRowNum][deskColNum].play() == True:
            self.broadcastDeskInfo()

    def endGameHandler(self, msg, player):
        data = msg["data"]
        deskRowNum = data['row_num']%6
        deskColNum = data['col_num']%5
        if self.desks[deskRowNum][deskColNum].end() == False:
            self.broadcastDeskInfo()
            self.broadcastRankList()

    def chooseDeskHandler(self, msg, player):
        try:
            data = msg["data"]
            deskRowNum = int(data['row_num']%6)
            deskColNum = int(data['col_num']%5)
            info = {}
            info['row_num'] = deskRowNum
            info['col_num'] = deskColNum
            if self.desks[deskRowNum][deskColNum].addPlayer(player) == True:
                info['is_choose_desk_success'] = True
                info['player_num'] = len(self.desks[deskRowNum][deskColNum].players)
            else:
                info['is_choose_desk_success'] = False
            self.server.sendToClient(player.connectID,1002,1005,info)
            if info['is_choose_desk_success'] == True:
                self.broadcastDeskInfo()
        except BaseException,e:
            print "Error In Choose Desk Handler"
            print e
            print self.desks[deskRowNum][deskColNum]

    def leaveDeskHandler(self,msg,player):
        data = msg["data"]
        deskRowNum = data['row_num']%6
        deskColNum = data['col_num']%5
        print "LeaveDeskHandler:",deskRowNum,",",deskColNum
        info = {}
        if self.desks[deskRowNum][deskColNum].leave(player.connectID) == True:
            info['is_leave_desk_success'] = True
        else:
            info['is_leave_desk_success'] = False

        if info['is_leave_desk_success'] == True:
            self.broadcastDeskInfo()

    def broadcastNewChat(self):
        message = self.chatMessage[len(self.chatMessage)-1]
        for key in self.playersInHall:
            player = self.playersInHall[key]
            self.server.sendToClient(player.connectID, 1002, 1004, {"message":message})

    def broadcastOnlineList(self):
        players = []
        for key in self.playersInHall:
            player = self.playersInHall[key]
            players.append({
                'nickname':player.nickname,\
                'win_times':player.winTime,\
                'lose_times':player.loseTime,\
                'draw_times':player.drawTime\
            })
        for key in self.playersInHall:
            player = self.playersInHall[key]
            self.server.sendToClient(player.connectID,1002,1001,{"players":players})

    def getCurrentDeskInfos(self):
        deskInfos = []
        for row in xrange(len(self.desks)):
            for col in xrange(len(self.desks[row])):
                deskInfo = {}
                deskInfo["row_num"] = row
                deskInfo["col_num"] = col
                deskInfo["players"] = self.desks[row][col].players
                deskInfo["is_playing"] = self.desks[row][col].isPlaying
                deskInfos.append(deskInfo)
        return deskInfos

    def broadcastDeskInfo(self):
        try:
            deskInfos = self.getCurrentDeskInfos()
            for key in self.playersInHall:
                player = self.playersInHall[key]
                self.server.sendToClient(player.connectID,1002,1003,{"desk_infos":deskInfos})
        except BaseException,e:
            print "Error in broadcast Desk Info"
            print e
            print self.getCurrentRankList()

    def getCurrentRankList(self):
        sql = 'SELECT nickname,win_times,draw_times,lose_times FROM user ORDER BY win_times DESC '
        playerInfos = self.server.database.runSQL(sql, DBState.FETCH_ALL)
        players = []
        print "Get Current Ranklist"
        for playerInfo in playerInfos:
            player = {}
            player['nickname'] = playerInfo[0]
            player['win_times'] = playerInfo[1]
            player['draw_times'] = playerInfo[2]
            player['lose_times'] = playerInfo[3]
            players.append(player)
        print players
        return players

    def broadcastRankList(self):
        players = self.getCurrentRankList()
        print "Broadcast Ranklist"
        print players
        for key in self.playersInHall:
            player = self.playersInHall[key]
            self.server.sendToClient(player.connectID,1002,1003,{"players":players})


class RoomService(Service):
    serviceID = 1003

    def __init__(self,parent = None):
        Service.__init__(self,self.serviceID,parent)
        self.initData()

    def initData(self):
        self.registers({\
                        1001 : self.arriveRoomHandler,\
                        1002 : self.sendMessageHandler,\
                        1003 : self.leaveRoomHandler,\
                        1004 : self.takeChessHandler,\
                        1005 : self.getReadyHandler,\
                        1006 : self.disreadyHandler,\
                        1007 : self.requestUndoHandler,\
                        1008 : self.acceptUndoHandler,\
                        1009 : self.notAcceptUndoHandler,\
                        1010 : self.commitLostHandler,\
                        })
        self.rooms = []
        for i in xrange(31):
            self.rooms.append(Room(i,self))

    def arriveRoomHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].addPlayer(player,player.connectID)
        self.broadcastPlayers(roomID)

    def removePlayerFromAllRooms(self,connectID):
        for room in self.rooms:
            room.leaveRoom(connectID,connectID)

    def sendMessageHandler(self,msg,player):
        try:
            data = msg['data']
            roomID = data['room_id']
            messageString = data['message']
            self.rooms[roomID].addChat(player.connectID,messageString)
            self.broadcastLastChat(roomID)
        except BaseException,e:
            print "Error sending mesaage handler"
            print e
            print msg

    def leaveRoomHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].leaveRoom(player.connectID,player.connectID)
        self.broadcastPlayers(roomID)

    def takeChessHandler(self,msg,player):
        try:
            data =msg['data']
            roomID = data['room_id']
            rowNum = data['row_num']
            colNum = data['col_num']
            try:
                step = {}
                step['side'] = self.rooms[roomID].players[player.connectID]['side']
                step['row_num'] = rowNum
                step['col_num'] = colNum
            except BaseException,e:
                print "Init Step Error"
                print e
                print self.rooms[roomID].players
            self.rooms[roomID].takeAChess(player.connectID,step)
            #DEBUG
            #print "after takeAChess!"
            #raw_input()
            try:
                if self.rooms[roomID].isWin():

                    winnerConnectID = self.rooms[roomID].lastStepPlayerConnectID()
                    loserConnectID = self.rooms[roomID].getAnotherConnectID(winnerConnectID)
                    self.rooms[roomID].giveWinResultInDatabaseAndGiveInfo(winnerConnectID)
                    self.rooms[roomID].giveLoseResultInDatabaseAndGiveInfo(loserConnectID)
                    self.rooms[roomID].restart()
                    self.broadcastPlayers(roomID)
                    self.broadcastChessCells(roomID)
                elif self.rooms[roomID].isDraw():
                    oneConnectID = player.connectID
                    anotherConnectID = self.rooms[roomID].getAnotherConnectID(oneConnectID)
                    self.rooms[roomID].giveDrawResultInDatabaseAndGiveInfo(oneConnectID)
                    self.rooms[roomID].giveDrawResultInDatabaseAndGiveInfo(anotherConnectID)
                    self.rooms[roomID].restart()
                    self.broadcastPlayers(roomID)
                    self.broadcastChessCells(roomID)
            except BaseException,e:
                print "Error while Judge and take action"
                print e
        except BaseException,e:
            print "Error in taking Chess"
            print e
            print msg

    def getReadyHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].getReady(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u" prepared")
    def disreadyHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].disready(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u" cancel prepared")

    def requestUndoHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        print "Get a undo request"
        self.rooms[roomID].requestForUndo(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u" want to withdraw")
    def acceptUndoHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].acceptForUndo(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u" admit to withdraw")

    def notAcceptUndoHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].rejectForUndo(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u" reject to withdraw")

    def commitLostHandler(self,msg,player):
        try:
            data = msg['data']
            roomID = data['room_id']
            loserConnectID = player.connectID
            winnerConnectID = self.rooms[roomID].getAnotherConnectID(loserConnectID)
            self.rooms[roomID].giveWinResultInDatabaseAndGiveInfo(winnerConnectID)
            self.rooms[roomID].giveLoseResultInDatabaseAndGiveInfo(loserConnectID)
            self.rooms[roomID].restart()
            self.broadcastPlayers(roomID)
            self.broadcastChessCells(roomID)
            self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u" admit defeat")
        except BaseException,e:
            print "Error in commit Lost handler"
            print e
            print msg['data']

    def broadcastLastChat(self,roomID):
        try:
            room =self.rooms[roomID]
            lastChat = room.chatList[len(room.chatList)-1]
            data = {}
            data['nickname'] = lastChat['nickname']
            data['message'] = lastChat['message']
            self.broadcast(roomID,1003,1001,data)
        except BaseException,e:
            print "Error in broadcast Last Chat"
            print e
            print self.rooms[roomID]

    def broadcastChessCells(self,roomID):
        room = self.rooms[roomID]
        chessCells = room.chessCells
        self.broadcast(roomID,1003,1002,{"chess_cells":chessCells})

    def broadcastPlayers(self,roomID):
        room = self.rooms[roomID]
        self.broadcast(roomID,1003,1003,{"players":room.players})

    def broadcastNewMessage(self,roomID,eventInfoString):
        try:
            print "Send New Message!!!"
            print eventInfoString
            self.broadcast(roomID,1003,1004,{"event":eventInfoString})
        except BaseException,e:
            print "Error in broadcast New Mesage"
            print e
            print eventInfoString

    def broadcast(self,roomID,serviceID,commandID,data):
        room = self.rooms[roomID]
        for connectID in room.players:
            self.server.sendToClient(connectID,serviceID,commandID,data)

