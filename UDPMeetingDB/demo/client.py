import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit
import socketio

sio = socketio.Client()
room = 'room2'

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        self.lineEdit = QLineEdit(self)

        self.sendButton = QPushButton('Send', self)
        self.sendButton.clicked.connect(self.send_message)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.lineEdit)
        vbox.addWidget(self.sendButton)

        self.setLayout(vbox)
        self.setWindowTitle('Chat Room')
        self.setGeometry(600, 600, 700, 500)

    def send_message(self):
        message = self.lineEdit.text()
        self.lineEdit.clear()
        sio.emit('message', {'username': 'User', 'room': room, 'message': message})

    def display_message(self, data):
        self.textEdit.append(data['username'] + ': ' + data['message'])

@sio.on('connect')
def on_connect():
    print('connection established')
    sio.emit('join', {'username': 'User', 'room': room})

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

@sio.on('receive_message')
def on_message(data):
    print('message received with ', data)
    
    window.display_message(data)

def run_app():
    global window
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    run_app()
