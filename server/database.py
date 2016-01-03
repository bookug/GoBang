#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import sqlite3

class Database(object):
    def __init__(self,databasePath):
        object.__init__(self)
        self.path = databasePath

    def setup(self):
        self.createTable()

    def connect(self):
        try:
            connect = sqlite3.connect(self.path)
            return connect
        except BaseException,e:
            print 'Database connect Error'
            print e
            print self.path

    def createTable(self):
        try:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS player(\
                          id              INTEGER        PRIMARY KEY   AUTOINCREMENT, \
                          nickname        VARCHAR(255)       NOT NULL UNIQUE ,\
                          password        VARCHAR(255)       NOT NULL,\
                          win_times       INTEGER(8)        DEFAULT 0,\
                          lose_times      INTEGER(8)        DEFAULT 0,\
                          draw_times      INTEGER(8)        DEFAULT 0,\
                          create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
                          )")
            cursor.execute("CREATE TABLE IF NOT EXISTS game(\
                          id              INTEGER        PRIMARY KEY   AUTOINCREMENT, \
                          player_a_id     INTEGER(8)        NOT NULL,\
                          player_b_id     INTEGER(8)        NOT NULL,\
                          is_player_a_win BOOLEAN           NOT NULL,\
                          is_draw         BOOLEAN           NOT NULL,\
                          create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
                          )")
            cursor.execute("CREATE TABLE IF NOT EXISTS hall_chat_record(\
                          id              INTEGER       PRIMARY KEY   AUTOINCREMENT, \
                          speaker_id      INTEGER(8)        DEFAULT 0,\
                          message         TEXT              DEFAULT 0,\
                          create_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
                          )")
            cursor.close()
            connection.close()
        except BaseException,e:
            print 'Error while creating DB tables'
            print e

