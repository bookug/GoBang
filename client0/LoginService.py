#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Service import Service

class LoginService(Service):
    serviceID = 1001
    def __init__(self,parent):
        Service.__init__(self,self.serviceID,parent)
        self.initData()
    def initData(self):
        self.registers({\
            1001 : self.loginSuccessHandler,\
            1002 : self.loginFailedHandler\
        })
        self.director = self.parent.parent.parent.parent
        print "Director is"
        print type(self.director)

    def loginSuccessHandler(self,msg,owner):
        print "LoginSuccessHandler"
        data = msg['data']
        self.emit(\
            SIGNAL('goToHallFromLoginWindow(bool,int,int)'),\
            data['is_first_login'],data['table_col_num'],\
            data['table_row_num'])
    def loginFailedHandler(self,msg,owner):
        print "LoginFailedHandler"
        self.emit(SIGNAL('loginFailed(QString)'),u"密码错误，或已经登陆！")