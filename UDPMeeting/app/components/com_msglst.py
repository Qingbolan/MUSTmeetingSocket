import sys
from PyQt5.QtCore import Qt, QRect, QPointF,QSize
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QVBoxLayout
from qfluentwidgets import PushButton, StrongBodyLabel, LineEdit,ListWidget,TextEdit,ToolButton
from qfluentwidgets import FluentIcon as FIF
from ..common.config import cfg


DEFAULT_HEAD = "path_to_default_profile_image.png"
DEFAULT_MSG = 'Hello, is there anyone?'
DEFAULT_TIMESTAMP = '00:00 PM'
DEFAULT_INITIALS = 'XX'
DEFAULT_INITIALS_BG = '#555555'

class InitialsLabel(StrongBodyLabel):
    def __init__(self, initials, color):
        super().__init__()
        self.setText(initials)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"background-color: {color}; color: white; border-radius: 15px;")
        # self.setFixedSize(30, 30)
        font = self.font()
        font.setPointSize(10)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        

class TextItem(QWidget):
    def __init__(self, listItem, listView, text=DEFAULT_MSG, timestamp=DEFAULT_TIMESTAMP, lr=True, initials=DEFAULT_INITIALS, color=DEFAULT_INITIALS_BG):
        super().__init__()
        self.listItem = listItem
        self.listView = listView

        # Create the main horizontal layout
        hbox = QHBoxLayout()
        # hbox.setContentsMargins(15, 10, 15, 10)
        # hbox.setSpacing(10)

        # Create the profile picture (or initials label)
        # self.initials_label = InitialsLabel(initials, color)
        self.initials_label = ToolButton(initials)
        self.initials_label.setIconSize(QSize(40, 40))
        # self.initials_label.setBaseSize(QSize(40, 40))
        # self.initials_label.setFixedSize(40, 40)  # Size of the profile picture

        # Create the timestamp label
        self.timestamp_label = StrongBodyLabel(timestamp)
        self.timestamp_label.setStyleSheet("color: grey;")

        # Create the text bubble
        # self.message_bubble = BubbleText(listItem, listView, text, timestamp, lr)
        self.message_bubble = ToolButton(text)
        # self.message_bubble.setStyleSheet("background-color: transparent;")
        self.message_bubble.setText(text)

        # Create a vertical layout for the timestamp and text bubble
        vbox = QVBoxLayout()
        vbox.addWidget(self.timestamp_label, 0, Qt.AlignLeft if lr else Qt.AlignRight)
        vbox.addWidget(self.message_bubble, 0, Qt.AlignLeft if lr else Qt.AlignRight)
        vbox.setSpacing(0)

        # Add widgets to the horizontal layout
        if lr:  # If the message is from the sender
            hbox.addWidget(self.initials_label, 0, Qt.AlignTop)
            hbox.addLayout(vbox)
            hbox.addStretch(1)
        else:  # If the message is from the receiver
            hbox.addStretch(1)
            hbox.addLayout(vbox)
            hbox.addWidget(self.initials_label, 0, Qt.AlignTop)

        self.setLayout(hbox)

# class ImageItem(QWidget):
#     '''显示文字的Widget内容，为了让消息可以删除增加listItem和list传递到文本控件'''
#     def __init__(self, listItem, listView, img = DEFAULT_MSG, lr=True, head = DEFAULT_HEAD):
#         super(ImageItem,self).__init__()
#         hbox = QHBoxLayout()
#         img = BubbleImage(listItem,listView,img,lr)
#         head = LabelHead(head)
#         head.setFixedSize(50,50)

#         if lr is not True:
#             hbox.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Preferred))
#             hbox.addWidget(img)
#             hbox.addWidget(head)
#         else:
#             hbox.addWidget(head)
#             hbox.addWidget(img)
#             hbox.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Preferred))
            
#         hbox.setContentsMargins(0,0,0,0)
#         self.setLayout(hbox)
#         self.setContentsMargins(0,0,0,0)


from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QTimer

