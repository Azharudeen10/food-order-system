from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from routes import register_routes
from flask_socketio import SocketIO

load_dotenv()

DATABASE = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI")


app = Flask(__name__)
CORS(app)

# base directory of your project
basedir = os.path.abspath(os.path.dirname(__file__))

# point uploads into static/uploads under your app
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, os.getenv("UPLOAD_FOLDER"))
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


client = MongoClient(MONGO_URI)
db = client[DATABASE]

socketio = SocketIO(app, cors_allowed_origins="*")
register_routes(app, db, socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True)
