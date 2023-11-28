import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import cv2
import numpy as np

class VideoPlayer(QWidget):
    def __init__(self, udp_address, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.cap = cv2.VideoCapture(udp_address)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30 fps

    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

def main():
    app = QApplication(sys.argv)

    # UDP 地址
    udp_address = "udp://127.0.0.1:8900"

    player = VideoPlayer(udp_address)
    player.setWindowTitle("Video Player")
    player.setGeometry(100, 100, 800, 600)
    player.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
