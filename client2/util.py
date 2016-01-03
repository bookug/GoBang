#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

#this is the lower level of package except built-in 

class Util:
    def __init__(self):
        print "hello, this is util!"

    @staticmethod
    def getRowAndColNumber(roomID):
        rowNum = (roomID-1)/5
        colNum = (roomID-1)%5
        return rowNum,colNum

    @staticmethod   #no self included
    def GetScore(winTimes,loseTimes,drawTimes):
        return winTimes * 10 - loseTimes * 8

class BoardCell:
    White = 0
    Black = 1
    Empty = 2
    StateDict = {\
        0   :   u"white",\
        1   :   u"black",\
        2   :   u"empty"\
        }

class PlayerSide:
    White = 0
    Black = 1
    StateDict = {\
        0:u"white",\
        1:u"black"\
        }

class PlayerState:
    NotReady = 0
    Ready = 1
    TakingChess = 2
    WaitingForTaking = 3
    WaitingForUndo = 4
    MakingDecisionForUndo = 5
    StateDict = {\
        0:u'not prepared',
        1:u'well prepared',
        2:u'thinking...',
        3:u'waiting...',
        4:u'request to withdraw',
        5:u'whether to withdraw'
        }

class BoardDirection:
    Left = 0
    Right = 1
    Down = 2
    Up = 3
    UpLeft = 4
    DownRight = 5
    UpRight = 6
    DownLeft = 7

class BoardDeskState:
    Empty = 0
    OnlyLeftPersonWaiting = 1
    OnlyRightPersonWaiting = 2
    TwoPersonWaiting = 3;
    Playing = 4;

