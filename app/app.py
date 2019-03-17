import pandas as pd
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy.engine import Connection, create_engine, Engine
from flask_cors import CORS


# con_string = os.getenv("DB_CONN", "not found")  # todo (see how to store this in an infra file)
CON_STRING = 'postgresql://postgres:postgres@ec2-18-222-180-141.us-east-2.compute.amazonaws.com:5432'
# db_table =  os.getenv("DB_TABLE", "not found")  # todo
DB_TABLE = 'locations'

# maximum number of records that can be returned by the 'get_all' API
MAX_RECORDS =  1000
# db_table =  os.getenv("MAX_RECORDS", "not found")  # todo

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)


# df = pd.DataFrame({"name": ["test"], "address": ["test address"], "type": ["house"]})


def insert_data(df: pd.DataFrame):
    engine = create_engine(CON_STRING)
    df.to_sql(name=DB_TABLE, con=engine, index=False, if_exists='append')
    engine.dispose()


def fetch_data():
    engine = create_engine(CON_STRING)
    df = pd.read_sql(f"select * from {DB_TABLE} limit {MAX_RECORDS}", con=engine)
    engine.dispose()
    return df


# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('address', type=str)
parser.add_argument('type', type=str)


class AllLocations(Resource):
    def get(self):
        df = fetch_data()
        df['created'] = df['created'].astype(str)
        df['id'] = df['id'].astype(str)
        data = {'data': df.to_dict(orient='split')['data']}
        return data


class AddLocation(Resource):
    def get(self):
        args = parser.parse_args()
        df = pd.DataFrame(args, index=[0])
        insert_data(df)
        return args


api.add_resource(AllLocations, '/get_all')
api.add_resource(AddLocation, '/add_new')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1221, debug=True)
