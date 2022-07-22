from flask import Flask, request, render_template
import sqlite3

from dbclient import DBClient

app = Flask(__name__)


@app.route('/')
def v_timestamp():
    db_client = DBClient('OLXScrapper.db')
    data = db_client.fetch_all_items()
    return render_template('item_list.html', data=data)

if __name__ == '__main__':
    app.run()