# coding:utf-8

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QSplitter
from qfluentwidgets import (FluentIcon, IconWidget, TextEdit,StrongBodyLabel,TogglePushButton,BodyLabel)

from qfluentwidgets import FluentIcon as FIF
from .launcher_interface import GalleryInterface
from ..common.translator import Translator
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.signal_bus import signalBus
# from ..common.processmanage import kill_process
from ..components.syscommand import SysCommand

from PyQt5.QtWidgets import QSizePolicy

class ModifiedIconCardView(QWidget):
    """ Modified Model card view to occupy maximum available height """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # Title at the top
        self.titleLabel = StrongBodyLabel(self.tr('命令行终端'), self)

        self.textEdit = SysCommand(self)
        # self.textEdit.setMarkdown("## stable diffusion 启动器 v1.1.3 \n * 2023.8.30 🚀\n * 一个便捷快速的启动器 ")
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.infoPanel = sdLauncherInfoPanel(FIF.COMMAND_PROMPT, self)
        self.infoPanel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.textEdit)
        self.splitter.addWidget(self.infoPanel)
        self.splitter.setStretchFactor(1, 1)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.titleLabel)  # Add the title to the top
        self.vBoxLayout.addWidget(self.splitter)
        self.vBoxLayout.setStretchFactor(self.splitter, 1)

        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)

    def __setQss(self):
        self.setObjectName('iconViewWithTopTitle')
        self.splitter.setStyleSheet("QSplitter::handle { background-color: transparent; }")
        StyleSheet.ICON_INTERFACE.apply(self)

    def setStatus(self,pid):
        self.sdFolder=cfg.get(cfg.sdFolders)
        print(self.sdFolder)
        self.Env=cfg.get(cfg.environFolders)
        print(self.Env)
        
        pythonPath = self.Env + "/python/python.exe"
        print(pythonPath)

        self.textEdit.launcher(f"cd {self.sdFolder}")
        self.textEdit.launcher(f"{pythonPath} webui.py --autolaunch")

class sdLauncherInfoPanel(QFrame):
    """ Model info panel """

    def __init__(self, model: FluentIcon, parent=None):
        super().__init__(parent=parent)\
        
        self.pid = 0

        self.iconWidget = IconWidget(model, self)
        self.iconNameTitleLabel = BodyLabel(self.tr('运行状态'), self)
        self.iconNameLabel = BodyLabel(model.value, self)
        self.enumNameTitleLabel = BodyLabel(self.tr('运行模式'), self)
        self.enumNameLabel = BodyLabel("模式L " + model.name, self)

        self.toggleButton = TogglePushButton('终止运行', self, FIF.REMOVE_FROM)
        # self.setStatusStopping()
        # self.toggleButton.clicked.connect(self.setStatusStopping)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 20, 16, 20)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(45)
        self.vBoxLayout.addWidget(self.iconNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.iconNameLabel)
        self.vBoxLayout.addSpacing(34)
        self.vBoxLayout.addWidget(self.enumNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.enumNameLabel)

        self.vBoxLayout.addSpacing(34)
        self.vBoxLayout.addWidget(self.toggleButton)

        self.iconWidget.setFixedSize(48, 48)
        self.setFixedWidth(216)

        self.iconNameTitleLabel.setObjectName('subTitleLabel')
        self.enumNameTitleLabel.setObjectName('subTitleLabel')

    def setIcon(self, icon: FluentIcon):
        self.iconWidget.setIcon(icon)
        self.nameLabel.setText(icon.value)
        self.iconNameLabel.setText(icon.value)
        self.enumNameLabel.setText("FluentIcon."+icon.name)

    # def setStatusStopping(self):
    #     self.toggleButton.setCheckable(False)
    #     self.toggleButton.setChecked(False)
    #     if self.pid != 0:
    #         success = kill_process(self.pid)
    #         if success:
    #             print(f"Successfully killed process with PID: {self.pid}")
    #         else:
    #             print(f"Failed to kill process with PID: {self.pid}")
    #     self.pid = 0

    def setStatusRunning(self,pid):
        print(pid)
        self.pid = pid
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(True)


# Update the TextInterface to use the new ModifiedIconCardView
class TextInterface(GalleryInterface):
    """ Model interface """

    def __init__(self, parent=None):
        super().__init__(
            title="启动以及命令行界面",
            subtitle="",
            parent=parent
        )
        self.setObjectName('textInterface')

        self.iconView = ModifiedIconCardView(self)
        self.vBoxLayout.addWidget(self.iconView)
        
        self.sdStatueEmit()
        
    def sdStatueEmit(self):
        signalBus.sdLaunchSignal.connect(self.iconView.setStatus)
        signalBus.sdLaunchSignal.connect(self.iconView.infoPanel.setStatusRunning)
