from flask import Blueprint, jsonify
from ..models import User

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/search/<username>', methods=['GET'])
def search_user(username):
    users = User.query.filter(User.username.ilike(f'%{username}%')).all()
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_data)

