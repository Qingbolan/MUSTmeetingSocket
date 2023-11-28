import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit, QFormLayout
import socketio

sio = socketio.Client()
room = 'default_room'

# 全局变量来存储窗口实例
login_window = None
chat_window = None

class ChatWindow(QWidget):
    def __init__(self, token, username):
        super().__init__()
        self.token = token
        self.username = username  # 保存用户名以用于发送消息
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
        # 发送消息时附带用户名和令牌
        sio.emit('chat_message', {'username': self.username, 'token': self.token, 'room': room, 'message': message})

    def display_message(self, data):
        self.textEdit.append(data['username'] + ': ' + data['message'])

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.usernameInput = QLineEdit(self)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton('Login', self)
        self.loginButton.clicked.connect(self.login)

        formLayout = QFormLayout()
        formLayout.addRow('Username:', self.usernameInput)
        formLayout.addRow('Password:', self.passwordInput)
        formLayout.addWidget(self.loginButton)

        self.setLayout(formLayout)
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 200, 120)

    def login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        response = requests.post('http://localhost:7100/auth/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            global chat_window
            token = response.json()['access_token']
            chat_window = ChatWindow(token, username)  # 将用户名传递给聊天窗口
            chat_window.show()
            self.close()
        else:
            print("Login failed.")

@sio.on('connect')
def on_connect():
    print('Connection established')
    global chat_window
    if chat_window:
        # 加入房间时附带用户名和令牌
        sio.emit('join_room', {'username': chat_window.username, 'token': chat_window.token, 'room': room})

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from server')

@sio.on('receive_message')
def on_message(data):
    global chat_window
    if chat_window:
        chat_window.display_message(data)

def run_app():
    global login_window
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

def run_app():
    global login_window
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    # sio.connect('http://localhost:7100')  # 在应用程序事件循环开始之前建立连接
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
