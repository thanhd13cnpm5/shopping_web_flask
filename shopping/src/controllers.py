from flask import redirect, render_template, request, session, url_for, jsonify, flash
from sqlalchemy import JSON

from utils import *
import json

@app.route("/login", methods=["get", "post"])
def login():
    ermg=""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = validate_user(username=username, password=password)
        if user:
            session["admin"] = admin
            if "next" in request.args:
                return redirect(request.args["next"])
            return redirect(url_for("index"))
        else:
            ermg= "Đăng nhập không thành công"
    return render_template("login.html", ermg=ermg)

@app.route("/logout")
def logout():
    session["admin"] = None
    return redirect(url_for("home"))


@app.route("/home", methods=['GET', 'POST'])
def home():
    products = product.query.all()
    return render_template("home.html", products=products)

@app.route("/shop", methods=['GET', 'POST'])
def shop():
    products = product.query.all()
    return render_template("shop.html", products=products)

@app.route("/detailProduct/<int:id>", methods=['GET', 'POST'])
def detailProduct(id):
    pro = product.query.get(id)
    return render_template("single-product.html", pro=pro)

@app.route("/register_costumer", methods=["GET", "POST"])
def register_costumer():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = str(hashlib.md5(request.form["password"].strip().encode("utf-8")).hexdigest())
        email = request.form["email"]
        new = user.query.filter_by(email=email).first()

        if new is not None:
            return redirect(url_for("home"))
        User = user(name=name, username=username, password=password, email=email)
        db.session.add(User)
        db.session.commit()

        return redirect(url_for("logincostumer"))

    return render_template("registercostumer.html")

@app.route("/logincostumer", methods=["get", "post"])
def logincostumer():
    ermg=""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

        User = user.query.filter_by(username=username, password=password).first()

        if not User is None:
            return redirect(url_for("home"))
        else:
            ermg = "login failed"
    return render_template('logincostumer.html',ermg=ermg)


@app.route("/logoutcostumer")
def logoutcostumer():
    session["user"] = None
    return redirect(url_for("home"))

@app.route("/index", methods=['GET', 'POST'])
def index():
    products = product.query.all()
    cata = catagory.query.all()
    return render_template("index.html", products=products, cata=cata)

@app.route("/catagorylist", methods=['GET', 'POST'])
def catagorylist():
    catagories = catagory.query.all()
    return render_template("catagorylist.html", catagories=catagories)

@app.route("/addproduct", methods = ['POST', 'GET'])
def addproduct():
    cata = catagory.query.all()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        discription = request.form["discription"]
        discount = request.form["discount"]
        image = request.form["image"]
        catagory_id = request.form["catagory"]

        pro = product(name=name, price=price, discription=discription, discount=discount, image=image, catagory_id=catagory_id)
        db.session.add(pro)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("addproduct.html", cata=cata)

@app.route("/addcatagory", methods=["POST","GET"])
def addcatagory():
    if request.method == "POST":
        name_catagory = request.form["name_catagory"]

        catagories = catagory(name_catagory=name_catagory)
        db.session.add(catagories)
        db.session.commit()
        return redirect(url_for("catagorylist"))

    return render_template("addcatagory.html")

@app.route("/updateproduct/<int:id>", methods=['POST', 'GET'])
def updateproduct(id):
    pro = product.query.get(id)
    if request.method == "POST":
        pro.name = request.form["name"]
        pro.price = request.form["price"]
        pro.discription = request.form["discription"]
        pro.discount = request.form["discount"]
        pro.image = request.form["image"]

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("updateproduct.html", pro=pro)

@app.route("/updatecatagory/<int:id>", methods=["POST","GET"])
def updatecatagory(id):
    catagories = catagory.query.get(id)
    if request.method == "POST":
        catagories.name_catagory = request.form["name_catagory"]

        db.session.commit()
        return redirect(url_for("catagorylist"))

    return render_template("updatecatagory.html", catagories=catagories)

@app.route("/deletecatagory/<int:id>", methods=["POST", "GET"])
def deletecatagory(id):
    cata = catagory.query.get(id)
    db.session.delete(cata)
    db.session.commit()

    return redirect(url_for("catagorylist"))

@app.route("/deleteproduct/<int:id>", methods=["POST", "GET"])
def deleteproduct(id):
    pro = product.query.get(id)
    db.session.delete(pro)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/api/cart", methods=["GET", "POST"])
def add_to_cart():
    if "cart" not in session:
        session["cart"] = {}
    cart = session["cart"]

    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    image = data.get('image')
    discription = data.get('discription')
    catagory_id = data.get('catagory_id')

    if id in cart:
       cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "image": image,
            "discription": discription,
            "catagory_id": catagory_id,
            "quantity": 1
        }

    session["cart"] = cart

    total_amount, total_quan = cart_stats(cart)

    return jsonify({
        "total_amount": total_amount,
        "total_quantity": total_quan,
        "cart": cart
    })

@app.route("/pay")
def payment():
    total_amount = cart_stats(session.get("price"))
    total_quan = cart_stats(session.get("count"))
    # total_amount,total_quan = cart_stats(session.get("cart"))
    return render_template("cart.html", total_amount=total_amount, total_quantity=total_quan)

@app.route("/api/pay", methods=["POST"])
def pay():
    if "cart" in session and session["cart"]:
        add_receipt(cart=session["cart"])
        del session["cart"]

        return jsonify({"message": "successed"})
    return jsonify({"message": "failed"})

@app.route("/api/cart/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    if "cart" in session:
        cart = session["cart"]
        if item_id in cart:
            del cart[item_id]
            session["cart"] = cart

            return jsonify({"message": "succeed", "code": 200, "item_id": item_id})
    return jsonify({"message": "failed", "code": 500})

@app.route("/api/cart/<item_id>", methods=["POST"])
def update_item(item_id):
    if "cart" in session:
        cart = session["cart"]
        data = request.json
        if item_id in cart and "quantity" in data:
            cart[item_id]["quantity"] = int(data["quantity"])
            session["cart"] = cart
            total_amount1 = cart_stats(session.get("price"))
            total_quan1 = cart_stats(session.get("count"))

            return jsonify({"message": "succeed", "code": 200,
                            "item_id": item_id, "total_quantity1": total_quan1,
                            "total_amount1": total_amount1})
    return jsonify({"message": "failed", "code": 500})

@app.route('/search', methods=['POST'])
def search():
    products = product.query.all()
    productsToRender = []
    for pro in products:
        if request.form["search"].lower().strip() in pro.name.lower().strip() \
                or request.form["search"].lower().strip() in pro.discription.lower().strip():
            productsToRender.append(pro)
    return render_template('search.html', products=productsToRender)

if __name__=="__main__":
    app.run(debug=True)
