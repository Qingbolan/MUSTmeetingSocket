
from PyQt5.QtWidgets import (QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from ..components.com_msglst import MsgList, CommentInputArea, Worker
from qfluentwidgets import FluentIcon as FIF
from ..common.config import cfg


from ..config import *

class ChatRoom(QWidget):

    new_message_signal = pyqtSignal(dict)  # 新的信号

    def __init__(self, username=cfg.userName.value,room="default_room"):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.userName = username
        self.msg_list = MsgList()
        self.msg_work = Worker(self.msg_list)

        layout.addWidget(self.msg_list,2)

        self.comment_input_area = CommentInputArea(self.msg_work,sio,room,self.userName)
        self.comment_input_area.setMaximumHeight(100)  # Set an appropriate maximum height
        self.comment_input_area.setMinimumHeight(50)  # Set an appropriate minimum height

        layout.addWidget(self.comment_input_area,1)

        self.new_message_signal.connect(self.update_message_list)


        # 新增代码：连接到 Socket.IO 服务器
        sio.emit('join', {'username': cfg.userName.value, 'room': room})

        # 注册 Socket.IO 事件
        @sio.on('connect')
        def on_connect():
            print('connection established')

        @sio.on('disconnect')
        def on_disconnect():
            print('disconnected from server')

        @sio.on('receive_message')
        def on_message(data):            
            self.new_message_signal.emit(data)

        self.test()

    @pyqtSlot(dict)
    def update_message_list(self, data):
        self.display_message(data)

    
    def display_message(self, data):
        self.msg_list.addTextMsg(data['message'], data['time'],self.userName==data['username'], f"app/resource/images/{data['username']}.jpg", "text")
        print(data['message'], data['time'],self.userName==data['username'], data['username'], "text")
        # addTextMsg(self, text, timestamp, ismyself, initials, color):

    def test(self):
        self.msg_list.addTextMsg("Hi everyone","2023-12-07 12:43:27" , True, "app/resource/images/logo.png", "text")
        # self.msg_list.addTextMsg("Hello", "2023-12-07 12:43:27", False, "app/resource/images/ShiHaoTong.jpg", "#32cd32")

    def addTextMsg(self, msg, time, is_user, name, color):
        # self.msg_list.addTextMsg(msg, time, is_user, f"app/resource/images/{name}.jpg", color)
        text = msg
        timestamp = "6:32 PM"
        lr = is_user
        initials = name
        print(initials)
        color = "#9acd32"
        # if self.msg_list is None:
        #     self.msg_list.add_message_signal.emit(text, timestamp, lr, initials, color)
        # else:
        self.msg_list.add_message_signal.emit(text, timestamp, lr, initials, color)
        # self.msg_list.addTextMsg(msg, "6:32 PM", is_user, "app/resource/images/ShiHaoTong.jpg", "#ebedf2")


# class ChatRoom(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout(self)
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.msg_list = MsgList()
#         self.msg_work = Worker(self.msg_list)

#         layout.addWidget(self.msg_list,2)

#         self.comment_input_area = CommentInputArea(self.msg_work)
#         self.comment_input_area.setMaximumHeight(100)  # Set an appropriate maximum height
#         self.comment_input_area.setMinimumHeight(50)  # Set an appropriate minimum height

#         layout.addWidget(self.comment_input_area,1)

#         self.test()

#     def test(self):
#         self.msg_list.addTextMsg("Hi everyone", "6:32 PM", True, "app/resource/images/Qingbolan.jpg", "#9acd32")

#     def addTextMsg(self, msg, time, is_user, name, color):
#         self.msg_list.addTextMsg(msg, time, is_user, name, color)