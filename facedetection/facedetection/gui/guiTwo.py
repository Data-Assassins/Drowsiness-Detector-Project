import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt , QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QPixmap 
from PyQt5.QtWidgets import QApplication, QWidget ,QDialog,QTableWidgetItem,QMessageBox
from PyQt5 import QtWidgets ,QtGui
from PyQt5.uic import loadUi
import cv2
import numpy as np
import csv

database={'admin': '1234','saadoun':'1234', 'haya': '1234', 'ali': '1234'}

# Home page 
class homeWindow(QDialog):
    def __init__(self):
        super(homeWindow, self).__init__()
        loadUi('facedetection/gui/guiHome.ui', self)
        self.setWindowTitle("Main Window")
        self.login.clicked.connect(self.login_clicked)
        self.signup.clicked.connect(self.signup_clicked)
    # login function will link to the login class then we show the login screen
    def login_clicked(self):
        # make object from login class
        login = loginWindow()
        # add it to the widget stack
        widget.addWidget(login)
        # to flip the screen to the login
        widget.setCurrentIndex(widget.currentIndex() + 1)
    # sign up function will link to the sign up class then we show the signup screen

    def signup_clicked(self):
        # make object from signup class
        signup = signupWindow()
        # add it to the widget stack
        widget.addWidget(signup)
        # to flip the screen to the signup
        widget.setCurrentIndex(widget.currentIndex() + 1)
# Login page
class loginWindow(QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        loadUi('facedetection/gui/guiLogin.ui', self)
        self.setWindowTitle("Login")
        # self.login.clicked.connect(self.login_clicked)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)
        self.backbutton.clicked.connect(self.back_button_function)
    # to handle the login button inside the login window
    def login_function(self):
        # get the username and password
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        # check if the username and password are correct and they are inside the database
        if username in database and database[username] == password:
            # if correct then show the main window
            print("Login Successful")
            user = mainWindow()
            widget.addWidget(user)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif len(username) == 0 and len(password) == 0:
            # if username and password are empty show error message
            self.errorfield.setText("* Please enter your username and password")

        else:
            # if not correct then show the error message
            self.errorfield.setText("* Username or Password is incorrect")

    # to handle the back button inside the login window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)


# signup page 
class signupWindow(QDialog):
    def __init__(self):
        super(signupWindow, self).__init__()
        loadUi('facedetection/gui/guiSignup.ui', self)
        self.setWindowTitle("Signup")
        self.signup.clicked.connect(self.signup_function)
        self.backbutton.clicked.connect(self.back_button_function)

    # to handle the signup button inside the signup window
    def signup_function(self):
        # get the username and password
        username = self.usernamefield.text()
        password = self.passwordfield.text()
        passwordconfirm = self.passwordconfirmfield.text()

        # check if the username and password are correct and they are inside the database
        if password != passwordconfirm:
            # if not correct then show the error message
            self.errorfield.setText("* Password does not match") 

        elif username not in database and password == passwordconfirm:
            # if correct then show the main window
            print("Sign up Successful")
            # add the username and password to the database
            database[username] = password
            main = mainWindow()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif len(username) == 0 or len(password)==0 or len(passwordconfirm)== 0:
            # if username and password are empty show error message
            self.errorfield.setText("* Please enter your username and password")

        elif username in database:
            # if user name is found in the database
            self.errorfield.setText("* Username is Taken")

        else:
            # if not correct then show the error message
            self.errorfield.setText("* Something went Wrong")

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)

# report page       
class reportWindow(QDialog):
    def __init__(self):
        super(reportWindow, self).__init__()
        loadUi('facedetection/gui/guiReport.ui', self)
        self.setWindowTitle("Report")
        self.backbutton.clicked.connect(self.back_button_function)
        self.Reporttable.setColumnWidth(0,300)
        self.Reporttable.setColumnWidth(1,300)
        self.Reporttable.setColumnWidth(2,318)
        #Row count
        #Column count
        # self.Reporttable.setColumnCount(3)  
        self.read_report()

    def read_report(self):
        """read from csv file"""
        with open('report.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # self.Reporttable.setRowCount(len(list(reader))-1)
            self.Reporttable.setRowCount(13)
            for row in reader:
                print("this is row", row)
                for i in range(len(row)):
                    # self.Reporttable.setItem(read each line in the reader,row_num, each value to the table column count)
                    self.Reporttable.setItem(reader.line_num-2,i,QTableWidgetItem(row[i]))

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)

############################################################################################
###########################################  guitwo ########################################
############################################################################################
# Home page 
class mainWindow(QDialog):
    def __init__(self):
        super(mainWindow, self).__init__()
        loadUi('facedetection/gui/mainWindow.ui', self)
        self.start.clicked.connect(self.start_clicked)
        self.report.clicked.connect(self.report_function) 
        self.backbutton.clicked.connect(self.back_button_function)
    def start_clicked(self):
        videoScreen = videoWindow()
        widget.addWidget(videoScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # to handle the report button inside the user window
    def report_function(self):
        report = reportWindow()
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)

# Cam page
class videoWindow(QDialog):
    def __init__(self):
        super(videoWindow, self).__init__()
        loadUi('facedetection/gui/videoWindow.ui', self)
        self.backbutton.clicked.connect(self.back_button_function)
        self.video = videoLabel(self.videoLabel)
        self.video.run_thread(self.edited)
        self.backbutton.clicked.connect(self.back_button_function)
        
    @pyqtSlot(np.ndarray,name="edited")
    def edited(self,image):
        self.video.update_image(image)

    def back_button_function(self):
    # to flip the screen to the main window
        # self.camera.release()
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)


# to play the cam inside the label
class videoLabel(QWidget):
    def __init__(self , label):
        # super(videoLabel, self).__init__()
        # self.videoLabel = QLabel()
        self.camera = cv2.VideoCapture(0)
        self.shape = self.get_resolution(self.camera)
        self.videoLabel = label
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
    home = homeWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(home)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting From The Application")