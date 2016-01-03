#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Service import Service

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


