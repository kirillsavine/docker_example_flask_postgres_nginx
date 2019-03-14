import pandas as pd
import os
import socket
import getpass
import threading, webbrowser

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy.engine import Connection, create_engine, Engine

# con_string = os.getenv("DB_CONN", "not found")  # todo (see how to store this in an infra file)
con_string = 'postgresql://postgres:postgres@localhost:5432'
# db_table =  os.getenv("DB_TABLE", "not found")  # todo
db_table = 'postgres.log'

app = Flask(__name__)
api = Api(app)


def insert_data(df: pd.DataFrame, engine: Engine):
    df.to_sql(name="log", con=engine, index=False, if_exists='append')

def fetch_data(engine: Engine):
    df.read_sql(f"select * from {db_table}")

class Map(Resource):
    def get(self, id):
        return {todo_id: todos[id]}

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

    engine = create_engine(con_string)
    df = pd.DataFrame({'user': ['123'], 'x': [1]})
    insert_data(df, engine)
    engine.dispose()

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
