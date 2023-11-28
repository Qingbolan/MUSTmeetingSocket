from flask import Blueprint
from flask_socketio import emit, join_room, leave_room, send,SocketIO
from .. import socketio
from flask_jwt_extended import jwt_required, get_jwt_identity


chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# @socketio.on('join_room', namespace='/chat')
# # @jwt_required()
# def handle_join_room(data):
#     # current_user_id = get_jwt_identity()
#     join_room(data['room'])
#     emit('room_announcement', {'message': f"{data['username']} has joined the room."}, room=data['room'])

# @socketio.on('leave_room', namespace='/chat')
# def handle_leave_room(data):
#     leave_room(data['room'])
#     emit('room_announcement', {'message': f"{data['username']} has left the room."}, room=data['room'])

# @socketio.on('chat_message', namespace='/chat')
# def handle_chat_message(data):
#     emit('receive_message', {'message': data['message']}, room=data['room'])

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def handle_message(data):
    emit('receive_message', data, room=data['room'])