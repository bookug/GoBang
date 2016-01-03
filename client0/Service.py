#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Service(QObject):
    def __init__(self,sid,parent = None):
        QObject.__init__(self,None)
        self.service_id = sid
        self.commands = {}
        self.parent = parent

    def setParent(self,dispatcher):
        self.parent = dispatcher

    def handle(self,msg,owner):
        commandID = msg['command_id']
        if not commandID in self.commands:
            raise Exception('Wrong Command %s'%commandID)
        function = self.commands[commandID]
        return function(msg,owner)
    def register(self,commandID,function):
        self.commands[commandID] = function

    def registers(self,CommandDict):
        for commandID in CommandDict:
            self.register(commandID,CommandDict[commandID])
        return 0
