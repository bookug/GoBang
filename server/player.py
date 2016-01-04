#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import time

class Player:
    def __init__(self, connectID, server):
        try:
            self.connectID = connectID
            self.server = server
            self.initData()
        except BaseException, e:
            print time.ctime(), "Player Init Error"
            print e

    def initData(self):
        self.playerID = None
        self.nickname = None
        self.password = None
        self.winTime  = 0
        self.loseTime = 0
        self.drawTime = 0
        self.createTime = None

    def setLoginInfo(self,playerID,nickname,password,winTime,loseTime,drawTime,createTime):
        self.playerID = playerID
        self.nickname = nickname
        self.password = password
        self.createTime = createTime

    def hasLogin(self):
        if type(self.playerID) == type(None):
            return False
        else:
            return True

    def uploadNewPlayerInfoToDatabase(self):
        try:
            print "Upload New Player!"
            connect =self.server.database.connect()
            cursor = connect.cursor()
            cursor.execute('UPDATE player SET win_times = %d,lose_times = %d,draw_times = %d WHERE id = %d'%(self.winTime,self.loseTime,self.drawTime,self.id))
            connect.commit()
            cursor.close()
            connect.close()
        except BaseException,e:
            print "Error Upload New Plyaer into db"
            print e


    def updatePlayerInfoWithIDFromDatabase(self):
        if not self.hasLogin():
            raise Exception("The Player has no player ID")
        connect = self.server.database.connect()
        cursor = connect.cursor()
        cursor.execute('SELECT nickname,password,win_time,lose_time,draw_time,create_time FROM player WHERE id = %d'%self.playerID)
        record = cursor.fetchone()
        cursor.close()
        connect.close()
        if(record == None):
            raise Exception("Update Player Info With ID From Database failed!")

        self.nickname,self.password,self.winTime,self.loseTime,self.drawTime,self.createTime = record

    def updatePlayerInfoWithNicknameFromDatabase(self):
        try:
            if self.nickname == None:
                raise Exception("The Player has no nickname")
            connect = self.server.database.connect()
            cursor = connect.cursor()
            cursor.execute('SELECT id,password,win_times,lose_times,draw_times,create_time FROM player WHERE nickname = "%s"'%self.nickname)
            record = cursor.fetchone()
            if(record == None):
                raise Exception("Update Player Info With nickname From Database failed!")

            self.id,self.password,self.winTime,self.loseTime,self.drawTime,self.createTime = record
        except BaseException,e:
            print "UpdatePlayerInfoWithNicknameFromDB Error"
            print e

    def hasNicknameInDatabase(self):
        try:
            if self.nickname == None:
                raise Exception("Has no nickname")
            if self.server.database == None:
                raise Exception("Database is not exist")
            connect = self.server.database.connect()
            if connect == None:
                raise Exception('Connection failed!')
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM player WHERE nickname = "%s"'%self.nickname)
            result = cursor.fetchone()
            cursor.close()
            connect.close()
            if result == None:
                return False
            else:
                return True
        except BaseException,e:
            print "Has Nick Name In Database Error"
            print e

    @staticmethod
    def getPasswordByNickname(nickname,server):
        print "GettingPasswordByNickname"

        print "Server.server",server

        print "AfterGetPasswordByNickname"
        connect =server.database.connect()
        cursor = connect.cursor()
        cursor.execute('SELECT password FROM player WHERE nickname = "%s"'%nickname)
        result = cursor.fetchone()
        cursor.close()
        connect.close()
        if result == None:
            return False
        else:
            return result[0]

