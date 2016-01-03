#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'
from login_window import Ui_LoginWindow
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Client import Client
from ClientThread import ClientThread
from Hall import Hall
class LoginWindow (QWidget):
    def __init__(self,director):
        QWidget.__init__(self)
        self.director = director
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.loginButton,SIGNAL('clicked()'),self.onLoginButtonClickedEvent)

    def onLoginButtonClickedEvent(self):
        if self.director.clientThread == None:
            self.director.clientThread = ClientThread(self.director)
            client = Client(8,str(self.ui.ServerIPText.text()),self.ui.PortNumberText.text().toInt()[0],0.1,self.director.clientThread)
            self.director.clientThread.begin(client)
            self.director.connectSlotAndSignalWithServices()
        else:
            self.director.clientThread.client.close()
            self.director.clientThread.client.isAlive = False
            self.director.clientThread = ClientThread(self.director)
            client = Client(8,str(self.ui.ServerIPText.text()),self.ui.PortNumberText.text().toInt()[0],0.1,self.director.clientThread)
            self.director.clientThread.begin(client)
            print "get another client"
            self.director.connectSlotAndSignalWithServices()
        data = {}

        data['nickname'] = unicode(self.ui.NicknameText.text())
        data['password'] = unicode(self.ui.PasswordText.text())
        self.director.clientThread.client.sendToServer(1001,1001,data)
        self.director.playerNickname = data['nickname']

    def connectWithService(self):
        self.disconnect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('goToHallFromLoginWindow(bool,int,int)'),self.goToHallFromLoginWindow)
        self.disconnect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('loginFailed(QString)'),self.loginFailed)
        self.connect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('goToHallFromLoginWindow(bool,int,int)'),self.goToHallFromLoginWindow)
        self.connect(self.director.clientThread.client.dispatcher.services[1001],\
                     SIGNAL('loginFailed(QString)'),self.loginFailed)

    def goToHallFromLoginWindow(self,isFirstLogin,tableColNum,tableRowNum):
        print "Go To Hall From Login Window"
        if isFirstLogin:
            QMessageBox.about(None,u"欢迎光临",u"欢迎第一次登陆")
        else:
            QMessageBox.about(None,u'欢迎光临',u"欢迎再次登陆")
        self.close()
        print "Type self director:",self.director
        self.hall = Hall(tableRowNum,tableColNum,self.director )
        self.hall.show()

    def loginFailed(self,errorString):
        QMessageBox.about(None,u"登陆失败！",errorString)

