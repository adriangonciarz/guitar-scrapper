import base64
import sqlite3
import uuid
from sqlite3 import Error

from utils import Item

sql_create_items_table_query = """CREATE TABLE IF NOT EXISTS items (
                                id text PRIMARY KEY,
                                link text NOT NULL,
                                brand text,
                                model text,
                                price float
                            );"""


class DBClient:
    def __init__(self, db_file):
        self.conn = None
        self.__create_connection(db_file)

    def __del__(self):
        if self.conn:
            self.conn.close()

    def create_items_table(self):
        self.__execute_sql(sql_create_items_table_query)

    def insert_item(self, item: Item, autocommit=True):
        hash_id = base64.b64encode(item.link.encode('ascii')).decode() if item.link else str(uuid.uuid4())
        insert_query = "INSERT INTO items(id,link,brand,model,price) VALUES('{}','{}','{}','{}','{}');".format(hash_id,
                                                                                                               item.link,
                                                                                                               item.brand,
                                                                                                               item.model,
                                                                                                               item.price)
        print(insert_query)
        self.__execute_sql(insert_query)
        if autocommit:
            self.__commit()

    def insert_items(self, items: [Item]):
        for item in items:
            self.insert_item(item, autocommit=False)
        self.__commit()

    def __create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def __execute_sql(self, sql_string):
        try:
            c = self.conn.cursor()
            c.execute(sql_string)
        except Error as e:
            print(e)

    def __commit(self):
        self.conn.commit()

    def select_all_items_and_print(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM items')
        rows = c.fetchall()
        print(rows)


if __name__ == '__main__':
    items = [
        Item(1, 'PRS Custom 24', '2050', 'http://onet.pl?item=1232345'),
        Item(2, 'PRS 408', '3500', 'http://onet.pl?item=12a3454'),
    ]
    cli = DBClient('test_db.db')
    cli.insert_items(items)
    cli.select_all_items_and_print()
