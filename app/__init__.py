import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.database import db
from app.error_handlers import register_error_handlers
from app.event.views import event
from app.main.views import main
from app.user.views import user

app = Flask(__name__)
load_dotenv()
DEBUG = os.getenv('DEBUG') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
PORT = int(os.getenv('PORT'))
DATABASE = os.getenv('DATABASE')
WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED')

app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['PORT'] = PORT
app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

# Blueprints registration
app.register_blueprint(event)
app.register_blueprint(user)
app.register_blueprint(main)

# Error handlers
register_error_handlers(app)

if __name__=='__main__':
    app.run()
