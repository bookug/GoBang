#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

from ClientThread import ClientThread
import LoginWindow
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
class GoBang(QObject):
    goBang = None

    @staticmethod
    def GetScore(winTimes,loseTimes,drawTimes):
        return winTimes * 10 - loseTimes * 8

    @classmethod
    def GetGoBang(cls):
        if cls.goBang == None:
            return GoBang()
        else:
            return cls.goBang

    def __init__(self):
        QObject.__init__(self,None)
        self.initData()

    def initData(self):
        self.clientThread = None
        self.loginWindow = LoginWindow.LoginWindow(self)
        self.hall = None
        self.chessRoom = None
        self.playerNickname = ""

    def connectSlotAndSignalWithServices(self):
        self.loginWindow.connectWithService()

    def serverCrashedAlert(self):
        QMessageBox.about(None,u"服务器异常",u'欧漏！服务器挂掉了！')

    def run(self):
        app = QApplication(sys.argv)
        self.loginWindow.show()
        sys.exit(app.exec_())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    GoBang.GetGoBang().loginWindow.show()
    sys.exit(app.exec_())