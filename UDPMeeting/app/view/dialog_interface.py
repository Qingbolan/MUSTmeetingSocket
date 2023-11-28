# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget)
from PyQt5.QtWidgets import QSizePolicy

from qfluentwidgets import StrongBodyLabel, ListWidget, SegmentedWidget,CommandBar

from PyQt5.QtCore import QPoint, Qt, QStandardPaths
from PyQt5.Qt import QPoint, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QSizePolicy,QHBoxLayout
from qfluentwidgets import (Action, CommandBar, Action,
                            CommandBarView, Flyout, StrongBodyLabel, FlyoutAnimationType)
from qfluentwidgets import FluentIcon as FIF
from ..components.com_msglst import MsgList, CommentInputArea
from ..components.com_onesBoard import UsersDisplayWidget
from ..components.com_chat_page import ChatRoom


# 用户列表模块
class UserList(ListWidget):
    def __init__(self):
        super().__init__()
        self.addItem("Fred (You)")
        self.addItem("Tara")

# 公共聊天模块
class PublicChat(ChatRoom):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        
# 会议室信息模块
class MeetingHeader(QWidget):
    def __init__(self):
        super().__init__()
        self.info_label = StrongBodyLabel("Cameras of MeetingRoom are here!")
        layout = QVBoxLayout(self)
        layout.addWidget(self.info_label)

# 功能按钮区模块
class MeetingBoardArea(QWidget):
    def __init__(self):
        super().__init__()
        self.is_default = True
        self.layout = QVBoxLayout(self)
        # 添加功能按钮
        self.info_label = StrongBodyLabel("function Board of MeetingRoom is here!")
        # layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.commandBar=self.createCommandBar()
        self.layout.addWidget(self.commandBar,Qt.AlignCenter)

        self.users_display_widget = None

        if self.is_default:
            users_data = [
                {'name': 'Alice', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': True},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                {'name': 'Bob', 'avatar': 'app/resource/images/Qingbolan.jpg', 'is_online': False},
                # ... Add more user data as needed
            ]

            self.users_display_widget = UsersDisplayWidget(users_data)
            self.layout.addWidget(self.users_display_widget)
        # self.chat_button = PushButton("Chat")
        # self.polling_button = PushButton("Polling")
        # self.webcams_button = PushButton("Webcams")
        # self.audio_button = PushButton("Audio")
        # self.emojis_button = PushButton("Emojis")
        # self.screen_sharing_button = PushButton("Screen Sharing")
        # self.breakout_rooms_button = PushButton("Breakout Rooms")
        # self.whiteboard_button = PushButton("Whiteboard")
        # 将按钮添加到布局
        # layout.addWidget(self.chat_button)
        # layout.addWidget(self.polling_button)
        # layout.addWidget(self.webcams_button)
        # layout.addWidget(self.audio_button)
        # layout.addWidget(self.emojis_button)
        # layout.addWidget(self.screen_sharing_button)
        # layout.addWidget(self.breakout_rooms_button)
        # layout.addWidget(self.whiteboard_button)
        

    def createCommandBar(self):
        bar = CommandBar(self)
        bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)


        newPhoto = Action(FIF.ADD, self.tr('新建'), shortcut='Ctrl+N')
        newPhoto.triggered.connect(self.open_image)

        zoom_in = Action(FIF.ZOOM_IN, self.tr('放大'),shortcut='Ctrl+U')
        zoom_in.triggered.connect(self.large_click)

        zoom_out = Action(FIF.ZOOM_OUT, self.tr('缩小'),shortcut='Ctrl+D')
        zoom_out.triggered.connect(self.small_click)


        bar.addActions([
            newPhoto,
            Action(FIF.ROTATE, self.tr('Rotate')),
            zoom_in,
            zoom_out
        ])

        bar.addSeparator()
        bar.addActions([
            Action(FIF.EDIT, self.tr('Edit'), checkable=True),
            Action(FIF.INFO, self.tr('Info')),
            Action(FIF.DELETE, self.tr('Delete')),
            Action(FIF.SAVE, self.tr('Save'), triggered=self.saveImage),
            Action(FIF.SHARE, self.tr('Share')),
        ])
        bar.addHiddenAction(Action(FIF.PRINT, self.tr('Print'), shortcut='Ctrl+P'))
        bar.addHiddenAction(Action(FIF.SETTING, self.tr('Settings'), shortcut='Ctrl+S'))

        return bar

    def createCommandBarFlyout(self):
        view = CommandBarView(self)

        view.addAction(Action(FIF.SHARE, self.tr('Share')))
        view.addAction(Action(FIF.SAVE, self.tr('Save'), triggered=self.saveImage))
        view.addAction(Action(FIF.HEART, self.tr('Add to favorate')))
        view.addAction(Action(FIF.DELETE, self.tr('Delete')))

        view.addHiddenAction(Action(FIF.PRINT, self.tr('Print'), shortcut='Ctrl+P'))
        view.addHiddenAction(Action(FIF.SETTING, self.tr('Settings'), shortcut='Ctrl+S'))
        view.resizeToSuitableWidth()

        x = self.imageLabel.width()
        pos = self.imageLabel.mapToGlobal(QPoint(x, 0))
        Flyout.make(view, pos, self, FlyoutAnimationType.FADE_IN)

    def saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('Save image'),
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='PNG (*.png)'
        )
        if not ok:
            return

        self.imageLabel.image.save(path)

    def open_image(self):
        img_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "*.jpg;;*.png;;*.jpeg")
        if img_name:
            self.box.set_image(img_name)
    
    def on_image_clicked(self, img_path):
        self.box.set_image(img_path)
        self.update()

    def large_click(self):
        if self.box.scale < 2:
            self.box.scale += 0.1
            self.box.adjustSize()
            self.update()

    def small_click(self):
        if self.box.scale > 0.1:
            self.box.scale -= 0.2
            self.box.adjustSize()
            self.update()

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

