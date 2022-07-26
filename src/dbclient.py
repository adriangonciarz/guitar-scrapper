import base64
import uuid
from sqlite3 import Error

from config import config
from utils import sanitize_string_for_database
from models import Item
import mysql.connector

sql_create_items_table_query = """CREATE TABLE IF NOT EXISTS items (
                                id VARCHAR(255) PRIMARY KEY,
                                title TEXT NOT NULL,
                                link TEXT NOT NULL,
                                brand TINYTEXT,
                                model TINYTEXT,
                                price FLOAT,
                                currency TINYTEXT,
                                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                            );"""


class DBClient:
    def __init__(self, db_name=None):
        self.conn = None
        self.db_name = db_name
        self.__create_connection()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def create_items_table(self):
        self.__execute_sql(sql_create_items_table_query)

    def insert_item(self, item: Item, autocommit=True):
        hash_id = base64.b64encode(item.link.encode('ascii')).decode() if item.link else str(uuid.uuid4())
        insert_query = "INSERT INTO items(id,title,link,brand,model,price,currency) VALUES('{}','{}','{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE last_updated=CURRENT_TIMESTAMP;".format(
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
        c.execute('SELECT * FROM items ORDER BY last_updated DESC')
        return c.fetchall()

    def fetch_brand_items(self, brand_name):
        c = self.conn.cursor()
        c.execute(f"SELECT * FROM items WHERE brand='{brand_name}' ORDER BY last_updated DESC")
        return c.fetchall()

    def create_database(self, db_name):
        self.conn.cursor().execute(f"CREATE DATABASE {db_name}")

    def __create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=self.db_name
            )
            print('DB Connection successful')
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
