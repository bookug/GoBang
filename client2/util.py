#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

#this is the lowest level of package except built-in 

import math

class Util:
    def __init__(self):
        print "hello, this is util!"

    #this is used in board.py
    @staticmethod
    def getRowAndColumnNum(ID):
        row = math.floor((ID - 1) / 5)
        col = (ID - 1) % 5
        return row, col

    #this is used in game.py
    @staticmethod
    def getRowAndColNumber(roomID):
        rowNum = (roomID-1)/5
        colNum = (roomID-1)%5
        return rowNum,colNum

    @staticmethod   #no self included, can be called by others
    def GetScore(winTimes, loseTimes, drawTimes):
        return winTimes * 10 - loseTimes * 8

    @staticmethod
    def getIDFromRowAndColNum(rowNum, colNum):
        return rowNum * 5 + colNum + 1

#NTC: keep almostly same as in server/

class CellState:
    EMPTY = 2
    WHITE = 0
    BLACK = 1
    StateDict = {\
        2   :   u"empty",\
        0   :   u"white",\
        1   :   u"black",\
        }

class PlayerSide:
    WHITE = 0
    BLACK = 1
    StateDict = {\
        0 : u"white",\
        1 : u"black"\
        }

class PlayerState:
    NOT_READY = 0
    READY = 1
    TAKING_CHESS = 2
    WAITING_FOR_TAKING = 3
    WAITING_FOR_UNDO = 4
    MAKING_DECISION_FOR_UNDO = 5
    StateDict = {\
        0 : u'not prepared',
        1 : u'well prepared',
        2 : u'thinking...',
        3 : u'waiting...',
        4 : u'request to withdraw',
        5 : u'whether to withdraw'
        }

class Configure:
    PADDING = 20
    CELL_WIDTH = 32
    CELL_HEIGHT = 32
    ROW_SIZE = 15
    COL_SIZE = 15
    #for Desk
    BACKGROUND_WIDTH = 121
    BACKGROUND_HEIGHT = 119
    PLAYER_WIDTH = 32
    PLAYER_HEIGHT = 32

class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3
    UP_LEFT = 4
    DOWN_RIGHT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7

class GameState:
    EMPTY = 0
    ONLY_LEFT_PERSON_WAITING = 1
    ONLY_RIGHT_PERSON_WAITING = 2
    TWO_PERSON_WAITING = 3;
    PLAYING = 4;

def getCellLeftTopPosition(rowNum,colNum):
    '''
    number start from zero
    '''
    x = Configure.PADDING + colNum * Configure.CELL_WIDTH - 0.5 * Configure.CELL_WIDTH
    y = Configure.PADDING + rowNum * Configure.CELL_HEIGHT - 0.5 * Configure.CELL_HEIGHT
    return x, y

def getCellNumberFromPosition(x,y):
    colNum, rowNum = int((x - Configure.PADDING + 0.5 * Configure.CELL_WIDTH) / Configure.CELL_WIDTH), int((y - Configure.PADDING + 0.5 * Configure.CELL_HEIGHT) / Configure.CELL_HEIGHT)
    if colNum >= 0 and colNum < Configure.COL_SIZE and rowNum >= 0 and rowNum < Configure.ROW_SIZE:
        return rowNum,colNum
    else:
        return -1,-1  #error

def isRowNumValid(m):
    if m < Configure.ROW_SIZE and m >= 0:
        return True
    else:
        return False

def isColNumValid(n):
    if n < Configure.COL_SIZE and n >= 0:
        return True
    else:
        return False

