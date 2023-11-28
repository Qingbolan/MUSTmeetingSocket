from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QFrame, QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize
from qfluentwidgets import SmoothScrollArea,ToolButton,CaptionLabel

class UserAvatar(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(100, 100)
        self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)
        self.setMask(self.pixmap().mask())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        # Draw the circular avatar
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.pixmap())

class UserStatusIndicator(QLabel):
    def __init__(self, is_online=True, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(10, 10)
        self.setStyleSheet("QLabel { background-color: %s; border-radius: 5px; }" % ('green' if is_online else 'red'))

class UserWidget(QFrame):
    def __init__(self, user_name, avatar_path, is_online=True, parent=None):
        super().__init__(parent=parent)
        # self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setFixedSize(100, 100)

        layout = QVBoxLayout()
        
        # avatar_pixmap = QPixmap(avatar_path)
        # self.avatar = UserAvatar(avatar_pixmap)
        self.avatar = ToolButton(avatar_path)
        self.avatar.setIconSize(QSize(80, 80))
        self.avatar.setStyleSheet("ToolButton { border-radius: 50%; }")  # Set the border-radius


        self.line2_layout = QHBoxLayout()
        self.username = CaptionLabel(user_name)
        self.line2_layout.addWidget(self.username, Qt.AlignHCenter)
        self.status_indicator = UserStatusIndicator(is_online)
        self.line2_layout.addWidget(self.status_indicator, Qt.AlignHCenter)

        # Align username label in the center below the avatar
        self.username.setAlignment(Qt.AlignCenter)

        # Add widgets to the layout
        layout.addWidget(self.avatar)
        # layout.addWidget(self.username)
        # layout.addWidget(self.status_indicator, 0, Qt.AlignHCenter)
        layout.addLayout(self.line2_layout,0)

        self.setLayout(layout)

class UsersDisplayWidget(QWidget):
    def __init__(self, users_data, max_avatars_per_row=5, parent=None):
        super().__init__(parent=parent)
        self.v_layout = QVBoxLayout()
        self.v_layout.setAlignment(Qt.AlignCenter)
        
        current_h_layout = QHBoxLayout()
        current_h_layout.addStretch(1)  # Add a stretchable space to center the avatars

        for index, user_data in enumerate(users_data):
            if index % max_avatars_per_row == 0 and index != 0:
                current_h_layout.addStretch(1)  # Add a stretchable space on the right
                self.v_layout.addLayout(current_h_layout)  # Add the filled row to the vertical layout
                current_h_layout = QHBoxLayout()  # Create a new row
                current_h_layout.addStretch(1)  # Add a stretchable space on the left

            user_widget = UserWidget(user_data['name'], user_data['avatar'], user_data['is_online'])
            current_h_layout.addWidget(user_widget)

        current_h_layout.addStretch(1)  # Add a stretchable space on the right for the last row
        self.v_layout.addLayout(current_h_layout)  # Add the last row to the vertical layout

        self.setLayout(self.v_layout)

    def calculate_avatars_per_row(self, total_users):
        # This is an example strategy to calculate avatars per row
        # You can implement more complex logic depending on your requirements
        if total_users <= 5:
            return total_users
        elif total_users <= 10:
            return 5
        else:
            return 6  # or more, depending on your maximum width

# Example usage
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    users_data = [
        {'name': 'Alice', 'avatar': 'app/resource/images/kunkun.png', 'is_online': True},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        {'name': 'Bob', 'avatar': 'app/resource/images/kunkun.png', 'is_online': False},
        # ... Add more user data as needed
    ]

    users_display_widget = UsersDisplayWidget(users_data)
    users_display_widget.show()
    users_display_widget.resize(800, 600)

    sys.exit(app.exec_())
