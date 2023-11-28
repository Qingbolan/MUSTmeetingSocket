# coding: utf-8

from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout

from qfluentwidgets import NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow, SplashScreen, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF

from .launcher_interface import GalleryInterface
from .setting_interface import SettingInterface
from .text_interface import TextInterface
from .dialog_interface import DialogInterface
from .user_interface import UserInterface
from .central_interface import centralInterface
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common.resource import *
from ..common.config import cfg

# from ..components.browser import Browser

import os

# import logging
import psutil
import GPUtil

# # 日志设置
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # 创建一个文件处理器并设置级别为 INFO
# file_handler = logging.FileHandler('app.log', mode='w')
# file_handler.setLevel(logging.INFO)

# # 创建一个格式器
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)

# # 添加文件处理器到默认的记录器
# logger = logging.getLogger()
# logger.addHandler(file_handler)
# logger.info('___App started___') 

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)


class UpdateTitleThread(QThread):
    update_title_signal = pyqtSignal(str)

    def run(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                gpu_usage = gpu.load * 100
            else:
                gpu_usage = "N/A"

            self.update_title_signal.emit(f'MUST_UDPmeeting (CPU: {cpu_usage}% - GPU: {gpu_usage}%)')

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.resizeEvent(None)

        self.settingInterface = SettingInterface(self)
        self.textInterface = TextInterface(self)
        self.dialogInterface = DialogInterface()
        self.userInterface = UserInterface()
        self.centralInterface = centralInterface()

        self.current_working_directory = os.getcwd()
        self.project_name = os.path.basename(self.current_working_directory)
        self.project_interface = f"{self.project_name}.interface"

        # initialize layout
        self.initLayout()
        self.initUpdateThread()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def initLayout(self):
        signalBus.switchToSampleCard.connect(self.switchToSample)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.centralInterface, FIF.HOME, "HOME CENTER")
        self.addSubInterface(self.textInterface, FIF.COMMAND_PROMPT, "RUNNING WINDOWS")
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.dialogInterface, FIF.CHAT, "MEETING ROOM")

        self.navigationInterface.addSeparator()
        self.navigationInterface.addItem(
                routeKey = self.project_interface,
                icon = self.file_icon(self.current_working_directory),
                text = self.project_name,
                onClick = lambda name=self.project_name: signalBus.switchToSampleCard.emit(self.userInterface.objectName(), 0),
                position = NavigationItemPosition.SCROLL,
                parentRouteKey=None
            )
        

        self.add_items_recursively(self.project_interface, self.current_working_directory)

        # add custom widget to bottom
        self.navigationInterface.addItem(
                routeKey = self.project_interface,
                icon = FIF.ALBUM,
                text = self.project_name,
                onClick = signalBus.switchToSampleCard.emit(self.userInterface.objectName(), 0),
                position = NavigationItemPosition.BOTTOM,
                parentRouteKey=None
            )

        # self.navigationInterface.addWidget(
        #     routeKey='avatar',
        #     widget=NavigationAvatarWidget('账号设置',':/gallery/images/logo.png'),
        #     onClick=self.onSupport,
        #     position=NavigationItemPosition.BOTTOM
        # )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('SETTING'), NavigationItemPosition.BOTTOM)
        
    def file_icon(self, file):
        if file.endswith('.py'):
            return FIF.CLOUD
        elif file.endswith('.h'):
            return FIF.FOLDER
        else:
            return FIF.PEOPLE
        
    def add_items_recursively(self, parent_interface, path):
        for item_name in os.listdir(path):
            full_item_path = os.path.join(path, item_name)
            self.navigationInterface.addItem(
                routeKey = f"{item_name}.interface",
                icon = self.file_icon(item_name),
                text = item_name,
                onClick = lambda name=item_name: signalBus.switchToSampleCard.emit(self.userInterface.objectName(), 0),
                position = NavigationItemPosition.SCROLL,
                parentRouteKey=parent_interface
            )
            if os.path.isdir(full_item_path):
                print(f'Adding {item_name} to {parent_interface}')
                self.add_items_recursively(f"{item_name}.interface", full_item_path)  # 递归调用

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('MUST_QuickCPP')

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
    
    def initUpdateThread(self):
        self.update_thread = UpdateTitleThread()
        self.update_thread.update_title_signal.connect(self.setWindowTitle)
        self.update_thread.start()

    
    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        """ add sub interface """
        self.stackedWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )


    def onSupport(self):
        w = MessageBox(
            'stable diffusion启动器🚀版本1.13',
            '基于stable-diffusion-webui开发的完全开源的stable diffusion资源整合包,在保证整个项目完整的情况下可一键启动',
            self
        )
        w.yesButton.setText('一键启动')
        w.cancelButton.setText('下次再说')
        if w.exec():
            signalBus.switchToSampleCard.emit('textInterface', 0)
            # import os
            # if os.path.exists(self.sdFolder):
            #     os.chdir(self.sdFolder)
            signalBus.sdLaunchSignal.emit(1)
            # print(f"{pythonPath} webui.py --autolaunch")


    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
    

    def switchToEditor(self, routeKey, filename):
        """ switch to sample """
        interfaces = self.findChildren(UserInterface)
        found = False
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
        
        if not found:
            self.addSubInterface(self.editorInterface, FIF.HOME, "代码编辑")
            self.stackedWidget.setCurrentWidget(self.editorInterface, False)
    
