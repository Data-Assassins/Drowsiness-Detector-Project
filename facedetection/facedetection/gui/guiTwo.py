import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt , QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QPixmap 
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog
from PyQt5 import QtWidgets ,QtGui
from PyQt5.uic import loadUi
import cv2
import numpy as np


class mainWindow(QDialog):
    def __init__(self):
        super(mainWindow, self).__init__()
        loadUi('facedetection/gui/mainWindow.ui', self)
        self.start.clicked.connect(self.start_clicked)

    def start_clicked(self):
        videoScreen = videoWindow()
        widget.addWidget(videoScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class videoWindow(QDialog):
    def __init__(self):
        super(videoWindow, self).__init__()
        loadUi('facedetection/gui/videoWindow.ui', self)
        self.backbutton.clicked.connect(self.back_button_function)
        self.video = videoLable(self.videoLabel)
        self.video.run_thread(self.edited)
    @pyqtSlot(np.ndarray,name="edited")
    def edited(self,image):
        self.video.update_image(image)
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)

class videoLable(QWidget):
    def __init__(self , lable):
        self.videoLabel = QLabel()
        self.camera = cv2.VideoCapture(0)
        self.shape = self.get_resolution(self.camera)
        self.videoLabel = lable
        self.videoLabel.resize(self.shape[0], self.shape[1])

    def run_thread(self,edited):
        self.thread = videoThread(self.camera)
        self.thread.pixmap.connect(edited)
        self.thread.start()
    def get_resolution(self , camera):
        ret , frame = camera.read()
        return frame.shape
    # @pyqtSlot(np.ndarray)
    def update_image(self, image):
        print("image updated")
        qtFrame = self.convert_cv2_to_qt(image)
        self.videoLabel.setPixmap(qtFrame)

    def convert_cv2_to_qt(self, image):
        rgbFrame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbFrame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(rgbFrame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        p = convertToQtFormat.scaled(self.videoLabel.width(), self.videoLabel.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def closeThread(self):
        self.thread.stop()


class videoThread(QThread):
    pixmap = pyqtSignal(np.ndarray)
    def __init__(self , camera):
        super(videoThread, self).__init__()
        self._flag = True
        self.camera = camera
    def run(self):
        while self._flag:
            print("Thread is runing")
            ret , frame = self.camera.read()
            
            self.pixmap.emit(frame)
        self.camera.release()

    def stop(self):
        self._flag = False
        self.wait()

# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = mainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(home)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting From The Application")