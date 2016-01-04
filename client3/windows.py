# -*- coding: utf-8 -*-

__author__ = 'zengli'

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

class LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName(_fromUtf8("LoginWindow"))
        LoginWindow.resize(400, 440)
        LoginWindow.setStyleSheet(_fromUtf8("border-image: url(:/img/login_skin.png);"))
        self.label = QtGui.QLabel(LoginWindow)
        self.label.setGeometry(QtCore.QRect(20, 80, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("border-image:none;"))
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setLineWidth(-5)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(LoginWindow)
        self.label_2.setGeometry(QtCore.QRect(20, 130, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("border-image:none;"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(LoginWindow)
        self.label_3.setGeometry(QtCore.QRect(20, 180, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("border-image:none;"))
        self.label_3.setMidLineWidth(0)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.loginButton = QtGui.QPushButton(LoginWindow)
        self.loginButton.setGeometry(QtCore.QRect(120, 290, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.loginButton.setFont(font)
        self.loginButton.setStyleSheet(_fromUtf8("border-image: url(:/img/pushbutton.png);"))
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.PortNumberText = QtGui.QLineEdit(LoginWindow)
        self.PortNumberText.setGeometry(QtCore.QRect(120, 130, 181, 31))
        self.PortNumberText.setStyleSheet(_fromUtf8("border-image:none;\n"
""))
        self.PortNumberText.setObjectName(_fromUtf8("PortNumberText"))
        self.ServerIPText = QtGui.QLineEdit(LoginWindow)
        self.ServerIPText.setGeometry(QtCore.QRect(120, 80, 181, 31))
        self.ServerIPText.setStyleSheet(_fromUtf8("border-image:none;\n"
""))
        self.ServerIPText.setObjectName(_fromUtf8("ServerIPText"))
        self.NicknameText = QtGui.QLineEdit(LoginWindow)
        self.NicknameText.setGeometry(QtCore.QRect(120, 180, 181, 31))
        self.NicknameText.setStyleSheet(_fromUtf8("border-image:none;\n"
""))
        self.NicknameText.setObjectName(_fromUtf8("NicknameText"))
        self.label_4 = QtGui.QLabel(LoginWindow)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(_fromUtf8("border-image:none;"))
        self.label_4.setMidLineWidth(0)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.PasswordText = QtGui.QLineEdit(LoginWindow)
        self.PasswordText.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordText.setGeometry(QtCore.QRect(120, 230, 181, 31))
        self.PasswordText.setStyleSheet(_fromUtf8("border-image:none;\n"
""))
        self.PasswordText.setObjectName(_fromUtf8("PasswordText"))

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        LoginWindow.setTabOrder(self.ServerIPText, self.PortNumberText)
        LoginWindow.setTabOrder(self.PortNumberText, self.NicknameText)
        LoginWindow.setTabOrder(self.NicknameText, self.PasswordText)
        LoginWindow.setTabOrder(self.PasswordText, self.loginButton)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Form", None))
        self.label.setText(_translate("LoginWindow", "server IP", None))
        self.label_2.setText(_translate("LoginWindow", "port address", None))
        self.label_3.setText(_translate("LoginWindow", "nickname", None))
        self.loginButton.setText(_translate("LoginWindow", "login", None))
        self.PortNumberText.setText(_translate("LoginWindow", "4829", None))
        self.ServerIPText.setText(_translate("LoginWindow", "127.0.0.1", None))
        self.NicknameText.setText(_translate("LoginWindow", "bookug", None))
        self.label_4.setText(_translate("LoginWindow", "passwd", None))
        self.PasswordText.setText(_translate("LoginWindow", "12345678", None))

class HallWindow(object):
    def setupUi(self, HallWindow):
        HallWindow.setObjectName(_fromUtf8("HallWindow"))
        HallWindow.resize(1000, 900)
        self.HallTitle = QtGui.QLabel(HallWindow)
        self.HallTitle.setGeometry(QtCore.QRect(10, 10, 701, 91))
        self.HallTitle.setStyleSheet(_fromUtf8("background-color: #FFF5EE;\n"
"font: 50 30pt \"Arial\";"))
        self.HallTitle.setObjectName(_fromUtf8("HallTitle"))
        self.Tables = QtGui.QTableWidget(HallWindow)
        self.Tables.setGeometry(QtCore.QRect(10, 110, 701, 511))
        self.Tables.setStyleSheet(_fromUtf8("background-color: #52720E;"))
        self.Tables.setObjectName(_fromUtf8("Tables"))
        self.Tables.setColumnCount(0)
        self.Tables.setRowCount(0)
        self.RankListTitle = QtGui.QLabel(HallWindow)
        self.RankListTitle.setGeometry(QtCore.QRect(720, 10, 221, 41))
        self.RankListTitle.setStyleSheet(_fromUtf8("background-color: #E2C9B5;\n"
"font: 75 18pt \"Arial\";"))
        self.RankListTitle.setObjectName(_fromUtf8("RankListTitle"))
        self.RankList = QtGui.QTableWidget(HallWindow)
        self.RankList.setGeometry(QtCore.QRect(720, 60, 221, 381))
        self.RankList.setStyleSheet(_fromUtf8("background-color: #000000;"))
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
        self.OnlineListTitle.setStyleSheet(_fromUtf8("background-color: #E2C9B5;\n"
"font: 75 20pt \"Arial\";"))
        self.OnlineListTitle.setObjectName(_fromUtf8("OnlineListTitle"))
        self.OnlineList = QtGui.QTableWidget(HallWindow)
        self.OnlineList.setGeometry(QtCore.QRect(720, 500, 221, 291))
        self.OnlineList.setStyleSheet(_fromUtf8("background-color: #000000;"))
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
        self.ChatBox.setStyleSheet(_fromUtf8("background-color: #FFFAFA;"))
        self.ChatBox.setObjectName(_fromUtf8("ChatBox"))
        self.MessageText = QtGui.QPlainTextEdit(self.ChatBox)
        self.MessageText.setGeometry(QtCore.QRect(10, 10, 681, 101))
        self.MessageText.setStyleSheet(_fromUtf8("background-color: #3CB371;"))
        self.MessageText.setReadOnly(True)
        self.MessageText.setCenterOnScroll(False)
        self.MessageText.setObjectName(_fromUtf8("MessageText"))
        self.SendButton = QtGui.QPushButton(self.ChatBox)
        self.SendButton.setGeometry(QtCore.QRect(620, 120, 71, 31))
        self.SendButton.setStyleSheet(_fromUtf8("background-color: rgb(215, 170, 127);\n"
"font: 100 11pt \"Arial\";"))
        self.SendButton.setObjectName(_fromUtf8("SendButton"))
        self.InputText = QtGui.QTextEdit(self.ChatBox)
        self.InputText.setGeometry(QtCore.QRect(10, 120, 601, 31))
        self.InputText.setStyleSheet(_fromUtf8("background-color: #FFFF77;"))
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
        self.HallTitle.setText(_translate("HallWindow", "<html><head/><body><p align=\"center\">Welcome to GoBang Center</p></body></html>", None))
        self.RankListTitle.setText(_translate("HallWindow", "<html><head/><body><p align=\"center\">Rank List</p></body></html>", None))
        item = self.RankList.horizontalHeaderItem(0)
        item.setText(_translate("HallWindow", "name", None))
        item = self.RankList.horizontalHeaderItem(1)
        item.setText(_translate("HallWindow", "wins", None))
        item = self.RankList.horizontalHeaderItem(2)
        item.setText(_translate("HallWindow", "scores", None))
        item = self.RankList.horizontalHeaderItem(3)
        item.setText(_translate("HallWindow", "draws", None))
        item = self.RankList.horizontalHeaderItem(4)
        item.setText(_translate("HallWindow", "loses", None))
        self.OnlineListTitle.setText(_translate("HallWindow", "<html><head/><body><p align=\"center\">Online User</p></body></html>", None))
        item = self.OnlineList.horizontalHeaderItem(0)
        item.setText(_translate("HallWindow", "name", None))
        item = self.OnlineList.horizontalHeaderItem(1)
        item.setText(_translate("HallWindow", "wins", None))
        item = self.OnlineList.horizontalHeaderItem(2)
        item.setText(_translate("HallWindow", "scores", None))
        item = self.OnlineList.horizontalHeaderItem(3)
        item.setText(_translate("HallWindow", "draws", None))
        item = self.OnlineList.horizontalHeaderItem(4)
        item.setText(_translate("HallWindow", "loses", None))
        self.SendButton.setText(_translate("HallWindow", "sent", None))
        self.SendButton.setShortcut(_translate("HallWindow", "Return", None))
        self.actionSendMessage.setText(_translate("HallWindow", "SendMessage", None))
        self.actionSendMessage.setToolTip(_translate("HallWindow", "send message", None))
        self.actionSendMessage.setShortcut(_translate("HallWindow", "Ctrl+Return", None))

class RoomWindow(object):
    def setupUi(self, RoomWindow):
        RoomWindow.setObjectName(_fromUtf8("RoomWindow"))
        RoomWindow.resize(948, 800)
        #RoomWindow.setStyleSheet(_fromUtf8("background-color: #528191;"))
        self.RoomTitle = QtGui.QLabel(RoomWindow)
        self.RoomTitle.setGeometry(QtCore.QRect(205, 10, 541, 71))
        self.RoomTitle.setStyleSheet(_fromUtf8("background-color: #FFF5EE;\n"
"\n"
"\n"
"font:30 20pt \"Arial\";"))
        self.RoomTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.RoomTitle.setObjectName(_fromUtf8("RoomTitle"))
        self.ChessBoardBackground = QtGui.QWidget(RoomWindow)
        self.ChessBoardBackground.setGeometry(QtCore.QRect(200, 90, 551, 531))
        self.ChessBoardBackground.setStyleSheet(_fromUtf8("background-color: #8D4B27;"))
        self.ChessBoardBackground.setObjectName(_fromUtf8("ChessBoardBackground"))
        self.ChessBoard = QtGui.QWidget(self.ChessBoardBackground)
        self.ChessBoard.setGeometry(QtCore.QRect(30, 20, 490, 490))
        self.ChessBoard.setStyleSheet(_fromUtf8("background-color: #FFD700;"))
        self.ChessBoard.setObjectName(_fromUtf8("ChessBoard"))
        self.ChatBox = QtGui.QWidget(RoomWindow)
        self.ChatBox.setGeometry(QtCore.QRect(10, 630, 921, 161))
        self.ChatBox.setStyleSheet(_fromUtf8("background-color: #FDF5E6;"))
        self.ChatBox.setObjectName(_fromUtf8("ChatBox"))
        self.InputText = QtGui.QTextEdit(self.ChatBox)
        self.InputText.setGeometry(QtCore.QRect(10, 120, 821, 31))
        self.InputText.setStyleSheet(_fromUtf8("background-color: 28FF77;"))
        self.InputText.setObjectName(_fromUtf8("InputText"))
        self.SendButton = QtGui.QPushButton(self.ChatBox)
        self.SendButton.setGeometry(QtCore.QRect(840, 120, 71, 31))
        self.SendButton.setStyleSheet(_fromUtf8("background-color: rgb(255, 170, 127);\n"
"font: 75 11pt \"Arial\";"))
        self.SendButton.setObjectName(_fromUtf8("SendButton"))
        self.MessageText = QtGui.QPlainTextEdit(self.ChatBox)
        self.MessageText.setReadOnly(True)
        self.MessageText.setGeometry(QtCore.QRect(10, 10, 901, 101))
        self.MessageText.setStyleSheet(_fromUtf8("background-color: 556B2F;"))
        self.MessageText.setObjectName(_fromUtf8("MessageText"))
        self.MyInfoBox = QtGui.QWidget(RoomWindow)
        self.MyInfoBox.setGeometry(QtCore.QRect(10, 320, 181, 301))
        self.MyInfoBox.setStyleSheet(_fromUtf8("background-color: #808000;\n"
"font: 6 10pt \"Arial\";"))
        self.MyInfoBox.setObjectName(_fromUtf8("MyInfoBox"))
        self.LabelNickName = QtGui.QLabel(self.MyInfoBox)
        self.LabelNickName.setGeometry(QtCore.QRect(20, 90, 51, 31))
        self.LabelNickName.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelNickName.setObjectName(_fromUtf8("LabelNickName"))
        self.LabelScore = QtGui.QLabel(self.MyInfoBox)
        self.LabelScore.setGeometry(QtCore.QRect(20, 120, 51, 31))
        self.LabelScore.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelScore.setObjectName(_fromUtf8("LabelScore"))
        self.LabelWinTime = QtGui.QLabel(self.MyInfoBox)
        self.LabelWinTime.setGeometry(QtCore.QRect(20, 150, 51, 31))
        self.LabelWinTime.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelWinTime.setObjectName(_fromUtf8("LabelWinTime"))
        self.LabelDrawTime = QtGui.QLabel(self.MyInfoBox)
        self.LabelDrawTime.setGeometry(QtCore.QRect(20, 180, 51, 31))
        self.LabelDrawTime.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelDrawTime.setObjectName(_fromUtf8("LabelDrawTime"))
        self.LabelLoseTime = QtGui.QLabel(self.MyInfoBox)
        self.LabelLoseTime.setGeometry(QtCore.QRect(20, 210, 51, 31))
        self.LabelLoseTime.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelLoseTime.setObjectName(_fromUtf8("LabelLoseTime"))
        self.Draw = QtGui.QLabel(self.MyInfoBox)
        self.Draw.setGeometry(QtCore.QRect(80, 180, 81, 31))
        self.Draw.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.Draw.setObjectName(_fromUtf8("Draw"))
        self.NickName = QtGui.QLabel(self.MyInfoBox)
        self.NickName.setGeometry(QtCore.QRect(80, 90, 81, 31))
        self.NickName.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.NickName.setObjectName(_fromUtf8("NickName"))
        self.Score = QtGui.QLabel(self.MyInfoBox)
        self.Score.setGeometry(QtCore.QRect(80, 120, 81, 31))
        self.Score.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.Score.setObjectName(_fromUtf8("Score"))
        self.LoseTime = QtGui.QLabel(self.MyInfoBox)
        self.LoseTime.setGeometry(QtCore.QRect(80, 210, 81, 31))
        self.LoseTime.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.LoseTime.setObjectName(_fromUtf8("LoseTime"))
        self.WinTime = QtGui.QLabel(self.MyInfoBox)
        self.WinTime.setGeometry(QtCore.QRect(80, 150, 81, 31))
        self.WinTime.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.WinTime.setObjectName(_fromUtf8("WinTime"))
        self.LabelSide = QtGui.QLabel(self.MyInfoBox)
        self.LabelSide.setGeometry(QtCore.QRect(20, 60, 51, 31))
        self.LabelSide.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelSide.setObjectName(_fromUtf8("LabelSide"))
        self.Side = QtGui.QLabel(self.MyInfoBox)
        self.Side.setGeometry(QtCore.QRect(80, 60, 81, 31))
        self.Side.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.Side.setObjectName(_fromUtf8("Side"))
        self.State = QtGui.QLabel(self.MyInfoBox)
        self.State.setGeometry(QtCore.QRect(80, 240, 81, 31))
        self.State.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";\n"
"color: rgb(255, 0, 0);"))
        self.State.setObjectName(_fromUtf8("State"))
        self.LabelState = QtGui.QLabel(self.MyInfoBox)
        self.LabelState.setGeometry(QtCore.QRect(20, 240, 51, 31))
        self.LabelState.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelState.setObjectName(_fromUtf8("LabelState"))
        self.LabelState_3 = QtGui.QLabel(self.MyInfoBox)
        self.LabelState_3.setGeometry(QtCore.QRect(50, 20, 51, 31))
        self.LabelState_3.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelState_3.setObjectName(_fromUtf8("LabelState_3"))
        self.ControlBox = QtGui.QWidget(RoomWindow)
        self.ControlBox.setGeometry(QtCore.QRect(760, 10, 171, 611))
        self.ControlBox.setStyleSheet(_fromUtf8("background-color: #E2C9A5;"))
        self.ControlBox.setObjectName(_fromUtf8("ControlBox"))
        self.ReadyButton = QtGui.QPushButton(self.ControlBox)
        self.ReadyButton.setGeometry(QtCore.QRect(20, 400, 131, 51))
        self.ReadyButton.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.ReadyButton.setObjectName(_fromUtf8("ReadyButton"))
        self.AdmitDefeatButton = QtGui.QPushButton(self.ControlBox)
        self.AdmitDefeatButton.setGeometry(QtCore.QRect(20, 470, 131, 51))
        self.AdmitDefeatButton.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.AdmitDefeatButton.setObjectName(_fromUtf8("AdmitDefeatButton"))
        self.UndoButton = QtGui.QPushButton(self.ControlBox)
        self.UndoButton.setGeometry(QtCore.QRect(20, 540, 131, 51))
        self.UndoButton.setStyleSheet(_fromUtf8("font: 10pt \"Arial\" ;"))
        self.UndoButton.setObjectName(_fromUtf8("UndoButton"))
        self.LiveText = QtGui.QPlainTextEdit(self.ControlBox)
        self.LiveText.setGeometry(QtCore.QRect(10, 50, 151, 341))
        self.LiveText.setStyleSheet(_fromUtf8("background-color: rgb(254, 254, 254);\n"
"font: 10pt \"Arial\";"))
        self.LiveText.setReadOnly(True)
        self.LiveText.setPlainText(_fromUtf8(""))
        self.LiveText.setObjectName(_fromUtf8("LiveText"))
        self.LiveTitle = QtGui.QLabel(self.ControlBox)
        self.LiveTitle.setGeometry(QtCore.QRect(10, 10, 151, 31))
        self.LiveTitle.setStyleSheet(_fromUtf8("font: 13pt \"Arial\";"))
        self.LiveTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.LiveTitle.setObjectName(_fromUtf8("LiveTitle"))
        self.EnemyInfoBox = QtGui.QWidget(RoomWindow)
        self.EnemyInfoBox.setGeometry(QtCore.QRect(10, 10, 181, 301))
        self.EnemyInfoBox.setStyleSheet(_fromUtf8("background-color: #E2C1A5;"))
        self.EnemyInfoBox.setObjectName(_fromUtf8("EnemyInfoBox"))
        self.LabelNickName_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelNickName_2.setGeometry(QtCore.QRect(20, 90, 51, 31))
        self.LabelNickName_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelNickName_2.setObjectName(_fromUtf8("LabelNickName_2"))
        self.LabelScore_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelScore_2.setGeometry(QtCore.QRect(20, 120, 51, 31))
        self.LabelScore_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelScore_2.setObjectName(_fromUtf8("LabelScore_2"))
        self.LabelWinTime_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelWinTime_2.setGeometry(QtCore.QRect(20, 150, 51, 31))
        self.LabelWinTime_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelWinTime_2.setObjectName(_fromUtf8("LabelWinTime_2"))
        self.LabelDrawTime_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelDrawTime_2.setGeometry(QtCore.QRect(20, 180, 51, 31))
        self.LabelDrawTime_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelDrawTime_2.setObjectName(_fromUtf8("LabelDrawTime_2"))
        self.LabelLoseTime_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelLoseTime_2.setGeometry(QtCore.QRect(20, 210, 51, 31))
        self.LabelLoseTime_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelLoseTime_2.setObjectName(_fromUtf8("LabelLoseTime_2"))
        self.EnemyDrawTime = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemyDrawTime.setGeometry(QtCore.QRect(80, 180, 81, 31))
        self.EnemyDrawTime.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.EnemyDrawTime.setObjectName(_fromUtf8("EnemyDrawTime"))
        self.EnemyNickName = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemyNickName.setGeometry(QtCore.QRect(80, 90, 81, 31))
        self.EnemyNickName.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.EnemyNickName.setObjectName(_fromUtf8("EnemyNickName"))
        self.EnemyScore = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemyScore.setGeometry(QtCore.QRect(80, 120, 81, 31))
        self.EnemyScore.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.EnemyScore.setObjectName(_fromUtf8("EnemyScore"))
        self.EnemyLoseTime = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemyLoseTime.setGeometry(QtCore.QRect(80, 210, 81, 31))
        self.EnemyLoseTime.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.EnemyLoseTime.setObjectName(_fromUtf8("EnemyLoseTime"))
        self.EnemyWinTime = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemyWinTime.setGeometry(QtCore.QRect(80, 150, 81, 31))
        self.EnemyWinTime.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.EnemyWinTime.setObjectName(_fromUtf8("EnemyWinTime"))
        self.LabelSide_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelSide_2.setGeometry(QtCore.QRect(20, 60, 51, 31))
        self.LabelSide_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelSide_2.setObjectName(_fromUtf8("LabelSide_2"))
        self.EnemySide = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemySide.setGeometry(QtCore.QRect(80, 60, 81, 31))
        self.EnemySide.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";"))
        self.EnemySide.setObjectName(_fromUtf8("EnemySide"))
        self.EnemyState = QtGui.QLabel(self.EnemyInfoBox)
        self.EnemyState.setGeometry(QtCore.QRect(80, 240, 81, 31))
        self.EnemyState.setStyleSheet(_fromUtf8("font: 8pt \"Arial\";\n"
"color: rgb(255, 0, 0);"))
        self.EnemyState.setObjectName(_fromUtf8("EnemyState"))
        self.LabelState_2 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelState_2.setGeometry(QtCore.QRect(20, 240, 51, 31))
        self.LabelState_2.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelState_2.setObjectName(_fromUtf8("LabelState_2"))
        self.LabelState_4 = QtGui.QLabel(self.EnemyInfoBox)
        self.LabelState_4.setGeometry(QtCore.QRect(50, 20, 51, 31))
        self.LabelState_4.setStyleSheet(_fromUtf8("font: 10pt \"Arial\";"))
        self.LabelState_4.setObjectName(_fromUtf8("LabelState_4"))

        self.retranslateUi(RoomWindow)
        QtCore.QMetaObject.connectSlotsByName(RoomWindow)
        RoomWindow.setTabOrder(self.InputText, self.SendButton)
        RoomWindow.setTabOrder(self.SendButton, self.MessageText)
        RoomWindow.setTabOrder(self.MessageText, self.ReadyButton)
        RoomWindow.setTabOrder(self.ReadyButton, self.AdmitDefeatButton)
        RoomWindow.setTabOrder(self.AdmitDefeatButton, self.UndoButton)
        RoomWindow.setTabOrder(self.UndoButton, self.LiveText)

    def retranslateUi(self, RoomWindow):
        RoomWindow.setWindowTitle(_translate("RoomWindow", "Form", None))
        self.RoomTitle.setText(_translate("RoomWindow", "<html><head/><body><p>have fun playing the GoBang</p></body></html>", None))
        self.SendButton.setText(_translate("RoomWindow", "send", None))
        self.LabelNickName.setText(_translate("RoomWindow", "nick: ", None))
        self.LabelScore.setText(_translate("RoomWindow", "score: ", None))
        self.LabelWinTime.setText(_translate("RoomWindow", "wins: ", None))
        self.LabelDrawTime.setText(_translate("RoomWindow", "draws: ", None))
        self.LabelLoseTime.setText(_translate("RoomWindow", "loses: ", None))
        self.Draw.setText(_translate("RoomWindow", "draw", None))
        self.NickName.setText(_translate("RoomWindow", "nick", None))
        self.Score.setText(_translate("RoomWindow", "score", None))
        self.LoseTime.setText(_translate("RoomWindow", "loses", None))
        self.WinTime.setText(_translate("RoomWindow", "wins", None))
        self.LabelSide.setText(_translate("RoomWindow", "side: ", None))
        self.Side.setText(_translate("RoomWindow", "side", None))
        self.State.setText(_translate("RoomWindow", "status", None))
        self.LabelState.setText(_translate("RoomWindow", "status: ", None))
        self.LabelState_3.setText(_translate("RoomWindow", "own", None))
        self.ReadyButton.setText(_translate("RoomWindow", "Ready", None))
        self.AdmitDefeatButton.setText(_translate("RoomWindow", "AdmitDefeat", None))
        self.UndoButton.setText(_translate("RoomWindow", "Undo", None))
        self.LiveTitle.setText(_translate("RoomWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Live</span></p></body></html>", None))
        self.LabelNickName_2.setText(_translate("RoomWindow", "nick: ", None))
        self.LabelScore_2.setText(_translate("RoomWindow", "score: ", None))
        self.LabelWinTime_2.setText(_translate("RoomWindow", "wins: ", None))
        self.LabelDrawTime_2.setText(_translate("RoomWindow", "draws: ", None))
        self.LabelLoseTime_2.setText(_translate("RoomWindow", "loses: ", None))
        self.EnemyDrawTime.setText(_translate("RoomWindow", "draws", None))
        self.EnemyNickName.setText(_translate("RoomWindow", "nick", None))
        self.EnemyScore.setText(_translate("RoomWindow", "score", None))
        self.EnemyLoseTime.setText(_translate("RoomWindow", "loses", None))
        self.EnemyWinTime.setText(_translate("RoomWindow", "wins", None))
        self.LabelSide_2.setText(_translate("RoomWindow", "side: ", None))
        self.EnemySide.setText(_translate("RoomWindow", "side", None))
        self.EnemyState.setText(_translate("RoomWindow", "status", None))
        self.LabelState_2.setText(_translate("RoomWindow", "status: ", None))
        self.LabelState_4.setText(_translate("RoomWindow", "other", None))

