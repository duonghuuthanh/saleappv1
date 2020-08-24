from saleapp import admin, db
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Product, Category, User

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))
