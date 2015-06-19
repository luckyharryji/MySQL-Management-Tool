__author__ = 'xiangyu'

import MySQLdb
import json
from flask import session, request


class MySqlClient(object):
    error_code = ''

    _db = None
    _cur = None
    host = None
    port = None
    user = None
    password = None

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.user = username
        self.password = password
        try:
            self._db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, port=self.port)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg
            raise Exception(error_msg)
        self._cur = self._db.cursor()

    def choose_database(self, dbname):
        try:
            self.db.select_db(dbname)
        except MySQLdb.Error as e:
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            raise Exception(error_msg)

    def insert(self, table_name, data):
        columns = data.keys()
        _command = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_command, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        return self.cur.execute(_sql, tuple(_params))

    def get_all_people_info(self):
        people_list = self._db.cursor()
        people_list.execute("use TestConnect")
        people_list.execute("select * from People")
        peoples = [dict(title=row[0], text=row[1]) for row in people_list.fetchall()]
        people_list.close()
        return json.dumps(peoples)

    def get_database_names(self):
        databases = self._db.cursor()
        databases.execute("show databases")
        database_names = [row[0] for row in databases.fetchall()]
        databases.close()
        return json.dumps(database_names)

    def get_tables_name(self):
        table_list = self._db.cursor()
        table_list.execute("use TestConnect")
        table_list.execute("show tables")
        table_names = [row[0] for row in table_list.fetchall()]
        table_list.close()
        return json.dumps(table_names)

    def create_new_database(self, db_name):
        try:
            database_list = self._db.cursor()
            database_list.execute("show databases")
            for row in database_list.fetchall():
                if db_name == row[0]:
                    database_list.close()
                    return json.dumps(dict(status="exist"))
            database_list.execute("create database if not exists " + db_name)
            database_list.close()
            return json.dumps(dict(status="success"))
        except MySQLdb.Error, e:
            database_list.close()
            print "Mysql ERROR %d : %s" % (e.args[0], e.args[1])
            return json.dumps(dict(status="error", error=e.args[0], meassage=e.args[1]))

    def delete_database(self, db_name):
        try:
            database_list = self._db.cursor()
            database_list.execute("drop database if exists " + db_name)
            database_list.close()
            return json.dumps(dict(status="success"))
        except MySQLdb.Error, e:
            database_list.close()
            return json.dumps(dict(status="error", error=e.args[0], meassage=e.args[1]))

    def __del__(self):
        try:
            self._db.close()
            self._cur.close()
        except:
            pass

    def close(self):
        self.__del__()