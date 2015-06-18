__author__ = 'xiangyu'

import MySQLdb
import json
from flask import session, request


class MySqlClient(object):
    def __init__(self, host, port, username, password):
        self.db = MySQLdb.connect(host=host, user=username, passwd=password, port=port)

    def get_all_people_info(self):
        people_list = self.db.cursor()
        people_list.execute("use TestConnect")
        people_list.execute("select * from People")
        peoples = [dict(title=row[0], text=row[1]) for row in people_list.fetchall()]
        people_list.close()
        return json.dumps(peoples)

    def get_database_names(self):
        databases = self.db.cursor()
        databases.execute("show databases")
        database_names = [row[0] for row in databases.fetchall()]
        databases.close()
        return json.dumps(database_names)


    def get_tables_name(self):
        table_list = self.db.cursor()
        table_list.execute("use TestConnect")
        table_list.execute("show tables")
        table_names = [row[0] for row in table_list.fetchall()]
        table_list.close()
        return json.dumps(table_names)