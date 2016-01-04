#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import time

class Util:
    test = 1

    @staticmethod
    def isRowNumValid(m):
        if m < 15 and m >= 0:
            return True
        else:
            return False

    @staticmethod
    def isColNumValid(n):
        if n < 15 and n >= 0:
            return True
        else:
            return False


#NTC: keep almostly same as in server/

class CellState:
    EMPTY = 2     #DEBUG
    WHITE = 0
    BLACK = 1

class Direction:
    #NTC: line, 0-1, 2-3, 4-5, 6-7
    LEFT = 0;
    RIGHT = 1;
    DOWN = 2;
    UP = 3;
    UP_LEFT = 4;
    DOWN_RIGHT = 5;
    UP_RIGHT = 6;
    DOWN_LEFT = 7;

class PlayerSide:
    WHITE = 0
    BLACK = 1

class PlayerState:
    NOT_READY = 0
    READY = 1
    TAKING_CHESS = 2
    WAITING_FOR_TAKING = 3
    WAITING_FOR_UNDO = 4
    MAKING_DECISION_FOR_UNDO = 5

class DBState:
    FETCH_NONE = 0
    FETCH_ONE = 1
    FETCH_ALL = 2

def singleton(cls,*args,**kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    return _singleton

def logTime():
    print "[",time.ctime(),"]"

def log(string):
    try:
        logTime()
        print string
    except BaseException,e:
        print "Error while finding log",e

