
import sqlite3

class CRUD:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name + ".db")
        self.db_name = db_name

    def checkExistTable(self, table_name):
        checkTable_exist_query = "SELECT name FROM sqlite_master"
        cur = self.conn.cursor()
        res = cur.execute(checkTable_exist_query)
        result = res.fetchall()
        if not result or table_name not in [res[0] for res in result]:
            return False
        
        return True


    def create(self, table_name, columns):

        columns_list = ','.join(columns)
        sql_query = """CREATE TABLE {} ({})""".format(table_name, columns_list)
        cur = self.conn.cursor()
        cur.execute(sql_query)

        return True

    def insert(self, table_name, columns, values):
        columns = ','.join(columns)
        placeholder_values = ','.join(['?']*len(values))
        sql_query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, columns, placeholder_values)
        cur = self.conn.cursor()
        cur.execute(sql_query, tuple(values))
        self.conn.commit()

    def read(self, table_name, columns = '*'):
        if columns == '*':
            columns = self.getColumnName(table_name)

        column_list = ','.join(columns)

        sql_query = "SELECT {} FROM {}".format(column_list, table_name)
        cur = self.conn.cursor()

        res = cur.execute(sql_query)
        return columns, res.fetchall()

    def getColumnName(self, table_name):
        sql_query = "PRAGMA table_info({})".format(table_name)
        cur = self.conn.cursor()

        res =  cur.execute(sql_query)
        columns = list(map(lambda x: x[1], res.fetchall()))

        return columns
    
    def getTables(self):
        sql_query = "SELECT name FROM sqlite_master"
        cur = self.conn.cursor()

        res = cur.execute(sql_query)
        return res.fetchall() 

    def readLimit(self, table_name, columns = '*', limited = 1):
        if columns == '*':
            columns = self.getColumnName(table_name)

        column_list = ','.join(columns)
        
        sql_query = "SELECT {} FROM {} LIMIT {}".format(column_list, table_name, limited)
        cur = self.conn.cursor()

        res = cur.execute(sql_query)

        return columns, res.fetchall()



