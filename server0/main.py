#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import json
import time

from net import NetHost, NET_NEW, NET_LEAVE, NET_TIMER, NET_DATA
from database import Database
from dispatcher import Dispatcher
from player import Player
from service import LoginService, HallService, RoomService
from util import *

class Server(NetHost):
    def __init__(\
            self,\
            headMode = 8,\
            port = 4829,\
            timeInterval = 10000,\
            sleepInterval = 0.5,\
            databasePath = './.gobang.db'\
            ):
        NetHost.__init__(self,headMode)
        self.initData(headMode,port,timeInterval,sleepInterval,databasePath)
        self.setup()

    def __del__(self):
        print "Server Lost!"

    def setup(self):
        self.setupDatabase()
        self.setupDispatcher()
        self.setupServer()
        print self.connectedClients

    def setupServer(self):
        try:
            self.startup(self.port)
            print '[',time.ctime(),']','Server startup at port:',self.port
            self.settimer(self.timerInterval)
        except BaseException,e:
            print "Error while setup server"
            print e

    def setupDispatcher(self):
        self.dispatcher.setParent(self)
        services = {}
        services[LoginService.serviceID] = LoginService(self.dispatcher)
        services[HallService.serviceID]  = HallService(self.dispatcher)
        services[RoomService.serviceID] = RoomService(self.dispatcher)
        self.dispatcher.registers(services)
        print "Setup Dispatcher"
        print services

    def setupDatabase(self):
        self.database.connect()
        try:
            self.database.setup()
        except BaseException,e:
            print "Error while setup db"
            print e
    
    def initData(self,headMode,port,timeInterval,sleepInterval,databasePath):
        self.database = Database(databasePath)
        try:
            self.headMode = headMode
            self.port = port
            self.timerInterval = timeInterval
            self.sleepInterval = sleepInterval
            self.dispatcher = Dispatcher()
            self.connectedClients = {}
            print "Type of clients = ",type(self.connectedClients)
        except BaseException,e:
            print "Error while server init data"
            print e

    def hasNicknameInConnectedClients(self, nickname):
        for connectID in self.connectedClients:
            if self.connectedClients[connectID].nickname == nickname:
                print "Has Nickname connected!!"
                print connectID," ",nickname
                return True
        return False

    def connectionEventHandler(self,connectID,messageString = ''):
        print "clientsType is ",type(self.connectedClients)
        try:
            log(str(connectID) + " comes")
            self.connectedClients[connectID] = Player(connectID,self)
            #self.sendToClient(connectID,1001,1001,"Fuck you in connection handler")
        except BaseException,e:
            log("Error in Connection Event")
            print type(self.connectedClients)
            print e

    def disconnectionEventHandler(self,connectID,messageString = ''):
        try:
            log(str(connectID) + ' leaves')
            del self.connectedClients[connectID]
            self.dispatcher.services[1002].leaveHall(connectID)
            self.dispatcher.services[1003].removePlayerFromAllRooms(connectID)
        except BaseException,e:
            log("Error in disconnect")
            print e

    def timerEventHandler(self,connectID,messageString = ''):
        #log(str(connectID) + ":timer triggered!")
        #print "Clients type = " ,type(self.connectedClients)
        pass

    def messageEventHandler(self, connectID, message = ''):
        try:
            log(str(connectID) + " sends a message!")
            self.dispatcher.dispatch(message,self.connectedClients[connectID])
            #self.sendToClient(connectID,1001,1001,"Fuck you in messageEventHandler")
        except BaseException,e:
            log("Error in message Event Handler")
            print message
            print e

    def sendToClient(self, connectID, serviceID, commandID, data):
        message = {}
        message['create_time'] = time.time()
        message['service_id'] = serviceID
        message['command_id'] = commandID
        message['data'] = data
        messageString = json.dumps(message)
        self.send(connectID,messageString)
        print "Send message To ",connectID,":",messageString

    def run(self):
        while True:
            try:
                try:
                    time.sleep(self.sleepInterval)
                except KeyboardInterrupt, e:
                    break;
                except BaseException, e:
                    print "Error while Server Sleep"
                    print e
                try:
                    try:
                        self.process()
                    except BaseException, e:
                        print "Error while Server Processing!"
                        print e
                    try:
                        eventType , connectID , lparam ,messageString = self.read()
                    except BaseException, e:
                        print "Error while Server Reading()"
                    try:
                        if eventType < 0:
                            #print "Wrong Event:",eventType
                            continue
                    except BaseException, e:
                        print "Errow while Finding Wrong Event"
                    try:
                        if eventType == NET_NEW:
                            self.connectionEventHandler(connectID,messageString)
                        if eventType == NET_LEAVE:
                            self.disconnectionEventHandler(connectID,messageString)
                        if eventType == NET_TIMER:
                            self.timerEventHandler(connectID,messageString)
                        if eventType == NET_DATA:
                            #self.sendToClient(connectID,1001,1001,"Fuck you in NETDATA")
                            message = None
                            try:
                                message = json.loads(messageString)
                                self.messageEventHandler(connectID,message)
                            except BaseException, e:
                                logTime()
                                print e
                    except BaseException, e:
                        log("Error while handling Event")
                        print e
                except KeyboardInterrupt, e:
                    break
                except BaseException, e:
                    print "Error while server working in loop"
                    print e
            except KeyboardInterrupt, e:
                break
            except BaseException, e:
                print "Error while server loop"
                print e

if __name__ == '__main__':
    server = Server()
    server.run()

