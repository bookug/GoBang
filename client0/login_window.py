# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_window.ui'
#
# Created: Sun May 25 12:03:10 2014
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

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName(_fromUtf8("LoginWindow"))
        LoginWindow.resize(370, 345)
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
        self.ServerIPText.setText(_translate("LoginWindow", "123.57.165.67", None))
        self.NicknameText.setText(_translate("LoginWindow", "bookug", None))
        self.label_4.setText(_translate("LoginWindow", "passwd", None))
        self.PasswordText.setText(_translate("LoginWindow", "password", None))

import img_rc
