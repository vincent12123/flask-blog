from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inisialisasi app Flask
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'mysecretkey'  # Gunakan app.config, bukan variabel biasa

# Inisialisasi SQLAlchemy dan LoginManager
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Import routes setelah inisialisasi
from app import routes
