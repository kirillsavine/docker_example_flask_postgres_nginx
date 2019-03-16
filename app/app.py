import pandas as pd
import os
import socket
import getpass
import threading, webbrowser

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy.engine import Connection, create_engine, Engine

# con_string = os.getenv("DB_CONN", "not found")  # todo (see how to store this in an infra file)
CON_STRING = 'postgresql://postgres:postgres@ec2-18-222-180-141.us-east-2.compute.amazonaws.com:5432'
# db_table =  os.getenv("DB_TABLE", "not found")  # todo
DB_TABLE = 'public.log'

app = Flask(__name__)
api = Api(app)


def insert_data(df: pd.DataFrame, engine: Engine):
    df.to_sql(name="log", con=engine, index=False, if_exists='append')

def fetch_data():
    engine = create_engine(CON_STRING)
    df = pd.read_sql(f"select * from {DB_TABLE}", con=engine)
    engine.dispose()
    return df



class Map(Resource):
    def get(self, id):
        return {id: todos[id]}

    def put(self, id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[id]}


@app.route("/")
def hello():
    user = getpass.getuser()

    html = "<h3>Hello, the name is: <code>{name}</code>!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>User:</b> {user}<br>" \
           "<hr> files:<br> {files}"

    files = '<br>'.join(os.listdir('.'))


    df = pd.DataFrame({'user': ['123'], 'x': [1]})
    insert_data(df)

    return html.format(
        name=os.getenv("MY_ENV_VAR", "not found"),
        hostname=socket.gethostname(),
        user=user,
        files=files
    )


if __name__ == "__main__":
    port = '80'
    url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(host='0.0.0.0', port=port, debug=True)
