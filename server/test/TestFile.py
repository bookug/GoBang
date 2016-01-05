#-*- encoding:UTF-8 -*-

__author__ = 'zengli'

import database

db = Database.Database("./.gobang.db")
connect = db.connect()
cursor = connect.cursor()
sql = "SELECT * FROM user"
cursor.execute(sql)
connect.commit()
print cursor.fetchall()
cursor.close()
connect.close()

