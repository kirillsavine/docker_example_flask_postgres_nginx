from flask import Flask
import pandas as pd
import os
import socket
import getpass
import threading, webbrowser
from sqlalchemy.engine import Connection, create_engine, Engine

app = Flask(__name__)


def insert_data(df: pd.DataFrame, engine: Engine):
    df.to_sql(name="log", con=engine, index=False, if_exists='append')


@app.route("/")
def hello():
    user = getpass.getuser()

    html = "<h3>Hello, the name is: <code>{name}</code>!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>User:</b> {user}<br>" \
           "<hr> files:<br> {files}"

    files = '<br>'.join(os.listdir('.'))
    con_string = os.getenv("DB_CONN", "not found")
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
