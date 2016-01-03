# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hall_window.ui'
#
# Created: Sat May 24 18:59:59 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_HallWindow(object):
    def setupUi(self, HallWindow):
        HallWindow.setObjectName(_fromUtf8("HallWindow"))
        HallWindow.resize(950, 800)
        self.HallTitle = QtGui.QLabel(HallWindow)
        self.HallTitle.setGeometry(QtCore.QRect(10, 10, 701, 91))
        self.HallTitle.setStyleSheet(_fromUtf8("background-color: #E2C9A5;\n"
"font: 75 36pt \"微软雅黑\";"))
        self.HallTitle.setObjectName(_fromUtf8("HallTitle"))
        self.Tables = QtGui.QTableWidget(HallWindow)
        self.Tables.setGeometry(QtCore.QRect(10, 110, 701, 511))
        self.Tables.setStyleSheet(_fromUtf8("background-color: #51719E;"))
        self.Tables.setObjectName(_fromUtf8("Tables"))
        self.Tables.setColumnCount(0)
        self.Tables.setRowCount(0)
        self.RankListTitle = QtGui.QLabel(HallWindow)
        self.RankListTitle.setGeometry(QtCore.QRect(720, 10, 221, 41))
        self.RankListTitle.setStyleSheet(_fromUtf8("background-color: #E2C9A5;\n"
"font: 75 18pt \"微软雅黑\";"))
        self.RankListTitle.setObjectName(_fromUtf8("RankListTitle"))
        self.RankList = QtGui.QTableWidget(HallWindow)
        self.RankList.setGeometry(QtCore.QRect(720, 60, 221, 381))
        self.RankList.setStyleSheet(_fromUtf8("background-color: #E2C9A5;"))
        self.RankList.setShowGrid(True)
        self.RankList.setGridStyle(QtCore.Qt.NoPen)
        self.RankList.setColumnCount(5)
        self.RankList.setObjectName(_fromUtf8("RankList"))
        self.RankList.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.RankList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.RankList.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.RankList.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.RankList.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.RankList.setHorizontalHeaderItem(4, item)
        self.OnlineListTitle = QtGui.QLabel(HallWindow)
        self.OnlineListTitle.setGeometry(QtCore.QRect(720, 450, 221, 41))
        self.OnlineListTitle.setStyleSheet(_fromUtf8("background-color: #E2C9A5;\n"
"font: 75 18pt \"微软雅黑\";"))
        self.OnlineListTitle.setObjectName(_fromUtf8("OnlineListTitle"))
        self.OnlineList = QtGui.QTableWidget(HallWindow)
        self.OnlineList.setGeometry(QtCore.QRect(720, 500, 221, 291))
        self.OnlineList.setStyleSheet(_fromUtf8("background-color: #E2C9A5;"))
        self.OnlineList.setObjectName(_fromUtf8("OnlineList"))
        self.OnlineList.setColumnCount(5)
        self.OnlineList.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.OnlineList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.OnlineList.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.OnlineList.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.OnlineList.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.OnlineList.setHorizontalHeaderItem(4, item)
        self.ChatBox = QtGui.QWidget(HallWindow)
        self.ChatBox.setGeometry(QtCore.QRect(10, 630, 701, 161))
        self.ChatBox.setStyleSheet(_fromUtf8("background-color: #E2C9A5;"))
        self.ChatBox.setObjectName(_fromUtf8("ChatBox"))
        self.MessageText = QtGui.QPlainTextEdit(self.ChatBox)
        self.MessageText.setGeometry(QtCore.QRect(10, 10, 681, 101))
        self.MessageText.setStyleSheet(_fromUtf8("background-color: #FFFFFF;"))
        self.MessageText.setReadOnly(True)
        self.MessageText.setCenterOnScroll(False)
        self.MessageText.setObjectName(_fromUtf8("MessageText"))
        self.SendButton = QtGui.QPushButton(self.ChatBox)
        self.SendButton.setGeometry(QtCore.QRect(620, 120, 71, 31))
        self.SendButton.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 127);\n"
"font: 100 11pt \"微软雅黑\";"))
        self.SendButton.setObjectName(_fromUtf8("SendButton"))
        self.InputText = QtGui.QTextEdit(self.ChatBox)
        self.InputText.setGeometry(QtCore.QRect(10, 120, 601, 31))
        self.InputText.setStyleSheet(_fromUtf8("background-color: #FFFFFF;"))
        self.InputText.setObjectName(_fromUtf8("InputText"))
        self.actionSendMessage = QtGui.QAction(HallWindow)
        self.actionSendMessage.setObjectName(_fromUtf8("actionSendMessage"))

        self.retranslateUi(HallWindow)
        QtCore.QObject.connect(self.actionSendMessage, QtCore.SIGNAL(_fromUtf8("triggered()")), self.SendButton.click)
        QtCore.QMetaObject.connectSlotsByName(HallWindow)
        HallWindow.setTabOrder(self.InputText, self.SendButton)
        HallWindow.setTabOrder(self.SendButton, self.MessageText)
        HallWindow.setTabOrder(self.MessageText, self.Tables)
        HallWindow.setTabOrder(self.Tables, self.RankList)
        HallWindow.setTabOrder(self.RankList, self.OnlineList)

    def retranslateUi(self, HallWindow):
        HallWindow.setWindowTitle(_translate("HallWindow", "Form", None))
        self.HallTitle.setText(_translate("HallWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">五 </span><span style=\" color:#000000;\">子</span><span style=\" color:#ffffff;\"> 棋</span> 游 戏 大 厅</p></body></html>", None))
        self.RankListTitle.setText(_translate("HallWindow", "<html><head/><body><p align=\"center\">排行榜</p></body></html>", None))
        item = self.RankList.horizontalHeaderItem(0)
        item.setText(_translate("HallWindow", "姓名", None))
        item = self.RankList.horizontalHeaderItem(1)
        item.setText(_translate("HallWindow", "胜绩", None))
        item = self.RankList.horizontalHeaderItem(2)
        item.setText(_translate("HallWindow", "积分", None))
        item = self.RankList.horizontalHeaderItem(3)
        item.setText(_translate("HallWindow", "平手", None))
        item = self.RankList.horizontalHeaderItem(4)
        item.setText(_translate("HallWindow", "败绩", None))
        self.OnlineListTitle.setText(_translate("HallWindow", "<html><head/><body><p align=\"center\">当前在线</p></body></html>", None))
        item = self.OnlineList.horizontalHeaderItem(0)
        item.setText(_translate("HallWindow", "姓名", None))
        item = self.OnlineList.horizontalHeaderItem(1)
        item.setText(_translate("HallWindow", "胜绩", None))
        item = self.OnlineList.horizontalHeaderItem(2)
        item.setText(_translate("HallWindow", "积分", None))
        item = self.OnlineList.horizontalHeaderItem(3)
        item.setText(_translate("HallWindow", "平手", None))
        item = self.OnlineList.horizontalHeaderItem(4)
        item.setText(_translate("HallWindow", "负绩", None))
        self.SendButton.setText(_translate("HallWindow", "发 送", None))
        self.SendButton.setShortcut(_translate("HallWindow", "Return", None))
        self.actionSendMessage.setText(_translate("HallWindow", "SendMessage", None))
        self.actionSendMessage.setToolTip(_translate("HallWindow", "发送消息", None))
        self.actionSendMessage.setShortcut(_translate("HallWindow", "Ctrl+Return", None))

