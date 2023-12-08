import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QColorDialog
from PyQt5.QtGui import *
from threading import Thread

from .Tools.Permissions import Permission
from .Tools.network import MConnection
import math
from PyQt5.QtCore import *

from qfluentwidgets import (Action, CommandBar, Action,
                            CommandBarView, Flyout, StrongBodyLabel, FlyoutAnimationType)
from qfluentwidgets import FluentIcon as FIF


class DrawingArea(QWidget):
    mousePressed = pyqtSignal(QMouseEvent)
    mouseMoved = pyqtSignal(QMouseEvent)
    mouseReleased = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        super(DrawingArea, self).__init__(parent)
        self.initImage()
        self.brushSize = 3
        self.brushColor = Qt.black
        self.drawingTool = 'pencil'
        self.drawing = False
        self.lastPoint = QPoint()
        self.rectStartPoint = QPoint()
        self.tempImage = None

    def initImage(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newImage = QImage(self.width(), self.height(), QImage.Format_RGB32)
            newImage.fill(Qt.white)
            painter = QPainter(newImage)
            painter.drawImage(QPoint(0, 0), self.image)
            self.image = newImage

    def mousePressEvent(self, event):
        # print("Mouse pressed")
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            if self.drawingTool in ['rectangle', 'ellipse']:
                self.rectStartPoint = event.pos()
                self.tempImage = self.image.copy()
            # if event.button() == Qt.LeftButton:
            self.mousePressed.emit(event)

    def mouseMoveEvent(self, event):
        # print("Mouse moved")
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            if self.drawingTool in ['rectangle', 'ellipse']:
                self.image = self.tempImage.copy()
                painter = QPainter(self.image)
                self.drawShape(event.pos(), painter)
            else:
                painter = QPainter(self.image)
                self.drawLineTo(event.pos(), painter)
            painter.end()
            self.update()
            self.mouseMoved.emit(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            if self.drawingTool in ['rectangle', 'ellipse']:
                painter = QPainter(self.image)
                self.drawShape(event.pos(), painter)
                painter.end()
            self.drawing = False
            self.update()
            self.mouseReleased.emit(event)

    def drawLineTo(self, endPoint, painter):
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.lastPoint = endPoint

    def drawShape(self, endPoint, painter):
        rect = QRect(self.rectStartPoint, endPoint).normalized()
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if self.drawingTool == 'rectangle':
            painter.drawRect(rect)
        elif self.drawingTool == 'ellipse':
            painter.drawEllipse(rect)

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def setTool(self, tool):
        print(tool)
        self.drawingTool = tool

    def setColor(self, color):
        self.brushColor = color

    def clearImage(self):
        self.image.fill(Qt.white)
        self.update()

class Whiteboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Whiteboard')
        self.setGeometry(1000, 1000, 1000, 1000)

        self.drawingArea = DrawingArea()

        layout = QVBoxLayout()
        self.commandBar=self.createCommandBar()
        layout.addWidget(self.commandBar,Qt.AlignCenter)
        layout.addWidget(self.drawingArea)

        # centralWidget = QWidget()
        self.setLayout(layout)
        # self.setCentralWidget(centralWidget)

        self.show()
    
    
    def createCommandBar(self):
        bar = CommandBar(self)
        bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)


        pencilTool = Action(FIF.ADD, self.tr('Pencil'), shortcut='Ctrl+P')
        pencilTool.triggered.connect(lambda: self.drawingArea.setTool('pencil'))
        bar.addAction(pencilTool)

        RectangleTool = Action(FIF.ZOOM_IN, self.tr('Rectangle'),shortcut='Ctrl+R')
        RectangleTool.triggered.connect(lambda: self.drawingArea.setTool('rectangle'))
        bar.addAction(RectangleTool)

        EllipseTool = Action(FIF.ZOOM_OUT, self.tr('Ellipse'),shortcut='Ctrl+E')
        EllipseTool.triggered.connect(lambda: self.drawingArea.setTool('ellipse'))
        bar.addAction(EllipseTool)

        bar.addSeparator()

        sltColorTool = Action(FIF.ZOOM_IN, self.tr('Color'),shortcut='Ctrl+R')
        sltColorTool.triggered.connect(self.selectColor)
        bar.addAction(sltColorTool)

        CleanTool = Action(FIF.ZOOM_OUT, self.tr('Clean'),shortcut='Ctrl+E')
        CleanTool.triggered.connect(self.drawingArea.clearImage)
        bar.addAction(CleanTool)
        
        return bar

    def selectColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.drawingArea.setColor(color)


class DrawingTools(Whiteboard):
    Colors = {'b': QColor('blue'), 'r': QColor('red'), 'g': QColor('green'), 'o': QColor('#ff8c00'),
              'y': QColor('yellow'), 'c': QColor('cyan'), 'p': QColor('purple'), 
              'd': QColor('black'), 's': QColor('white')}
    line_width = 2

    def __init__(self, connection=MConnection("ac","180.94.143.9", 8500)):
        super().__init__()
        self.connection = connection
        self.permissions = Permission(self.connection)
        self.drawingArea.drawingTool = 'pencil'  # 初始化 drawingTool 属性
        self.color = 'black'  # 初始化默认颜色
        # 重新绑定事件处理函数
        self.drawingArea.mousePressed.connect(self.onMouseDown)
        self.drawingArea.mouseMoved.connect(self.onMouseMove)
        self.drawingArea.mouseReleased.connect(self.onMouseUp)
        self.start_message_receiving_thread()

    def run(self):
        while True:
            try:
                msg = self.my_connexion.receive_message()
                if( msg[0] in ['O', 'C', 'L', 'R', 'S', 'E', 'D', 'Z', 'T', 'DR']):
                    self.draw_from_message(msg)
                    self.save_and_load.append_to_Logs(msg)
                elif( msg[0] in ['P', 'A', 'RE']):
                    self.permissions.user_communication(msg)
                    self.update_connected_user()
                elif( msg[0] in ['TA'] ):
                    self.print_message(msg)
            except ValueError:
                pass
            except IndexError:
                pass
            except ConnectionResetError:
                self.myWhiteBoard.destroy()

    def onMouseDown(self, event):
        self.left_but = "down"
        # print("left click")
        self.x1_line_pt, self.y1_line_pt = event.pos().x(), event.pos().y()

    def onMouseUp(self, event):
        self.left_but = "up"
        # print("released")
        self.x2_line_pt, self.y2_line_pt = event.pos().x(), event.pos().y()
        if self.drawingArea.drawingTool != "pencil":
            self.sendDrawingCommand()

    def onMouseMove(self, event):
        # print("moving!!!")
        if self.drawingArea.drawingTool == "pencil" and self.left_but == "down":
            self.pencil_draw(event)
        if self.drawingArea.drawingTool == "eraser" and self.left_but == "down":
            self.eraser_draw(event)
        if self.drawingArea.drawingTool == "line" and self.left_but == "down":
            self.line_draw(event)

    def pencil_draw(self, event):
        # print("drawing")
        msg = ('D', self.x1_line_pt, self.y1_line_pt, event.x(), event.y(), self.color, self.connection.ID)
        self.connection.send_message(msg)
        print("[Pencil]Sent message:", msg)
        self.x1_line_pt, self.y1_line_pt = event.x(), event.y()

    def sendDrawingCommand(self):
        print("Sending drawing command")
        msgType = self.getMsgTypeFromTool(self.drawingArea.drawingTool)
        msg = [msgType, self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt, self.color, self.connection.ID]
        print(msg)
        self.connection.send_message(msg)

    def getMsgTypeFromTool(self, tool):
        return {'line': 'L', 'oval': 'O', 'rectangle': 'R', 'circle': 'C', 'square': 'S'}.get(tool, 'L')

    def draw_from_message(self, msg):
        _type = msg[0]
        if _type in ['O', 'C', 'L', 'R', 'T']:
            self.draw_shape_from_message(msg)

    def draw_shape_from_message(self, msg):
        _type = msg[0]
        a, b, c, d = map(float, msg[1:5])
        color = self.Colors[msg[5]]
        painter = QPainter(self.drawingArea.image)
        painter.setPen(QPen(color, self.line_width))

        if _type == 'O':
            painter.drawEllipse(QRectF(int(a), int(b), int(c - a), int(d - b)))
        elif _type == 'C':
            radius = math.sqrt((c - a) ** 2 + (d - b) ** 2) / 2
            painter.drawEllipse(QPointF(int((a + c) / 2), int((b + d) / 2)), int(radius), int(radius))
        elif _type == 'L':
            painter.drawLine(int(a), int(b), int(c), int(d))
        elif _type == 'R':
            painter.drawRect(QRectF(int(a), int(b), int(c - a), int(d - b)))
        elif _type == 'T':
            text = " ".join(msg[1:-3])
            painter.drawText(QPointF(int(a), int(b)), text)
        elif _type == 'D':
            painter.drawLine(int(a), int(b), int(c), int(d))

        painter.end()
        self.drawingArea.update()

    def start_message_receiving_thread(self):
        self.message_thread = Thread(target=self.receive_and_process_messages)
        self.message_thread.daemon = True
        self.message_thread.start()

    def receive_and_process_messages(self):
        while True:
            try:
                msg = self.connection.receive_message()
                print("Received message:", msg)
                self.process_message(msg)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def process_message(self, msg):
        if msg:
            _type = msg[0]
            if _type in ['O', 'C', 'L', 'R', 'T']:
                self.draw_from_message(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # my_connexion = MConnection("ac","180.94.143.9", 8500)
    # permissions = Permission(my_connexion)

    ex = DrawingTools()
    sys.exit(app.exec_())
