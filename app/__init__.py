from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from .config import Config
from .models import db, Employee
from .routes import orders, session 

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Register blueprints
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)

# Initialize LoginManager
login = LoginManager(app)
login.login_view = "session.login"

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))
