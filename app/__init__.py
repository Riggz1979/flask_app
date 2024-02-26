from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.database import db
from app.error_handlers import register_error_handlers
from app.event.views import event, EventListView, EventDetailView
from app.main.views import main
from app.user.views import user, UserListView, UserDetailView

import os

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
app.config['WTF_CSRF_ENABLED'] = False

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

# Class-based rules for task 40
app.add_url_rule('/class/users/', view_func=UserListView.as_view('user_list'))
app.add_url_rule('/class/users/<int:id>/', view_func=UserDetailView.as_view('user_detail'))
app.add_url_rule('/class/events/', view_func=EventListView.as_view('event_list'))
app.add_url_rule('/class/events/<int:id>/', view_func=EventDetailView.as_view('event_detail'))
# Error handlers
register_error_handlers(app)
print(app.config.get('DEBUG'))
