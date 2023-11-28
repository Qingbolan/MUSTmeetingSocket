from flask_sqlalchemy import SQLAlchemy
from .database import db
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
import os

socketio = SocketIO()
login_manager = LoginManager()
jwt = JWTManager()


def init_app(app):
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Server.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key_here'  # JWT 密钥
    db.init_app(app)
    
    
    login_manager.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    
    with app.app_context():
        db.create_all()



def create_app(app):    
    from .routes.chat import chat_bp
    from .routes.auth import auth_bp
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)
    init_app(app)
    return app
