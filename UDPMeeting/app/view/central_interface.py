# coding:utf-8
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar,
                            SegmentedToggleToolWidget, FluentIcon)
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QSplitter
from qfluentwidgets import (Pivot,qrouter, SegmentedWidget,BodyLabel)
from ..components.QCodeEditor import QCodeEditor,CppHighlighter
from ..components.com_user_home_page import *
from ..components.com_msglst import *
from ..components.com_chat_page import ChatRoom
from ..common.config import cfg


from PyQt5.QtWidgets import QSizePolicy




class FriendInfolist(QWidget):
    def __init__(self, userImageList: list, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # self.meetingName = StrongBodyLabel(meetingName)
        # layout.addWidget(self.meetingName)

        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(0)  # No extra spacing
        self.line2_layout.setAlignment(Qt.AlignLeft)  # Align items to the left
        for user in userImageList:
            userImage = ToolButton(user)
            # userImage.setStyleSheet("ToolButton { border-radius: 50%; }")  # Set the border-radius
            userImage.setIconSize(QSize(40, 40))
            self.line2_layout.addWidget(userImage,0, Qt.AlignLeft)

        layout.addLayout(self.line2_layout, Qt.AlignLeft)


class centralInterface(QWidget):
    """ Tab interface """

    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName('centralInterface')

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabCount = 1

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.movableCheckBox = CheckBox(self.tr('IsTabMovable'), self)
        self.scrollableCheckBox = CheckBox(self.tr('IsTabScrollable'), self)
        self.shadowEnabledCheckBox = CheckBox(self.tr('IsTabShadowEnabled'), self)
        self.tabMaxWidthLabel = BodyLabel(self.tr('TabMaximumWidth'), self)
        self.tabMaxWidthSpinBox = SpinBox(self)
        self.closeDisplayModeLabel = BodyLabel(self.tr('TabCloseButtonDisplayMode'), self)

        self.closeDisplayModeComboBox = ComboBox(self)

        # self.friendsLabel = SubtitleLabel(FIF.PEOPLE,self.tr('Friends'), self)
        self.friendsLabel = SubtitleLabel(self.tr('ALL Friends'), self)
        self.friendsList = FriendInfolist(['app/resource/images/Qingbolan.jpg', 'app/resource/images/ShiHaoTong.jpg', 'app/resource/images/Arbitrary.jpg'])

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        # self.songInterface = QLabel('Song Interface', self)
        self.userHomeInterface = UserProfile(cfg.userName.value)
        
        self.albumInterface = ChatRoom()
        # self.artistInterface = QLabel('Artist Interface', self)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.shadowEnabledCheckBox.setChecked(True)

        self.tabMaxWidthSpinBox.setRange(60, 400)
        self.tabMaxWidthSpinBox.setValue(self.tabBar.tabMaximumWidth())

        self.closeDisplayModeComboBox.addItem(self.tr('Always'), userData=TabCloseButtonDisplayMode.ALWAYS)
        self.closeDisplayModeComboBox.addItem(self.tr('OnHover'), userData=TabCloseButtonDisplayMode.ON_HOVER)
        self.closeDisplayModeComboBox.addItem(self.tr('Never'), userData=TabCloseButtonDisplayMode.NEVER)
        self.closeDisplayModeComboBox.currentIndexChanged.connect(self.onDisplayModeChanged)

        self.addSubInterface(self.userHomeInterface,
                             'tabSongInterface', self.tr('userHome'), FIF.HOME)
        self.addSubInterface(self.albumInterface,
                             'tabAlbumInterface', self.tr('Group_meeting_one'), FIF.CHAT)

        self.controlPanel.setObjectName('controlPanel')
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.connectSignalToSlot()

        qrouter.setDefaultRouteKey(
            self.stackedWidget, self.userHomeInterface.objectName())

    def connectSignalToSlot(self):
        self.movableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setMovable(self.movableCheckBox.isChecked()))
        self.scrollableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setScrollable(self.scrollableCheckBox.isChecked()))
        self.shadowEnabledCheckBox.stateChanged.connect(
            lambda: self.tabBar.setTabShadowEnabled(self.shadowEnabledCheckBox.isChecked()))

        self.tabMaxWidthSpinBox.valueChanged.connect(self.tabBar.setTabMaximumWidth)

        self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        # self.setFixedHeight(280)
        # self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.movableCheckBox)
        self.panelLayout.addWidget(self.scrollableCheckBox)
        self.panelLayout.addWidget(self.shadowEnabledCheckBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.tabMaxWidthLabel)
        self.panelLayout.addWidget(self.tabMaxWidthSpinBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.closeDisplayModeLabel)
        self.panelLayout.addWidget(self.closeDisplayModeComboBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.friendsLabel)

        # self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.friendsList, 0, Qt.AlignTop)


    def addSubInterface(self, widget: QLabel, objectName, text, icon):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onDisplayModeChanged(self, index):
        mode = self.closeDisplayModeComboBox.itemData(index)
        self.tabBar.setCloseButtonDisplayMode(mode)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        self.tabBar.setCurrentTab(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def addTab(self):
        text = f'addnewChat({self.tabCount})'
        self.addSubInterface(FIF.CHAT)
        self.tabCount += 1

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(QLabel, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()


class TabInterface(QWidget):
    """ Pivot interface """

    Nav = SegmentedWidget

    def __init__(self):
        super().__init__()
        self.setObjectName('centralInterface')

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.songInterface = QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                             HIGHLIGHT_CURRENT_LINE=True,
                             SyntaxHighlighter=CppHighlighter)
        self.userHomeInterface = UserProfile("Qingbolan")
        self.albumInterface = QCodeEditor(self)
        self.artistInterface = QCodeEditor(self)

        # add items to pivot
        self.addSubInterface(self.userHomeInterface, 'userHomeInterface', self.tr('userHome'))
        self.addSubInterface(self.albumInterface, 'albumInterface', self.tr('group_meeting1'))

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignJustify)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.pivot.setCurrentItem(self.songInterface.objectName())

        qrouter.setDefaultRouteKey(self.stackedWidget, self.songInterface.objectName())

    def addSubInterface(self, widget: BodyLabel, objectName, text):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())
