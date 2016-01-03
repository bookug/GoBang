#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

import threading
from threading import Thread

from Client import Client

class ClientThread(threading.Thread):
    def __init__(self,parent = None):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.initData(parent)
    def initData(self,parent):
        self.parent = parent
        self.client = None
        self.lock = threading.RLock()
    def begin(self,client):
        self.client = client
        if client == None:
            return False;
        else:
            self.start()
    def run(self):
        self.client.run(self.lock)



