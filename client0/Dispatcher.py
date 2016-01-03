#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

import Service

class Dispatcher(object):
    def __init__(self,parent = None):
        self.services = {}
        self.parent = parent

    def setParent(self,server):
        self.parent = server

    def dispatch(self,msg,owner):
        try:
            serviceID = msg['service_id']
            if not serviceID in self.services:
                raise Exception('Bad Service %d'%serviceID)
            service = self.services[serviceID]
            service.handle(msg,owner)
        except BaseException,e:
            print "Error in Client Dispatcher dispatching"
            print e
    def register(self,serviceID,service):
        service.setParent(self)
        self.services[serviceID] = service

    def registers(self,serviceDict):
        for serviceKey in serviceDict:
            self.register(serviceKey,serviceDict[serviceKey])
        return 0