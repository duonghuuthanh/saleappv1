from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from saleapp import app, dao, utils, login
from saleapp import decorator
from flask_login import login_user, logout_user
from saleapp.decorator import login_required
import json


@app.route("/")
def index():
    return render_template("index.html",
                           products=dao.read_products(),
                           latest_products=dao.read_products(is_latest=True))


@app.route("/products")
def product_list():
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    from_price = float(request.args["from_price"]) if request.args.get("from_price") else None
    to_price = float(request.args["to_price"]) if request.args.get("to_price") else None

    return render_template("product-list.html", products=dao.read_products(keyword=keyword,
                                                                           from_price=from_price,
                                                                           to_price=to_price))


@app.route("/products/detail/<int:product_id>")
def product_detail(product_id):
    return render_template("product-detail.html")


@app.route("/products/<int:category_id>")
def product_list_by_cate(category_id):
    return render_template("product-list.html", products=dao.read_products_by_cate_id(cate_id=category_id))


@app.route("/api/products/<int:product_id>", methods=["delete"])
def delete_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({"status": 200, "product_id": product_id})

    return jsonify({"status": 500, "error_message": "Something Wrong!!!"})


@app.route("/products/add", methods=["get", "post"])
@decorator.login_required
def add_product():
    """
    add: /products/add
    update: /products/add?product_id
    :return: template
    """
    err_msg = None
    if request.method.lower() == "post":
        if request.args.get("product_id"): # UPDATE
            d = dict(request.form.copy())
            d["product_id"] = request.args["product_id"]
            if dao.update_product(**d):
                return redirect(url_for('product_list', product_id=d["product_id"]))
            else:
                err_msg = "Something wrong, go back later!!!"
        else: # ADD
            if dao.add_product(**dict(request.form)):
                return redirect(url_for('product_list'))
            else:
                err_msg = "Something wrong, go back later!!!"

    categories = dao.read_categories()
    product = None
    if request.args.get("product_id"):
        product = dao.read_product_by_id(product_id=int(request.args["product_id"]))

    return render_template("product-add.html", categories=categories, product=product, err_msg=err_msg)


@app.route("/products/export")
def export_product():
    p = utils.export()

    return send_file(filename_or_fp=p)


@app.route("/api/pro/<int:product_id>", methods=["delete"])
def del_pro(product_id):
    if dao.del_product(product_id=product_id):
        return jsonify({"status": 200, "product_id": product_id})

    return jsonify({"status": 500, "err_msg": "Something Wrong!!!"})


@app.route("/login", methods=["get", "post"])
def signin_user():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for('index'))
        else:
            err_msg = "Something wrong!!!"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("index"))


@app.route("/register", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mat khau khong khop"
        else:
            if dao.add_user(name=name, username=username, password=password):
                return redirect(url_for("signin_user"))
            else:
                err_msg = "Something Wrong!!!"

    return render_template("register.html", err_msg=err_msg)


@app.route("/cart", methods=['get', 'post'])
@login_required
def cart():
    err_msg = ""
    if request.method == 'POST':
        if 'cart' in session and session['cart']:
            if dao.add_receipt(cart_products=session["cart"].values()):
                session['cart'] = None
                return redirect(url_for('cart'))
            else:
                err_msg = "Add receipt failed"
        else:
            err_msg = "No products in cart"

    return render_template("payment.html", err_msg=err_msg)


@app.route("/api/cart", methods=["post"])
def add_to_cart():
    data = json.loads(request.data)
    product_id = data.get("product_id")
    name = data.get("name")
    price = data.get("price")
    if "cart" not in session or session['cart'] == None:
        session["cart"] = {}

    cart = session["cart"]

    product_key = str(product_id)
    if product_key in cart: # đa từng bỏ sản phẩm product_id vào giỏ
        cart[product_key]["quantity"] = cart[product_key]["quantity"] + 1
    else: # bỏ sản phẩm mới vào giỏ
        cart[product_key] = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session["cart"] = cart
    q = 0
    s = 0
    for c in list(session["cart"].values()):
        q = q + c['quantity']
        s = s + c['quantity'] * c['price']

    return jsonify({"success": 1, "quantity": q, 'sum': s})



@app.context_processor
def append_cate():
    common = {
        "categories": dao.read_categories()
    }

    if 'cart' in session and session['cart']:
        q = 0
        s = 0
        for c in list(session["cart"].values()):
            q = q + c['quantity']
            s = s + c['quantity'] * c['price']

        common['cart_quantity'] = q
        common['cart_price'] = s

    return common


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    from saleapp.admin import *

    app.run(debug=True, port=5000)