class MsgList(ListWidget):
    # Define a signal that can carry the parameters needed for the new message
    add_message_signal = pyqtSignal(str, str, bool, str, str)

    def __init__(self):
        super(MsgList, self).__init__()
        # Connect the signal to the slot
        self.add_message_signal.connect(self.addTextMsg)
        # self.setFixedWidth(400)


    @pyqtSlot(str, str, bool, str, str)
    def addTextMsg(self, text, timestamp, ismyself, initials, color):
        listItem = QListWidgetItem(self)
        textItem = TextItem(listItem, self, text, timestamp, ismyself, initials, color)
        listItem.setSizeHint(textItem.sizeHint())
        self.addItem(listItem)
        self.setItemWidget(listItem, textItem)

    # def addImageMsg(self,img = DEFAULT_IMG, lr = True, head = DEFAULT_HEAD):
    #     it = QListWidgetItem(self)
    #     wid = self.size().width()
    #     item = ImageItem(it,self,img,lr,head) #增加必须指定本list和本item用于删除item
    #     # item.setEnabled(False) #对象灰度显示，不能导致ITEM不可选
    #     it.setSizeHint(item.sizeHint())
    #     it.setFlags(Qt.ItemIsEnabled)# 设置Item不可选择
    #     self.addItem(it)
    #     self.setItemWidget(it,item)
    #     self.setCurrentItem(it)


class Worker(QObject):

    add_message_signal = pyqtSignal(str, str, bool, str, str)


    def __init__(self, msg_list:MsgList = None):
        super(Worker, self).__init__()
        self.msg_list = msg_list
        if msg_list is not None:
            self.add_message_signal.connect(self.add_message)

    # A method that's called to add a message; it could be connected to a signal in the real application
    def add_message_test(self, msg_list=None):
        # Emit the signal with the necessary parameters
        text = "Hi everyone"
        timestamp = "6:32 PM"
        lr = True
        initials = "app/resource/images/Qingbolan.jpg"
        color = "#9acd32"
        if msg_list is None:
            self.msg_list.add_message_signal.emit(text, timestamp, lr, initials, color)
        else:
            msg_list.add_message_signal.emit(text, timestamp, lr, initials, color)

    def add_message(self, msg:dict, msg_list=None):
        # Emit the signal with the necessary parameters
        text = msg['text']
        timestamp = msg['timestamp']
        lr = msg['lr']
        initials = msg['initials']
        color = msg['color']
        if msg_list is None:
            self.msg_list.add_message_signal.emit(text, timestamp, lr, initials, color)
        else:
            msg_list.add_message_signal.emit(text, timestamp, lr, initials, color)


from PyQt5.QtWidgets import QHBoxLayout
from qfluentwidgets import TextEdit, PushButton

class CommentInputArea(QWidget):
    def __init__(self, work:Worker = None, sio=None, room=None, userName="User", parent=None):
        super().__init__(parent=parent)
        self.work = work
        self.sio = sio
        self.room = room
        self.userName = userName
        self.setupUi()

    def setupUi(self):
        # Create the horizontal layout
        h_layout = QHBoxLayout(self)
        h_layout.setContentsMargins(5, 5, 5, 5)  # Adjust margins as needed

        # Create the text edit where users can type their message
        self.text_edit = TextEdit(self)
        self.text_edit.setPlaceholderText("Please input your message...")  # Placeholder text
        h_layout.addWidget(self.text_edit, 1)  # Add text edit to layout with stretch

        # Create the send button
        self.send_button = PushButton("send",self)
        # Optionally connect the button to a slot to handle the send action
        self.send_button.clicked.connect(self.on_send_clicked)
        h_layout.addWidget(self.send_button,0,Qt.AlignTop)

        self.setLayout(h_layout)

    def on_send_clicked(self):
        # Get the text from the text edit
        text = self.text_edit.toPlainText()
        print(text)
        self.sio.emit('message', {'username': cfg.userName.value, 'room': self.room, 'message': text})

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ml = MsgList()
    ml.setMinimumSize(400, 1000)
    ml.addTextMsg("Hi everyone", "6:32 PM", True, "app/resource/images/Qingbolan.jpg", "#9acd32")
    ml.addTextMsg("Hello", "6:32 PM", False, "app/resource/images/ShiHaoTong.jpg", "#ebedf2")
    ml.show()
    worker = Worker(ml)

    # QTimer to simulate an event triggering the signal emission
    timer = QTimer()
    timer.timeout.connect(lambda: worker.add_message_test())
    timer.start(500)  # For example, emit the signal every 5 seconds
    sys.exit(app.exec_())
