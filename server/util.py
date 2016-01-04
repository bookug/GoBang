#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

class Util:
    a = 1

class CellState:
    WhiteChess = 0
    BlackChess = 1
    NoChess = 2

class Direction:
    Left = 0;
    Right = 1;
    Down = 2;
    Up = 3;
    UpLeft = 4;
    UpRight = 5;
    DownLeft = 6;
    DownRight = 7;

class PlayerSide:
    White = 0
    Black = 1

class PlayerState:
    NotReady = 0
    Ready = 1
    TakingChess = 2
    WaitingForTaking = 3
    WaitingForUndo = 4
    MakingDecisionForUndo = 5

def singleton(cls,*args,**kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    return _singleton

