from flask import Flask
from config import Config
from .extensions import db, login_manager, migrate

def CreateApp(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Initialize Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        if user and not user.deleted:
            return user
        return None
    
    with app.app_context():

        from app import models

        @app.shell_context_processor
        def make_shell_context():
            return {'db': db, 'models': models}

    # Register blueprints


    @app.route('/')
    def index():
        return "Welcome to the Flask Web Application!"
    
    return app