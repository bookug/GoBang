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

class CellState:
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

class Configure:
    padding = 20
    cellWidth = 32
    cellHeight = 32
    rowSize = 15
    colSize = 15
    #for Desk
    backgroundWidth = 121
    backgroundHeight = 119
    playerWidth = 32
    playerHeight = 32

class Direction:
    Left = 0
    Right = 1
    Down = 2
    Up = 3
    UpLeft = 4
    DownRight = 5
    UpRight = 6
    DownLeft = 7

class GameState:
    Empty = 0
    OnlyLeftPersonWaiting = 1
    OnlyRightPersonWaiting = 2
    TwoPersonWaiting = 3;
    Playing = 4;

def getCellLeftTopPosition(rowNum,colNum):
    '''
    number start from zero
    '''
    x = Configure.padding + colNum * Configure.cellWidth - 0.5 * Configure.cellWidth
    y = Configure.padding + rowNum * Configure.cellHeight - 0.5 * Configure.cellHeight
    return x, y

def getCellNumberFromPosition(x,y):
    colNum, rowNum = int((x - Configure.padding + 0.5 * Configure.cellWidth )/Configure.cellWidth), int((y - Configure.padding + 0.5 * Configure.cellHeight)/Configure.cellHeight)
    if colNum >= 0 and colNum < Configure.colSize and rowNum >= 0 and rowNum < Configure.rowSize :
        return rowNum,colNum
    else:
        return -1,-1  #error

def isRowNumValid(m):
    if m < Configure.rowSize and m >= 0:
        return True
    else:
        return False

def isColNumValid(n):
    if n < Configure.colSize and n >= 0:
        return True
    else:
        return False

