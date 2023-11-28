from ..components.com_user_home_page import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import SegmentedWidget


class UserInterface(QWidget):
    
    Nav = SegmentedWidget

    def __init__(self):
        super().__init__()
        self.setObjectName('userInterface')

        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.pivot = self.Nav(self)
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.user_home_page = UserProfile("Qingbolan")
        h_layout.addWidget(self.user_home_page)
        self.setLayout(h_layout)  # Set the layout for the widget
