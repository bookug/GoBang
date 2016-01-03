#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

from game import Login

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

#other file should not include this
#multiple app can be loaded here

class GoBang(QObject):
    gobang = None

    @classmethod
    def GetGoBang(cls):
        if cls.gobang == None:
            return GoBang()
        else:
            return cls.gobang

    def __init__(self):
        QObject.__init__(self,None)
        self.initData()

    def initData(self):
        self.clientThread = None
        self.loginWindow = Login(self)
        self.hall = None
        self.chessRoom = None
        self.playerNickname = ""

    def connectSlotAndSignalWithServices(self):
        self.loginWindow.connectWithService()

    def serverCrashedAlert(self):
        QMessageBox.about(None, u"server crashed", u"server is crashed!")

    def run(self):
        app = QApplication(sys.argv)
        self.loginWindow.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GoBang.GetGoBang().loginWindow.show()
    sys.exit(app.exec_())

