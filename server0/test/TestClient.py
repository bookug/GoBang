#-*- encoding:UTF-8 -*-
__author__ = 'gzs2478'

from netstream import *
import json
import time
if __name__ == '__main__':
    try:
        client = netstream(8)
        client.connect('127.0.0.1',12345)
        if client.state != NET_STATE_ESTABLISHED:
            print "connect failed!"
            print "First Status :",client.status()
        command = {}
        command['sid'] = 0
        command['cid'] = 1
        command['time'] = time.ctime()
        command['command'] = None
        commandString = json.dumps(command)
        client.send(commandString)
        client.nodelay(0)
        client.nodelay(1)
        while True:
            time.sleep(0.5)
            client.process()
            print "Status :",client.status()
            data = client.recv()
            print "Get:",data

    except BaseException, e:
        print e
        client.close()

