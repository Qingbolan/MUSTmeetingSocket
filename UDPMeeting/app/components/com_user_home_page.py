import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QHBoxLayout,
    QListWidgetItem, QFormLayout,QFrame,QDialog
)
from qfluentwidgets import StrongBodyLabel,SubtitleLabel, LineEdit, PushButton, ListWidget, Dialog, ToolButton,TitleLabel
from PyQt5.QtCore import Qt, QSize


# Placeholder function for backend signature update
def update_user_signature(user_id, new_signature):
    print(f"User {user_id}'s new signature: {new_signature}")
    # Implement actual update logic here

# Placeholder function for backend password change
def change_user_password(user_id, old_password, new_password):
    print(f"User {user_id}'s password change requested")
    # Implement actual update logic here

class ChangePasswordDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Change Password')
        layout = QFormLayout(self)

        self.old_password_edit = LineEdit(self)
        self.old_password_edit.setEchoMode(LineEdit.Password)
        self.new_password_edit = LineEdit(self)
        self.new_password_edit.setEchoMode(LineEdit.Password)
        self.confirm_password_edit = LineEdit(self)
        self.confirm_password_edit.setEchoMode(LineEdit.Password)

        layout.addRow("Old Password", self.old_password_edit)
        layout.addRow("New Password", self.new_password_edit)
        layout.addRow("Confirm New Password", self.confirm_password_edit)

        change_button = PushButton('Change Password', self)
        change_button.clicked.connect(self.onChangePassword)

        layout.addWidget(change_button)

    def onChangePassword(self):
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        
        if new_password != confirm_password:
            print("New passwords do not match")
            return
        
        # Call the backend password change function
        change_user_password(self.user_id, old_password, new_password)
        self.accept()


class MeetingInfoWidget(QWidget):
    def __init__(self, meetingName: str, userImageList: list, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.meetingName = StrongBodyLabel(meetingName)
        layout.addWidget(self.meetingName)

        self.line2_layout = QHBoxLayout()
        self.line2_layout.setSpacing(0)  # No extra spacing
        self.line2_layout.setAlignment(Qt.AlignLeft)  # Align items to the left
        for user in userImageList:
            userImage = ToolButton(user)
            # userImage.setStyleSheet("ToolButton { border-radius: 50%; }")  # Set the border-radius
            userImage.setIconSize(QSize(40, 40))
            self.line2_layout.addWidget(userImage,0, Qt.AlignLeft)

        layout.addLayout(self.line2_layout, Qt.AlignLeft)

class UserProfile(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = str(user_id)
        self.controlPanel = QFrame(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # User avatar
        h_layout = QHBoxLayout()
        self.panelLayout = QVBoxLayout(self.controlPanel)
        self.panelLayout.setSpacing(4)

        v_layout = QVBoxLayout()
        avatar = ToolButton(f'app/resource/images/{self.user_id}.jpg')
        avatar.setIconSize(QSize(150, 150))
        # avatar.setStyleSheet("ToolButton { border-radius: 50%; }")  # Set the border-radius
        # avatar.setPixmap(QPixmap('app/resource/images/Qingbolan.jpg').scaled(180, 180, Qt.KeepAspectRatio))
        h_layout.addWidget(avatar, alignment=Qt.AlignHCenter)

        # Non-editable information
        username_label = TitleLabel(self.user_id, self)
        v_layout.addWidget(username_label, alignment=Qt.AlignVCenter)

        self.panelLayout.setSpacing(4)
        birthday_label = StrongBodyLabel('Birthday: 2001/11/22', self)
        v_layout.addWidget(birthday_label, alignment=Qt.AlignVCenter)

        self.panelLayout.setSpacing(4)
        sign_label = StrongBodyLabel('Signal: yjh2022', self)
        v_layout.addWidget(sign_label, alignment=Qt.AlignVCenter)

        self.panelLayout.setSpacing(4)
        change_password_button = PushButton('change password', self)
        change_password_button.clicked.connect(self.onChangePassword)
        v_layout.addWidget(change_password_button)

        h_layout.addLayout(v_layout)

        layout.addLayout(h_layout)


        # update_signature_button = QPushButton('更新签名', self)
        # update_signature_button.clicked.connect(self.onUpdateSignature)
        # layout.addWidget(update_signature_button)

        # Change password button

        separator = QWidget(self)
        separator.setFixedHeight(2)
        # separator.setStyleSheet("background-color: #c3c3c3;")
        layout.addWidget(separator)


        # Recent meetings list
        meetings_list_label = SubtitleLabel('Recent Meeting', self)
        layout.addWidget(meetings_list_label)

        self.meetings_list = ListWidget(self)
        layout.addWidget(self.meetings_list)
        self.populate_meetings()  # Populate the list with recent meetings

        self.setLayout(layout)

    def onUpdateSignature(self):
        new_signature = self.signature_edit.text()
        update_user_signature(self.user_id, new_signature)

    def onChangePassword(self):
        dialog = ChangePasswordDialog(self.user_id, self)
        dialog.exec_()

    def populate_meetings(self):
        # for i in range(5):
        #     meeting_name = f'Meeting {i+1}'
        #     user_image_list = [':/gallery/images/kunkun.png', ':/gallery/images/kunkun.png']

        #     # Create a QListWidgetItem
        #     meeting_item = QListWidgetItem(self.meetings_list)
        #     self.meetings_list.addItem(meeting_item)

        #     # Create an instance of MeetingInfoWidget and set it as the item widget
        #     meeting_widget = MeetingInfoWidget(meeting_name, user_image_list)
        #     self.meetings_list.setItemWidget(meeting_item, meeting_widget)

        #     meeting_widget_size = meeting_widget.sizeHint()
        #     meeting_item.setSizeHint(meeting_widget_size)
        meeting_name ='Group Meeting One'
        user_image_list = ['app/resource/images/Qingbolan.jpg', 'app/resource/images/ShiHaoTong.jpg', 'app/resource/images/Arbitrary.jpg']

        # Create a QListWidgetItem
        meeting_item = QListWidgetItem(self.meetings_list)
        self.meetings_list.addItem(meeting_item)

        # Create an instance of MeetingInfoWidget and set it as the item widget
        meeting_widget = MeetingInfoWidget(meeting_name, user_image_list)
        self.meetings_list.setItemWidget(meeting_item, meeting_widget)

        meeting_widget_size = meeting_widget.sizeHint()
        meeting_item.setSizeHint(meeting_widget_size)

        meeting_name ='Voice Meeting Test'
        user_image_list = ['app/resource/images/Qingbolan.jpg', 'app/resource/images/ShiHaoTong.jpg']

        # Create a QListWidgetItem
        meeting_item = QListWidgetItem(self.meetings_list)
        self.meetings_list.addItem(meeting_item)

        # Create an instance of MeetingInfoWidget and set it as the item widget
        meeting_widget = MeetingInfoWidget(meeting_name, user_image_list)
        self.meetings_list.setItemWidget(meeting_item, meeting_widget)

        meeting_widget_size = meeting_widget.sizeHint()
        meeting_item.setSizeHint(meeting_widget_size)

if __name__ == '__main__':
    app = QApplication([])
    profile = UserProfile(user_id=1)  # Placeholder user ID
    profile.setGeometry(100, 100, 300, 600)
    profile.show()
    sys.exit(app.exec_())
