#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import sqlite3

from util import DBState

class Database(object):
    def __init__(self,databasePath):
        object.__init__(self)
        self.path = databasePath

    def setup(self):
        self.createTable()

    def connect(self):
        try:
            connect = sqlite3.connect(self.path)
            print "connect:db connected!"
            return connect
        except BaseException,e:
            print 'Database connect Error'
            print e
            print self.path

    def runSQL(self, string, state):
        print string
        print state
        try:
            conn = self.connect()
            print "db connected!"
            cursor = conn.cursor()
            cursor.execute(string)
            print "sql command executed!"
            result = None
            if state == DBState.FETCH_ONE:
                print "fetch one!"
                result = cursor.fetchone()
            elif state == DBState.FETCH_ALL:
                print "fetch all!"
                result = cursor.fetchall()
            print "data fetched!"
            if result != None:
                print "the result is " ,result
            else:
                print "result is none"
            conn.commit()
            print "commited!"
            cursor.close()
            print "cursor closed!"
            conn.close()
            print "connection closed!"
            return result
        except BaseException, e:
            print e
            raise Exception("error in runSQL!")

    #TODO:room and chat tables are not used
    def createTable(self):
        try:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS user(\
                          id              INTEGER        PRIMARY KEY   AUTOINCREMENT, \
                          nickname        VARCHAR(255)       NOT NULL UNIQUE ,\
                          password        VARCHAR(255)       NOT NULL,\
                          win_times       INTEGER(8)        DEFAULT 0,\
                          lose_times      INTEGER(8)        DEFAULT 0,\
                          draw_times      INTEGER(8)        DEFAULT 0,\
                          create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
                          )")
            cursor.execute("CREATE TABLE IF NOT EXISTS room(\
                          id              INTEGER        PRIMARY KEY   AUTOINCREMENT, \
                          player_a_id     INTEGER(8)        NOT NULL,\
                          player_b_id     INTEGER(8)        NOT NULL,\
                          is_player_a_win BOOLEAN           NOT NULL,\
                          is_draw         BOOLEAN           NOT NULL,\
                          create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
                          )")
            cursor.execute("CREATE TABLE IF NOT EXISTS chat(\
                          id              INTEGER       PRIMARY KEY   AUTOINCREMENT, \
                          speaker_id      INTEGER(8)        DEFAULT 0,\
                          message         TEXT              DEFAULT 0,\
                          create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
                          )")
            cursor.close()
            connection.close()
        except BaseException, e:
            print 'Error while creating DB tables'
            print e

