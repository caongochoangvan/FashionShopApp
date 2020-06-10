from fashionshop import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from flask import current_app, session


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    birthday = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    gender = db.Column(db.String(10), nullable = False, default = 'Female')
    # db.relationship
    comments = db.relationship('Comment', backref='author', lazy = True)
    # def get_reset_token(self, expires_sec = 1):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     else:
    #         return User.query.get(user_id)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)  
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    content_chatbot = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    def __repr__(self):
        return f"Comment('{self.title}','{self.date_posted}')" 

class Product(db.Model):
    # __searchable__ = ['title','description']
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(100), nullable = False) 
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(), nullable = True, default='default.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    cartitems = db.relationship('CartItem', backref='Product', lazy = True)
    comments = db.relationship('Comment', backref='product', lazy = True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Product('{self.title}','{self.price}','{self.image_file}')" 

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(100), nullable = False)
    products = db.relationship('Product', backref='type', lazy = True)
    def __repr__(self):
        return f"Category('{self.name}')" 
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    infor_id = db.Column(db.Integer, db.ForeignKey('infor.id'))
    def __repr__(self):
        return f"CartItem('{self.quantity}')" 
class Infor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    country = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(100), nullable = False)
    postcode = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(100), nullable = False)
    cartitems = db.relationship("CartItem", backref="cart", lazy = 'dynamic')
    order_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    total_price = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"Infor('{self.name}','{self.address}','{self.phone}')"
