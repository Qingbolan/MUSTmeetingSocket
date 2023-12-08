import socketio
sio = socketio.Client()
# room = 'default_room'
chat_server_address = 'http://home.fqgy.qingbolan.net:18900'
sio.connect(chat_server_address)