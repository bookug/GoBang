#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

#to use threading.Thread:
#http://www.cppblog.com/len/archive/2008/06/24/54472.html
#http://blog.csdn.net/cnmilan/article/details/8849895
#http://python.jobbole.com/81546/

import time
import json
from PyQt4 import QtGui
from PyQt4 import QtCore
import threading
from threading import Thread

from dispatcher import Dispatcher
from net import NetStream, NET_STATE_ESTABLISHED, NET_STATE_STOP
from service import LoginService, HallService, RoomService

class Client(NetStream, QtCore.QObject):
    def __init__(self, headMode = 8, serverIP = '127.0.0.1', serverPort = 4829, sleepInterval = 0.1, parent = None):
        NetStream.__init__(self, headMode)
        QtCore.QObject.__init__(self)
        print "Client Init ",serverIP,serverPort
        self.initData(serverIP, serverPort, sleepInterval, parent)
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

    def sendToServer(self, serviceID, commandID, data):
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

    #NTC: the lock is not used!
    def run(self, lock):
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

class ClientThread(threading.Thread):
    def __init__(self,parent = None):
        threading.Thread.__init__(self)
        #enable the client to execute if terminal closed
        self.setDaemon(True)
        self.initData(parent)

    def initData(self, parent):
        self.parent = parent
        self.client = None
        self.lock = threading.RLock()

    def begin(self, client):
        self.client = client
        if client == None:
            return False;
        else:
            self.start()

    def run(self):
        self.client.run(self.lock)

