from bson.objectid import ObjectId

class FoodModel:
    COLLECTION = "food_items"

    @staticmethod
    def create(db, name, price):
        doc = {
            "name": name, 
            "price": price}
        res = db[FoodModel.COLLECTION].insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    @staticmethod
    def list_all(db):
        cursor = db[FoodModel.COLLECTION].find()
        return [{"id": str(d["_id"]), "name": d["name"], "price": d["price"]} for d in cursor]


class OrderModel:
    COLLECTION = "orders"

    @staticmethod
    def create(db, table_no, items, customer_name, mobile):
        doc = {
            "table_no": table_no,
            "items": items,
            "customer_name": customer_name,
            "mobile": mobile,
            "server_id": None
        }
        res = db[OrderModel.COLLECTION].insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    @staticmethod
    def list_all(db):
        cursor = db[OrderModel.COLLECTION].find()
        out = []
        for d in cursor:
            out.append({
                "id":          str(d["_id"]),
                "table_no":    d["table_no"],
                "items":       d["items"],
                "customer_name": d.get("customer_name"),
                "mobile":      d.get("mobile"),
                "server_id":   d.get("server_id")
            })
        return out

    @staticmethod
    def assign_server(db, order_id, server_id):
        res = db[OrderModel.COLLECTION].update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"server_id": server_id}}
        )
        return res.modified_count
