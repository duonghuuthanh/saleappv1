from saleapp import dao, app
import csv
import os


def export():
    products = dao.read_products()
    p = os.path.join(app.root_path, "data/products.csv")

    with open(p, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "description", "price", "image", "category_id"])
        writer.writeheader()
        for pro in products:
            writer.writerow(pro)

    return p
