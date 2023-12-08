from PyQt5.QtWidgets import QDialog, QVBoxLayout,  QFormLayout
from qfluentwidgets import TitleLabel, LineEdit, PushButton, MessageBox, StrongBodyLabel,AvatarWidget,ToolButton
from PyQt5.QtGui import QPixmap, QColor, QPalette, QBrush
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MUST Meeting Login / Register")
        self.setFixedSize(400, 350)
        
        palette = QPalette()
        brush = QBrush(QColor(30, 30, 30))  # 暗色背景，RGB值可以根据需要调整
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        # 初始化表单
        self.initLoginForm()

    def initLoginForm(self):
        # 清理现有布局
        self.clearLayout(self.layout)

        # # 重新添加图片
        # self.layout.addWidget(self.labelImage)

        # 登录表单布局
        formLayout = QFormLayout()
        formLayout.setSpacing(10)
        formLayout.setAlignment(Qt.AlignCenter)
        self.username = LineEdit(self)
        self.password = LineEdit(self)
        self.password.setEchoMode(LineEdit.Password)
        formLayout.addRow(AvatarWidget('app/resource/images/Qingbolan.jpg',self))
        formLayout.addRow(StrongBodyLabel("Username:"), self.username)
        formLayout.addRow(StrongBodyLabel("Password:"), self.password)
        self.layout.addLayout(formLayout)

        # 登录按钮
        self.loginButton = PushButton("Login", self)
        self.loginButton.clicked.connect(self.handleLogin)
        self.layout.addWidget(self.loginButton)

        # 注册切换按钮
        self.registerButton = PushButton("Go to Register", self)
        self.registerButton.clicked.connect(self.initRegisterForm)
        self.layout.addWidget(self.registerButton)

    def initRegisterForm(self):
        # 清理现有布局
        self.clearLayout(self.layout)

        # 注册表单布局
        formLayout = QFormLayout()
        self.username = LineEdit(self)
        self.password = LineEdit(self)
        self.confirmPassword = LineEdit(self)
        self.email = LineEdit(self)
        self.password.setEchoMode(LineEdit.Password)
        self.confirmPassword.setEchoMode(LineEdit.Password)
        formLayout.addRow(AvatarWidget('app/resource/images/Qingbolan.jpg',self))
        formLayout.addRow(StrongBodyLabel("Username:"), self.username)
        formLayout.addRow(StrongBodyLabel("Password:"), self.password)
        formLayout.addRow(StrongBodyLabel("Confirm Password:"), self.confirmPassword)
        formLayout.addRow(StrongBodyLabel("Email:"), self.email)
        self.layout.addLayout(formLayout)

        # 注册按钮
        self.registerButton = PushButton("Register", self)
        self.registerButton.clicked.connect(self.handleRegister)
        self.layout.addWidget(self.registerButton)

        # 登录切换按钮
        self.loginButton = PushButton("Go to Login", self)
        self.loginButton.clicked.connect(self.initLoginForm)
        self.layout.addWidget(self.loginButton)

    def handleLogin(self):
        # 登录逻辑
        self.accept()

    def handleRegister(self):
        # 注册逻辑
        MessageBox.information(self, "Register", "Register logic not implemented.")

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def getUsername(self):
        return self.username.text()
