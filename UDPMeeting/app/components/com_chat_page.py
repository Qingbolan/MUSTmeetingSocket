
from PyQt5.QtWidgets import (QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from ..components.com_msglst import MsgList, CommentInputArea, Worker
from qfluentwidgets import FluentIcon as FIF


class ChatRoom(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.msg_list = MsgList()
        self.msg_work = Worker(self.msg_list)

        layout.addWidget(self.msg_list,2)

        self.comment_input_area = CommentInputArea(self.msg_work)
        self.comment_input_area.setMaximumHeight(100)  # Set an appropriate maximum height
        self.comment_input_area.setMinimumHeight(50)  # Set an appropriate minimum height

        layout.addWidget(self.comment_input_area,1)

        self.test()

    def test(self):
        self.msg_list.addTextMsg("Hi everyone", "6:32 PM", True, "FR", "#9acd32")
        self.msg_list.addTextMsg("Hello", "6:32 PM", False, "TA", "#32cd32")

    def addTextMsg(self, msg, time, is_user, name, color):
        self.msg_list.addTextMsg(msg, time, is_user, name, color)