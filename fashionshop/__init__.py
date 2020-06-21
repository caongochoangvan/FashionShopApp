from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.permanent_session_lifetime = timedelta(minutes = 20)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
es = Elasticsearch()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from fashionshop import routes