from flask import request, jsonify
from models import FoodModel, OrderModel

def register_routes(app, db, socketio):
    @app.route("/api/foods", methods=["GET", "POST"])
    def foods():
        if request.method == "POST":
            data = request.json
            doc = FoodModel.create(db, data["name"], data["price"])
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

    @socketio.on("accept_order", namespace="/servers")
    def handle_accept(data):
        updated = OrderModel.assign_server(db, data["order_id"], data["server_id"])
        if updated:
            socketio.emit(
                "order_accepted",
                {"order_id": data["order_id"], "server_id": data["server_id"]},
                namespace="/admin"
            )
