__author__ = 'xiangyu'

import MySQLdb
import json
from flask import session, request


class MySqlClient(object):
    def __init__(self, host, port, username, password, db='TestConnect'):
        self.db = MySQLdb.connect(host=host, user=username, passwd=password, port=port, db=db)

    def get_people_list(self):
        people_list = self.db.cursor()
        people_list.execute("select * from People")
        people_num = people_list.rowcount
        peoples = []
        for i in range(people_num):
            row = people_list.fetchone()
            peoples.append({'id': row[0], 'name': row[1]})
        people_list.close()
        return json.dumps({'peoples': peoples})


# try:
#     MySqlClient = MySQLdb.connect(host='localhost', user='root', passwd='19930801', port=3306)
#     cur = MySqlClient.cursor()
#     cur.execute("show databases")
#     for i in range(cur.rowcount):
#         row = cur.fetchone()
#         print row[0]
#     cur.execute("use TestConnect")
#     cur.execute("select * from People")
#     for i in range(cur.rowcount):
#         row = cur.fetchone()
#         print row
#         print row[0], row[1]
#     cur.close()
#     MySqlClient.close()
#
# except MySQLdb.Error, e:
#     print "Mysql Error %d: %s" % (e.args[0], e.args[1])