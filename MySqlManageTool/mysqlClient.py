__author__ = 'xiangyu'

import MySQLdb

try:
    MySqlClient = MySQLdb.connect(host='localhost', user='root', passwd='19930801', port=3306)
    cur = MySqlClient.cursor()
    # # cur.execute("CREATE TABLE IF NOT EXISTS \
    # #     People(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
    # cur.execute("INSERT INTO People(Name) VALUES('Siyu Yang')")
    # cur.execute("INSERT INTO People(Name) VALUES('Hanxiong Wang')")
    cur.execute("show databases")
    for i in range(cur.rowcount):
        row = cur.fetchone()
        print row[0]
    cur.execute("use TestConnect")
    cur.execute("select * from People")
    for i in range(cur.rowcount):
        row = cur.fetchone()
        print row
        print row[0], row[1]
    cur.close()
    MySqlClient.close()

except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])