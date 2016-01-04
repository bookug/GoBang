__author__ = 'gzs2478'

import Database
db = Database.Database("./go_bang.db3")
connect = db.connect()
cursor = connect.cursor()
#sql = 'INSERT INTO player(nickname,password) VALUES("%s","%s")'%("qqq","qqq")
#sql = "UPDATE player SET win_times = 1,lose_times = 1,draw_times = 1 WHERE id = 2"
sql = "SELECT * FROM player"
cursor.execute(sql)
connect.commit()
print cursor.fetchall()
cursor.close()
connect.close()