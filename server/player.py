#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import time

from util import DBState

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
            sql = 'UPDATE user SET win_times = %d,lose_times = %d,\
                    draw_times = %d WHERE id = %d'%(self.winTime,\
                    self.loseTime,self.drawTime,self.playerID)
            print "the sql is: ", sql
            self.server.database.runSQL(sql, DBState.FETCH_NONE)
        except BaseException, e:
            print "Error Upload New Player into db"
            print e

    #def updatePlayerInfoWithIDFromDatabase(self):
    #    if not self.hasLogin():
    #        raise Exception("The Player has no player ID")
    #    record = self.server.database.runSQL('SELECT nickname,password,win_time,lose_time,draw_time,create_time FROM user WHERE id = %d'%self.playerID, DBState.FETCH_ONE)
    #    #record = cursor.fetchone()
    #    if (record == None):
    #        raise Exception("Update Player Info With ID From Database failed!")
    #    self.nickname,self.password,self.winTime,self.loseTime,self.drawTime,self.createTime = record

    def updatePlayerInfoWithNicknameFromDatabase(self):
        try:
            if self.nickname == None:
                raise Exception("The Player has no nickname")
            sql = 'SELECT id,password,win_times,lose_times,draw_times,create_time FROM user WHERE nickname = "%s"'%self.nickname
            print "the sql is: ", sql
            record = self.server.database.runSQL(sql, DBState.FETCH_ONE)
            #DEBUG
            #print "the record is " ,record
            #raw_input()
            #record = cursor.fetchone()
            if (record == None):
                raise Exception("Update Player Info With nickname From Database failed!")
            self.playerID, self.password, self.winTime, self.loseTime, self.drawTime, self.createTime = record
        except BaseException,e:
            print "UpdatePlayerInfoWithNicknameFromDB Error"
            print e

    def hasNicknameInDatabase(self):
        try:
            if self.nickname == None:
                raise Exception("Has no nickname")
            if self.server.database == None:
                raise Exception("Database is not exist")
            sql = 'SELECT * FROM user WHERE nickname = "%s"'%self.nickname
            print "the sql is: ", sql
            result = self.server.database.runSQL(sql, DBState.FETCH_ONE)
            #result = cursor.fetchone()
            if result == None:
                return False
            else:
                return True
        except BaseException,e:
            print "Has Nick Name In Database Error"
            print e

    #@classmethod: cls
    def getPasswordByNickname(self, nickname, server):
        print "GettingPasswordByNickname"
        sql = 'SELECT password FROM user WHERE nickname = "%s"'%nickname
        print "the sql is: ", sql
        result =server.database.runSQL(sql, DBState.FETCH_ONE)
        #result = cursor.fetchone()
        if result == None:
            return False
        else:
            return result[0]

