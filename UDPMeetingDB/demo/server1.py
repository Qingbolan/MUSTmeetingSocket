from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from datetime import datetime  # 导入 datetime 模块

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    # 获取当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send(f"{username} has entered the room. Time: {now}", room=room)
    print(f"{username} has entered the room. Time: {now}, room: {room}")

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    # 获取当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send(f"{username} has left the room. Time: {now}", room=room)
    print(f"{username} has left the room. Time: {now}, room: {room}")

@socketio.on('message')
def handle_message(data):
    # 获取当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 包含用户名、房间号和时间
    message = {
        "username": data['username'],
        "room": data['room'],
        "time": now,
        "message": data['message']
    }
    emit('receive_message', message, room=data['room'])
    print(f"Message: {data['message']}, Time: {now}, room: {data['room']}")

if __name__ == '__main__':
    socketio.run(app, debug=False)
