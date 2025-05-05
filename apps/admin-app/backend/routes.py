from flask import request, jsonify
from models import FoodModel, OrderModel, ServerModel
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from models import FoodModel, OrderModel

def register_routes(app, db, socketio):
    @app.route("/api/foods", methods=["GET", "POST"])
    def foods():
        if request.method == "POST":
            name        = request.form["name"]
            price       = int(request.form["price"])
            description = request.form.get("description", "")
            file        = request.files.get("image")
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                image_url = f"/static/uploads/{filename}"

            doc = FoodModel.create(db, name, price, description, image_url)
            return jsonify(doc), 201

        return jsonify(FoodModel.list_all(db))


    @app.route("/api/orders", methods=["GET", "POST"])
    def orders():
        if request.method == "POST":
            data = request.json
            doc = OrderModel.create(
                db,
                data["table_no"],
                data["items"],
                data.get("name"),
                data.get("mobile")
            )
            socketio.emit("new_order", doc, namespace="/servers")
            return jsonify(doc), 201
        return jsonify(OrderModel.list_all(db))

    @app.route("/api/servers", methods=["GET", "POST"])
    def servers():
        if request.method == "POST":
            data = request.json
            doc = ServerModel.create(db, data["name"], data["age"])
            return jsonify(doc), 201
        return jsonify(ServerModel.list_all(db))

    @socketio.on("accept_order", namespace="/servers")
    def handle_accept(data):
        updated = OrderModel.assign_server(db, data["order_id"], data["server_id"])
        if updated:
            socketio.emit(
                "order_accepted",
                {"order_id": data["order_id"], "server_id": data["server_id"]},
                namespace="/admin"
            )
