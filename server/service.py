#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from util import ChessCellState, ChessBoardDirection
from util import PlayerSide, PlayerState  

class Service(QObject):
    def __init__(self,sid,parent = None):
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
        Service.__init__(self,self.serviceID,parent)
        self.initData()

    def initData(self):
        self.registers({\
                        1001 : self.loginHandler\
                        })

    def loginHandler(self,msg,player):
        try:
            print "Login Handler!!"
            print msg,player
            server = self.parent.parent
            data = msg['data']
            if self.server.hasNicknameInConnectedClients(data['nickname']):
                server.sendToClient(player.connectID,1001,1002,{})
                return
            player.nickname = data['nickname']

            password = player.getPasswordByNickname(player.nickname,server)

            if password == False:
                self.signUpPlayer(data,player)
                server.sendToClient(player.connectID,1001,1001,{'is_first_login':True,'table_col_num':5,'table_row_num':6})
            else:
                if password == data['password']:
                    player.updatePlayerInfoWithNicknameFromDatabase()
                    server.sendToClient(player.connectID,1001,1001,{'is_first_login':False,'table_col_num':5,'table_row_num':6})
                else:
                    server.sendToClient(player.connectID,1001,1002,{})
        except BaseException,e:
            print "LoginHandler Error"
            print e
            print data


    def signUpPlayer(self,playerInfo,player):
        try:
            #print "SignUpPlayer!!",playerInfo['nickname'],playerInfo['password']

            server = self.parent.parent
            connect = server.database.connect()
            cursor = connect.cursor()
            sqlCommand = 'INSERT INTO player(nickname,password) VALUES("%s","%s")'%(playerInfo['nickname'],playerInfo['password'])
            print sqlCommand
            cursor.execute(sqlCommand)
            print "Cursor Execute!"
            connect.commit()
            cursor.close()
            connect.close()

            player.updatePlayerInfoWithNicknameFromDatabase()
        except BaseException,e:
            self.parent.parent.log("Error while signup Player!")
            print e
            print playerInfo
            #print sqlCommand


class Desk(object):
    def __init__(self):
        self.players = {}
        self.isPlaying = False
    def addPlayer(self,player):
        if(len(self.players)<2):
            if(not self.players.has_key(player.connectID)):
                print "---------------------------------------"
                print "Adding players:",player.connectID
                print self.players
                print "---------------------------------------"
                if(type(player) == type({})):
                    print "AddPlayer Dict"
                    self.players[player.connectID] = player
                else:
                    print "Adding Player Info"
                    playerInfo = {}
                    playerInfo["nickname"] = player.nickname
                    playerInfo['id'] = player.playerID
                    playerInfo['win_times'] = player.winTime
                    playerInfo['lose_times'] = player.loseTime
                    playerInfo['draw_times'] = player.drawTime
                    self.players[player.connectID] = playerInfo

                return True
            else:
                print "already has key!"
                return False
        else:
            return False

    def leave(self,connectID):
        print "leaving Desk ",connectID
        print self.players.keys()
        if self.players.has_key(connectID):
            print connectID," leaving!!!"
            del self.players[connectID]
            return True
        else:
            return False

    def play(self):
        if(len(self.players)==2 and self.isPlaying == False):
            self.isPlaying = True
            return True
        else:
            return False
    def end(self):
        if(self.isPlaying == True):
            self.isPlaying = False
            return True
        else:
            return False

class HallService(Service):
    serviceID = 1002

    def __init__(self,parent):
        Service.__init__(self,self.serviceID,parent)
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

    def leaveHall(self,connectID):
        if self.playersInHall.has_key(connectID):
            del self.playersInHall[connectID]

            for rowNum in xrange(len(self.desks)):
                row = self.desks[rowNum]
                for colNum in xrange(len(row)):
                    self.desks[rowNum][colNum].leave(connectID)

            self.broadcastOnlineList()
            self.broadcastDeskInfo()

    def arriveHallHandler(self,msg,player):
        self.playersInHall[player.connectID] = player
        self.broadcastOnlineList()
        deskInfos = self.getCurrentDeskInfos()
        players = self.getCurrentRankList()
        self.server.sendToClient(player.connectID,1002,1003,{"desk_infos":deskInfos})
        self.server.sendToClient(player.connectID,1002,1002,{"players":players})

    def sendMessageHandler(self,msg,player):
        data = msg['data']
        chatMessage = data['message']
        createTime = data['create_time']
        self.chatMessage.append({player.nickname:chatMessage})
        self.broadcastNewChat()

    def leaveHallHandler(self,msg,player):
        self.leaveHall(player.connectID)

    def startGameHandler(self,msg,player):
        data = msg["data"]
        deskRowNum = data['row_num']%6
        deskColNum = data['col_num']%5
        if self.desks[deskRowNum][deskColNum].play() == True:
            self.broadcastDeskInfo()

    def endGameHandler(self,msg,player):
        data = msg["data"]
        deskRowNum = data['row_num']%6
        deskColNum = data['col_num']%5
        if self.desks[deskRowNum][deskColNum].end() == False:
            self.broadcastDeskInfo()
            self.broadcastRankList()

    def chooseDeskHandler(self,msg,player):
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


    #todo leaving Desk Handler
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
            self.server.sendToClient(player.connectID,1002,1004,{"message":message})
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
        connect = self.server.database.connect()
        cursor = connect.cursor()
        cursor.execute('SELECT nickname,win_times,draw_times,lose_times FROM player ORDER BY win_times DESC ')
        playerInfos = cursor.fetchall()
        players = []
        cursor.close()
        connect.close()
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


