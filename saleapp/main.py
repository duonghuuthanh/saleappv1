from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from saleapp import app, dao, utils
from saleapp import decorator


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def product_list():
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    from_price = float(request.args["from_price"]) if request.args.get("from_price") else None
    to_price = float(request.args["to_price"]) if request.args.get("to_price") else None

    return render_template("product-list.html", products=dao.read_products(keyword=keyword,
                                                                           from_price=from_price,
                                                                           to_price=to_price))


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
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.check_login(username=username, password=password)
        if user:
            # Login thanh cong
            session["user"] = user
            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for('index'))
        else:
            err_msg = "Something wrong!!!"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None

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
                return redirect(url_for("login"))
            else:
                err_msg = "Something Wrong!!!"

    return render_template("register.html", err_msg=err_msg)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
