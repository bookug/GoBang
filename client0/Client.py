#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'
from Dispatcher import Dispatcher
from netstream import netstream,NET_STATE_ESTABLISHED,NET_STATE_STOP
import time
import json
from PyQt4 import QtGui
from PyQt4 import QtCore
from LoginService import LoginService
from HallService import HallService
from RoomService import RoomService

class Client(netstream,QtCore.QObject):
    def __init__(self,headMode = 8,serverIP = '123.57.165.67',serverPort = 4829,sleepInterval = 0.1,parent = None):
        netstream.__init__(self,headMode)
        QtCore.QObject.__init__(self)
        print "Client Init ",serverIP,serverPort
        self.initData(serverIP,serverPort,sleepInterval,parent)
        self.setup()
        self.parent.parent.connect(self,QtCore.SIGNAL('serverCrashedAlert()'),self.parent.parent.serverCrashedAlert)
    def initData(self,serverIP,serverPort,sleepInterval,parent):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.sleepInterval = sleepInterval
        self.dispatcher = Dispatcher()
        self.parent = parent
        self.isAlive = True
        self.hasBegan = False
    def killClient(self):
        self.isAlive = False

    def setup(self):
        self.setupDispatcher()
        self.setupClient()

    def setupDispatcher(self):
        self.dispatcher.setParent(self)
        services = {\
            1001 : LoginService(self.dispatcher),\
            1002 : HallService(self.dispatcher),\
            1003 : RoomService(self.dispatcher)
        }
        self.dispatcher.registers(services)

    def setupClient(self):
        print self.serverPort,"\n",self.serverIP
        self.connect(self.serverIP,self.serverPort)
        self.nodelay(0)
        self.nodelay(1)

    def sendToServer(self,serviceID,commandID,data):
        message = {}
        message['create_time'] = time.time()
        message['service_id'] = serviceID
        message['command_id'] = commandID
        message['data'] = data
        try:
            messageString = json.dumps(message)
        except TypeError,e:
            print "Error while dumping json"
            print e
            print message

        print "Sending Messgae:",message
        self.send(messageString)

    #notices the lock is not used!
    def run(self,lock):
        try:
            while self.isAlive:

                time.sleep(self.sleepInterval)
                self.process()
                if self.state == NET_STATE_ESTABLISHED:
                    self.hasBegan = True

                if self.hasBegan == True:
                    print "Current State:",self.state
                    if self.state == NET_STATE_STOP:
                        self.emit(QtCore.SIGNAL('serverCrashedAlert()'))
                        self.isAlive = False
                    messageString = self.recv()
                    #drop empty Message
                    if(messageString == ''):
                        continue
                    else:
                        print "Message:",messageString
                    try:
                        message = json.loads(messageString)

                    except ValueError,e:
                        message = messageString
                    self.dispatcher.dispatch(message,self)

        except BaseException,e:
            print time.ctime(),":Error in running Client"
            print e
