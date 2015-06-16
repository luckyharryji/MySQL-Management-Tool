__author__ = 'xiangyu'

import MySQLdb
import json
from flask import session, request


class MySqlClient(object):
    def __init__(self, host, port, username, password, db='TestConnect'):
        self.db = MySQLdb.connect(host=host, user=username, passwd=password, port=port, db=db)

    def get_all_people_info(self):
        people_list = self.db.cursor()
        people_list.execute("select * from People")
        peoples = [dict(title=row[0], text=row[1]) for row in people_list.fetchall()]
        people_list.close()
        return json.dumps(peoples)