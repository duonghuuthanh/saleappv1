from saleapp import app
import json
import os


def read_products(keyword=None, from_price=None, to_price=None):
    with open(os.path.join(app.root_path, "data/products.json"), encoding="utf-8") as f:
        products = json.load(f)

        if keyword:
            return [product for product in products if product["name"].lower().find(keyword.lower()) >= 0]

        if from_price and to_price:
            return [product for product in products if product["price"] >= from_price and product["price"] <= to_price]

    return products


def read_products_by_cate_id(cate_id):
    return [product for product in read_products() if product["category_id"] == cate_id]
    # products = read_products()
    # result = []
    # for product in products:
    #     if product.category_id == cate_id:
    #         result.append(product)
    #
    # return result


if __name__ == "__main__":
    print(read_products())