import time

class Room(object):
    def __init__(self,ID,service):
        self.players = {}#key:connectID
        self.service = service
        self.ID = ID
        self.whosTurn = PlayerSide.White
        self.startTurn = PlayerSide.White
        self.chessStepList = []
        self.chessCells = []
        self.chatList = []
        for rowNum in xrange(15):
            row = []
            for colNum in xrange(15):
                chessCell = ChessCellState.NoChess
                row.append(chessCell)
            self.chessCells.append(row)

    def restart(self):
        self.whosTurn = self.startTurn
        self.chessStepList = []
        self.chessCells = []
        for rowNum in xrange(15):
            row = []
            for colNum in xrange(15):
                chessCell = ChessCellState.NoChess
                row.append(chessCell)
            self.chessCells.append(row)

        for connectID in self.players:
            self.players[connectID]['state'] = PlayerState.NotReady

    def addChat(self,sennderConnectID,messageString):
        try:
            self.chatList.append({'nickname':self.players[sennderConnectID]['nickname'],'message':messageString})
        except BaseException,e:
            print "Error while room adding Chat "
            print e
            print self.players
    def addPlayer(self,player,connectID):
        if len(self.players)<2:
            playerInfo = {}
            playerInfo['nickname'] = player.nickname
            playerInfo['id'] = player.id
            playerInfo['win_times'] = player.winTime
            playerInfo['lose_times'] = player.loseTime
            playerInfo['draw_times'] = player.drawTime
            playerInfo['state'] = PlayerState.NotReady
            if len(self.players) == 0:
                playerInfo['side'] = PlayerSide.White
            else:
                for key in self.players:
                    player = self.players[key]
                    side = player['side']
                    if side == PlayerSide.White:
                        playerInfo['side'] = PlayerSide.Black
                    else:
                        playerInfo['side'] = PlayerSide.White
            self.players[connectID] = playerInfo

            return True
        else:
            return False

    def updatePlayers(self):
        for connectID in self.players:

            player = self.service.server.connectedClients[connectID]
            player.updatePlayerInfoWithNicknameFromDatabase()
            self.players[connectID]['win_times'] = player.winTime
            self.players[connectID]['lose_times'] = player.loseTime
            self.players[connectID]['draw_times'] = player.drawTime

    def removePlayer(self,connectID):
        if len(self.players)>0:
            if self.players.has_key(connectID):
                del self.players[connectID]
                return True

        return False

    def getReady(self,connectID):
        if self.players.has_key(connectID):
            self.players[connectID]['state'] = PlayerState.Ready
            if self.isAllReady():
                print "All is ready and start to play"
                self.startToPlay()
            else:
                self.service.broadcastPlayers(self.ID)

        else:
            raise Exception("Wrong Player Getting Ready")

    def disready(self,connectID):
        if self.players.has_key(connectID):
            self.players[connectID]['state'] = PlayerState.NotReady
            self.service.broadcastPlayers(self.ID)

    def isAllReady(self):
        if len(self.players) == 2:
            for key in self.players:
                player = self.players[key]
                if player['state'] != PlayerState.Ready:
                    return False
            return True
        return False

    def startToPlay(self):
        self.whosTurn = self.startTurn
        if(self.startTurn == PlayerSide.White):
            self.startTurn = PlayerSide.Black
        else:
            self.startTurn = PlayerSide.White

        for key in self.players:
            player = self.players[key]
            if player['side'] == self.whosTurn:
                player['state'] = PlayerState.TakingChess
            else:
                player['state'] = PlayerState.WaitingForTaking
        self.service.broadcastPlayers(self.ID)


    def getWhosTurn(self):
        connectID = False
        for key in self.players:
            if self.players[key]['side'] == PlayerState.TakingChess:
                connectID = key
        return connectID

    def addStepToStepList(self,cellState,rowNum,colNum):
        step = {'cell_state':cellState,'row_num':rowNum,'col_num':colNum}
        self.chessStepList.append(step)

    def takeAChess(self,connectID,step):
        try:
            side = step['side']
            rowNum = step['row_num']
            colNum = step['col_num']
            if self.players[connectID]['state'] == PlayerState.TakingChess:
                if side == self.whosTurn:
                    if(self.chessCells[rowNum][colNum] == ChessCellState.NoChess):
                        self.chessCells[rowNum][colNum] = side
                        self.addStepToStepList(side,rowNum,colNum)
                        self.players[connectID]['state'] = PlayerState.WaitingForTaking
                        for key in self.players:
                            if key != connectID:
                                self.players[key]['state'] = PlayerState.TakingChess
                                self.whosTurn = self.players[key]['side']
                        self.service.broadcastChessCells(self.ID)
                        self.service.broadcastPlayers(self.ID)
                        self.service.broadcastNewMessage(self.ID,(self.players[connectID]['nickname'])+u"走了"+str(rowNum)+u"行"+str(colNum)+u"列")
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except BaseException,e:
            print "Error when taking a chess"
            print e
            print step

    def getAnotherConnectID(self,connectID):
        if not self.players.has_key(connectID):
            return False
        if len(self.players) != 2:
            return False
        for key in self.players:
            if key != connectID:
                return key
    def popChessList(self):
        lastStep = self.chessStepList[len(self.chessStepList)-1]
        rowNum,colNum,cellState = lastStep['row_num'],lastStep['col_num'],lastStep['cell_state']
        if self.chessCells[rowNum][colNum] == cellState:
            self.chessCells[rowNum][colNum] = ChessCellState.NoChess
            return self.chessStepList.pop()
        else:
            return False

    def makeUndo(self,undoMakerConnectID):
        print "Make Undo"
        player = self.players[undoMakerConnectID]
        side = self.players[undoMakerConnectID]['side']
        flag = True
        if len(self.chessStepList) == 1:
            if self.chessStepList[len(self.chessStepList)-1]['cell_state'] == player['side']:
                self.popChessList()
                flag = True
            else:
                flag = False
        elif len(self.chessStepList)>1:
            self.popChessList()
            if self.chessStepList[len(self.chessStepList)-1]['cell_state'] == player['side']:
                self.popChessList()
        else:
            flag = False

        self.whosTurn = self.players[undoMakerConnectID]['side']
        self.players[undoMakerConnectID]['state'] = PlayerState.TakingChess
        self.players[self.getAnotherConnectID(undoMakerConnectID)]['state'] = PlayerState.WaitingForTaking

        return flag
    def requestForUndo(self,requesterConnectID):
        print "request for undo"
        if self.players.has_key(requesterConnectID):
            print "has key"
            self.players[requesterConnectID]['state'] = PlayerState.WaitingForUndo
            self.players[self.getAnotherConnectID(requesterConnectID)]['state'] = PlayerState.MakingDecisionForUndo
            self.service.server.sendToClient(self.getAnotherConnectID(requesterConnectID),1003,1005,{})
        else:
            print "Has no key",requesterConnectID
            print self.players.keys()
            return False



    def acceptForUndo(self,acceptUndoConnectID):
        print "Accept For undo"
        if not self.players.has_key(acceptUndoConnectID):
            return False
        print "BeforeMakeUndo:",time.ctime()
        self.makeUndo(self.getAnotherConnectID(acceptUndoConnectID))
        print "Before BroadcastPlayers:",time.ctime()
        self.service.broadcastPlayers(self.ID)
        print "Before BroadcastChessCells:",time.ctime()
        self.service.broadcastChessCells(self.ID)

    def rejectForUndo(self,rejectUndoConnectID):
        print "Reject For undo"
        if self.players[rejectUndoConnectID]['side'] == self.whosTurn:
            self.players[rejectUndoConnectID]['state'] = PlayerState.TakingChess
            self.players[self.getAnotherConnectID(rejectUndoConnectID)]['state'] = PlayerState.WaitingForTaking
        else:
            self.players[self.getAnotherConnectID(rejectUndoConnectID)]['state'] = PlayerState.TakingChess
            self.players[rejectUndoConnectID]['state'] = PlayerState.WaitingForTaking
        self.service.broadcastPlayers(self.ID)
        self.service.server.sendToClient(self.getAnotherConnectID(rejectUndoConnectID),1003,1006,{})

    def isWin(self):
        try:
            lastStep = self.chessStepList[len(self.chessStepList)-1]
            if self.isWonSinceLastStep(lastStep['row_num'],lastStep['col_num']):
                return True
            else:
                return False
        except BaseException,e:
            print "Error while isWin"
            print e

    def lastStepSide(self):
        try:
            return self.chessStepList[len(self.chessStepList)-1]['cell_state']
        except BaseException,e:
            print "Error in last Step Side"
            print self.chessStepList
            print len(self.chessStepList)-1
    def lastStepPlayerConnectID(self):
        try:
            lastSide = self.lastStepSide()
            for connectID in self.players:
                player = self.players[connectID]
                if player['side'] == lastSide:
                    return connectID
        except BaseException,e:
            print "Error in last step Player ConnectID"
            print e
            print self.players
    def isDraw(self):
        print "Is draw!",len(self.chessStepList)
        return len(self.chessStepList) == 15 * 15


    def isWonSinceLastStep(self,rowNum,colNum):
        try:
            for i in xrange(4):
                j = 2*i
                firstChessNumber = self.getSameSideChessNumber(j,rowNum,colNum,self.chessCells[rowNum][colNum])
                secondChessNumber = self.getSameSideChessNumber(j+1,rowNum,colNum,self.chessCells[rowNum][colNum])
                print "In side ",i," has ",firstChessNumber,secondChessNumber
                if firstChessNumber+secondChessNumber>=4:
                    return True
            return False
        except BaseException,e:
            print "Error while isWonSinceLastStep"
            print e
    @staticmethod
    def isRowNumAvailable(m):
        if m<15 and m>=0:
            return True
        else:
            return False

    @staticmethod
    def isColNumAvailable(n):
        if n<15 and n>=0:
            return True
        else:
            return False

    def getSameSideChessNumber(self,direction,rowNum,colNum,side):
        sum = 0
        currentSide = self.chessCells[rowNum][colNum]
        m,n = rowNum,colNum
        if direction == ChessBoardDirection.Down:
            for i in range(4):
                m = m + 1
                print "Judging Down side"
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    print "M,N Available ","currentSide:",side,"NextSide:",self.chessCells[m][n]
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                        print "get one"
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.Up:
            for i in range(4):
                m = m - 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.Left:
            for i in range(4):
                n = n - 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.Right:
            for i in range(4):
                n = n + 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.UpLeft:
            for i in range(4):
                m = m - 1
                n = n - 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.UpRight:
            for i in range(4):
                m = m - 1
                n = n + 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.DownLeft:
            for i in range(4):
                m = m + 1
                n = n + 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == ChessBoardDirection.DownRight:
            for i in range(4):
                m = m + 1
                n = n - 1
                if Room.isRowNumAvailable(m) and Room.isColNumAvailable(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        return sum    

    def leaveRoom(self,leaverConnectID,connectID):
        anotherConnectID = self.getAnotherConnectID(leaverConnectID)
        if anotherConnectID == False:
            self.removePlayer(leaverConnectID)
        else:
            if self.players[anotherConnectID]['state'] == PlayerState.Ready\
            or self.players[anotherConnectID]['state'] == PlayerState.NotReady:
                self.removePlayer(leaverConnectID)
            else:
                self.removePlayer(leaverConnectID)
                self.giveWinResultInDatabaseAndGiveInfo(anotherConnectID)
                self.giveLoseResultInDatabaseAndGiveInfo(leaverConnectID)
                self.service.broadcastPlayers(self.ID)

    def giveWinResultInDatabaseAndGiveInfo(self,connectID):
        try:
            player = self.service.server.connectedClients[connectID]
            player.winTime = player.winTime + 1
            player.uploadNewPlayerInfoToDatabase()
            self.updatePlayers()
            self.service.server.sendToClient(connectID,1003,1007,{})
        except BaseException,e:
            print "Error in give win result "
            print e
    def giveLoseResultInDatabaseAndGiveInfo(self,connectID):
        try:
            player = self.service.server.connectedClients[connectID]
            player.loseTime = player.loseTime + 1
            player.uploadNewPlayerInfoToDatabase()
            self.updatePlayers()
            self.service.server.sendToClient(connectID,1003,1008,{})
        except BaseException,e:
            print "Error in give lose result "
            print e
    def giveDrawResultInDatabaseAndGiveInfo(self,connectID):
        player = self.service.server.connectedClients[connectID]
        player.drawTime = player.drawTime + 1
        player.uploadNewPlayerInfoToDatabase()
        self.updatePlayers()
        self.service.server.sendToClient(connectID,1003,1009,{})

class RoomService(Service):
    serviceID = 1003
    def __init__(self,parent):
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
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u"准备好了")
    def disreadyHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].disready(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u"取消准备")
    def requestUndoHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        print "Get a undo request"
        self.rooms[roomID].requestForUndo(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u"请求悔棋")
    def acceptUndoHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].acceptForUndo(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u"接受悔棋")
    def notAcceptUndoHandler(self,msg,player):
        data = msg['data']
        roomID = data['room_id']
        self.rooms[roomID].rejectForUndo(player.connectID)
        self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u"拒绝悔棋")
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
            self.broadcastNewMessage(roomID,unicode(self.rooms[roomID].players[player.connectID]['nickname'])+u"居然认输了！")
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