from qfluentwidgets import ListWidget, ScrollArea, StrongBodyLabel

# UserList, PublicChat, MeetingInfo, and ButtonsArea classes remain the same

class MeetingWindow(QWidget):
    def __init__(self):
        # super().__init__()
        # self.setWindowTitle('Demo Meeting - BigBlueButton')
        # self.setGeometry(400, 400, 1200, 1000)

        h_layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self.public_chat = PublicChat()
        h_layout.addWidget(self.public_chat, 1)

        right_v_layout = QVBoxLayout()

        self.right_v_layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.meeting_header = MeetingHeader()
        right_v_layout.addWidget(self.meeting_header)  # No stretch factor

        self.meeting_board = MeetingBoardArea()
        right_v_layout.addWidget(self.meeting_board, 1)  # A stretch factor of 1 to take up remaining space


        h_layout.addLayout(right_v_layout, 2)

        central_widget = QWidget()
        central_widget.setLayout(h_layout)
        self.setCentralWidget(central_widget)

class ModifiedIconCardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        h_layout = QHBoxLayout()
        self.public_chat = PublicChat()
        h_layout.addWidget(self.public_chat, 1)

        right_v_layout = QVBoxLayout()
        self.meeting_info = MeetingHeader()
        right_v_layout.addWidget(self.meeting_info, 1)

        self.buttons_area = MeetingBoardArea()
        right_v_layout.addWidget(self.buttons_area, 3)

        h_layout.addLayout(right_v_layout, 2)
        self.setLayout(h_layout)  # Set the layout for the widget

class DialogInterface(QWidget):
    
    Nav = SegmentedWidget

    def __init__(self):
        super().__init__()
        self.setObjectName('dialogInterface')

        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.pivot = self.Nav(self)
        h_layout = QHBoxLayout()
        self.public_chat = PublicChat()
        h_layout.addWidget(self.public_chat, 1)

        right_v_layout = QVBoxLayout()
        self.meeting_info = MeetingHeader()
        right_v_layout.addWidget(self.meeting_info, 1)

        self.buttons_area = MeetingBoardArea()
        right_v_layout.addWidget(self.buttons_area, 3)

        h_layout.addLayout(right_v_layout, 2)
        self.setLayout(h_layout)  # Set the layout for the widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MeetingWindow()
    mainWin.show()
    sys.exit(app.exec_())
