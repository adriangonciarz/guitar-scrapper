import base64
import sqlite3
import uuid
from sqlite3 import Error
from utils import sanitize_string_for_database
from models import Item

sql_create_items_table_query = """CREATE TABLE IF NOT EXISTS items (
                                id text PRIMARY KEY,
                                title text NOT NULL,
                                link text NOT NULL,
                                brand text,
                                model text,
                                price float,
                                currency text,
                                created timestamp NOT NULL DEFAULT current_timestamp
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
        insert_query = "INSERT INTO items(id,title,link,brand,model,price,currency) VALUES('{}','{}','{}','{}','{}','{}','{}');".format(
            hash_id,
            sanitize_string_for_database(item.name),
            item.link,
            sanitize_string_for_database(item.brand) if item.brand else None,
            sanitize_string_for_database(item.model) if item.model else None,
            item.price,
            item.currency
        )
        print(insert_query)
        self.__execute_sql(insert_query)
        if autocommit:
            self.__commit()

    def insert_items(self, items: [Item]):
        for item in items:
            self.insert_item(item, autocommit=False)
        self.__commit()

    def fetch_brands(self):
        c = self.conn.cursor()
        c.execute("SELECT brand FROM items GROUP BY brand;")
        return c.fetchall()

    def fetch_all_items(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM items')
        return c.fetchall()

    def fetch_brand_items(self, brand_name):
        c = self.conn.cursor()
        c.execute(f"SELECT * FROM items WHERE brand='{brand_name}'")
        return c.fetchall()

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
