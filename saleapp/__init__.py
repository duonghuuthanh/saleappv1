from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "BG\xeb\xdd\t\xf1\x93\xbeWp\xbb\xffla V"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/saledb?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
admin = Admin(app=app, name='QUẢN LÝ BẢN HÀNG', template_mode='bootstrap3')
