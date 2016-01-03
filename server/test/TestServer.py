#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

from netstream import nethost
import netstream
import json
import time

if __name__ == '__main__':
    server = nethost(8)
    server.startup(12345)
    print 'Server startup at port:',server.port
    server.settimer(10000)

    while True:
        time.sleep(0.5)
        server.process()
        event , wparam , lparam , data = server.read()

        if event < 0:
            #print "Wrong Event:",event
            continue
        print "Event = %d wparam%xh lparam=%xh data='%s'"%(event,wparam,lparam,data)

        if event == netstream.NET_NEW:
            print "Some one(",wparam,")come in"
            server.send(wparam,"RE: Welcome!")
        if event == netstream.NET_LEAVE:
            print "Some one(",wparam,")leave"
        if event == netstream.NET_TIMER:
            print "Timer triggerred:",time.ctime()
            server.send(wparam,'RE: time pass..')
        if event == netstream.NET_DATA:
            server.send(wparam,'RE: ' + data)
            command = json.loads(data)
            print "Get Command ",command['time']
            print command

            if command['command'] == 'exit':
                print 'Client request to exit'
                server.close(wparam)

