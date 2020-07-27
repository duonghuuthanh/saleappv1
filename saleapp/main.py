from flask import render_template, request, redirect, url_for, jsonify
from saleapp import app
from saleapp import dao


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


if __name__ == "__main__":
    app.run(debug=True)
