# startup_script.py
from flask import Flask
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def setup_database(app):
    with app.app_context():
        db.create_all()  # 创建所有数据库表
        add_initial_user()  # 添加初始用户

def add_initial_user():
    if User.query.filter_by(username='Qingbolan').first() is None:
        # 如果用户不存在，则创建新用户
        new_user = User(
            username='Qingbolan', 
            password_hash=generate_password_hash('MUSTmeeting2023')
        )
        db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':
    app = create_app(Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates'))  # 创建 Flask 应用
    setup_database(app)  # 设置数据库并添加初始用户
