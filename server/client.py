#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import time

class Client(object):
    def __init__(self,connectID,server):
        object.__init__(self)
        try:
            self.connectID = connectID
            self.server = server
        except BaseException, e:
            print time.ctime()," Error in Client InitData"
            print e

