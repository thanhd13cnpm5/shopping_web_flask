from flask import json, jsonify
import hashlib
from models import *

def read_users():
    with open(os.path.join(app.root_path, "data/users.json"),
              encoding="utf-8") as f:
        return json.load(f)

def validate_user(username, password):
    users = read_users()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    for user in users:
        if user["username"].strip() == username.strip() and user["password"] == password:
            return user
    return None



def cart_stats(cart):
    count = 0
    price = 0
    if cart:
        for p in cart.values():
            price = price + p["quantity"] * p["price"]
            count = count + p["quantity"]
        return price, count

def add_receipt(cart):
    receipt = Receipt(customer_id=1)
    db.session.add(receipt)

    for p in list(cart.values()):
        detail = ReceiptDetail(quantity=p["quantity"], price=p["price"], product_id=p["id"], receipt=receipt)
        db.session.add(detail)

    db.session.commit()
