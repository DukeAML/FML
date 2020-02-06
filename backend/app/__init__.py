from flask import Flask
from flask_cors import CORS
from config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from app import routes

# see following for flask help: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world 