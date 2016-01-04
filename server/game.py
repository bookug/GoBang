#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time

from util import CellState, Direction, DBState, PlayerSide, PlayerState  
from util import *

#NTC: used in hall,  different from Desk in client/board.py
class Desk(object): 
    def __init__(self):
        self.players = {}
        self.isPlaying = False

    def addPlayer(self, player):
        if(len(self.players) < 2):
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

    def leave(self, connectID):
        print "leaving Desk ",connectID
        print self.players.keys()
        if self.players.has_key(connectID):
            print connectID," leaving!!!"
            del self.players[connectID]
            return True
        else:
            return False

    def play(self):
        if(len(self.players) == 2 and self.isPlaying == False):
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


class Room(object):
    def __init__(self, ID, service):
        self.players = {}     #key:connectID
        self.service = service
        self.ID = ID
        self.whosTurn = PlayerSide.WHITE
        self.startTurn = PlayerSide.WHITE
        self.chessStepList = []
        self.chessCells = []
        self.chatList = []
        for rowNum in xrange(15):
            row = []
            for colNum in xrange(15):
                chessCell = CellState.EMPTY
                row.append(chessCell)
            self.chessCells.append(row)

    def restart(self):
        self.whosTurn = self.startTurn
        self.chessStepList = []
        self.chessCells = []
        for rowNum in xrange(15):
            row = []
            for colNum in xrange(15):
                chessCell = CellState.EMPTY
                row.append(chessCell)
            self.chessCells.append(row)

        for connectID in self.players:
            self.players[connectID]['state'] = PlayerState.NOT_READY

    def addChat(self, senderConnectID, messageString):
        try:
            self.chatList.append({'nickname':self.players[senderConnectID]['nickname'],'message':messageString})
        except BaseException,e:
            print "Error while room adding Chat "
            print e
            print self.players

    def addPlayer(self, player, connectID):
        if len(self.players) < 2:
            playerInfo = {}
            playerInfo['nickname'] = player.nickname
            playerInfo['id'] = player.playerID
            playerInfo['win_times'] = player.winTime
            playerInfo['lose_times'] = player.loseTime
            playerInfo['draw_times'] = player.drawTime
            playerInfo['state'] = PlayerState.NOT_READY
            if len(self.players) == 0:
                playerInfo['side'] = PlayerSide.WHITE #default
            else:
                for key in self.players:
                    player = self.players[key]
                    side = player['side']
                    if side == PlayerSide.WHITE:
                        playerInfo['side'] = PlayerSide.BLACK
                    else:
                        playerInfo['side'] = PlayerSide.WHITE
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

    def removePlayer(self, connectID):
        if len(self.players) > 0:
            if self.players.has_key(connectID):
                del self.players[connectID]
                return True
        return False

    def getReady(self,connectID):
        if self.players.has_key(connectID):
            self.players[connectID]['state'] = PlayerState.READY
            if self.isAllReady():
                print "All is ready and start to play"
                self.startToPlay()
            else:
                self.service.broadcastPlayers(self.ID)
        else:
            raise Exception("Wrong Player Getting Ready")

    def disready(self,connectID):
        if self.players.has_key(connectID):
            self.players[connectID]['state'] = PlayerState.NOT_READY
            self.service.broadcastPlayers(self.ID)

    def isAllReady(self):
        if len(self.players) == 2:
            for key in self.players:
                player = self.players[key]
                if player['state'] != PlayerState.READY:
                    return False
            return True
        return False

    def startToPlay(self):
        self.whosTurn = self.startTurn
        if(self.startTurn == PlayerSide.WHITE):
            self.startTurn = PlayerSide.BLACK
        else:
            self.startTurn = PlayerSide.WHITE
        for key in self.players:
            player = self.players[key]
            if player['side'] == self.whosTurn:
                player['state'] = PlayerState.TAKING_CHESS
            else:
                player['state'] = PlayerState.WAITING_FOR_TAKING
        self.service.broadcastPlayers(self.ID)

    def getWhosTurn(self):
        connectID = False
        for key in self.players:
            if self.players[key]['side'] == PlayerState.TAKING_CHESS:
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
            if self.players[connectID]['state'] == PlayerState.TAKING_CHESS:
                if side == self.whosTurn:
                    if(self.chessCells[rowNum][colNum] == CellState.EMPTY):
                        self.chessCells[rowNum][colNum] = side
                        self.addStepToStepList(side,rowNum,colNum)
                        self.players[connectID]['state'] = PlayerState.WAITING_FOR_TAKING
                        for key in self.players:
                            if key != connectID:
                                self.players[key]['state'] = PlayerState.TAKING_CHESS
                                self.whosTurn = self.players[key]['side']
                        self.service.broadcastChessCells(self.ID)
                        self.service.broadcastPlayers(self.ID)
                        self.service.broadcastNewMessage(self.ID,(self.players[connectID]['nickname'])+u" take "+str(rowNum)+u" row "+str(colNum)+u" col")
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
            self.chessCells[rowNum][colNum] = CellState.EMPTY
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
        self.players[undoMakerConnectID]['state'] = PlayerState.TAKING_CHESS
        self.players[self.getAnotherConnectID(undoMakerConnectID)]['state'] = PlayerState.WAITING_FOR_TAKING
        return flag

    def requestForUndo(self,requesterConnectID):
        print "request for undo"
        if self.players.has_key(requesterConnectID):
            print "has key"
            self.players[requesterConnectID]['state'] = PlayerState.WAITING_FOR_UNDO
            self.players[self.getAnotherConnectID(requesterConnectID)]['state'] = PlayerState.MAKING_DECISION_FOR_UNDO
            self.service.server.sendToClient(self.getAnotherConnectID(requesterConnectID),1003,1005,{})
        else:
            print "Has no key",requesterConnectID
            print self.players.keys()
            return False

    def acceptForUndo(self, acceptUndoConnectID):
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
            self.players[rejectUndoConnectID]['state'] = PlayerState.TAKING_CHESS
            self.players[self.getAnotherConnectID(rejectUndoConnectID)]['state'] = PlayerState.WAITING_FOR_TAKING
        else:
            self.players[self.getAnotherConnectID(rejectUndoConnectID)]['state'] = PlayerState.TAKING_CHESS
            self.players[rejectUndoConnectID]['state'] = PlayerState.WAITING_FOR_TAKING
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
            print len(self.chessStepList) - 1

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
                firstChessNumber = self.getSameSideCount(j,rowNum,colNum,self.chessCells[rowNum][colNum])
                secondChessNumber = self.getSameSideCount(j+1,rowNum,colNum,self.chessCells[rowNum][colNum])
                print "In side ",i," has ",firstChessNumber,secondChessNumber
                if firstChessNumber+secondChessNumber>=4:
                    return True
            return False
        except BaseException,e:
            print "Error while isWonSinceLastStep"
            print e

    def getSameSideCount(self,direction,rowNum,colNum,side):
        sum = 0
        m,n = rowNum,colNum
        if direction == Direction.DOWN:
            for i in range(4):
                m = m + 1
                print "Judging Down side"
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    print "M,N Available ","currentSide:",side,"NextSide:",self.chessCells[m][n]
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                        print "get one"
                    else:
                        break
                else:
                    break
        elif direction == Direction.UP:
            for i in range(4):
                m = m - 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == Direction.LEFT:
            for i in range(4):
                n = n - 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == Direction.RIGHT:
            for i in range(4):
                n = n + 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == Direction.UP_LEFT:
            for i in range(4):
                m = m - 1
                n = n - 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == Direction.UP_RIGHT:
            for i in range(4):
                m = m - 1
                n = n + 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == Direction.DOWN_LEFT:
            for i in range(4):
                m = m + 1
                n = n + 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
                    if side == self.chessCells[m][n]:
                        sum = sum + 1
                    else:
                        break
                else:
                    break
        elif direction == Direction.DOWN_RIGHT:
            for i in range(4):
                m = m + 1
                n = n - 1
                if Util.isRowNumValid(m) and Util.isColNumValid(n):
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
            if self.players[anotherConnectID]['state'] == PlayerState.READY\
            or self.players[anotherConnectID]['state'] == PlayerState.NOT_READY:
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

