from flask import Flask, render_template, request

from config.config import DB_NAME
from dbclient import DBClient

app = Flask(__name__)


@app.route('/')
def index():
    db_client = DBClient(DB_NAME)
    brands = db_client.fetch_brands()
    return render_template('index.html', brands=brands)


@app.route('/all')
def all_items():
    db_client = DBClient(DB_NAME)
    data = db_client.fetch_all_items()
    return render_template('item_list.html', data=data)


@app.route('/brands', methods=['GET'])
def brand_items():
    args = request.args
    name = args.get('name')
    model = args.get('model')
    db_client = DBClient(DB_NAME)
    if model:
        data = db_client.fetch_brand_model_items(name, model)
    else:
        data = db_client.fetch_brand_items(name)
    return render_template('item_list.html', data=data)


if __name__ == '__main__':
    app.run()
