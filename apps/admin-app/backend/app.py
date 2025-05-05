from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient

import config
from routes import register_routes

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

# MongoDB client
client = MongoClient(config.MONGODB_URI)
db = client[config.DB_NAME]
print(f"▶︎ Connected to MongoDB: {config.MONGODB_URI}, DB: {config.DB_NAME}")

# Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

# Routes (pass in db and socketio)
register_routes(app, db, socketio)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
